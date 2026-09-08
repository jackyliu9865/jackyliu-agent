---
tags: [note, skills, kpmg-deck, design]
---

# Slide design principles

Composition: the artboard, the grid, worked examples of what good looks like,
minimal text, high visual density, clarity.

**Read this before laying out a slide.** `brand.md` says what colour and
what size. `layouts.md` says which placeholders exist. This says how to compose.

---

## 0. Look at the target first

`references/visual-reference/` holds 38 rendered pages from three finished decks built
on this master. **Everything below describes those pages.** Look at them before laying
out a data slide and compare your render against them afterwards, because a rule you
have read is not a page you have seen. `00 — Visual Reference Index.md` names the four
compositions they use.

The single most common failure this fixes: pouring every data slide into
`Analysis_Horizontal` with a bullet list beside one chart. That is the DD-readout
shape. Published thought leadership stacks **two exhibits** in a 20.40 cm column with
**prose**, not bullets, in a 7.20 cm read column that reaches the bottom of the page.

## 1. The artboard

**A slide is a fixed canvas, 33.87 cm by 19.05 cm, and you compose inside it.** You
are not filling boxes, you are placing elements on a page. The distinction is the
whole difference between a deck that reads as designed and one that reads as
generated.

Every slide has the same four zones, inherited from the master and not negotiable:

| Zone | Top (cm) | Bottom (cm) | What lives there |
|---|---|---|---|
| **Title band** | 1.22 | 2.72 | The finding, 44pt KPMG Bold |
| **Strapline** | 2.72 | 3.73 | The one-line argument, 9pt bold Pacific Blue |
| **Content** | 3.73 | 16.32 | Everything you build. **12.60 cm of vertical room, and that is all you get** |
| **Footer** | 16.32 | 19.05 | The source strip (idx 17, y 16.32, height 1.00) then master furniture. Nothing goes below the source strip |

**The content zone is smaller than people assume.** 12.60 cm tall by 28.40 cm wide.
A deck fails on layout most often because someone designed for a full page and then
squeezed. Design for 12.60 cm from the start.

**Before you write a line of build code, decide the composition.** Sketch it as a
sentence: "left two-thirds a five-year revenue and margin chart, right third three
sentences on the margin story, source line beneath". If you cannot say the
composition in a sentence, the slide has more than one argument on it.

---

## 2. The grid

Everything sits on the column lines below. **Nothing is positioned by eye, and
nothing is nudged to look right.** Most of what reads as professional is things
lining up; most of what reads as amateur is things nearly lining up.

| Guide | cm |
|---|---|
| Left margin | 2.73 |
| Content width | 28.40 |
| Right edge | 31.13 |
| Two columns | col 2 starts 17.43, each 13.70 wide |
| Three columns | 2.73 / 12.28 / 21.83, each 9.30 wide |
| Content top | 3.73 |
| Content bottom | 16.32 |
| Half-height rows | row 2 starts 10.13 |

`deckkit` exports these as `GRID`, in centimetres, so you never retype them.

**The gutters are what the eye reads.** The two-column split leaves **1.00 cm**
between columns; the three-column split leaves **0.25 cm**, which is tight, so
three columns need short text or they read as a wall. Keep gutters constant down
the page. A gutter that changes between rows is the most visible
sloppiness on a slide and nobody can say why it looks wrong.

**Vertical rhythm.** Pick one spacing unit for the deck and make every vertical gap
a multiple of it. Three values total: between the strapline and the first element,
between elements, and between an element and its source line. Not fifteen.

**Optical alignment beats mathematical alignment for text.** A text box's visible
left edge is its inset, not its frame, so a chart whose axis labels start at 2.72
and a text box whose frame starts at 2.72 will not look aligned. Align what the eye
sees.

---

## 3. Composition patterns

Pick one deliberately. **A deck where every content slide uses the same pattern
wastes the template**, and it is exactly how the last HTML dashboard ended up with
half its right-hand column empty on every exhibit.

