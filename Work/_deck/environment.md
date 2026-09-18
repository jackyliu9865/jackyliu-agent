---
type: environment
last_checked: 2026-09-09
---

# Deck build environment

What works on this Mac, and what does not. Volatile: check the date above, and
re-run `python3 design/scripts/doctor.py` if it is stale.

## Working

| Piece | Version | For |
|---|---|---|
| Python | **Two interpreters.** Homebrew's 3.14.7 at `/usr/local/bin/python3` is first on `PATH`; stock 3.9.6 at `/usr/bin/python3` | Everything. Both carry the five packages and both pass the selftest |
| `python-pptx` | 1.0.2 | The build. Nothing works without it |
| `openpyxl` | 3.1.5 | The data booklet |
| `python-docx` | 1.2.0 | Mode A reading a `.docx` source |
| `pypdf` | 6.16.2 | Mode A reading a `.pdf` source |
| The master | 2 masters, 32 layouts, 0 slides | 26 authoring layouts |
| Fonts | 9 faces, registered | `KPMG` and `KPMG Logo` families live. See below |

`doctor.py` reports **ready to build**.

### Python — two interpreters, both working

Installing Homebrew brought in Python 3.14.7, which now shadows the stock 3.9.6
the packages were first installed into. For a day, plain `python3 build.py`
failed with `No module named 'pptx'`.

Fixed by installing the five packages into Homebrew's Python as well. PEP 668
blocks a plain `pip install` there, so the sanctioned user-site override was
used:

```bash
/usr/local/bin/python3 -m pip install --user --break-system-packages python-pptx openpyxl python-docx pypdf pymupdf
```

The package selftest passes **0 findings across 27 gates on 3.14.7**, so the
newer interpreter is safe to build on. `/usr/bin/python3` still works as a
fallback.

### Fonts — resolved

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

**Licence.** The faces are licensed to KPMG by Commercial Type. Internal use
across your own devices is covered; handing the files outside KPMG is not. The
vault-root `.gitignore` excludes every `.ttf` and `**/assets/fonts/`, and
`fonts.check_not_tracked()` fails loudly if that ever breaks.

**`doctor.py` gives a false green on fonts.** Its check is a directory listing,
and a listing cannot see registration or quarantine. It reported
`assets/fonts (bundled) 9 faces` and `ready to build` throughout, while every
title rendered in Helvetica. Trust a resolution probe, never the listing.

## Render and visual check — working

| Piece | State |
|---|---|
| Homebrew | `/usr/local/bin/brew` |
| LibreOffice | 26.8.0.3, `/usr/local/bin/soffice` |
| PyMuPDF | 1.26.5, the `pdftoppm` substitute |
| `pdftoppm` | **Absent.** poppler did not install |

**QA step 4 passes.** The template deck embeds `KPMG-Bold` three times alongside
the Arial faces, so the font resolves end to end.

```bash
soffice --headless --convert-to pdf deck.pptx --outdir .
```

```bash
python3 -c "import re,io;print(sorted(set(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+#,\-_]+)', io.open('deck.pdf','rb').read()))))"
```

**QA step 5 runs through PyMuPDF** rather than `pdftoppm`. No patch to the
package was needed; call it directly:

```python
import fitz
for i, page in enumerate(fitz.open("deck.pdf"), 1):
    page.get_pixmap(dpi=110).save("evidence/page-%02d.png" % i)
```

To restore the documented `pdftoppm` path instead:

```bash
brew install poppler
```

**LibreOffice's first headless run is slow.** It builds a user profile and can
take minutes, which looks like a hang. It is warm afterwards. Give any first
`soffice` call a long timeout.

**Icons now work.** `icons.place()` needs LibreOffice for the raster fallback and
no longer raises.

### What the render pass immediately caught

The gates cannot see composition, and the first look at the template deck found
two defects that all 27 gates passed:

- **Empty grey boxes** beside each recommendation strip on `Key findings_2
  columns` — placeholders idx 52 and 73, never filled and never dropped
- **Content stops around y 4.5 cm** on the findings and exhibit pages, well above
  the master's half-height line at 10.13. `design-principles.md` §7 check 7 fails

This is why §4 of `AGENTS.md` requires a render and a read.

## Fixed in the local fork

`doctor.py` printed `pip3 install --user pptx` for the missing dependency, and
the package is **`python-pptx`** — `pptx` is a different project on PyPI. The
name-mapping dict at `design/scripts/doctor.py:54` handled `docx` and missed
`pptx`.

**Patched.** `design/` is a local fork, so it was fixed in place rather than
worked around. Recorded in the house-changes table in
[[SKILL|the pipeline]] so an upstream merge conflict is recognisable.

## Related

- [[SKILL|the pipeline]]
