---
tags: [note, skills, kpmg-deck, qa]
---

# QA checklist

**The agent flags every area where QA is not met.** The checklist is
incorporated as code. `scripts/qa.py` runs it and prints PASS or FAIL
per gate. A gate that reports PASS actually ran; anything that cannot be
automated honestly prints as MANUAL rather than being quietly assumed.

**Provenance.** The KPMG PPT training deck, which the original review pointed
at, is not on this machine. The checklist below is built from the house-style
QRG, sections 4, 5 and 9, the only house-style artefact present. It is bundled
at `references/house-style-qrg.md` and mirrors the vault note
`Career/KPMG House Style — PowerPoint & Report QRG.md`. **When the
training deck is supplied, this file and `qa.py` need reconciling against it.**

---

## Running it

```python
import qa, databooklet
bp = databooklet.check_booklet(prs)
qa.report(prs, booklet_problems=bp)
```

`scripts/selftest.py` runs the whole thing against a fixture deck that
exercises every exhibit type. Run it after any change to the skill.

---

## Automated gates

| Gate | What it fails on | Source |
|---|---|---|
| **Correct master, no strays** | Slides sitting on more than one master | QRG §9, style check |
| **Closed palette only** | Any shape or series filled off the palette | `brand.md` |
| **Type scale** | A hand-set font size outside 6/7/8/9/10/14/18/24/44/66pt | QRG §4 |
| **Colour carries a key** | A chart with more than one series and no legend; a legend over 8pt | House rule |
| **Traffic lights have a scale** | RAG chips on a slide whose note never says what red, amber and green mean | House rule |
| **Exhibit title and basis** | A chart with no exhibit title, or no basis line | `exhibits.md` §1 |
| **Every exhibit sourced** | A chart or table on a content slide with no source line | QRG §3 |
| **UK English** | US `-ize` / `-ization` spellings. Words built on *size* (unsized, downsized, right-sizing) are correct UK English and are exempt | QRG §8 |
| **Acronyms** | `K.P.I.` style full stops, or a **plural** `KPI's`. A **possessive** acronym (`BCT's rise`) is correct and is not flagged | QRG §9 |
| **Percentage points** | A move stated "from 30% to 35%" described as an increase of 5% | QRG §9 |
| **Telephone format** | A number not in international `+852 xxxx xxxx` form | QRG §9 |
| **Nothing below the line** | Content past the floor at y 16.33 cm. The source strip (idx 17, idx 18, `EXHIBIT_SOURCE`) legitimately sits below it and is held to the strip instead. A table's height is estimated from its text, because PowerPoint grows rows to fit and reports nothing | Master marker |
| **Draft stamp** | Reports `INFO`, not `FAIL`: the banner is correct on a draft and comes off in the master for a final version | QRG §9 |
| **Charts linked to the booklet** | A chart with no booklet entry, or an entry with no basis or source | House rule |

| **No text overlapping text** | Two text shapes sharing space. A callout over its own chart is intended and exempt | House rule |
| **Nothing bleeds into the read column** | A left-column exhibit crossing into the commentary at the same height | House rule |
| **Exhibit width on the grid** | Any chart or table not 13.70 cm or 28.40 cm wide. There is nothing legitimate in between | House rule |
| **Exhibit fills a page slot** | An exhibit at an arbitrary rectangle rather than a named full / half / quarter slot | House rule |
| **Text fits its box** | Text estimated to overflow the shape it is drawn in, which a geometric overlap check cannot see | House rule |
| **Exhibit title fits one line** | An exhibit title that wraps to two. The fix is a shorter sentence, never a smaller font | House rule |

| **House style, find and replace** | The QRG find-and-replace list: `n/a`, `versus`, `e.g.`, contractions, FY form, spacing, currency, spaced hyphen for an en dash, single-digit ordinals, `circa`, and `%` loose in prose. Judgement calls sit in `HOUSE_STYLE_REVIEW` and report without failing | QRG §3 |

| **Exhibits are charts, not pictures** | Any picture larger than about 2.6 cm on both sides. An exhibit is a native chart with its own embedded workbook; icons are the exception | House rule |

**Twenty-one gates in `qa.GATES`.** Plus the structural gates in `deckkit.check()`,
which run first: title over 36 characters, placeholder still showing prompt text,
empty source or strapline, chart with its own title or gridlines, chart font over
10pt, over 20 categories. **`check()` fails, it does not warn**, and `save()`
raises on any finding.

