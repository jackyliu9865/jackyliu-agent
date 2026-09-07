---
tags: [note, skills, kpmg-deck, design, visual-reference]
date: 2026-08-26
last_updated: 2026-08-27
---

# Visual reference — what a finished page looks like

Added 26 August 2026 on house instruction: *"Why doesn't this look like the other
outputs, asymmetrical warfare, capital allocators market, future of money?"*

The written rules in `design-principles.md` and `exhibits.md` describe this. They did
not make it happen, because a rule you read is not a page you have seen. **These 38
rendered pages are the target.** Look at them before laying out a data slide, and
compare the finished render against them afterwards.

| Deck | Pages | Source |
|---|---|---|
| `capital-allocators-*.jpg` | 14 | Hong Kong — The Capital Allocator's Market |
| `new-machine-economy-*.jpg` | 12 | The New Machine Economy |
| `asymmetric-warfare-*.jpg` | 12 | Asymmetric Warfare — Doctrine and the Corporate Playbook |

All three are built on this master, by this skill. **They are private work product:
they stay on this machine and in this vault, and no page of them is published,
uploaded or pasted into any third-party tool.**

---

## The page shape they all share

Every data page in all three decks is one of four compositions. None of them is a
placeholder layout with a bullet list beside a chart, which is the DD-readout shape and
the reason a deck built only from `Analysis_Horizontal` looks like a different document.

### Pattern A — two stacked exhibits, prose read on the right

`capital-allocators-04`, `new-machine-economy-04`, `asymmetric-warfare-05`

The workhorse. The exhibit column is **13.70 cm**, the master's own column
(`TL["plot_x"]`, `TL["plot_w"]`), the read column is **13.70 cm** at 17.43
(`TL["read_x"]`, `TL["read_w"]`), and the read runs the **full height** of both
exhibits. Two exhibits means two arguments that compound, not one argument cut in half.

*Corrected 26 August 2026. This paragraph previously said 20.40 cm and 7.20 cm, which
is `TL_WIDE`. That is not what these decks do. Measured across all 38 pages: every
exhibit in all three decks is **13.70 or 28.40 cm wide and nothing in between**, and
every read column is 13.70 (or 9.30 in a three-column page). Not one exhibit is 20.40.
`qa.gate_exhibit_width` enforces exactly those two widths, so the old numbers would have
failed the build, and the code sample below — which uses `quarter_top_left` at 13.70 —
was already right while the prose beside it was wrong.*

```python
ex.chart_exhibit(s, "line_markers", cats, series, title=..., basis=...,
                 slot="quarter_top_left", chart_id="C1")   # top exhibit
ex.chart_exhibit(s, "column", cats2, series2, title=..., basis=...,
                 slot="quarter_bottom_left", chart_id="C2")  # bottom exhibit
ex.commentary(s, paragraphs, heading="Reading the two exhibits")
ex.exhibit_source(s, "Source: ...")                        # one source for the page
```

### Pattern B — chart above, table below, prose read on the right

`asymmetric-warfare-06`

Same frame as A, with the lower exhibit a `data_table()` instead of a chart. Use it
when the second thing the reader needs is values rather than a shape, typically the
underlying study, the peer set or the workings.

### Pattern C — one full-width exhibit, prose read in columns beneath

`capital-allocators-06`

For an exhibit that genuinely needs the width: a dumbbell across twelve sectors, a long
category axis, a timeline. The read becomes **two or three short columns underneath**,
not a right-hand column. Nothing else goes on the page.

### Pattern D — full-bleed statement page

`capital-allocators-01`, `new-machine-economy-01`

Cover and divider. Template artwork, nothing added.

---

## What the read column does, and does not do

**Prose, not bullets.** Look at any of the 38 pages: there is not a bullet glyph in the
read column of any of them. Short paragraphs, one idea each, each ending in a full
stop: a body paragraph is not a bullet, and only bullets go unpunctuated (house
instruction, 27 August 2026, correcting what this file said before that date, and
the reason the rendered pages above show no terminal stops). `ex.commentary()` adds
it for you; `deckkit.bullets()` is for the
DD placeholder layouts and produces a different document.

**A dark-blue header bar when the column needs naming.** "Reading the two exhibits",
"Why they disagree", "The machines are already here in numbers". `ex.header_bar()`, or
`commentary(heading=...)`.

**It reaches the bottom.** If the read stops two thirds of the way down, the
composition is wrong, not the writing. Merge two thin slides, add the second exhibit,
or move to Pattern C.

---

## Exhibit furniture, on every one of the 38 pages

1. **Slide title is the finding**, 44pt, one line. Never a topic.
2. **Strapline is the so-what**, one sentence, Pacific blue, directly beneath.
3. **Exhibit title in KPMG Blue bold 10pt**, stating what that exhibit shows. Each
   exhibit on the page gets its own.
4. **Basis line in grey beneath it**: period, units, scope, population. This is what
   lets a reader check the number.
5. **Series labelled at the end of the line**, not in a legend, wherever there is room.
   See `new-machine-economy-04`: "Automated: 60.5" sits at the line end.
6. **Data labels on the values that carry the argument**, not on every point.
7. **One focal colour.** Everything else grey. `ex.focal(n, index)`.
8. **One source line for the whole page**, 6pt, at 15.72 cm.

---

## Colour means one thing per page, and the page says what

House note, 26 August 2026, on a RAG chip that meant nothing: *"These colours have to mean
something yea?"*

Every non-default colour on a page encodes one stated thing, and the note or a legend
says what. A traffic light carried over from a different scale, an accent used because
the shape looked bare, or a palette applied because a chart had three series and the
palette had three colours, are all decoration. Decoration comes out.

Test it in one sentence: *"On this page, blue means ___."* If the sentence will not
finish, the colour is wrong.

## Related

- [[design-principles]]
- [[exhibits]]
- [[brand]]
- [[qa-checklist]]
