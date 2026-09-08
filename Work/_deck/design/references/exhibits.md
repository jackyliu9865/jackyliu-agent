---
tags: [note, skills, kpmg-deck, design, exhibits]
---

# Data exhibits

**KPMG runs on graphing and data-heavy analysis.** The failure this file
exists to stop: a deck of text blocks with two charts in seventeen slides,
colours that meant nothing, and a table that read as a grid of words.

Read this before `design-principles.md` on any slide that carries a number.
That file says how to compose a page. This says what an exhibit is.

**Evidence base.** Three published KPMG decks, read page by page:
*Splintering supply chains*, *Hong Kong: the capital allocator's market*, and
*Virtual assets: 2025 review and 2026 outlook*. Every rule below is something
all three do.

---

## 0. The goal

**The goal is the most visually effective exhibit the given content supports.**

Two things follow, and they are in tension with each other, which is the point.

**The audience is a general reader, not a deal team.** A due-diligence readout
can be dense because the reader is paid to work through it. A published piece
has to earn attention in about five seconds. So the exhibit does the arguing,
the read supports it, and anything that is neither gets cut.

**But the content is the client's, not yours.** "Based on content given" is the
limit: make what is there look as good as it can be made to look. Do not add a
finding, extend a list to balance a column, or invent a datapoint to complete a
series. If a slide is thin, the composition is wrong, not the content.

What this means in practice:

- **One exhibit should carry the page.** A general reader takes one idea per page
- **Direct labels beat legends.** A legend is a lookup; a label is a fact
- **Annotate the thing you want looked at.** An event marker, a reference line
  or one callout, per `§8`. A chart that needs a paragraph to explain it is the
  wrong chart
- **Spend colour once.** `sorted_bar(highlight=...)` exists for exactly this
- **White space is not waste.** Density is the DD house style; a published page
  is allowed to breathe

## 1. The five-part grammar

An exhibit is never a bare chart. In the published work it is always five
parts, in this order, with no exceptions across the pages read:

| Part | Specification | Why it exists |
|---|---|---|
| **Exhibit title** | The finding, as a sentence. Arial **10pt bold, KPMG Blue**, left aligned, no internal margin | A chart titled with a noun makes the reader do the analysis |
| **Basis line** | Period, units, scope, and **which axis carries what**. Arial 8pt, Grey 1, directly beneath | An exhibit with no basis is a chart nobody can check |
| **The plot** | No gridlines, no chart title, no border. Direct labels on the marks | |
| **The key** | Adjacent to the data, labelled **in words** | Colour without a key is decoration |
| **Source** | Named document, issuer or database. 6pt | |

`exhibits.chart_exhibit()` makes this impossible to forget: you cannot draw the
plot without passing the title and the basis, and it registers the numbers in
the data booklet as it goes.

**The basis line is the part people skip and the part reviewers check.**
Worked examples, lifted verbatim from the published decks:

- `2018-2025, USD billion (column, LHS) and % (dot, RHS)`
- `2000–2025, times growth, size of bubbles represents 2025 export value`
- `Return on capital minus the sector's cost of capital (ROIC−WACC, ROE−COE for Financials), FY20 – FY25`
- `2001–2025, Quadrants are pegged to 2001 CI and OF median levels. Firm quantity is fixed at top 100 by revenue per year`

### Reconciling the QRG with "no chart title"

The house-style QRG says a chart title is Arial 10pt bold KPMG Blue, left
aligned. `design-principles.md` says a chart carries no title because the 44pt
slide title already holds the finding. Both are right, and the published decks
show how: the chart object itself has **no** title, and the title is drawn as a
text box above the plot. That is what `exhibit_head()` does.

---

## 2. Every chart links to the data booklet

**Every graph links to the accompanying databooklet**, which is the source of
record.

Exhibits register their numbers as they are drawn, so `databooklet.write()`
produces the booklet *from* the deck. The two cannot drift apart, and
`databooklet.check_booklet()` fails a deck that holds a chart the booklet does
not, or a booklet entry with no basis or no source.

