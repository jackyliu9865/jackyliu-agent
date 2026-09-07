---
tags: [note, skills]
date: 2026-08-05
last_updated: 2026-08-21
---

# Brand specification

Extracted from the master, the theme, and the two reference layouts the template
ships for exactly this purpose (`Color palette & useful tools/buttons` and
`FOR REFERENCE_Table formatting`). Where this file and your instinct disagree,
this file wins — these are the values the deck will be checked against.

## Colours

The template declares a named custom palette. **This is a closed set.** Nothing
outside it belongs in a deck, and most of it is reserved for specific jobs.
Introducing an off-palette colour is the single most visible way a slide reads
as not-ours.

### Core

| Name | Hex | Where it's used |
|---|---|---|
| Dark Blue | `0C233C` | All title text, all body text, header bars, cover/divider/back-cover backgrounds |
| KPMG Blue | `00338D` | Charts only |
| Cobalt Blue | `1E49E2` | Theme accent 1; UpSlide section dividers |
| Pacific Blue | `00B8F5` | Straplines, the "DRAFT FOR DISCUSSION" banner, chart series |
| Blue | `76D2FF` | Charts |
| Light Blue | `ACEAFF` | Subsection divider background, "Read more" buttons, table header rows, charts |
| Blue Accent 1 | `D2DBF9` | Charts |
| White | `FFFFFF` | Content-slide background; text on dark fills |

### Greys

`333333` (Grey 1) · `666666` (Grey 2) · `989898` (Grey 3) · `B2B2B2` (Grey 4) ·
`E5E5E5` (Grey 5)

Grey 5 is the fill behind the summary/recommendation strips on Key findings
layouts and is also a legal chart colour. The others are for rules, dividers and
de-emphasised text.

### Reserved accents

`510DBC` Dark Purple · `7213EA` Purple · `B497FF` Light Purple ·
`008E7E` Dark Green · `00C0AE` Green · `7AFFBD` Light Green ·
`AB0D82` Dark Pink · `FD349C` Pink · `FFA3DA` Light Pink

These exist in the theme but the template never uses them on a content slide.
Don't reach for them to add variety. Use them only if the person explicitly asks
for a KPMG accent colour by name.

### Charts

Assign series in this order and stop when you run out — don't wrap around into
unrelated colours:

1. `0C233C` Dark Blue
2. `ACEAFF` Light Blue
3. `00B8F5` Pacific Blue
4. `00338D` KPMG Blue
5. `D2DBF9` Blue Accent 1
6. `76D2FF` Blue

If a chart needs more than six series, or needs a visually separate group of
series, draw from the secondary set: `34556D` Blue Gray, `77A8BE` Aqua,
`96CEE4` Light Turquoise, `E5E5E5` Grey 5.

`deckkit.CHART_SERIES` and `CHART_EXTRA` hold these in order.

### RAG / traffic lights

**Only** these three, and **only** for status:

- Red `ED2124`
- Amber `F1C44D`
- Green `269924`

Red is not a highlight colour. If something isn't a status rating, it doesn't get
one of these.

## Type

One display face and one text face. There is no third size for emphasis — use
bold.

| Role | Size | Weight | Colour | Face |
|---|---|---|---|---|
| Content slide title | 44pt | — | `0C233C` | KPMG Bold |
| Cover / divider title | 66pt | — | White on cover & back cover, black on dividers | KPMG Bold |
| Cover subtitle & date | 14pt (11pt from level 3) | — | White | Arial |
| Strapline (idx 18) | 9pt | bold | `00B8F5` | Arial |
| Body level 1 | 9pt | **bold** | `0C233C` | Arial |
| Body level 2 | 9pt | regular | `0C233C` | Arial |
| Body levels 3–5 | 9pt | regular | `0C233C` | Arial, bulleted `•` |
| Header bars | 9pt | bold | White on `0C233C` | Arial |
| Table text | 8pt | see table rules | — | Arial |
| "Read more" buttons | 8pt | bold | `0C233C` on `ACEAFF` | Arial |
| Source / footnote (idx 17) | 6pt | regular | — | Arial |
| Master footer & classification | 6pt | — | — | Arial |

## Fonts: installed, and never bundled

The brand faces are **KPMG** (display) and **Arial** (everything else). The
template asks for `KPMG Bold` on titles and `Arial` on all body text.

**Installed on this machine, 21 August 2026.** Nine faces from Commercial Type,
version 1.1 (2016), designed by Christian Schwartz and Paul Barnes: KPMG Bold,
Light, Extralight and Thin, each with an italic, plus the `KPMGLOGO1.ttf` dingbat
face.

**Two families, verified against the macOS font registry on 21 August 2026:**

