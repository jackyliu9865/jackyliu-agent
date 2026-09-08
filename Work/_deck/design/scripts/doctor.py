#!/usr/bin/env python3
"""What this machine has, what it lacks, and what that costs you.

Added 25 August 2026. The skill is meant to be self-contained: clone or unzip
it, build a deck, and the titles come out in KPMG Bold. This proves that on a
given machine in one command instead of leaving it to be discovered halfway
through a build.

    python3 scripts/doctor.py

Exits 1 only if something REQUIRED is missing. Optional pieces are reported
with what you lose without them, because a deck that builds with a warning
beats a deck that does not build.
"""
import importlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

# The vault note the bundled mirror is taken from. Absent on a machine without
# the vault, which is the whole point of bundling it, so this is never fatal.
VAULT_QRG = os.path.expanduser(
    "~/PA. Record/Career/KPMG House Style — PowerPoint & Report QRG.md")
MIRROR = os.path.join(SKILL, "references", "house-style-qrg.md")

OK, WARN, BAD = "ok  ", "warn", "MISS"


def _line(state, label, detail=""):
    print("  [%s] %-34s %s" % (state, label, detail))


def check_python():
    v = sys.version_info
    ok = v >= (3, 8)
    _line(OK if ok else BAD, "python %d.%d.%d" % v[:3],
          "" if ok else "3.8 or newer needed")
    return ok


def check_module(name, required, why):
    try:
        m = importlib.import_module(name)
        ver = getattr(m, "__version__", "")
        _line(OK, name, ver)
        return True
    except ImportError:
        _line(BAD if required else WARN, name,
              "%s  (pip3 install --user %s)" % (why, {"docx": "python-docx", "pptx": "python-pptx"}.get(name, name)))
        return not required


def check_binary(name, why):
    path = shutil.which(name)
    _line(OK if path else WARN, name, path or why)
    return True


def check_template():
    path = os.path.join(SKILL, "assets", "template.pptx")
    if not os.path.exists(path):
        _line(BAD, "assets/template.pptx", "the master is missing")
        return False
    try:
        from pptx import Presentation
    except ImportError:
        _line(WARN, "assets/template.pptx", "present, unread without python-pptx")
        return True
    prs = Presentation(path)
    n_layouts = sum(len(m.slide_layouts) for m in prs.slide_masters)
    ok = len(prs.slides) == 0 and n_layouts >= 26
    _line(OK if ok else WARN, "assets/template.pptx",
          "%d masters, %d layouts, %d slides"
          % (len(prs.slide_masters), n_layouts, len(prs.slides)))
    return True


def check_fonts():
    try:
        import fonts
    except ImportError as exc:
        _line(BAD, "fonts.py", str(exc))
        return False
    bundled = os.path.join(SKILL, "assets", "fonts")
    n_bundled = (len([f for f in os.listdir(bundled) if f.lower().endswith(".ttf")])
                 if os.path.isdir(bundled) else 0)
    _line(OK if n_bundled >= 9 else WARN, "assets/fonts (bundled)",
          "%d faces" % n_bundled if n_bundled else
          "none bundled; decks will build in Arial")
    try:
        target = fonts.user_font_dir()
        installed = [f for f in os.listdir(target)
                     if f.lower().startswith("kpmg")] if os.path.isdir(target) else []
    except Exception as exc:                      # never fatal
        _line(WARN, "installed faces", "could not read: %r" % exc)
        return True
    _line(OK if installed else WARN, "installed faces",
          "%d in %s" % (len(installed), target) if installed
          else "none yet; new_deck() installs them on first run")
    return True


