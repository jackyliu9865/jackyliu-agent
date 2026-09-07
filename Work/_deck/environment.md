---
type: environment
last_checked: 2026-09-01
---

# Deck build environment

What works on this Mac, and what does not. Volatile: check the date above, and
re-run `python3 design/scripts/doctor.py` if it is stale.

## Working

| Piece | Version | For |
|---|---|---|
| Python | 3.9.6, stock macOS | Everything |
| `python-pptx` | 1.0.2 | The build. Nothing works without it |
| `openpyxl` | 3.1.5 | The data booklet |
| `python-docx` | 1.2.0 | Mode A reading a `.docx` source |
| `pypdf` | 6.16.2 | Mode A reading a `.pdf` source |
| The master | 2 masters, 32 layouts, 0 slides | 26 authoring layouts |
| Fonts | 9 faces, registered | `KPMG` and `KPMG Logo` families live. See below |

`doctor.py` reports **ready to build**.

### Fonts — RESOLVED 1 September 2026

Nine Commercial Type faces at `design/assets/fonts/`, installed to
`~/Library/Fonts`. Both families now registered: `KPMG` and `KPMG Logo`.

```
asked "KPMG Bold"  ->  postscript=KPMG-Bold  family=KPMG
asked "KPMG Light" ->  postscript=KPMG-Light family=KPMG
```

**Root cause, worth knowing because it will recur.** The faces were downloaded
from Notion, so Gatekeeper stamped `com.apple.quarantine` on every file.
**macOS silently refuses to activate a quarantined font.** Font Book copied the
file in, reported the filename as already present, and never activated it. Every
title rendered in Helvetica.

The fix was two steps, and one alone was not enough:

```bash
xattr -d com.apple.quarantine ~/Library/Fonts/*.ttf
```

```bash
killall fontd
```

`fontd` respawns on demand. Strip the flag on the vault copies too, or
`fonts.py` reintroduces quarantined files on the next `new_deck()`.

**Any newly downloaded font will hit this again.** Check with
`xattr <file> | grep quarantine` before assuming a font is broken.

**`doctor.py` gives a false green on fonts.** Its check is a directory listing,
and a listing cannot see registration or quarantine. It reported
`assets/fonts (bundled) 9 faces` and `ready to build` throughout, while every
title rendered in Helvetica. Trust a resolution probe, never the listing.

## Blocked

**QA steps 4 and 5 cannot run.** They need `soffice` and `pdftoppm`. Neither is
installed, and there is no Homebrew on this Mac.

| Step | What it does | Consequence of the gap |
|---|---|---|
| 4 | Converts to PDF and reads the embedded fonts | Cannot prove titles rendered in KPMG Bold rather than Arial |
| 5 | Rasterises every page to JPG | Cannot look at any page. `check()` sees geometry, never composition |

**§4 of `AGENTS.md` forbids reporting a check that did not run.** Until these are
installed, every deck ships with the gap stated in the delivery note. Steps 1 to
3 do run and still gate the build:

- `qa.report()` — structural, brand and house style, in-process. `save()` raises
  on a finding
- `scan_text.py` — every string, as a separate gate
- `validate_pptx.py` — parts, relationships, layouts, masters

### The fix

Installing needs an administrator password, so it is yours to run.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install --cask libreoffice && brew install poppler
```

LibreOffice can also be installed from its own `.dmg` without Homebrew, which
covers step 4 and step 5 needs `poppler` separately.

## Known defect in the skill

`doctor.py` prints `pip3 install --user pptx` for the missing dependency. The
package is **`python-pptx`**; `pptx` is a different project on PyPI. The
name-mapping dict at `design/scripts/doctor.py:54` translates `docx` and misses
`pptx`. `SKILL.md` has it right.

Left unpatched on purpose: `design/` is imported and never edited, so a local fix
would be lost on the next import. Follow `SKILL.md` instead.

## Related

- [[START-HERE]]