Booklet sheets: **Index** (one row per exhibit: id, slide, kind, title, basis,
units, source, source type), **Chart_Data** (long format, one row per point)
and **Read me**. Cell colours follow the house data standard: yellow input,
green formula, blue primary source, purple secondary or market source, orange
caveat. A source that says "estimate", "analysis", "illustrative" or "model" is
classified purple automatically, so an illustrative number cannot pass itself
off as measured.

A chart built with raw `deckkit.chart()` never registers, so the gate fails it.
That is deliberate: `deckkit.chart()` stays for a quick internal sketch, and
`exhibits.chart_exhibit()` is the one that ships.

---

## 3. Which exhibit for which question

| The question | Exhibit | Function |
|---|---|---|
| How did one measure move over time | Column, or line past about 8 periods | `chart_exhibit` |
| How do categories rank | Bar, sorted by value, never alphabetically | `chart_exhibit("bar")` |
| Where does each item sit, **and how far did it move** | **Dumbbell**, two marks joined by a rule | `dumbbell` |
| Two genuinely different units on one page | **Combo**: columns on LHS, detached markers on RHS | `combo_exhibit` |
| Two variables plus a magnitude | **Bubble**, size as the third variable | `bubble_exhibit` |
| How a mix shifted | 100% stacked column or area | `chart_exhibit("column_stacked_100")` |
| The same measure across regions, segments or peers | **Small multiples**, one scale, one key | `multiples_head` + `chart_exhibit(group=…)` |
| How a whole divides | **Share bar**, segments labelled in place | `share_bar` |
| The three numbers that carry the page | **KPI band**, number, label, basis | `kpi_band` |
| Exact values, n up to about 20 | **Data table** as an exhibit, titled and sourced | `data_table` |
| The qualities that define a group | **Key features band**, cobalt, columns split by white rules | `key_features` |

**Never**: pie charts, doughnuts, 3D, gradients, drop shadows, dual axes other
than the sanctioned combo below.

### The one sanctioned dual axis

`combo_exhibit()` is the only exception to the no-dual-axis rule, because the
published work uses it and uses it correctly. It is permitted only when all
three hold:

1. the two series are in **genuinely different units**, not the same unit rescaled
2. the second series is drawn as **detached markers, not a line**, so it cannot be misread as a trend
3. the basis line **names both axes**, `(column, LHS)` and `(dot, RHS)`

The function refuses to build if the basis line does not contain LHS and RHS.

### Category count

`check()` **fails** past **20** categories, not 12, and `save()` raises on it: it
is a stop, not a warning, and calling it a warning here was wrong. The published
HKEX deck runs 21 bars with in-bar labels and reads perfectly, because the
labels are direct and the bars are sorted. Past 20, trim the window, use small
multiples, or use a table. See `§12` for the long-time-series case and the one
sanctioned escape.

---

## 4. Colour has to mean something

The house question on the first draft was **"What do these colours mean?"**,
asked of red chips that encoded nothing. That is now a gate, not a guideline.

- **One accent, actually applied to the thing you want looked at.** Everything else neutral
- **A key wherever colour encodes anything** beyond a single accent: a second series, a category, a RAG scale, a before-and-after pair. `qa.gate_chart_legend` fails a multi-series chart with no key
- **A traffic-light chip needs its scale stated on the slide.** `qa.gate_rag_key` fails a slide with RAG chips whose note does not say what red, amber and green mean. If you cannot state the scale, the colour is decoration and comes out
- **Ordered categories use the ordered ramp** `exhibits.SEQ_BLUE`, dark to light. Unordered categories use `CHART_SERIES`
- **Say what a colour means before you choose it.** If you cannot say it in a sentence, do not use it

---

## 5. Layout

### An exhibit fills a page slot

**An exhibit occupies a whole slot: half page, quarter page, full page, or two
on one page.** Map graphics follow the same rule.

