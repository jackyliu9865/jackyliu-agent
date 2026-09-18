---
type: proposal-section
section: 6
---

# Your KPMG team

**One page in the body, titled "Your committed core team", in all four
references.** Full CVs go in the appendices, one page per person, and never in
the body. The body page sells the team in a glance; the appendix proves it.

Opens on a `Section divider` titled *Your KPMG team*.

## The body page

Hand-built on `Title only_Blank` or `One Column Text`. Five or six people in a
row.

| Element | Geometry |
|---|---|
| Optional group headers | y 2.70 — *Core execution team* at 19.50 cm, *Relationship leads* at 5.60 cm, where the team splits |
| Name | y 4.50 to 5.20, 3.60 to 4.30 cm per column |
| Photo | y 4.80 to 5.50, 2.10 cm wide |
| Title and practice | y 8.10 to 8.70 — *Partner, Tax due diligence and structuring* |
| Role label | y 8.40 to 9.20, 1.40 cm, reading *Role* |
| Bio | y 9.90 to 10.60, 3.50 to 4.20 cm wide, two to four sentences |
| Selected credentials strip | y 12.80 to 13.20 — a one-line list of engagements the team has shared |

The bio formula: *"[First name] has over N years of [deal] experience [in
geographies]. [He/She] has advised on… [sector, deal type, count]."* Years,
geographies and a count carry the weight. The third sentence names the
relationship or the prior knowledge of the target where one exists.

## The CV page, in the appendices

`Two Columns Text`. Title **"[Name] | [Role]"** — *Engagement lead*, *Tax due
diligence lead*, *Insurance sector SME*.

Geometry is given as **x, y from the top-left corner, then width × height**, in
centimetres. See [[build-api]].

| Element | x | y | w | h |
|---|---|---|---|---|
| Photo | 2.73 | 3.73 | 2.70 | 3.60 |
| Contact block | 2.73 | 7.56 | 5.02 | content |
| *Background* | 8.38 | 3.73 | 22.73 | to the content floor |


One CV per person on the body page. Where the appendix is long, a `Subsection divider` titled
*Appendix A: Team's CV* opens it.

### Contact block

Measured identically on both references. The whole block is one text box with
**all four text-frame margins set to 0** and autosize off; the spacing comes from
the paragraphs, never from the frame. Arial throughout, set explicitly.

| #   | Content                                                                          | Level | Size   | Weight   | Colour   | Spacing       |
| --- | -------------------------------------------------------------------------------- | ----- | ------ | -------- | -------- | ------------- |
| 1   | Name                                                                             | 0     | 10.5pt | **bold** | `0C233C` | 2pt after     |
| 2   | Grade — *Partner*, *Director*                                                    | 1     | 8pt    | **bold** | `0C233C` | 0pt after     |
| 3   | Practice — *Deal Advisory*. One line for most people; see below                  | 1     | 8pt    | regular  | inherit  | 0pt after     |
| —   | *blank paragraph*                                                                | 1     | —      | —        | —        | 0pt after     |
| 4   | Legal entity — *KPMG Advisory (Hong Kong) Limited*                               | 1     | 7pt    | regular  | inherit  | 0pt after     |
| 5   | Address, two or three lines                                                      | 1     | 7pt    | regular  | inherit  | 0pt after     |
| —   | *blank paragraph*                                                                | 1     | —      | —        | —        | 0pt after     |
| 6   | `Mobile: +852 ...`                                                               | 1     | 7pt    | regular  | inherit  | 0pt after     |
| 7   | `Email: first.last@kpmg.com`                                                     | 1     | 7pt    | regular  | inherit  | 0pt after     |
| —   | *blank paragraph*                                                                | 0     | —      | —        | —        | inherited     |
| 8   | **Education, Licenses and Certifications**                                       | 0     | 8pt    | regular  | `0C233C` | inherited     |
| 9   | Each qualification, one per line                                                 | 1     | 7pt    | regular  | inherit  | **line 0.85** |

**Row 3 is one line for most of the team**: the practice alone — *Deal
Advisory*, *Tax*, *Technology Consulting*.

