#!/usr/bin/env python3
"""Structural validation of a .pptx, with nothing but the standard library.

Added 25 August 2026, to close the last hole in the skill's self-containment.

Until now the file check in SKILL.md borrowed `validate.py` from the **pptx**
skill, which is a different package, needs `defusedxml`, and needs Python 3.10
or newer because it uses `match`. macOS ships 3.9.6, so the documented QA pass
could not run on a clean machine without first installing `uv`, building a
3.12 virtualenv and pip-installing into it. A skill whose own QA step needs
another skill and a second interpreter is not self-contained.

This checks the things that actually break a deck built by this skill, and it
runs on the interpreter that is already there:

  * the zip opens, and every entry inflates
  * `[Content_Types].xml` parses, and every part is typed by a Default
    extension or an Override
  * every XML part is well-formed
  * every relationship part points at a target that exists, for Internal
    targets, and resolves relative paths the way OPC does
  * every slide reaches exactly one slide layout, and every layout one master
  * no duplicate or absolute part names
  * against `--original`, the parts the template had that the deck lost

It does NOT schema-validate against the ECMA-376 XSDs. The pptx skill's
validator still does that and is worth running when it is installed; this is
the floor that always runs, not a replacement for the ceiling.

    python3 scripts/validate_pptx.py deck.pptx
    python3 scripts/validate_pptx.py deck.pptx --original assets/template.pptx

Exits 1 on any finding, so it can gate a build.
"""
import argparse
import posixpath
import sys
import zipfile
import xml.etree.ElementTree as ET

CT_NS = "{http://schemas.openxmlformats.org/package/2006/content-types}"
REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"

SLIDE_REL = ("http://schemas.openxmlformats.org/officeDocument/2006/"
             "relationships/slide")
LAYOUT_REL = ("http://schemas.openxmlformats.org/officeDocument/2006/"
              "relationships/slideLayout")
MASTER_REL = ("http://schemas.openxmlformats.org/officeDocument/2006/"
              "relationships/slideMaster")


def _rels_name(part):
    """The .rels part that describes `part`, in OPC's own layout."""
    head, tail = posixpath.split(part)
    return posixpath.join(head, "_rels", tail + ".rels")


def _resolve(base_part, target):
    """Resolve a relationship target against the part that declares it."""
    if target.startswith("/"):
        return target.lstrip("/")
    base_dir = posixpath.dirname(base_part)
    return posixpath.normpath(posixpath.join(base_dir, target))


def _read_rels(zf, names, part, problems):
    """{rId: (type, target_part_or_None_for_external)} for one part."""
    rels_name = _rels_name(part)
    if rels_name not in names:
        return {}
    try:
        root = ET.fromstring(zf.read(rels_name))
    except ET.ParseError as exc:
        problems.append("%s is not well-formed XML: %s" % (rels_name, exc))
        return {}
    out = {}
    for rel in root.findall(REL_NS + "Relationship"):
        rid = rel.get("Id")
        rtype = rel.get("Type") or ""
        target = rel.get("Target") or ""
        if (rel.get("TargetMode") or "Internal") == "External":
            out[rid] = (rtype, None)
            continue
        resolved = _resolve(part, target)
        if resolved not in names:
            problems.append(
                "%s: relationship %s points at %r, which is not in the package"
                % (rels_name, rid, resolved))
            out[rid] = (rtype, None)
        else:
            out[rid] = (rtype, resolved)
    return out