def check_font_render():
    """Presence is not use. Convert a one-slide deck and read the PDF."""
    if not shutil.which("soffice"):
        _line(WARN, "font actually renders", "needs soffice to prove it")
        return True
    import re
    import tempfile
    try:
        from deckkit import new_deck, add, fill, save
    except ImportError as exc:
        _line(WARN, "font actually renders", "cannot build a probe: %r" % exc)
        return True
    tmp = tempfile.mkdtemp(prefix="kpmg-deck-doctor-")
    pptx = os.path.join(tmp, "probe.pptx")
    prs = new_deck()
    s = add(prs, "Section divider")
    fill(s, title="Font probe")
    save(prs, pptx, verify=False)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    pptx, "--outdir", tmp],
                   capture_output=True, timeout=180)
    pdf = os.path.join(tmp, "probe.pdf")
    if not os.path.exists(pdf):
        _line(WARN, "font actually renders", "soffice produced no PDF")
        return True
    with open(pdf, "rb") as fh:
        blob = fh.read()
    faces = sorted({f.decode() for f in
                    re.findall(rb"/BaseFont\s*/([A-Za-z0-9+#,\-_]+)", blob)})
    got = any("KPMG" in f for f in faces)
    _line(OK if got else WARN, "font actually renders",
          ", ".join(faces) if got else
          "Arial only — titles will not be KPMG Bold: " + ", ".join(faces))
    return True


def check_house_style():
    """Is the bundled QRG still saying what the vault note says?

    Compared on **section headings**, not verbatim. The bundled copy legitimately
    differs from the vault note: the skill is packaged and carried between
    machines, so the personal name is redacted out of it while the vault keeps
    it. A verbatim diff reports that redaction as drift on every run, and a
    check that cries wolf gets ignored. Headings catch what actually matters —
    the vault note gaining, losing or renaming a rule section.
    """
    if not os.path.exists(MIRROR):
        _line(WARN, "house style QRG (bundled)", "mirror missing")
        return True
    if not os.path.exists(VAULT_QRG):
        _line(OK, "house style QRG (bundled)",
              "bundled copy in use; vault note not on this machine")
        return True
    import re

    def heads(path):
        with open(path) as fh:
            return [h.strip() for h in
                    re.findall(r"^#{1,3} (.+)$", fh.read(), re.M)]

    a, b = heads(MIRROR), heads(VAULT_QRG)
    if a == b:
        _line(OK, "house style QRG (bundled)",
              "%d sections, matches the vault note" % len(b))
        return True
    missing = [h for h in b if h not in a]
    extra = [h for h in a if h not in b]
    detail = []
    if missing:
        detail.append("vault has %d section(s) the mirror lacks: %s"
                      % (len(missing), "; ".join(missing[:2])))
    if extra:
        detail.append("mirror has %d the vault lacks" % len(extra))
    _line(WARN, "house style QRG (bundled)",
          "DRIFT: " + ", ".join(detail) + " — re-mirror it")
    return True


def main():
    print("\n  kpmg-deck doctor")
    print("  skill: %s\n" % SKILL)
    required = [
        check_python(),
        check_module("pptx", True, "required; nothing builds without it"),
        check_module("openpyxl", True, "required for the data booklet"),
        check_template(),
        check_fonts(),
    ]
    print()
    # Mode A reads the supplied document. .md and .txt need nothing; .docx and
    # .pdf each need a reader, and without them source_text.py returns no words
    # and the fidelity gate has nothing to check against.
    check_module("docx", False,
                 "Mode A cannot read a .docx source without it (python-docx)")
    check_module("pypdf", False,
                 "Mode A cannot read a .pdf source without it")
    check_binary("soffice", "optional: render pass and SVG icon fallbacks")
    check_binary("pdftoppm", "optional: page images for the visual check")
    check_font_render()
    check_house_style()

    print("\n  Self-contained: the master, all nine faces, every reference and")
    print("  the .pptx validator ship with the skill. soffice and pdftoppm are")
    print("  the only outside pieces, and they are needed only to look at the")
    print("  result, not to build it.")
    bad = not all(required)
    print("\n  %s\n" % ("SOMETHING REQUIRED IS MISSING" if bad
                        else "ready to build"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
