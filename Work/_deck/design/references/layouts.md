---
tags: [note, skills]
date: 2026-08-05
---

# Layout catalog

> **Units.** The geometry tables below are in **inches**, because that is how
> the template itself is authored and what `probe()` and `inspect_layout.py`
> report. The house standard for reasoning and for anything you place by hand is
> **centimetres**: see the cm grid in `brand.md` and the `GRID` dict exported by
> `deckkit`. Multiply an inch value by 2.54 to get cm.


Every layout available in `assets/template.pptx`, with the placeholder `idx`
numbers you pass to `fill()`. The idx numbers are not sequential and they differ
between layouts that look similar — read the table for the layout you're
actually using rather than guessing from a neighbouring one.

Sizes shown are the layout's own override. Where a cell says nothing about size,
the placeholder inherits the master: **44pt titles, 9pt body**. Inheritance is
the whole point — leave it alone and the slide is brand-correct for free.

Look up layouts by name (`add(prs, "Two Columns Text")`); the names are stable,
the indices are not.

## Choosing a layout

| You have | Use |
|---|---|
| Deck opener | `Cover page` |
| Start of a numbered section | `Section divider`, then `Subsection divider` |
| A chart or table plus commentary | `Analysis_Horizontal` (side by side) or `Analysis_Vertical` (chart on top) |
| Prose or bullets, one flow | `One Column Text` |
| Two parallel arguments | `Two Columns Text` |
| Findings with a per-finding RAG rating | `Key findings_*` — pick by column/block count |
| Financial summary tiles | `Summary Financials_6 blocks` / `_5 blocks` |
| A cover letter | `Transmittal Letter` |
| Deck closer | `Back Cover_Report` / `_Proposal` / `_Publications` |
| A title and nothing else (you're drawing the body yourself) | `Title only_Blank` or `Title Only_strapline` |
| **A three-column narrative page** with no exhibit on it | `1_Key findings_3 columns`, not hand-built columns |
| The same in two columns | `Key findings_2 columns` |

Layouts whose names start with `FOR REFERENCE_` or contain `DO NOT delete` are
not for authoring. The `FOR REFERENCE_Table formatting` layout is where the
table rules in `brand.md` come from; `UpSlide_*` layouts belong to the
automation add-in.

The template also carries a second slide master holding five UpSlide fixtures —
`Table of content Storage Layout`, `Section Divider Storage Layout`,
`SubSection Divider Storage Layout`, `Reminder shapes Storage Layout` and
`UpSlide Breadcrumb`. They are parts bins for the add-in, not layouts. That
leaves 26 authoring layouts, all of them documented below.

## Narrative pages go on the Key findings layouts

Added 25 August 2026, after four pages of a live deck were rebuilt. A page that
carries three short columns of prose and no exhibit was hand-built on
`Title only_Blank`, and every one of them left a third to a half of the page
empty, because a hand-placed text box is only as tall as its text.

`1_Key findings_3 columns` solves it with geometry rather than with more words:
a dark header bar per column, a **fixed 9.30 x 10.10 cm body box** whatever the
text length, and a summary strip per column along the bottom at y 14.43. Three
columns of unequal prose still line up, and the strips anchor the foot of the
page. `Key findings_2 columns` is the same idea in two.

**Both ship chips you have to deal with.** Each column carries a red RAG chip
(idx 72/73/74, or 72/77) and a grey "Value" chip beside its summary strip (idx
52/56/60, or 52/73). On a page that is not a status rating they encode nothing,
and `qa.gate_rag_key` fails the red one, correctly.

```python
s = add(prs, "1_Key findings_3 columns")
fill(s, title="Three groups have to move",
     ph54="Banks and payment networks", ph64=bullets_or_paras,
     ph55="Build rails that settle at machine speed",       # summary strip
     ...)
strapline(s, "...")          # this layout has no idx 18; strapline() falls back
drop(s, 72, 73, 74, 52, 56, 60)      # the chips this page does not use
shade(s, 55, 59, 63)                 # Grey 5 behind the summary strips
```

`shade()` matters: with the "Value" chip dropped, an unfilled summary strip
renders as an outlined white box that reads as an empty field. Grey 5 is the
fill the master already uses there.

**Neither layout has a strapline placeholder (idx 18).** `strapline()` falls
back to a brand-format text box on the grid, so you call it the same way.

## The repeating slots

Three idx values mean the same thing everywhere they appear, so learn them once:

- **`17`** — source / footnote strip at the bottom (6pt). Any slide showing data
  gets one. `note(slide, "Source: ...")`.
- **`18`** — strapline directly under the title (9pt bold Pacific Blue). This is
  the "so what" of the slide, in one sentence. `strapline(slide, "...")`.
- **`54`, `57`, `61`, `65`, `69`, `73`** — dark-blue header bars, 0.61 cm tall,
  white 9pt bold text. These are block/column titles.

On the Key findings layouts, three families of idx travel together per column:
a header bar, a body text box, a small RAG chip (0.41 cm square, `rag()` recolours
it), and a grey summary strip along the bottom. Read the table to pair them up.

### `Cover page`

Background: `0C233C`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | 1.07, 1.47  5.4 x 3.23 | ctrTitle | 66pt; text `FFFFFF`; “Title slide text only” |
| 11 | 1.07, 5.31  5.4 x 1.1 | body | 14pt; text `FFFFFF`; “Click to edit Master text styles” |
| 12 | 6.86, 1.47  5.4 x 4.96 | pic | 18pt; text `FFFFFF`; “Insert cover picture here” |
| 13 | 1.07, 6.43  5.39 x 0.39 | body | 14pt; text `FFFFFF`; “KPMG. Make the Difference.” |

**idx 12 is a picture placeholder, and an empty one is not invisible.** With no
approved cover image it renders as a dashed empty frame across the right half of
the cover, in the render and in PowerPoint. `check()` does not catch it, because
a picture placeholder holds no prompt text to match. Either put an approved image
in it or take it off with `drop(s, 12)`; a cover that is plain dark blue with the
title on it is correct and clean.

### `Section divider`

Background: `0C233C`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | 1.39, 1.92  6.31 x 3.18 | ctrTitle | 66pt; text `000000`; “Section name [PROPOSAL]” |

### `Subsection divider`

Background: `ACEAFF`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | 1.39, 1.92  6.31 x 3.18 | ctrTitle | 66pt; text `000000`; “Subsection name [PROPOSAL]” |

### `Title only_Blank`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |

### `Title Only_strapline`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |

### `One Column Text`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |
| 56 | 1.07, 1.47  11.18 x 4.96 | body | regular; “Click to edit Master text styles” |

### `Two Columns Text`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |
| 56 | 1.07, 1.47  5.39 x 4.96 | body | regular; “Click to edit Master text styles” |
| 57 | 6.86, 1.47  5.39 x 4.96 | body | regular; “Click to edit Master text styles” |

### `Analysis_Horizontal`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | 1.07, 0.48  11.18 x 0.59 | title | “Click to edit Master title style” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |
| 54 | 6.86, 1.47  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title for Commentary box” |
| 55 | 1.07, 1.47  5.39 x 4.96 | body | 18pt; bold; text `000000`; “Chart / Table” |
| 56 | 6.86, 1.7  5.39 x 4.73 | body | regular; “Click to edit Master text styles” |

### `Analysis_Vertical`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | 1.07, 0.48  11.18 x 0.59 | title | “Click to edit Master title style” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |
| 54 | 1.07, 3.99  11.18 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title for Commentary box” |
| 55 | 1.07, 1.47  11.18 x 2.44 | body | 18pt; bold; text `000000`; “Chart / Table” |
| 56 | 1.07, 4.22  11.18 x 2.2 | body | regular; “Click to edit Master text styles” |

### `Summary Financials_6 blocks`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 10 | 1.07, 1.47  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 11 | 1.07, 3.99  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 12 | 4.83, 1.47  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 13 | 4.84, 3.99  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 14 | 8.59, 1.47  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 15 | 8.59, 3.99  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |

### `Summary Financials_5 blocks`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 15 | 1.07, 3.99  5.54 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 16 | 6.72, 3.99  5.54 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 18 | 1.07, 1.07  11.18 x 0.39 | body | text `00B8F5`; “Use this strapline to” |
| 10 | 1.07, 1.47  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 12 | 4.83, 1.47  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |
| 14 | 8.59, 1.47  3.66 x 0.24 | body | 9pt; bold; text `FFFFFF`; fill `0C233C`; “Click to edit block title” |

### `FOR REFERENCE_Key Findings Overview`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | 1.07, 0.48  11.18 x 0.59 | title | “Click to edit Master title style” |

### `Key findings_1 column`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 52 | 11.78, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 54 | 1.07, 1.47  11.18 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 55 | 1.07, 5.68  10.71 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 56 | 1.07, 1.7  11.18 x 3.98 | body | regular; “Click to edit Master text styles” |
| 72 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |

### `Key findings_1 column half page`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 52 | 6.0, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 54 | 1.07, 1.47  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 55 | 1.07, 5.68  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 56 | 1.07, 1.7  5.39 x 3.98 | body | regular; “Click to edit Master text styles” |
| 72 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |

### `Key findings_2 columns`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 52 | 6.0, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 54 | 1.07, 1.47  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 55 | 1.07, 5.68  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 56 | 1.07, 1.7  5.39 x 3.98 | body | regular; “Click to edit Master text styles” |
| 72 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 73 | 11.78, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 74 | 6.86, 1.47  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 75 | 6.86, 5.68  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 76 | 6.86, 1.7  5.39 x 3.98 | body | regular; “Click to edit Master text styles” |
| 77 | 6.9, 1.51  0.16 x 0.16 | body | fill `ED2124` |

### `1_Key findings_3 columns`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 52 | 4.26, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 54 | 1.07, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 55 | 1.07, 5.68  3.19 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 56 | 8.02, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 57 | 4.83, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 59 | 4.83, 5.68  3.19 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 60 | 11.78, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 61 | 8.59, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 63 | 8.59, 5.68  3.19 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 64 | 1.07, 1.7  3.66 x 3.98 | body | regular; “Click to edit Master text styles” |
| 65 | 4.83, 1.7  3.66 x 3.98 | body | regular; “Click to edit Master text styles” |
| 66 | 8.59, 1.7  3.66 x 3.98 | body | regular; “Click to edit Master text styles” |
| 72 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 73 | 4.87, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 74 | 8.63, 1.51  0.16 x 0.16 | body | fill `ED2124` |

### `Key findings_4 blocks`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |
| 52 | 6.0, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 54 | 1.07, 1.47  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 55 | 1.07, 3.16  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 56 | 11.78, 3.16  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 57 | 6.86, 1.47  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 59 | 6.86, 3.16  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 68 | 1.07, 1.7  5.39 x 1.46 | body | regular; “Click to edit Master text styles” |
| 69 | 6.86, 1.7  5.39 x 1.46 | body | regular; “Click to edit Master text styles” |
| 72 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 73 | 6.9, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 74 | 6.0, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 75 | 1.07, 3.99  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 76 | 1.07, 5.68  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 77 | 11.78, 5.68  0.47 x 0.75 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 78 | 6.86, 3.99  5.39 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 79 | 6.86, 5.68  4.92 x 0.75 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 80 | 1.07, 4.22  5.39 x 1.46 | body | regular; “Click to edit Master text styles” |
| 81 | 6.86, 4.22  5.39 x 1.46 | body | regular; “Click to edit Master text styles” |
| 82 | 1.12, 4.03  0.16 x 0.16 | body | fill `ED2124` |
| 83 | 6.9, 4.03  0.16 x 0.16 | body | fill `ED2124` |

### `Key findings_6 blocks`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| 54 | 1.07, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| — (title) | inherits master | title | “Click to edit Master title style” |
| 52 | 4.26, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 55 | 1.07, 3.16  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 56 | 8.03, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 57 | 4.83, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 59 | 4.83, 3.16  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 60 | 11.78, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 61 | 8.59, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 63 | 8.59, 3.16  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 64 | 4.26, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 65 | 1.07, 3.99  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 67 | 1.07, 5.68  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 68 | 8.03, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 69 | 4.83, 3.99  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 71 | 4.83, 5.68  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 72 | 11.78, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 73 | 8.59, 3.99  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 75 | 8.59, 5.68  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 76 | 1.07, 1.7  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 77 | 4.83, 1.7  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 78 | 8.59, 1.7  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 79 | 1.07, 4.22  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 80 | 4.83, 4.22  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 81 | 8.59, 4.22  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 82 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 83 | 4.87, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 74 | 8.63, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 84 | 1.12, 4.03  0.16 x 0.16 | body | fill `ED2124` |
| 85 | 4.87, 4.03  0.16 x 0.16 | body | fill `ED2124` |
| 86 | 8.63, 4.03  0.16 x 0.16 | body | fill `ED2124` |

### `1_Key findings_6 blocks`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| 54 | 1.07, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| — (title) | inherits master | title | “Click to edit Master title style” |
| 52 | 4.26, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 55 | 1.07, 3.16  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 17 | 1.07, 6.43  11.18 x 0.39 | body | 6pt; regular; “Click to add note/source here. Note above source. Us” |
| 56 | 8.03, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 59 | 4.83, 3.16  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 60 | 11.78, 3.16  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 61 | 8.59, 1.47  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 63 | 8.59, 3.16  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 64 | 4.26, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 65 | 1.07, 3.99  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 67 | 1.07, 5.68  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 68 | 8.03, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 69 | 4.83, 3.99  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 71 | 4.83, 5.68  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 72 | 11.78, 5.68  0.47 x 0.74 | body | 9pt; bold; text `0C233C`; fill `E5E5E5`; “Value” |
| 73 | 8.59, 3.99  3.66 x 0.24 | body | text `FFFFFF`; fill `0C233C`; “Click to add title” |
| 75 | 8.59, 5.68  3.19 x 0.74 | body | text `000000`; “Click to add summary/KPMG recommendation” |
| 78 | 8.59, 1.7  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 79 | 1.07, 4.22  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 80 | 4.83, 4.22  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 81 | 8.59, 4.22  3.66 x 1.46 | body | regular; “Click to edit Master text styles” |
| 82 | 1.12, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 83 | 4.87, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 74 | 8.63, 1.51  0.16 x 0.16 | body | fill `ED2124` |
| 84 | 1.12, 4.03  0.16 x 0.16 | body | fill `ED2124` |
| 85 | 4.87, 4.03  0.16 x 0.16 | body | fill `ED2124` |
| 86 | 8.63, 4.03  0.16 x 0.16 | body | fill `ED2124` |
| 87 | 4.01, 1.49  0.71 x 0.2 | body | 8pt; text `0C233C`; fill `ACEAFF`; “Read more” |
| 88 | 4.83, 1.47  2.83 x 0.24 | body | text `FFFFFF`; “Click to add title” |
| 89 | 7.77, 1.49  0.71 x 0.2 | body | 8pt; text `0C233C`; fill `ACEAFF`; “Read more” |

### `Transmittal Letter`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| 10 | 1.07, 2.57  5.39 x 3.86 | body | text `000000`; “Click to edit Master text styles” |
| 11 | 6.86, 2.57  5.39 x 3.86 | body | text `000000`; “Click to edit Master text styles” |
| 14 | 1.07, 1.47  5.39 x 0.94 | body | 9pt; text `000000`; “[Client name, personnel, and address]” |
| 15 | 6.86, 1.47  5.39 x 0.94 | body | 9pt; regular; text `000000`; “[Date]” |

### `FOR REFERENCE_Table formatting`

| idx | box (x, y, w × h in **inches**; multiply by 2.54 for cm) | type | notes |
|---|---|---|---|
| — (title) | inherits master | title | “Click to edit Master title style” |

### `Back Cover_Report`

Background: `0C233C`

No placeholders — this layout is fixed artwork. Add the slide and leave it alone.

### `Back Cover_Proposal`

Background: `0C233C`

No placeholders — this layout is fixed artwork. Add the slide and leave it alone.

### `Back Cover_Publications`

Background: `0C233C`

No placeholders — this layout is fixed artwork. Add the slide and leave it alone.

### `UpSlide_Section Divider_DO NOT delete`

Background: `1E49E2`

No placeholders — this layout is fixed artwork. Add the slide and leave it alone.

### `UpSlide_Subsection Divider_DO NOT delete`

Background: `ACEAFF`

No placeholders — this layout is fixed artwork. Add the slide and leave it alone.


## Traps found building on this master

Moved out of `SKILL.md` 27 August 2026: these are read while laying out a slide, not before deciding what to build.

Each of these cost a rebuild on a real deck. They are in the code now, but the
reason belongs here.

- **A chart is 13.70 cm or 28.40 cm wide. Nothing between.** `gate_exhibit_width`
  enforces it and `gate_exhibit_slot` enforces the position too. `exhibits.TL_WIDE`
  (20.40 cm) therefore **cannot carry a chart or a table** — it is for hand-built
  content only. A chart at 20.40 crosses the slide's centre line and fails.
- **Pass `plot_rect` on any chart with many categories.** Without it the renderer
  is free to squeeze the plot into the top of its own frame and leave a dead band
  underneath. `plot_rect=(0.06, 0.03, 0.83, 0.84)` pins it.
- **Blank a category with `exhibits.sparse_labels()`, never with `""`.** PowerPoint
  collapses duplicate category names, so empty strings silently merge points; a run
  of ordinary spaces still draws a label stub and grows a row of tick marks along
  the axis. `sparse_labels()` uses distinct runs of zero-width spaces.
- **`databooklet.write(notes=...)` takes `(label, text)` pairs**, not a list of
  strings. A list of strings raises `too many values to unpack`.
- **`exhibits.data_table()` does not register in the booklet.** `chart_exhibit()`
  does; a table does not, so `check_booklet()` will not notice a table whose
  numbers are nowhere. If a table carries numbers a reader will check, register
  them yourself or make it a chart.
- **An unused placeholder is not free.** The Cover page's picture placeholder
  prints as a dashed empty frame across half the cover, and the Key findings
  layouts ship a red RAG chip per column that `gate_rag_key` fails because it
  encodes nothing. `drop()` takes them off; `shade()` puts the master's Grey 5
  back behind the summary strips the dropped "Value" chip was anchoring.
- **Hand-drawn shapes obey the type scale.** `gate_type_scale` fails 11pt on a
  shape you added yourself. The scale is 6/7/8/9/10/14/18/24/44/66.
- **The 20-category gate is a hard stop, not a warning.** `save()` raises. If a
  genuine long time series has to keep every point, `save(prs, path,
  verify="warn")` is the escape, and the override then belongs in the delivery
  note in words. Do not pass `verify="warn"` to make a screen go green.

## Related

- [[SKILLS — Library Index]]
- [[UNIVERSAL — Agent Rules & Standards]]
- [[Projects Index]]