Plus `scripts/validate_pptx.py`, which gates the file itself: zip integrity,
content types, XML well-formedness, relationship resolution, and every slide
reaching exactly one layout. Standard library only, so it runs on the Python
already on the machine.

### Corrections from live use

A gate that cries wolf gets ignored, which is worse than not having the gate.
Both were found on the first real deck the module ran against, and both were
the gate's fault:

| Reported | Verdict | Fix |
|---|---|---|
| `'unsized' is US spelling` | False positive. `-size` is not an `-ize` Americanism | `IZE_OK` now exempts any word built on *siz*, *priz* or *seiz* |
| `acronym with an apostrophe: "BCT's"` | False positive. The QRG rule is about plurals; a possessive acronym is correct English | `ACRONYM_APOS` now fires only where the apostrophe does plural work: after a number or quantifier, or before a plural verb |
| `title is 43 chars, limit 36` on a `Section divider` | False positive. A divider title is 66pt in a far bigger box, and `deckkit.check()` correctly allowed it. Two gates contradicting each other | `DIVIDER_TITLE_LIMIT = 66`, applied to cover and divider layouts |
| `write percentage in text` on `Share of cases by outcome, %` | False positive, mine, 26 Aug. A basis line declaring its units as `, %` is the exhibit grammar this skill mandates. Nine hits across two finished decks | The rule now fires only where the sign is loose in prose: exempt after a comma, and exempt before a parenthetical, which covers `% (dot, RHS)` |
| `write ordinals in words` on `75th percentile` | False positive, mine, 26 Aug. "Seventy-fifth percentile" is worse English than the thing being objected to | Single-digit ordinals only, which matches the one-to-nine-in-words golden rule |
| `no spaces either side of a slash` on `NOPAT / Revenue` | Not a defect. Eleven hits on one deck, all formulae and ratios, where a spaced slash is how the thing is written. The QRG's own wording is "check each instance" | Moved to `HOUSE_STYLE_REVIEW`: reported for review, does not fail the build |
| `bullet ends in a full stop` on the legal disclaimer | False positive. Multi-sentence boilerplate and the copyright line are prose, not bullets, and must keep their stops | `is_prose_block()` exempts any block carrying more than one sentence, plus copyright and trademark lines |

**Log false positives here rather than working around them in the deck.** The
temptation is to reword the slide until the gate goes quiet, and that leaves
the gate wrong for every deck after this one.

## Manual gates

Printed by `qa.report()` every run, because they cannot be automated honestly:

- Greyscale flick-through, to catch stray boxes and print problems
- Proofing language set to English (United Kingdom) via Review, Language, Set Proofing Language, **Document**. Every other route reverts
- Spell check run **after** the language is set
- Contents page filled in and matching the section headings
- Copyright year updated in the footer and on the back page
- Key issues boxes removed from the appendices
- Glossary alphabetical, sentence case, holding every abbreviation used

## Content fidelity

**When a document is supplied, use its words word for word and change none of
them.** The operative rules are in [[content-rules]].

```python
import source_text, qa
src = source_text.extract("input.docx")
src.report()                      # says what it could NOT read: picture text, scans
qa.content_fidelity(prs, src.text)          # mode="verbatim" is the default
```

**This is a verbatim-span check, not a word list.** Every string on a slide must
be built from contiguous runs of words taken from the document. Re-wrapping and
stopping early are fine; paraphrase, synonyms, inserted connectives, expanded
acronyms, reordering and mid-sentence deletion are not.

**An earlier version was too weak to be worth running.** It checked that every
word appeared *somewhere* in the input, in any order. Re-run against a deck that
had passed it clean, the current check found
**53 strings that had quietly been paraphrased** — every individual word came
from the article, which is exactly how a bag-of-words check gets fooled.

**Mid-sentence deletion fails even though it changes no words**, because it is
the edit that silently inverts meaning: drop "no" from "existing payment rails
have no native concept of delegated machine authority" and every remaining word
is still the document's. The check locates each run in the source and refuses a
cover whose runs sit within twelve words of each other, which separates quoting
two places from deleting from one sentence.