An exhibit does not get an arbitrary rectangle. It fills a named fraction of
the content zone, and the fractions come off the master's own guides: content
runs y 3.73 to 16.32, the half-height line is y 10.13, and the two columns are
2.73 and 17.43, each 13.70 wide.

| Slot | left, top, w x h (cm) | Use |
|---|---|---|
| `full` | 2.73, 3.73, 28.40 x 12.59 | One exhibit carries the page |
| `half_left` | 2.73, 3.73, 13.70 x 12.59 | The workhorse: exhibit left, read right |
| `half_right` | 17.43, 3.73, 13.70 x 12.59 | The read, or a second exhibit |
| `half_top` | 2.73, 3.73, 28.40 x 6.40 | Full-width pair, upper |
| `half_bottom` | 2.73, 10.13, 28.40 x 6.19 | Full-width pair, lower |
| `quarter_top_left` | 2.73, 3.73, 13.70 x 6.40 | Two on a page, with a read beside |
| `quarter_bottom_left` | 2.73, 10.13, 13.70 x 6.19 | " |
| `quarter_top_right` / `quarter_bottom_right` | 17.43, ... | " |

```python
ex.chart_exhibit(s, "column", cats, series, title=..., basis=...,
                 slot="quarter_top_left", source=SRC)
```

**The slot is the total footprint including the title and basis block.**
`slot=` works the plot height out from what the head leaves behind, so the
caller never does that arithmetic and never gets it wrong. `qa.gate_exhibit_slot`
fails an exhibit placed anywhere else.

**Why this matters and not just tidiness.** A 20.40 cm exhibit at the left
margin ends at 23.13 cm and crosses the slide's vertical centre at 16.94. The
master's column ends at 16.43 and stops short of centre by design. the owner's
words on seeing it: *"Obviously over the middle line and wrong format."* The
slots make that failure unreachable.

Two stacked exhibits must land on the half-height line, not at whatever heights
happened to fit. Before slots they sat at 5.03 and 11.05, which is why the page
read as two charts dropped onto a slide rather than a designed pair.

### The default is the master's own grid

**Graphs align to the left margin, at 13.70 cm wide.** The standard is the
standard; do not carry another publication's formatting into it.

That is the governing rule and it corrects an earlier version of this file. The
published thought-leadership pages use a publication grid; **this master is the
standard**, and a chart sits on its columns unless there is a reason not to.

`exhibits.TL`, the default, is the master's own two-column split:

| Guide | cm |
|---|---|
| Plot left | **2.73**, the left margin |
| Plot width | **13.70**, the master's column |
| Gutter | 1.00 |
| Read column left | 17.43 |
| Read column width | 13.70 |

**Charts align left. They do not float, and they are not centred.** Every
exhibit's left edge is the left margin unless it is the second element of a
two-column layout, in which case it is 17.43.

`exhibits.TL_WIDE` (plot 20.40, read 7.20) is **for hand-built content only, and
never for a chart or a table.** Offering it as a situational width for an
exhibit that "cannot be read at 13.70" contradicts the gates and fails every
build. `gate_exhibit_width`
allows exactly two widths, 13.70 and 28.40, and `gate_exhibit_slot` constrains
the position as well, so a chart at 20.40 is rejected — it ends at 23.13 and
crosses the slide's centre line at 16.94, which is the failure the gate was
written for.

**A long series that cannot be read at 13.70 goes to 28.40**, the `full` or
`half_top` slot, not to an in-between width. That is the actual answer to the
problem TL_WIDE looked like it solved.

`exhibits.TL_FULL` (plot 28.40) is for a table, or a hero exhibit with the read
beneath rather than beside it.

The read column is **prose in short paragraphs, not bullets**, and prose
paragraphs **do** take a terminal full stop. `commentary()` adds it.
A 13.70 cm column 12 cm tall needs
six to nine short paragraphs; two lines in it is the imbalance flagged
on the first draft. If the read is genuinely two lines, the exhibit goes full
width and the read sits underneath it.

### Stacked exhibit pair

