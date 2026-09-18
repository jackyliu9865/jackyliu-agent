---
type: proposal-section
section: 2
slide: 2
---

# Summary of our proposal

**One page, slide 2 in every reference.** The buyer who reads nothing else
reads this. It is the proposal in miniature: one column per section of the
deck, each carrying the section's headline in two to four sentences.

## The page

| Element | Value |
|---|---|
| Title | `Summary of our proposal` — verbatim in every reference |
| Layout | `Title only_Blank`, hand-composed |
| Columns | One per section the user chose, in the chosen order. Five in most references; six where a deck carried an extra section |
| Column width | 4.60 cm for five, 4.00 cm for six, across the 28.40 cm content width |
| Column header | y 3.70. The name of each chosen section, in the deck's order. The references use *Background* / *Overview*, *Our approach*, *Credentials*, *KPMG team*, *Scope & fees* |
| Column body | y 5.30. Two to four sentences. Dark Blue, 9pt |
| "Read more" | A button at the foot of each column, y 14.50, 2.60 cm wide, linking to the section |

**The column order follows the deck order**, so a deck that puts Scope before
Credentials lists them that way here.

## What each column says

The four references converge on a formula per column. Use the shape; write the
sentences from the supplied content.

Only the columns for sections the user chose appear. Drop a row here and the
section it summarises goes with it.

| Column | Opens with | Then |
|---|---|---|
| Background / Overview | *"We understand that [Client] ("You") are…"* — the transaction or requirement in one sentence | What the work will support |
| Our approach | *"We have set out our approach to…"* | The two or three things the approach does |
| Credentials | *"We excel in…"* or *"Our credentials and experience…"* | Named sectors and geographies, no client names |
| KPMG team | *"We have compiled a team with…"* | Why the leads fit: sector, deal type, relationship |
| Scope of work | *"We have outlined a preliminary scope of work based on our understanding of your requirements, focusing on…"* | *"We would appreciate the opportunity to discuss…"* |
| Fee estimate / Commercials | *"Based on our experience of similar engagements of this size and complexity, we have provided an indicative fee estimate. We believe that our fee estimate is competitive."* | *"However, we can adjust the work required to meet your…"* |

The fee sentence is identical in three of four references. Treat it as
boilerplate.

One reference gives each column a two-word bold lead-in above the paragraph —
*Strategic entry*, *Our integrated approach*, *Local insight, regional trust*,
*Tailored approach*, *Value proposition*. It reads well and costs one line. Use
it where the deck has a distinct pitch per section; skip it where the plain
section name does the job.

## Build

Five text boxes on the grid, hand-placed. No placeholder layout on the 2025
master gives five equal columns with a header, a body and a button, so this
page is composed rather than filled.

```python
s = add(prs, "Title only_Blank")
fill(s, title="Summary of our proposal")
# five columns: header at y 3.70, body at y 5.30, button at y 14.50
```

Column x positions for five at 4.60 cm with a 1.35 cm gutter, starting at the
left margin: 2.73, 8.68, 14.63, 20.58, 26.53. Stay on those.

## Checks before moving on

- Column count equals the number of chosen sections, and the order matches the deck
- Every column reaches the "Read more" button without a gap. A two-line column
  beside a five-line one reads as unfinished
- No number appears here that does not appear in the section it summarises
- The fee column carries no figure. The number lives on the fee page

## Related

- [[Proposal]] — the skeleton
- [[fees]] — where the fee sentence comes from
- [[understanding]] — the next section