**A lead partner can carry further title lines, chosen for what they prove about
this pursuit.** A sector lead role where the target sits in that sector, a
geography lead where the deal spans it. They are selected for relevance rather
than listed in full, so a partner with five titles shows the one or two that
answer the buyer's question. The reference gives the engagement lead *Head of
Value Creation, China* and *Head of Deal Strategy, Hong Kong*; everyone else on
that deck carries their practice and stops.

**Three things carry the structure.** Blank paragraphs separate the four groups,
rather than spacing values. The two headings — the name, and *Education,
Licenses and Certifications* — sit at **level 0**; everything else is level 1.
Only the last group tightens to 0.85 line spacing, because qualifications run
long and wrap.

Labels are written `Mobile:` and `Email:` with a colon and a space. A phone
number ships as the person supplied it and is never reformatted.

### Background and relevant experience

The right-hand column: two headed groups in one text box. Margins 0, autosize
off. **9pt throughout**, Arial inherited from the theme, **3pt space before every
paragraph and 0pt after**.

| # | Content | Level | Size | Colour |
|---|---|---|---|---|
| 1 | **Background** — the heading, verbatim | 0 | 9pt | `0C233C` |
| 2 | Three to five paragraphs, one idea each | 1 | 9pt | inherit |
| — | *blank paragraph* | 0 | — | — |
| 3 | **Professional and industry experience** — the heading, verbatim | 0 | 9pt | `0C233C` |
| 4 | Lead-in: *"Notable [sector] deals led by [first name] include:"* | 1 | 9pt | `000000` |
| 5 | One line per engagement | 1 | 9pt | `000000` |

**What the Background paragraphs say**, in the order the references use:

1. Seniority, practice and years — *"[First name] is a senior Partner in KPMG's
   Deal Advisory and Strategy practice with over 21 years of experience across
   [regions]."*
2. Where they are based and what they lead
3. How they work: the approach they are known for
4. Anything beyond client work — thought leadership, a sector lead role

**What each experience line says.** A transaction, a colon, then the part they
played: *"Acquisition of a leading [sector] chain by [acquirer type]: Buy-side
due diligence covering [scope]."* The client is a descriptor unless the deal is
public and named in the supplied content.

Order the lines by relevance to the pursuit, never by date. A reader scanning
five lines should find the closest match first.

> **Where the experience lines come from — NOT YET BUILT.**
>
> These lines are selected from an **experience base**: a per-person record of
> the engagements each individual has worked on. **That database does not exist
> yet and has to be created.** Until it does, this section has no source.
>
> **Selection, once it exists.** Filter each person's record on two axes and
> take the intersection:
>
> | Axis | Example values |
> |---|---|
> | Service type | FDD, CDD, VDD, tax DD, tax structuring, technology DD, integration, valuation, strategy |
> | Sector | The target's sector, then its adjacent sectors |
>
> A line earns its place by matching the service the proposal sells **and** the
> sector the target sits in. Where nobody on the team has both, show the closest
> match on service and say which sector it was in.
>
> **Until the base is built, the lines come from the pursuit team or the
> supplied content, and from nowhere else.** Never write an engagement from
> general knowledge of what a person at that grade probably did, and never
> reshape a real engagement to fit the pursuit. A fabricated credential in a
> proposal is the worst failure this whole profile can produce: §6 of
> `AGENTS.md` and the research ban in `design/references/content-rules.md` both
> apply. Where the lines are missing, **ask**.

**Length is set by the box rather than by a count.** The column runs from y 3.73
to the content floor. Where the list overruns, cut the least relevant line
rather than shrinking the type.

## Conventions

- Roles on the body page match the workstreams in [[scope]] one to one. A
  workstream with no named lead is a gap the buyer will find
- The engagement lead is first, the quality-review partner second where one is
  shown, then workstream leads, then relationship leads on the right
- Titles follow the house form: *Partner*, *Director*, *Associate Director*,
  *Manager*, *Assistant Manager*, *Analyst*
- Personal names appear in the deck and nowhere in this package. Supplied
  content ships as written; see `design/references/content-rules.md`

## Checks

- Every person on the body page has a CV in the appendix
- Every workstream in the scope has a lead on this page
- Photos are present or the *Image of the person* placeholder is removed; a
  labelled placeholder on a shipped page is the most visible defect in the
  references

## Related

- [[Proposal]] · [[credentials]] · [[scope]] · [[closing]]
