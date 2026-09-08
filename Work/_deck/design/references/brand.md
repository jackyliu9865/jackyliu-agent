---
tags: [note, skills, kpmg-deck, brand]
---

# Brand specification

Colour, type and grid, read off the master and the two reference layouts the
template ships for the purpose (`Color palette & useful tools/buttons`,
`FOR REFERENCE_Table formatting`).

**Where this file and instinct disagree, this file wins.** These are the values
the deck is checked against.

## Colours

The template declares a named custom palette. **It is a closed set**, and most of
it is reserved for a specific job. An off-palette colour is the most visible way
a slide reads as not-ours.

### Core

| Name | Hex | Used for |
|---|---|---|
| Dark Blue | `0C233C` | All title and body text, header bars, cover/divider/back-cover backgrounds |
| KPMG Blue | `00338D` | Charts only |
| Cobalt Blue | `1E49E2` | Theme accent 1; UpSlide section dividers |
| Pacific Blue | `00B8F5` | Straplines, the DRAFT banner, chart series |
| Blue | `76D2FF` | Charts |
| Light Blue | `ACEAFF` | Subsection divider background, "Read more" buttons, table header rows, charts |
| Blue Accent 1 | `D2DBF9` | Charts |
| White | `FFFFFF` | Content-slide background; text on dark fills |

### Greys

`333333` Grey 1 · `666666` Grey 2 · `989898` Grey 3 · `B2B2B2` Grey 4 ·
`E5E5E5` Grey 5

Grey 5 fills the summary strips on Key findings layouts and is a legal chart
colour. The others are for rules, dividers and de-emphasised text.

### Reserved accents

`510DBC` `7213EA` `B497FF` purples · `008E7E` `00C0AE` `7AFFBD` greens ·
`AB0D82` `FD349C` `FFA3DA` pinks

These exist in the theme and the template never uses them on a content slide.
Use one only when the user asks for a KPMG accent colour by name.

### Chart series order

Assign in this order and stop when you run out. Never wrap into unrelated
colours.

1. `0C233C` Dark Blue
2. `ACEAFF` Light Blue
3. `00B8F5` Pacific Blue
4. `00338D` KPMG Blue
5. `D2DBF9` Blue Accent 1
6. `76D2FF` Blue

Beyond six series, or for a visually separate group, draw from the secondary
set: `34556D` Blue Gray, `77A8BE` Aqua, `96CEE4` Light Turquoise, `E5E5E5`
Grey 5. `deckkit.CHART_SERIES` and `CHART_EXTRA` hold both in order.

### RAG

**Only** these three, and **only** for status: red `ED2124`, amber `F1C44D`,
green `269924`. Red is not a highlight colour.

## Type

One display face, one text face. There is no third size for emphasis — use bold.

| Role | Size | Weight | Colour | Face |
|---|---|---|---|---|
| Content slide title | 44pt | — | `0C233C` | KPMG Bold |
| Cover / divider title | 66pt | — | White on cover and back cover, black on dividers | KPMG Bold |
| Cover subtitle and date | 14pt (11pt from level 3) | — | White | Arial |
| Strapline (idx 18) | 9pt | bold | `00B8F5` | Arial |
| Body level 1 | 9pt | **bold** | `0C233C` | Arial |
| Body level 2 | 9pt | regular | `0C233C` | Arial |
| Body levels 3–5 | 9pt | regular | `0C233C` | Arial, bulleted `•` |
| Header bars | 9pt | bold | White on `0C233C` | Arial |
| Table text | 8pt | see table rules | — | Arial |
| "Read more" buttons | 8pt | bold | `0C233C` on `ACEAFF` | Arial |
| Source / footnote (idx 17) | 6pt | regular | — | Arial |
| Master footer and classification | 6pt | — | — | Arial |

**9pt body is deliberate.** The house style is dense and evidence-first. Where
content does not fit at 9pt, cut it or split the slide. Bumping to 14pt breaks
the layout.

Titles run at 70% line spacing, so a two-line title still fits its box. Body
paragraphs carry 6pt space-after — never add blank paragraphs for spacing.

**Body levels 1 and 2 have no bullet glyph.** Level 1 bold is a lead-in, level 2
the sentence under it, and only levels 3–5 are bullet lists. `bullets()` defaults
to level 2; pass `level=3` for visible bullets.

## Fonts

The brand faces are **KPMG** (display) and **Arial** (everything else). The
template asks for `KPMG Bold` on titles and Arial on all body text.

**Two families, and the second catches people out:**

| Family | Faces |
|---|---|
| `KPMG` | 8 — Bold, Light, Extralight, Thin, each with an italic |
| `KPMG Logo` | 1 — the dingbat from `KPMGLOGO1.ttf`. **A separate family**, so a `KPMG` glob or family reference misses it |

**Match on the full name.** `typeface="KPMG Bold"` resolves. PostScript names are
hyphenated (`KPMG-Bold`) and do not work in a `typeface` attribute.