| Pattern | Use when | Geometry |
|---|---|---|
| **Full-width hero** | One chart carries the whole slide. A five-year trend, a market-share gap, a driver tree | Chart spans 28.40 cm. Strapline above, two or three lines of read beneath, source under that |
| **Two-thirds / one-third** | A chart with a genuinely short read | Chart 18.63 cm, text 8.77 cm, keeping the 1.00 cm gutter. **No template layout gives this split** (`Analysis_Horizontal` is 13.70/13.70), so build it by hand on `Title only_Blank`. Only when the read is short by nature |
| **Half and half** | A chart with a substantial read that must sit beside it | 13.70 cm each, which is what `Analysis_Horizontal` gives. **Needs four or more sentences, or the right column goes empty** |
| **Small multiples** | The same measure across periods, segments or peers | Three to five panels across 28.40 cm, shared scale, shared baseline, one caption |
| **Three columns** | Situation, effect, opportunity. Any genuine triptych | 9.30 cm each. This is what `1_Key findings_3 columns` exists for |
| **Stacked pair** | A chart and its decomposition | Chart in the top 6 cm, bridge or breakdown beneath, aligned on the same x scale |
| **Full-width table** | n up to about 20 and exact values matter | 28.40 cm. A table is an exhibit: it gets a strapline and a source line |

**The rule that prevents the observed failure: measure the text before choosing the
split.** Three sentences beside a chart in a 13.69 cm column leaves a hole. Either
the chart goes full width with the text beneath it, or the analysis is genuinely
longer than it was. **If a column would sit more than about a third empty, the
wrong pattern was chosen.**

### The same rule applies vertically

**A short exhibit on a full-width slide leaves a dead band, and it reads exactly as
badly as an empty column.** A five-row table is about 5 cm tall on a 12.60 cm
canvas, so roughly 7 cm sits empty below it.

**The fix is never to stretch the exhibit.** Stretching row heights to fill space
makes a table look padded and a chart look distorted. Do one of these instead:

- **Move it into a two-thirds column** and put the read beside it. A short table
  usually has three or four sentences worth saying about it, and that is exactly
  the pattern that needs them.
- **Stack a second exhibit under it.** A working capital table above and the DSO
  trend beneath is one argument told twice, which is stronger than either alone.
- **Add the read underneath**, two or three lines at 9pt, then the source line.
- **Combine two thin slides into one.** Two five-row tables that each half-fill a
  slide are one slide.

**Sanity check:** content runs from y 3.73 to y 16.32, and the master's own
half-height line is y 10.13. If everything you have placed ends above 10.13, the
slide is half empty and needs one of the four moves above.

---

## 4. Minimal text, high visual

**One argument per slide.** The title states it. The strapline sharpens it. The
exhibit proves it. Everything else is support. A slide with two arguments is two
slides, and the reader takes neither.

- **The title is the finding, never the topic.** "Revenue grew 14% but mix
  deteriorated", not "Revenue". A slide titled with a noun is a wasted slide.
- **9pt body is deliberate and dense.** This is a due-diligence house style. Do not
  bump the size to improve readability: cut the words or split the slide.
- **Prose in short paragraphs, bullets only for genuine lists.** Every bullet is at
  least a full sentence. A bullet of three words is a label pretending to be a
  point.
- **Never more than about six bullets** in one block. Past that the reader stops
  reading and starts scanning, and scanning finds nothing.
- **Cut every sentence that describes the analysis.** The subject of a sentence is
  the company, the market or the number. (Fuller rule in the `pov-analysis` skill's
  `references/report-voice.md`, which is a separate package and may not be
  installed alongside this one.)
- **Numbers do the work.** "DSO rose from 54 to 71 days" beats "working capital
  efficiency deteriorated" in fewer characters and with more force.

**High visual means the evidence is seen, not read.** If a point can be a chart, it
is a chart. If a chart needs a paragraph to explain it, it is the wrong chart.

---

## 5. Clarity