| Family | Faces | Full names |
|---|---|---|
| `KPMG` | 8 | `KPMG Bold`, `KPMG Bold Italic`, `KPMG Light`, `KPMG Light Italic`, `KPMG Extralight`, `KPMG Extralight Italic`, `KPMG Thin`, `KPMG Thin Italic` |
| `KPMG Logo` | 1 | The dingbat face from `KPMGLOGO1.ttf`. **A separate family**, so a `KPMG` family reference will not reach it |

The **full name** is the string the template matches on, so `typeface="KPMG Bold"`
resolves directly. PostScript names are hyphenated (`KPMG-Bold`); do not use those
in a `typeface` attribute.

| Where | Path | Why |
|---|---|---|
| Live install | `~/Library/Fonts/KPMG-*.ttf` **and `KPMGLOGO1.ttf`** (the glob alone misses the logo face) | What macOS, PowerPoint and LibreOffice actually read |
| Master copy | `~/Library/Application Support/Artemis/fonts-vendor/kpmg/` | Survives a fonts folder reset; same off-vault pattern as `skills-vendor/` |

**Updated 25 August 2026: the skill now carries and deploys them itself.**
All nine faces live in `assets/fonts/` and `scripts/fonts.py` installs any the
machine lacks on the first `new_deck()` call. A new device is no longer a
checklist. The licensing position is unchanged and is enforced rather than
trusted: `assets/fonts/` is in `.gitignore`, and `fonts.check_not_tracked()`
fails loudly if that ever breaks.

**These files are never committed to the vault.** They are licensed to KPMG by
Commercial Type. The vault is a git repository that autosyncs to GitHub, so
placing them inside it would be redistribution of a commercial licence. This is
the same reasoning that keeps the vendored Anthropic skills out of the vault, and
it is not negotiable. A new machine installs them from the source files, not from
a pull.

**Verify before trusting a render.** Font presence is not the same as font use,
so check the real effect rather than the file listing. Build any slide and
convert it, then read the fonts the PDF actually embedded:

```bash
soffice --headless --convert-to pdf deck.pptx --outdir .
python3 -c "import re,io;print(sorted(set(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+#,\-_]+)', io.open('deck.pdf','rb').read()))))"
```

A correct render returns `KPMG-Bold` alongside `Arial-BoldMT`. If it returns only
Arial faces, the font is not resolving and every title in the deck is wrong,
whatever the file listing says.

**If the font is absent** (another machine, a colleague's copy, a CI box), fall
back to Arial Bold and **say so in the delivery note**. Do not restyle the deck
to compensate, and do not claim the brand check passed.

**One legacy gap.** The template still references `Univers Condensed Light` in 40
places, the pre-refresh KPMG face, and it is not installed and was not supplied.
Those references sit in older layouts. If a slide built on one of them renders
with unexpected metrics, this is the cause. Not worth chasing unless it shows up.

Titles run at 70% line spacing — a two-line title still fits its box. Body
paragraphs carry 6pt space-after, so don't add blank paragraphs for spacing.

**9pt body is deliberate.** This is a due-diligence house style: dense, evidence-
first, many short paragraphs. Don't "improve readability" by bumping to 14pt —
it breaks the layout and looks off-brand. If content doesn't fit at 9pt, cut it
or split the slide.

Body levels 1 and 2 have no bullet glyph. Level 1 bold works as a lead-in or
mini-heading, level 2 as the sentence under it, and only levels 3–5 are actual
bullet lists. `bullets()` defaults to level 2 for this reason — pass
`level=2` for a plain flow, `level=3` when you want visible bullets.

## Grid

**Measurements are in centimetres**, set 21 August 2026 after a deck shipped with inch values read as centimetres and every table came out 2.5x too small.
Inches are given alongside only because `python-pptx` takes `Inches()` and the
template's own geometry is authored in them. **Reason and specify in cm; convert at
the call site.** 1 inch = 2.54 cm.

Slide is **33.87 cm × 19.05 cm** (13.333" × 7.5"), the 16:9 widescreen page.

**These are read off the template's own placeholder geometry**, not converted from
the inch values. Corrected 21 August 2026: the first cm version was 0.01 low in five
places because it was back-converted rather than measured. Where this table and an
inch figure disagree, this table wins.

| Guide | Value (cm) | (approx inches) |
|---|---|---|
| Left margin | **2.73** | 1.07" |
| Right edge of content | **31.13** (width 28.40) | 12.26" |
| Two-column split | second column starts **17.43**, each **13.70** wide | 6.86" / 5.39" |
| Three-column split | **2.73 / 12.28 / 21.83**, each 9.30 wide | 1.07" / 4.83" / 8.59" |
| Title band | y 1.22, height 1.50 | y 0.48", height 0.59" |
| Strapline | y 2.72 | y 1.07" |
| Content top | y 3.73 | y 1.47" |
| Content bottom | y **16.32** | y 6.43" |
| Half-height split | second row starts y **10.13** | y 3.99" |
| Key findings summary strip | y 14.43 | y 5.68" |
| Source strip (idx 17) | y 16.32, height 1.00 | y 6.43" |

Derived, and worth knowing: the **content zone is 12.60 cm tall by 28.40 cm wide**,
the **two-column gutter is 1.00 cm** and the **three-column gutter is 0.25 cm**.

`deckkit` exports `CM = Cm` from `pptx.util`, so anything you place by hand is
written `CM(2.72)` rather than `Inches(1.07)`.

The master carries a marker reading **"NO CONTENT BELOW THIS LINE UNDER ANY
CIRCUMSTANCES"** at y 17.45 cm (6.87").

