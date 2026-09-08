---
type: deck-profile
deck_type: report
variants: [client, publication]
status: draft — awaiting sign-off
---

# Deck profile — Report

Read [[SKILL|the pipeline]] first. This file covers what is specific to a report.

A report is read without a presenter, months after it was written, by someone who
was not in the room. It carries its own argument. That is the whole reason it is
the densest of the three types.

## Two variants

Publication is a kind of report. The two share the type, the grid and the
palette, and they differ in composition, in closer, and in what the read column
does.

| | **Client** | **Publication** |
|---|---|---|
| Example | Due-diligence readout, valuation report, strategy findings | PWMA annual report, ROIC report series |
| Closer | `Back Cover_Report` | `Back Cover_Publications` |
| Built on | The placeholder layouts | `Title only_Blank` with `exhibits.*` furniture |
| Read column | Bullets, via `deckkit.bullets()` | **Prose, via `exhibits.commentary()`. No bullet glyph anywhere** |
| Ratings | `Key findings_*` with a RAG chip and the scale stated | None. Drop the chip with `deckkit.drop()`, then `shade()` |
| Source | One per slide, idx 17 | One for the whole page, 6pt at 15.72 cm |

**Getting this wrong is the failure the skill was corrected for.** A publication
built entirely from `Analysis_Horizontal` with bullets beside one chart comes out
looking like a due-diligence readout, because that is what it is.

## Front matter

| Order | Layout | Notes |
|---|---|---|
| 1 | `Cover page` | Title, subtitle, date, `KPMG. Make the Difference.` |
| 2 | `Transmittal Letter` | Client variant only, where the report takes a cover letter |
| 3 | `Title only_Blank` | Contents |
| 4 | `Section divider` | Then `Subsection divider` inside it |

## Section skeleton

**Client.** Executive summary, scope and basis, findings by workstream, financial
analysis, key risks, recommendations, appendices, methodology.

**Publication.** The argument, stated as a thesis. Section dividers are acts in
that argument. A topic tour fails the skill's own Mode B rule.

## Layout repertoire

**Client uses:** `One Column Text`, `Two Columns Text`, `Analysis_Horizontal`,
`Analysis_Vertical`, the `Key findings_*` family, `Summary Financials_6 blocks`
and `_5 blocks`, `Title Only_strapline`.

**Publication uses:** `Title only_Blank` almost throughout, with the four
compositions below. `1_Key findings_3 columns` for a genuine triptych of prose.

**Neither uses:** anything named `FOR REFERENCE_` or `DO NOT delete`. Those are
parts bins.

**Vary them.** A report where every slide is `One Column Text` wastes the
template.

## Compositions, publication variant

Named in `../design/references/visual-reference/00 — Visual Reference Index.md` and measured
across all 38 rendered pages. Every exhibit is **13.70 cm or 28.40 cm wide, and
nothing in between**; `qa.gate_exhibit_width` enforces it.

| Pattern | Use | Frame |
|---|---|---|
| **A** — two stacked exhibits, prose read right | The workhorse | Exhibits 13.70, read 13.70 at x 17.43, read runs the full height of both |
| **B** — chart above, table below, read right | When the second thing needed is values rather than a shape | Same frame as A |
| **C** — one full-width exhibit, read in columns beneath | A long category axis, a timeline, a twelve-sector dumbbell | Exhibit 28.40, two or three short read columns under it |
| **D** — full-bleed statement page | Cover and dividers | Template artwork, nothing added |

Two exhibits means two arguments that compound. One argument cut in half is a
different, worse page.

## Density

Expressed as the structural tests the skill already enforces, because a word
count would be a number I have not measured.

- **One argument per slide.** Two arguments is two slides.
- **The title states the finding.** A noun-phrase title is a wasted slide.
- **Content reaches past y 10.13 cm**, the master's own half-height line. Above
  it and the slide is half empty. Add the read, stack a second exhibit, move to a
  column, or merge two thin slides. Never stretch the exhibit.
- **No column more than about a third empty.** If it is, the composition is wrong.
- **Six bullets maximum** in one block, client variant. Every bullet is a full
  sentence.
- **9pt body.** If content does not fit, cut it or split the slide.

> A numeric words-per-slide cap can be added here. It needs measuring against the
> 38 reference pages first, and it is yours to set.

## Default mode

**Client** is usually Mode A: a document was supplied, the words are its own, and
`qa.content_fidelity(..., mode="verbatim")` must return zero.

**Publication** is usually Mode B: research first, into
`Work/<Engagement>/Research/`, with a verified data register before any slide is
drafted.

## Exhibits

- **Native charts only.** `exhibits.chart_exhibit()`, never a picture of a chart.
  A chart whose numbers are not in the data booklet is a build error.
- Exhibit title in KPMG Blue bold 10pt, stating what that exhibit shows.
- Basis line beneath it in grey: period, units, scope, population.
- Series labelled at the end of the line where there is room, in place of a
  legend.
- One focal colour, everything else neutral. Finish the sentence *"On this page,
  blue means ___"* or the colour comes out.
- Bars start at zero.
- Every share carries its whole.

## Before you call it done

The seven checks in `../design/references/design-principles.md` §7, then the QA pass in `../design/references/qa-checklist.md`.
Steps 4 and 5 are blocked on this machine; see [[environment]] and say so in
the delivery note.

## Related

- [[SKILL|the pipeline]]
- [[environment]]
- [[Proposal]]
- [[Talkbook]]