`mode="words"` keeps the old behaviour for the case where the person asked you to
write the content and the document is background rather than script.

Run this whenever the content was supplied rather than developed. **In Mode A it
must return zero**; see Rule 0 in `SKILL.md`.

## Rendering

`check()` and `qa.report()` cannot see composition. The render pass is still
required, and still mandatory:

```bash
soffice --headless --convert-to pdf deck.pptx --outdir .
python3 -c "import re,io;print(sorted(set(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+#,\-_]+)', io.open('deck.pdf','rb').read()))))"
pdftoppm -jpeg -r 110 deck.pdf slide
```

A correct render returns `KPMG-Bold` alongside `Arial-BoldMT`. Then look at
every page and run the seven composition checks in `design-principles.md` §7.


## The QA pass in full, and why each gate exists

The reasoning behind each gate, read while doing QA rather than before
deciding what to build.

`save()` runs `check(prs)` first and prints anything it finds. Fix the findings
rather than passing `verify=False` — each one is a defect that shows up on the
rendered slide:

- **Title over 36 characters.** Content titles get a 1.50cm-tall box at 44pt,
  which holds exactly one line. Longer titles wrap down into the strapline and
  overlap it. Shorten the title; the detail belongs in the strapline.
- **Placeholder still showing prompt text** ("Click to add…") — fill it or
  delete the shape.
- **Empty idx 17 or 18** — a data slide with no source, or a slide with no
  stated argument.
- **A chart with its own title, gridlines, a font over 10pt, or more than about
  twelve categories.** Without this, a hand-built chart with gridlines, a 24pt
  centred black title and 18pt axis text passes every other gate. Use `chart()`,
  which cannot produce those.
- **No source line or no strapline on a layout that has neither placeholder** —
  a table or chart slide built on `Title only_Blank` with nothing identifying its
  argument or its evidence. Call `strapline()` and `note()`; they fall back to a
  brand-format text box on the grid.

**Then run the design checks by eye, per slide** (`references/design-principles.md`,
section 7). `check(prs)` cannot see composition, so these are yours:

1. Does the title state a finding rather than a topic?
2. Is there exactly one argument on the slide?
3. **Is any column more than about a third empty?** If so the wrong composition was
   chosen: change the pattern rather than stretching the chart. This is the failure
   that ran through every exhibit of the last POV dashboard.
4. Does everything sit on the grid, with constant gutters?
5. Does every colour mean something, and is there a **legend wherever it does**?
6. Source line present, and every bar starting at zero?
7. **Does the content reach past about y 11 cm?** If not the slide is half empty
   vertically. Do not stretch the exhibit: add the read, stack a second exhibit,
   move it into a column, or merge two thin slides.

**Verify the font by rendering, not by listing.** The KPMG faces are installed at
`~/Library/Fonts/` on this machine, but presence is not use. Convert and read what
the PDF actually embedded:

```bash
soffice --headless --convert-to pdf deck.pptx --outdir .
python3 -c "import re,io;print(sorted(set(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+#,\-_]+)', io.open('deck.pdf','rb').read()))))"
```

A correct render returns `KPMG-Bold` alongside `Arial-BoldMT`. If only Arial faces
come back, the font is not resolving and every title in the deck is wrong. On a
machine without the font, fall back to Arial Bold and **say so in the delivery
note** rather than claiming the brand check passed.

Then validate the file, with the validator the skill carries:

```bash
python3 <skill>/scripts/validate_pptx.py out.pptx --original <skill>/assets/template.pptx
```

Pass `--original` — it reports any master, theme or layout the deck lost against
the template it was built from.

**Stdlib only, and it runs on the Python that is already there.** It opens the
package and checks that every entry inflates, that `[Content_Types].xml` types
every part, that every XML part is well-formed, that every internal relationship
resolves, and that every slide reaches exactly one layout and every layout one
master. Verified against two deliberately damaged fixtures: a deck with a slide
layout deleted (11 findings, naming every dangling reference) and a deck with one
slide truncated mid-XML (1 finding, naming the part).

**Self-contained by design.** This step used to borrow `validate.py` from the
**pptx** skill, which is a different package, needs
`defusedxml`, and needs Python 3.10 or newer because it uses `match`. macOS ships
3.9.6, so the documented QA pass could not run on a clean machine without first
installing `uv`, building a 3.12 virtualenv and pip-installing into it. A skill
whose own QA step needs another skill and a second interpreter is not
self-contained.

