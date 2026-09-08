---
tags: [note, skills, kpmg-deck, build]
date: 2026-09-08
---

# Build API — how to fill the master with code

**Read this at step 5 of the pipeline in `START-HERE.md`**, once the content is
written and the plan for each slide is agreed. `content-rules.md` governs what
the words may be; this governs how they get onto the page.

Generate decks by filling the real template, never by redrawing it.
`assets/template.pptx` carries the theme, the logo, the footer, the
classification line, the page numbers and 26 authoring layouts. Add a slide on a
layout and every font, size and colour is inherited correctly with no styling
code at all.

Redrawing the look from scratch does not work: KPMG Bold is not applied, the
logo and footer are gone, and the result is approximately right and wrong in
every detail a reviewer checks.

## Building

```python
import sys; sys.path.insert(0, "<path-to-design>/scripts")
from deckkit import *

prs = new_deck()

s = add(prs, "Cover page")
fill(s, title="Project Falcon",
        ph11=["Commercial due diligence", "", "12 August 2026"],
        ph13="KPMG. Make the Difference.")

s = add(prs, "One Column Text")
fill(s, title="Revenue grew but mix deteriorated",
        ph18="Growth is real; margin quality is not.",
        ph56=[("Headline", 0), ("Revenue rose 14% CAGR FY22–FY25.", 1)]
             + bullets(["Volume contributed 9pp of the 14pp.",
                        "Price/mix contributed 5pp, all from one contract."]),
        ph17="Source: Management accounts, KPMG analysis")

save(prs, "falcon.pptx")   # relative to the project folder; never machine-absolute
```

`fill()` keys are `ph<idx>`, and the idx numbers come from `layouts.md` — they
differ between layouts. Values are a string, a list of strings, or a list of
`(text, level)` tuples. `bullets(items)` builds the tuple list for you.

Levels are 0-based and the master assigns each one a job: **0 and 1** are
unbulleted paragraphs, **2 and deeper** carry the bullet glyph at increasing
indents. A lead-in with bullets under it is `[("Headline", 0)] + bullets([...])`.

The master makes level 0 bold, but every content layout overrides that back to
regular, so a lead-in will not look like a heading on its own. Where one must
stand out, put the emphasis in the header bar (`Analysis_*` idx 54, the Key
findings bars) rather than bolding body text by hand.

**`probe("Two Columns Text")` prints a layout's real placeholder map** — idx,
type and geometry — straight from the template. Use it when a layout is missing
from `layouts.md`, or to confirm one that is there.

Helpers: `note()` for the source line, `strapline()` for the key message,
`rag(slide, idx, "red"|"amber"|"green")` for traffic-light chips, `table()` for
brand-formatted tables (**cm by default**, `units="in"` for the old behaviour),
`drop()` to remove an unused placeholder, `shade()` to restore a fill a dropped
chip was carrying.

## Charts and tables

Build every exhibit with `exhibits.chart_exhibit()`, never `deckkit.chart()`
directly. The former registers its numbers so `databooklet.check_booklet()` can
prove the chart traces to the booklet, and an unregistered chart is a build
error.

Full signatures, every argument and the geometry are in **`exhibits.md`**. Read
it before any slide carrying a number.

## House style, enforced

`qa.gate_house_style` runs the QRG find-and-replace list over every string on
every slide, and `save()` raises on a finding.

Full rules are in **`house-style-qrg.md`**; deck-side typography, colour and
table formatting are in **`brand.md`**.

The four that catch people most often: **no full stops on bullets, though body
paragraphs do take one**; **sentence case** rather than title case; **numbers
one to nine in words**; and a percentage move is in **percentage points**.

On the first: the rule names *bullets*, meaning list items, and a prose
paragraph is not a bullet. `fill()` and `exhibits.commentary()` add the terminal
full stop to body paragraphs, and leave bullets, header bars, summary strips,
straplines, source lines and cover text alone. Notes and sources take a full
stop. `scripts/test_punctuation.py` asserts the whole matrix; run it after
touching `deckkit._is_prose_body`.

## The rules that matter most

- **Never assign `text_frame.text`.** It collapses the placeholder to one
  unstyled run and takes the inherited brand formatting with it. `deckkit`
  writes runs individually; anything going around it must do the same.
- **Never set a font size, face or colour on placeholder text.** Inheritance
  already gives the right one. An explicit `Pt(14)` on body text is a bug.
- **Only palette colours**, and only in their assigned role. RAG red, amber and
  green are for status ratings and nothing else.
- **9pt body is correct.** Dense is the house style. Where content does not fit,
  cut it or split the slide. Do not shrink boxes or grow type.
- **Nothing below the source strip at y 16.32 cm.** That is the footer zone and
  the master says so.
- **Fill the strapline and the source line.** Every content layout has both,
  because the house style demands an assertion and a provenance on each slide.
- **Never open `assets/specimen-deck.pptx` as a starting point.** Its 28 sample
  slides cross-link, and deleting them leaves orphans that collide with new
  slides and make PowerPoint report the file as corrupt. `new_deck()` opens the
  cleaned template. The specimen is for looking at. See [[slide-template]].

## Adding your own shapes

Some layouts give a blank region (`Title only_Blank`, the chart half of
`Analysis_Horizontal`). Shapes added there are yours to style, so apply the
brand by hand: Arial, 9pt body and 8pt in tables, palette fills, zero cell and
text insets, and stay inside the grid columns in `brand.md`. Charts go in as
native PowerPoint charts with `CHART_SERIES` colours in order.

**Place them in centimetres.** `deckkit` exports `CM` (alias of `pptx.util.Cm`)
and `GRID`, a dict of every guide in cm, so a shape on the second column of a
two-column split is `CM(GRID["col2_x"])` rather than a retyped inch literal.
`table()` takes cm by default. `in2cm()` and `cm2in()` convert a value read off
the template.

## The modules

| Module | What it is for |
|---|---|
| `deckkit` | Placeholders, tables, the grid, `save()`. The base layer |
| `exhibits` | Every exhibit type, the slot system, the read column. **Anything with a number in it** |
| `qa` | The gate set. `qa.report()` returns findings per gate |
| `databooklet` | Writes the booklet and proves every chart links to it |
| `icons` | SVG icons that stay vector and recolourable |
| `fonts` | Installs the nine faces on a new machine |
| `scan_text`, `validate_pptx`, `doctor`, `selftest`, `slides_to_md` | QA and diagnosis |

Each module's own docstring is the reference for its API.

## Traps

Layout-specific gotchas, each with what it costs and how to avoid it, are in
**`layouts.md`** under *Traps found building on this master*. Read it before
hand-placing anything on a layout you have not used.

## Related

- [[content-rules]] — what the words may be
- [[layouts]] · [[brand]] · [[exhibits]] · [[house-style-qrg]]
- [[qa-checklist]] — the QA pass
