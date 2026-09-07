#!/usr/bin/env python3
"""Wrap the skill and its fonts into one portable archive.

House note, 25 August 2026: "Save the skill and wrap the fonts into it."

Git carries the skill but deliberately never carries the fonts, because the
vault pushes to GitHub and the faces are licensed to KPMG by Commercial Type.
So a `git clone` alone gives you a skill that builds decks in Arial. This makes
the other half: a single archive holding the skill **and** the nine faces, for
moving between your own machines.

    python3 scripts/package.py            # default output, off-vault
    python3 scripts/package.py /some/dir

The archive is written OUTSIDE the vault by default, to the same off-repo
location the font master lives in, so it cannot be swept into a commit. It is
for internal use across your own devices. It is not a distribution: passing it
to anyone outside KPMG redistributes a commercial font licence.
"""
import os
import sys
import zipfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(HERE, ".."))
DEFAULT_OUT = os.path.expanduser(
    "~/Library/Application Support/Artemis/kpmg-deck-dist")

SKIP_DIRS = {"__pycache__", ".git", ".ipynb_checkpoints"}
SKIP_FILES = {".DS_Store"}
SKIP_EXT = {".pyc", ".pdf", ".jpg", ".jpeg", ".png"}
# Rendered check artefacts are rebuilt on demand; the specimen deck and its
# booklet are kept because they are the worked example the skill documents.
KEEP_ANYWAY = {"selftest.pptx", "selftest-databooklet.xlsx",
               "template.pptx", "specimen-deck.pptx"}

INSTALL = """# kpmg-deck, portable bundle

Self-contained: the skill plus all nine KPMG faces.

## Install

1. Unzip anywhere, for example `~/PA. Record/Skills/Execute/kpmg-deck`.
2. Symlink it where the agent looks for skills:

       ln -s "<unzipped path>" ~/.claude/skills/kpmg-deck

3. Build any deck. `new_deck()` calls `fonts.ensure_installed()`, which copies
   the faces into your user font directory on first run. No other setup.

## Verify

    python3 scripts/doctor.py      # what this machine has and lacks
    python3 scripts/selftest.py    # builds a fixture deck and gates it

`doctor.py` exits 1 only if something required is missing, and it proves the
font by rendering a probe rather than by listing files. `selftest.py` should
report **0 findings**. Then convert the deck it writes and confirm the render
embeds `KPMG-Bold` rather than falling back to Arial:

    soffice --headless --convert-to pdf assets/selftest.pptx --outdir .
    python3 -c "import re,io;print(sorted(set(re.findall(rb'/BaseFont\\s*/([A-Za-z0-9+#,\\-_]+)', io.open('selftest.pdf','rb').read()))))"

## Dependencies

`python-pptx` and `openpyxl` are required. LibreOffice (`soffice`) and poppler
(`pdftoppm`) are needed only for the render pass and for SVG icon fallbacks.

Nothing else. The master, all nine faces, every reference, the KPMG house-style
QRG and the .pptx validator are inside this archive. The validator is standard
library only and runs on the Python already on the machine, so there is no
second interpreter to build.

## The fonts

`assets/fonts/` holds nine faces licensed to KPMG by Commercial Type. They are
excluded from git on purpose and this archive is the only thing that carries
them. **Internal use across your own machines only.** Do not pass this archive
to anyone outside KPMG: that is redistribution of a commercial licence.
"""


def collect(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if f in SKIP_FILES:
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in SKIP_EXT and f not in KEEP_ANYWAY:
                continue
            full = os.path.join(base, f)
            yield full, os.path.relpath(full, root)


def build(out_dir=None):
    out_dir = out_dir or DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)
    name = "kpmg-deck-%s.zip" % date.today().isoformat()
    out = os.path.join(out_dir, name)

    fonts, total, count = 0, 0, 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in collect(SKILL):
            z.write(full, os.path.join("kpmg-deck", rel))
            total += os.path.getsize(full)
            count += 1
            if rel.startswith(os.path.join("assets", "fonts")):
                fonts += 1
        z.writestr("kpmg-deck/INSTALL.md", INSTALL)

    print("  wrote %s" % out)
    print("  %d files, %d font face(s), %.1f MB uncompressed, %.1f MB zipped"
          % (count, fonts, total / 1e6, os.path.getsize(out) / 1e6))
    if fonts == 0:
        print("  ! no fonts in the bundle. Seed assets/fonts/ from the "
              "licensed source before packaging, or the archive is pointless.")
    print("  Internal use across your own machines. Not for distribution: the "
          "faces are licensed to KPMG by Commercial Type.")
    return out


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