def validate(path, original=None, verbose=True):
    """Return a list of findings. Empty list is a pass."""
    problems = []

    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as exc:
        return ["%s does not open as a zip: %s" % (path, exc)]

    with zf:
        bad = zf.testzip()
        if bad is not None:
            problems.append("corrupt entry in the archive: %s" % bad)

        names = set(zf.namelist())

        for n in zf.namelist():
            if n.startswith("/"):
                problems.append("part name is absolute, which OPC forbids: %r"
                                % n)
        if len(zf.namelist()) != len(names):
            problems.append("the archive holds duplicate part names")

        # --- content types --------------------------------------------------
        if "[Content_Types].xml" not in names:
            problems.append("no [Content_Types].xml, so this is not an OPC "
                            "package")
            return problems
        try:
            ct = ET.fromstring(zf.read("[Content_Types].xml"))
        except ET.ParseError as exc:
            problems.append("[Content_Types].xml is not well-formed: %s" % exc)
            return problems

        defaults = {d.get("Extension", "").lower()
                    for d in ct.findall(CT_NS + "Default")}
        overrides = {o.get("PartName", "").lstrip("/")
                     for o in ct.findall(CT_NS + "Override")}

        for n in sorted(names):
            if n == "[Content_Types].xml" or n.endswith("/"):
                continue
            # posixpath.splitext treats a leading dot as a hidden name, so
            # "_rels/.rels" comes back with no extension. OPC types it by the
            # "rels" Default like any other part.
            ext = ("rels" if n.endswith(".rels")
                   else posixpath.splitext(n)[1].lstrip(".").lower())
            if n not in overrides and ext not in defaults:
                problems.append(
                    "%s has no content type: no Override for it and no Default "
                    "for .%s" % (n, ext))

        for name in sorted(overrides):
            if name not in names:
                problems.append(
                    "[Content_Types].xml declares an Override for %s, which is "
                    "not in the package" % name)

        # --- every XML part parses -----------------------------------------
        for n in sorted(names):
            if not (n.endswith(".xml") or n.endswith(".rels")):
                continue
            try:
                ET.fromstring(zf.read(n))
            except ET.ParseError as exc:
                problems.append("%s is not well-formed XML: %s" % (n, exc))

        # --- relationships resolve -----------------------------------------
        for n in sorted(names):
            if n.endswith(".rels") or n.endswith("/"):
                continue
            if _rels_name(n) in names:
                _read_rels(zf, names, n, problems)
        _read_rels(zf, names, "", problems)   # the package-level _rels/.rels

        # --- presentation, slides, layouts, masters ------------------------
        pres = "ppt/presentation.xml"
        if pres not in names:
            problems.append("no ppt/presentation.xml")
        else:
            pres_rels = _read_rels(zf, names, pres, problems)
            slides = sorted(t for rt, t in pres_rels.values()
                            if rt == SLIDE_REL and t)
            if not slides:
                problems.append("the presentation references no slides")
            for slide in slides:
                srels = _read_rels(zf, names, slide, problems)
                layouts = [t for rt, t in srels.values()
                           if rt == LAYOUT_REL and t]
                if len(layouts) != 1:
                    problems.append(
                        "%s reaches %d slide layouts; a slide takes exactly one"
                        % (slide, len(layouts)))
            layouts = sorted(n for n in names
                             if n.startswith("ppt/slideLayouts/")
                             and n.endswith(".xml"))
            for layout in layouts:
                lrels = _read_rels(zf, names, layout, problems)
                masters = [t for rt, t in lrels.values()
                           if rt == MASTER_REL and t]
                if len(masters) != 1:
                    problems.append(
                        "%s reaches %d slide masters; a layout takes exactly "
                        "one" % (layout, len(masters)))

        # --- against the template it was built from -------------------------
        if original:
            try:
                with zipfile.ZipFile(original) as ozf:
                    onames = set(ozf.namelist())
            except (zipfile.BadZipFile, OSError) as exc:
                problems.append("--original %s does not open: %s"
                                % (original, exc))
            else:
                # Directory entries are not parts; some writers emit them
                # and some do not, and their absence is never a defect.
                keep = {n for n in onames
                        if n.startswith(("ppt/slideMasters/", "ppt/theme/",
                                         "ppt/slideLayouts/"))
                        and not n.endswith((".rels", "/"))}
                lost = sorted(keep - names)
                for n in lost:
                    problems.append(
                        "the template had %s and the deck does not; a master, "
                        "theme or layout was dropped" % n)

    if verbose:
        if problems:
            print("  validate: %d finding(s)" % len(problems))
            for p in problems:
                print("   ! %s" % p)
        else:
            print("  validate: clean")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pptx")
    ap.add_argument("--original", help="the template it was built from; "
                                       "reports masters, themes or layouts "
                                       "the deck lost")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    problems = validate(args.pptx, args.original, verbose=not args.quiet)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