- **The reader should get the argument from the title and the exhibit alone**, in
  about five seconds. The body text is for the person who wants the detail, not for
  the person deciding whether to care.
- **One accent colour, actually applied to the thing you want looked at.** Data in
  KPMG Blue, the focal item in Pacific Blue, everything else neutral. Colour
  everywhere is colour nowhere.
- **A colour legend wherever colour encodes anything** beyond a single accent, placed
  next to the data rather than in a corner, and labelled in words. The review asked for this directly.
- **Direct labels on the data.** A legend the eye has to travel to is a tax on every
  reader.
- **No gridlines, no chart borders, no drop shadows, no gradients, no 3D, no pie
  charts, no dual axes.**
- **Bars start at zero.** Bars encode length, so a truncated baseline lies about the
  size of a difference. If the variation is too small to see from zero, use a line,
  a dot plot, an indexed series or a table.
- **A share is never shown without its whole.** A percentage-of-group figure carries
  the full breakdown, or the reader cannot size it.
- **Every data slide carries a source line** at idx 17: document, page, line.

---

## 6. What good looks like

**Study the standard, cite nothing.** The reference for craft is top-tier strategy
consulting output: one message per page, stated as the title; a single dominant
exhibit; very little body text; everything on a grid; heavy use of white space;
colour used once, on purpose.

**Never name or cite a competitor consultancy, or KPMG's own thought leadership, in
a client-facing deliverable.** Study it for craft, cite only primary, government,
agency and neutral sources. This rule is not negotiable and it applies to the deck
as much as the report.

**The best available worked example is bundled**: `assets/specimen-deck.pptx`. It is
a real deck on this master. Open it before building, and match its density, its
restraint and its layout variety. When a slide you have built looks worse than the
specimen, the difference is almost always one of three things: too much text, too
many colours, or things not lining up.

---

## 7. The seven checks before a slide is done

Run these on every content slide. They catch most of what a reviewer would.

1. **Does the title state a finding?** If it is a noun phrase, rewrite it.
2. **Is there exactly one argument on this slide?** If two, split it.
3. **Is any column more than about a third empty?** If so, the wrong composition
   was chosen. Change the pattern, do not stretch the chart.
4. **Does everything sit on the grid**, with constant gutters and a consistent
   vertical rhythm?
5. **Does every colour mean something, and is there a key wherever it does?**
6. **Is there a source line, and does every bar start at zero?**
7. **Does the content reach past y 10.13 cm?** That is the master's own half-height
   line, not a guess. If not, the slide is half empty vertically. Do not stretch the exhibit; add the read, stack a second exhibit,
   move it into a column, or merge two thin slides.

### Two helpers that make check 6 possible

`Title only_Blank` is where tables and hand-built exhibits go, and **it carries
neither a strapline slot (idx 18) nor a source slot (idx 17)**. That is how an
exhibit ships with no source line, which is precisely what happened on the last POV
dashboard.

`deckkit` closes it. `strapline()` and `note()` now fall back to `strapline_box()`
and `source_box()` when the layout has no placeholder, drawing a brand-format line
on the grid: 9 pt Arial bold Pacific Blue in the strapline band, 6 pt Arial black
just above the content floor. You call the same two functions on every layout and
they always work.

`check(prs)` also inspects layouts with no idx 17 or 18 and flags a content slide
that has a table, chart or picture but no source line or no strapline. It counts
tables and charts explicitly, because their text lives in cells rather than in a
shape text frame.

---

## 8. Where this fits

| Reference | Answers |
|---|---|
| `design-principles.md` (this file) | How to compose a slide |
| `brand.md` | What colour, what size, what the grid values are |
| `layouts.md` | Which placeholders each layout has, and their idx numbers |
| `../SKILL.md` | How to build it with `deckkit`, and the QA pass |
| POV skill `references/qa-checklist.md` | The full nine-gate QA when the deck is part of a POV |

## Related

- [[SKILLS — Library Index]]
- [[qa-checklist]]
- [[analytical-components]]
- [[report-voice]]