**The pptx skill's validator is still worth running when it happens to be
installed**, because it schema-validates against the ECMA-376 XSDs and this does
not. It is the ceiling; the bundled one is the floor that always runs.

Then render and look:

```bash
soffice --headless --convert-to pdf out.pptx --outdir .
pdftoppm -jpeg -r 150 out.pdf slide
```

**Dependencies. One command tells you where a machine stands:**

```bash
python3 <skill>/scripts/doctor.py
```

It reports the interpreter, `python-pptx` and `openpyxl`, the bundled template,
the bundled and installed fonts, `soffice` and `pdftoppm`, and whether the
house-style mirror still matches the vault note. It exits 1 only if something
**required** is missing, because a deck that builds with a warning beats a deck
that does not build.

It also **proves the font rather than listing it**: it builds a one-slide probe,
converts it, and reads the faces the PDF actually embedded. Presence is not use,
and this is the difference between "the fonts are installed" and "the titles are
in KPMG Bold".

| Piece | Needed for | Get it |
|---|---|---|
| `python-pptx` | **Everything.** `deckkit` imports it | `pip3 install --user python-pptx` |
| `openpyxl` | The data booklet | `pip3 install --user openpyxl` |
| `soffice` | Render pass, SVG icon fallbacks | `brew install --cask libreoffice` |
| `pdftoppm` | Page images for the visual check | `brew install poppler` |

Nothing else. The master, all nine faces, every reference, the house-style QRG
and the .pptx validator ship inside the skill.

If a binary is genuinely unavailable, say the render pass was skipped and why.
Do not claim the deck was visually checked when only `check(prs)` ran.

**Do not try to render through Microsoft PowerPoint via AppleScript.** It looks
like the better route, since PowerPoint has the real fonts and LibreOffice
substitutes KPMG Bold. It does not work: Office on macOS is sandboxed and
`save … as save as PDF` fails with error -9074 on any path outside its container,
including `~/Documents`. Use LibreOffice and
live with the font substitution, judging titles by character count rather than by
the preview.

View every page. LibreOffice substitutes KPMG Bold, so titles render wider than
they will in PowerPoint — judge titles by character count against the 28.40cm
box, not by the preview. What to look for:

- Text overflowing a placeholder, especially 9pt body in the shorter Key
  findings boxes
- Empty placeholders left showing prompt text ("Click to add…")
- Content below the 16.32cm source strip, colliding with the footer
- RAG chips left at their default red when the finding isn't red
- Any colour that isn't in the palette

```bash
python3 <skill>/scripts/scan_text.py out.pptx        # add --dump to read every string
```

`scan_text.py` replaces the old `markitdown | grep` step, which needed a separate
install and a newer Python than macOS ships. It uses python-pptx, already a hard
dependency, and exits 1 on any finding so it can gate a build. It flags unfilled
prompt text, titles over 36 characters, and empty straplines or source lines on
layouts that carry them.


## Mode A: why the fidelity gate is shaped as it is

The rule and the allowed/not-allowed table are in [[content-rules]]; the
reasoning is here.

### Why mid-sentence deletion is refused

**Why mid-sentence deletion is refused rather than allowed.** It is the edit
that silently inverts meaning: "Existing payment rails have no native concept of
delegated machine authority" becomes its own opposite when "no" is dropped, and
every remaining word is still the document's. An earlier version of this gate
passed exactly that string. A machine cannot tell a harmless dropped
parenthetical from a dropped negation, so both are failed and the fix is to
quote the shorter unbroken run instead. The check locates each run in the source
and refuses a cover whose runs sit within twelve words of each other, because
that is a deletion wearing a splice's clothes.

### Why the check is verbatim spans, not a word list

That last row is why the check is verbatim spans and not a word list. The old
bag-of-words version passed a deck that had quietly rewritten 53 strings, because
every individual word appeared somewhere in the article. `mode="words"` still
exists for the case where the person asked you to write the content and the
document is background rather than script, and it is too weak for anything else.

## Related

- [[exhibits]]
- [[design-principles]]
- [[brand]]
- [[KPMG House Style — PowerPoint & Report QRG]]
- [[SKILLS — Library Index]]