**Precisely: the content zone ends at y 16.32 cm, which is the top of the source
strip.** Placeholder idx 17, the mandatory source line, sits at exactly y 16.32 with
a height of 1.00 cm, so it occupies 16.32 to 17.32. Nothing you add goes **below the
source strip**. *(Corrected 21 August 2026: an earlier version said nothing goes
below 16.33 cm, which would have banned the source line the same file makes
mandatory.)*

Every content slide inherits from the master, and you don't need to draw any of
it: KPMG logo bottom-left, copyright line, "Document Classification: KPMG
Confidential", page number, the UpSlide nav circles top-right, and a 14pt bold
Pacific Blue **"DRAFT FOR DISCUSSION PURPOSES ONLY"** banner. That banner is on
the master, so it appears on every slide until someone edits the master — if the
person says the deck is final, tell them it has to be removed in the master
rather than silently covering it with a white box.

## Tables

Stated verbatim on the template's own reference layout:

- Cell margin **0.1cm** on all four sides
- Font size **8**
- **Title row**: `0C233C` fill, white bold text
- **Header row**: `ACEAFF` fill, `0C233C` bold text
- **Body**: transparent fill, black text

No banding, no first-row auto-emphasis from the table style, no gridline colour
games. `deckkit.table()` applies all of this; pass `title_row=True` when the
table needs a spanning title band above its headers, and `header_rows=2` for the
two-layer header pattern the template demonstrates.

Column headings bottom-align. **Totals bold, sub-totals not.** Percentages
italic, but never the percentage column heading. A zero in a table is a hyphen;
negatives go in brackets.

On any bar or column chart the value axis **starts at zero**, because a bar
encodes its value as length and a truncated baseline lies about the difference.
`deckkit.chart()` enforces it.

Numbers right-align, labels left-align. `deckkit.table()` does this by column
position, which is right for the ordinary case of a label column followed by
value columns.

## Things the template does that you should preserve

- **Straplines carry the argument.** The template gives every content layout a
  strapline slot because the house style is one assertion per slide, stated at
  the top. A slide titled "Revenue" with no strapline is a wasted slide; make it
  "Revenue grew 14% but mix deteriorated".
- **Sources are not optional.** Any slide with a number gets idx 17 filled.
- **Key findings layouts pair a finding with a rating — when the page is a
  rating.** Fill the RAG chip and state the scale in the note, or
  `qa.gate_rag_key` fails it: a red square that encodes nothing is decoration.
  **When the same layout is used for a narrative page**, which is what
  `layouts.md` now recommends for three columns of prose, there is no rating to
  give, and the chip comes off with `deckkit.drop()` rather than being left red
  and meaningless. Follow it with `deckkit.shade()` so the summary strips keep
  the Grey 5 the dropped "Value" chip was carrying. *(Reconciled 26 August
  2026: this bullet and the narrative-page guidance read as contradicting each
  other, and they do not — they cover different uses of one layout.)*
- **The summary strip at the bottom of Key findings layouts** (grey, y 14.43 cm /
  5.68") is for the recommendation, not a restatement of the finding.
- **Colour that encodes anything gets a legend.** Added 21 August 2026 on the reviewer's
  instruction: every deck and every chart carries a key explaining what each colour
  means. A single accent colour marking one focal item needs no key. Anything
  beyond that does: a second series, a category encoding, a RAG scale, a
  before-and-after pair. Place the key adjacent to the data, never off in a corner,
  and label it in words rather than by swatch alone.
- **Say what a colour means before you choose it.** If you cannot state the
  encoding in a sentence, the colour is decoration and should come out.

## Related

- [[SKILLS — Library Index]]
- [[UNIVERSAL — Agent Rules & Standards]]
- [[Projects Index]]