Two exhibits on one page, each with its own title and basis, sharing one source
line. Pass `draw_source=False` on the upper exhibit: it still registers its
source in the booklet, and the lower exhibit's source line covers both. Drawing
two source lines puts one of them in the gap above the lower exhibit's title,
where it collides. Use when the second exhibit decomposes the first. The HKEX deck's
"denominator problem" page is the model: the ten-year trend on top, the single
incremental-return comparison beneath it.

### Small multiples

One title, one basis, **one key for the row**, and panels on a shared scale.
Value-axis labels appear on the **first panel only**; repeating them three times
is three chances to read them differently. Pass `value_labels=False` on panels
two onward.

---

## 6. Tables are exhibits

`exhibits.data_table()` rather than `deckkit.table()` for anything a reader will
interrogate. Differences that matter:

- it carries the exhibit title and basis line, so a table is argued and sourced like a chart
- **row height comes from the row count**, not from stretching to fill a box. Stretched rows are what made the first draft's table read as padded
- numeric columns right-align with a gap from the next column, so a right-aligned header stops colliding with its left-aligned neighbour
- optional Grey 5 banding, as the published decks use

Table rules from the QRG still hold: 8pt, 0.1cm margins, numbers right, text
left, headings bottom aligned, totals bold, sub-totals not, percentages italic,
a zero is a hyphen, negatives in brackets.

**If the table is really a chart, make it a chart.** A column of "Over 3,000:1",
"About 60:1", "Over 300:1" is a ranked magnitude, and a ranked magnitude is a
bar chart. The table then holds the detail the chart cannot.

**`data_table()` does not register in the data booklet, and `check_booklet()`
cannot see that it has not.** `chart_exhibit()` registers
its numbers as it draws; a table does not, so a table full of figures can ship
with none of them in the booklet and every gate still green. For a qualitative
comparison table that is correct and nothing is missing. For a table a reader
will interrogate for numbers, either register them yourself with
`exhibits.register(...)` or make it a chart.

---

## 7. Icons stay vector

Icons are placed as pictures and should be SVG, so the fill colours can be
changed.

`icons.place()` writes an SVG the way PowerPoint writes one: a raster fallback
blip plus an `asvg:svgBlip` extension pointing at a real SVG part. PowerPoint
then offers Graphics Fill and Convert to Shape on it. `icons.recolour()` sets
every fill and stroke to a palette colour before it goes in, so a deck builds
in palette without anyone opening PowerPoint.

The raster fallback needs LibreOffice, which the render pass already requires.
Without it `place()` **refuses** rather than quietly inserting a flat picture,
because a silent downgrade is the failure being fixed.

`assets/icons/` currently holds a twelve-icon starter set drawn for this skill.
It is a stand-in. The firm's approved set drops in beside it.

---


## The two full signatures

A signature is read while writing the call. Both are load-bearing, so they are
written down here rather than guessed at.

```python
chart(slide, kind, categories, series, left, top, width, height,
      units="cm", number_format=None, data_labels=True, legend=None,
      colours=None, gap_width=60)

table(slide, rows, left, top, width, height,
      header_rows=1, title_row=False, col_widths=None, units="cm", align=None)
```

**`chart()` is the only way to draw a chart**, and charts are native PowerPoint
objects, never images. `kind` is one of `column`, `column_stacked`, `bar`, `line`,
`line_markers`, `scatter`. `series` is a list of `(name, [values])`. It applies the
brand rules for you: no gridlines, Arial 8pt axes and 6pt data labels, `CHART_SERIES`
colours in order, **no chart title** (the slide title carries the finding), and a
**zero baseline on every bar and column chart**. `number_format=None` infers a format
that does not drop precision, so 4.1 does not render as "4".

