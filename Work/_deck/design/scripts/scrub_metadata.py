#!/usr/bin/env python3
"""Strip personal data out of an Office file's collaboration metadata.

Added 26 August 2026. The bundled KPMG master carried, invisibly:

  * docProps/core.xml       creator and lastModifiedBy, real staff names
  * ppt/authors.xml         co-author display names, corporate email addresses
                            and Azure AD user GUIDs
  * ppt/commentAuthors.xml  the same, for comment threads
  * ppt/changesInfos/*      one record per edit, each naming the editor and
                            carrying their AD GUID

None of it was put there deliberately: Office writes it during collaboration and
it survives every save, every copy and every zip. It renders nowhere, so reading
the deck will never show it, and it travels with the file to any machine the
skill is installed on.

This is third-party personal data. Removing these parts does not change how the
file renders: they carry no layout, no theme and no content.

Run it on any deck before it leaves the machine, not just on the master.
"""
import argparse
import os
import re
import shutil
import zipfile

# Parts that exist only to record who did what. Safe to drop entirely.
DROP_EXACT = {"ppt/authors.xml", "ppt/commentAuthors.xml",
              "word/people.xml", "xl/persons/person.xml"}
DROP_PREFIX = ("ppt/changesInfos/", "ppt/revisionInfo")

# Fields inside docProps that name a person. Blanked rather than dropped,
# because the parts themselves are structural.
BLANK = ("dc:creator", "cp:lastModifiedBy", "cp:manager", "dc:contributor")


def scrub(path, *, inplace=True, verbose=True):
    """Returns (parts_removed, fields_blanked, names_found)."""
    src = zipfile.ZipFile(path)
    tmp = path + ".scrubbed"
    removed, blanked, found = [], [], set()

    NAME = re.compile(r'name="([^"]+)"|<dc:creator>([^<]*)<|'
                      r'<cp:lastModifiedBy>([^<]*)<|userId="S::([^:]+)::')

    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for item in src.infolist():
            n = item.filename
            if n in DROP_EXACT or n.startswith(DROP_PREFIX):
                data = src.read(n).decode("utf8", "ignore")
                for m in NAME.finditer(data):
                    found.update(g for g in m.groups() if g)
                removed.append(n)
                continue
            data = src.read(n)
            if n in ("docProps/core.xml", "docProps/app.xml"):
                t = data.decode("utf8", "ignore")
                for tag in BLANK:
                    for m in re.finditer(r"<%s>([^<]+)</%s>" % (tag, tag), t):
                        found.add(m.group(1)); blanked.append(tag)
                    t = re.sub(r"<%s>[^<]*</%s>" % (tag, tag),
                               "<%s></%s>" % (tag, tag), t)
                data = t.encode("utf8")
            out.writestr(item, data)
    src.close()

    # A scrubbed file that will not open is worse than a leaky one.
    check = zipfile.ZipFile(tmp)
    bad = check.testzip()
    if bad:
        os.remove(tmp)
        raise RuntimeError("scrubbed archive is corrupt at %r" % bad)
    check.close()

    if inplace:
        shutil.move(tmp, path)
    else:
        os.remove(tmp)      # --check must not litter the package
    if verbose:
        print("  %s" % os.path.basename(path))
        print("     parts removed : %d %s" % (len(removed), removed[:4]))
        print("     fields blanked: %s" % (sorted(set(blanked)) or "none"))
        print("     names/ids that were in the file: %d" % len(found))
        for f in sorted(found)[:12]:
            print("        - %s" % f)
    return removed, blanked, found


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--check", action="store_true",
                    help="report what is in there and change nothing")
    a = ap.parse_args()
    total = 0
    for f in a.files:
        _, _, found = scrub(f, inplace=not a.check)
        total += len(found)
    print("\n  %s: %d name or identifier string(s) across %d file(s)"
          % ("found" if a.check else "removed", total, len(a.files)))


if __name__ == "__main__":
    main()