**Presence is not use.** A font listed in a folder proves nothing about what a
deck rendered with. Install state, the render probe and the quarantine trap are
in `Work/_deck/environment.md`.

**Where the font is absent**, fall back to Arial Bold and say so in the delivery
note. Do not restyle the deck to compensate, and do not claim the brand check
passed.

**Legacy trap.** The template still references `Univers Condensed Light`, the
pre-refresh face, in 40 places on older layouts. It is not installed and was not
supplied. Unexpected metrics on one of those layouts is this. Not worth chasing
unless it shows up.

## Grid

**Everything is in centimetres.** Inches appear alongside only because
`python-pptx` takes `Inches()` and the template's geometry is authored in them.
Reason and specify in cm; convert at the call site. A call passing inches without
`units="in"` builds a table about 2.5× too small, so this is a correctness rule.

Slide is **33.87 × 19.05 cm** (13.333" × 7.5"), 16:9.

These are measured off the template's own placeholder geometry. **Where this
table and an inch figure disagree, this table wins.**

| Guide | cm | ≈ in |
|---|---|---|
| Left margin | **2.73** | 1.07" |
| Right edge of content | **31.13** (width 28.40) | 12.26" |
| Two-column split | second column at **17.43**, each **13.70** wide | 6.86" / 5.39" |
| Three-column split | **2.73 / 12.28 / 21.83**, each 9.30 wide | 1.07" / 4.83" / 8.59" |
| Title band | y 1.22, height 1.50 | y 0.48" |
| Strapline | y 2.72 | y 1.07" |
| Content top | y 3.73 | y 1.47" |
| Content bottom | y **16.32** | y 6.43" |
| Half-height split | second row at y **10.13** | y 3.99" |
| Key findings summary strip | y 14.43 | y 5.68" |
| Source strip (idx 17) | y 16.32, height 1.00 | y 6.43" |

Derived: the content zone is **12.60 cm tall by 28.40 cm wide**, the two-column
gutter is **1.00 cm**, the three-column gutter **0.25 cm**.

`deckkit` exports `CM` and `GRID`, so a shape on the second column is
`CM(GRID["col2_x"])` rather than a retyped literal.

**The content zone ends at y 16.32, which is the top of the source strip.**
Placeholder idx 17 occupies 16.32 to 17.32. Nothing goes below the source strip.
The master carries a caption reading *"NO CONTENT BELOW THIS LINE UNDER ANY
CIRCUMSTANCES"*. **The caption box sits at y 17.45; the line it labels is at
16.33**, which is the operative limit and the value `deckkit` exports as
`GRID["no_content_below"]`. Reading 17.45 as the limit lets content sit on top of
the footer.

Every content slide inherits the KPMG logo bottom-left, the copyright line, the
classification line, the page number, the UpSlide nav circles and a 14pt bold
Pacific Blue **DRAFT FOR DISCUSSION PURPOSES ONLY** banner. That banner is on the
master. Where the user says the deck is final, it has to come off in the master,
never be covered with a white box.

## Tables

Stated on the template's own reference layout:

- Cell margin **0.1 cm** on all four sides
- Font size **8**
- **Title row**: `0C233C` fill, white bold text
- **Header row**: `ACEAFF` fill, `0C233C` bold text
- **Body**: transparent fill, black text

No banding, no first-row auto-emphasis, no gridline colour games.
`deckkit.table()` applies all of it; pass `title_row=True` for a spanning title
band and `header_rows=2` for the two-layer header.

Column headings bottom-align. **Totals bold, sub-totals not.** Percentages
italic, though never the percentage column heading. A zero is a hyphen; negatives
go in brackets. Numbers right-align, labels left-align.

On any bar or column chart the value axis **starts at zero**, because a bar
encodes its value as length. `deckkit.chart()` enforces it.

## What the template does that you should preserve

- **Straplines carry the argument.** Every content layout has a strapline slot
  because the house style is one assertion per slide, stated at the top. "Revenue"
  is a wasted title; "Revenue grew 14% but mix deteriorated" is the slide.
- **Sources are not optional.** Any slide with a number fills idx 17.
- **Key findings layouts pair a finding with a rating** — when the page is a
  rating. Fill the RAG chip and state the scale in the note, or `qa.gate_rag_key`
  fails it. Where the same layout carries a narrative page — which `layouts.md`
  recommends for three columns of prose — there is no rating: drop the chip with
  `deckkit.drop()`, then `deckkit.shade()` so the summary strips keep their
  Grey 5.
- **The summary strip** at y 14.43 is for the recommendation, never a restatement
  of the finding.
- **Colour that encodes anything gets a legend**, placed next to the data and
  labelled in words. A single accent marking one focal item needs none. A second
  series, a category encoding, a RAG scale or a before-and-after pair does.
- **Say what a colour means before choosing it.** If you cannot finish the
  sentence "on this page, blue means ___", the colour is decoration. Cut it.