```python
s = add(prs, "Title only_Blank")
fill(s, title="Margin improved as revenue slowed")
strapline(s, "EBITDA grew faster than revenue in four of five years.")
chart(s, "column", ["FY21","FY22","FY23","FY24","FY25"],
      [("Revenue", [54.0, 58.2, 61.1, 63.0, 64.8]),
       ("EBITDA",  [4.1, 4.6, 5.2, 5.7, 6.3])],
      left=GRID["left"], top=GRID["content_top"],
      width=GRID["content_w"], height=11.0)
note(s, "Source: ar_pdfs/example_ar_2025.pdf, printed p.44, line 2.")
```

**`chart_from_data(slide, rows, chart_id, left, top, width, height, kind="column")`**
builds one straight from `Chart_Data` booklet rows, which is the path a POV
mandates: no chart drawn from a number that is not in the booklet.

**`table()` takes six positional arguments** before any keyword. `align` accepts a
per-column list of `"l"`, `"c"`, `"r"`; left out, it right-aligns only columns whose
body values are all numeric, so prose columns stay left.

```python
table(s, [["Force","Rating","Direction","Evidence"],
          ["Rivalry","Strong","Strengthening","Peer grew the market 40% against 2.8%"]],
      left=GRID["left"], top=GRID["content_top"],
      width=GRID["content_w"], height=4.0)
```

**`note()` and `strapline()` work on every layout.** They fill idx 17 and idx 18
where those exist, and fall back to `source_box()` and `strapline_box()` where they
do not. That matters because **`Title only_Blank`, the layout tables and hand-built
exhibits go on, carries neither slot**, which is how an exhibit ships with no source
line. `check(prs)` now flags a content slide on such a layout that has a table,
chart or picture but no source line or no strapline. Colour constants (`DARK_BLUE`,
`PACIFIC`, `CHART_SERIES`, …) are exported for charts and any shape you add by
hand.


## The modules, and what each is for

| Module | What it is for |
|---|---|
| `deckkit.py` | The master's placeholders: `new_deck`, `add`, `fill`, `note`, `strapline`, `rag`, `drop`, `shade`, `table`, `chart`, `check`, `save` |
| `exhibits.py` | Data exhibits. Charts: `chart_exhibit`, `line_exhibit` (end-labelled, optional log axis), `combo_exhibit`, `bubble_exhibit`, `waterfall`, `sorted_bar`, `dumbbell`. Furniture: `exhibit_head`, `commentary`, `key`, `header_bar`, `kpi_band`, `key_features`, `share_bar`, `data_table`, `multiples_head`, `small_multiples`, `panel_title`, `focal`, `sparse_labels` |
| `databooklet.py` | `write()` the .xlsx from the deck, `check_booklet()` to gate it |
| `qa.py` | 21 automated gates, the manual list, and `content_fidelity()`, which checks the deck against a supplied document as **contiguous verbatim spans**, not as a word list |
| `source_text.py` | Mode A. Pull the words out of a supplied `.md`, `.txt`, `.docx` or `.pdf`, including .docx tables and embedded chart categories, and **say what it could not reach** so picture text gets transcribed rather than silently lost |
| `validate_pptx.py` | The .pptx structural validator, **stdlib only**, runs on the Python already on the machine. Was borrowed from the pptx skill; bundled 25 Aug 2026 |
| `doctor.py` | What this machine has, what it lacks, and what that costs. Run it first on a new device |
| `icons.py` | `place()` a true SVG icon, `recolour()` it to palette |
| `fonts.py` | Self-deploying brand fonts. `new_deck()` calls `ensure_installed()`, which copies any missing face from `assets/fonts/` into the user font directory. A new machine needs no setup step |
| `package.py` | Wrap the skill **and its fonts** into one portable archive, for moving between your own machines. Git never carries the fonts, so this is the other half |
| `slides_to_md.py` | Export a deck one Markdown file per slide, plus an index |
| `selftest.py` | Builds a fixture deck using every exhibit type, gates it, and validates the file. Run after any change to the skill |

## Related

- [[design-principles]]
- [[brand]]
- [[qa-checklist]]
- [[layouts]]
- [[KPMG House Style — PowerPoint & Report QRG]]
- [[SKILLS — Library Index]]


---

## 8. Annotation

A chart that draws data and nothing else is not enough. The published decks
draw data **and the reader's route through it**.

None of it is possible without knowing where the plot area sits inside the
chart frame, and python-pptx does not expose that. So the engine stops guessing
and pins it: pass `plot_rect=INSET` to any chart, then build a matching
`PlotRect` and every annotation lands exactly.

```python
INSET = (0.10, 0.02, 0.87, 0.82)
ch = ex.chart_exhibit(s, "column", cats, series, title=..., basis=...,
                      left=L, top=T, width=W, height=H,
                      plot_rect=INSET, vmin=0, vmax=100)
r = ex.plot_rect(L, T, W, H, inset=INSET, vmin=0, vmax=100)
ex.reference_line(s, r, 50.0, "Half of all conflicts", side="right")
ex.event_line(s, r, r.x_at(22, n), "First attacks, Nov 2023")
ex.callout(s, r, r.x_at(37, n), r.y_at(34.11), "Trough came fourteen "
           "months after the first attack", dx=-2.9, dy=0.18)
ex.label_inside_bars(ch, number_format="0.0")
```

| Function | Use it for |
|---|---|
| `reference_line` | A hurdle, a break-even, a prior peak, labelled in words |
| `event_line` | The date something changed. The label clamps inside the plot |
| `callout` | The QRG call-out box, on the one mark that carries the argument |
| `label_inside_bars` | What keeps a 20-bar chart readable: the label travels with the mark |
| `sparkline` | A tiny inline series beside a number in a table or KPI tile |

**One annotation device per chart, chosen deliberately.** A reference line OR
an event marker OR a callout, not all three. Three devices on one chart is
clutter and the reader stops seeing any of them. Two tests before an annotation
stays: does it say something the axis does not already say, and does it say
something the read column does not already say? An event line at "2010" sitting
above an axis tick labelled 2010 fails the first. A callout repeating the read
word for word fails the second. Both shipped once and both came out.

**Put it in clear space.** A boxed note printed over the data it points at is
worse than no note. If there is no clear space, the chart is already full and
the annotation belongs in the read.

**Do not calibrate `INSET` against a LibreOffice render.** Verified 25 August
2026 with a probe chart pinned to the bottom-right quadrant: the manual layout
**is** honoured, and the horizontal position matched to the millimetre.
LibreOffice does however show a vertical offset of roughly 1 cm against the
specified inner rectangle. PowerPoint implements `layoutTarget="inner"` to
spec, so specifying the inset and deriving `PlotRect` from the same numbers is
exact there by construction. An earlier version was tuned to the LibreOffice
rendering, which would have moved every reference line the wrong way in
PowerPoint. **Judge annotation position in PowerPoint, not in the render.**

---

## 9. Overlap is a gate, not a judgement call

`qa.gate_overlap` and `qa.gate_column_bleed` compute bounding boxes and fail on
two text shapes sharing space, or an exhibit crossing into the commentary
column. They were added on 25 August 2026 after overlaps kept shipping: they
were being caught by eye off a render, which is not a method.

The first run found **41 overlaps across a deck that had already been reviewed
page by page.** A callout over a paragraph, a source line over an exhibit
title, a bold lead printed on its own supporting line.

**The single commonest cause: mixing geometries.** An exhibit moved to
`TL_WIDE` while its commentary stayed at the `TL` default, so the chart ran to
23.13 cm and the read column started at 17.43. **If the exhibit uses
`TL_WIDE`, its commentary must use `TL_WIDE["read_x"]` and
`TL_WIDE["read_w"]`.** Never mix the two on one slide.

A callout deliberately sits over its own chart, so the gate exempts overlaps
where one shape is a chart, table or picture. What it never permits is text on
text.

---

## 10. Slides as Markdown

`scripts/slides_to_md.py` exports a deck one Markdown file per slide, plus an
index. A .pptx cannot be read in Obsidian, diffed, searched or linked from
another note. This makes a deck reviewable as text and reachable from
`[[Vault Index]]`.

```bash
python3 scripts/slides_to_md.py deck.pptx out_dir/ --index "Deck name"
```

It carries the argument (title, strapline, exhibit titles, basis lines, the
read, sources) and the layout facts (which master layout, what sits where in
centimetres). Chart furniture such as category and value labels is skipped, so
the export reads as a document rather than a dump. **One-way, for review:** the
build script stays the source of truth.

The bundled sample deck is exported to `references/sample-slides/`.


---

## 11. Text overflow is invisible to a geometry check

A wrapped exhibit title prints its second line straight over its own basis
line, and `qa.gate_overlap` cannot see it, because
**the shape rectangles did not overlap**: the text overflowed its rectangle and
printed on top of whatever sat beneath. Only estimating the wrap catches it.

- `exhibits.est_lines(text, width_cm, size_pt, bold)` and `est_text_height(...)`
  estimate the rendered wrap. `_ADVANCE` is calibrated against rendered output:
  a 10pt bold title holds about **73 characters at 13.70 cm**
- `exhibit_head()` sizes the title and basis boxes to their wrapped height, so
  a long title pushes the plot down instead of printing over the basis
- `qa.gate_text_overflow` fails any text box holding more text than it can show
- `qa.gate_exhibit_title_length` fails a title that wraps to two lines. **The
  fix is a shorter sentence, not a smaller font.** A wrapped title also eats the
  slot's budget and pushes the plot down

This is the same class of defect as `deckkit.table_height`: PowerPoint grows a
table row to fit and reports nothing about it. Anywhere the rendered size can
differ from the shape size, the gate has to estimate rather than measure.

**Related trap, and the reason five annotations were silently misplaced.**
Converting exhibits to `slot=` left every hand-built
`plot_rect(left, top, width, height, ...)` call carrying the old hardcoded
numbers, so markers were positioned against a plot area that no longer existed.
Use `slot_plot_rect(name, title=..., basis=...)` instead: it derives the
rectangle from the same slot the chart was placed with, and measures the head
rather than assuming it, so the two cannot drift.

**Data labels on a line chart default to sitting ON the line.** Pass
`label_position="above"`.

---

## 12. Long series: pin the plot, blank the labels

Measured off a deck carrying a 50-week and a 20-quarter series.

**Pin the plot area on any chart with many categories.** Left to itself the
renderer is free to squeeze the plot into the top of its own frame and leave a
dead band underneath, which reads as a broken exhibit. `plot_rect=(0.06, 0.03,
0.83, 0.84)` fixes it, and `slot_plot_rect()` derives a matching `PlotRect` when
you also need to annotate.

**Blank the labels the axis should not print, with `sparse_labels()`.** Twenty
quarters at 8pt will otherwise rotate to 45 degrees and print a wall of dates.
Two traps make the obvious approaches fail:

- **an empty string does not work**, because PowerPoint collapses duplicate
  category names and the series quietly loses points
- **a run of spaces does not work either**: the label stub still draws, and the
  axis grows a row of tick marks where the blanks are

So each blank is a distinct number of zero-width spaces: unique to PowerPoint,
invisible to the reader.

```python
cats = ex.sparse_labels(quarters, {"Q2 2021", "Q2 2023", "Q2 2025", quarters[-1]})
ex.line_exhibit(s, cats, [("New repositories", values)],
                title=..., basis=..., slot="quarter_bottom_left",
                plot_rect=(0.06, 0.03, 0.83, 0.84))
```

`keep` also takes a predicate, `lambda i, v: ...`, when the rule is positional
rather than a set of names.

**The 20-category gate is a hard stop.** `check()` fails past 20 and `save()`
raises. Trimming the window is usually right, and the basis line then states the
window honestly. When a series genuinely has to keep every point — the peak the
slide argues would disappear under aggregation — `save(prs, path,
verify="warn")` is the escape, and the override belongs in the delivery note in
words. Passing `verify="warn"` to make a screen go green is not the same thing.
