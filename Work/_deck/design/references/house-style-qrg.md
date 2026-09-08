---
tags: [career, kpmg, powerpoint, house-style, reference, deliverable-standards]
status: active
---

# KPMG House Style — PowerPoint & Report QRG

Transcribed from the KPMG Diligence+ report template quick reference guide and
its associated review checklists. This is the standing reference for any KPMG
deliverable, decks included. The `kpmg-deck`
skill enforces the deck-relevant subset automatically; everything else is a
manual check.

**Source.** KPMG internal template guidance (Diligence+ report template QRG,
find-and-replace lists, chart and table checklist, general review checklist,
PowerPoint checklist, UK English and slide master guidance). Internal material:
stays in the vault, never published, never pasted into a third-party tool.

---

## 1. The rule that overrides the QRG on decks

**Bullets in decks do not take full stops.** House instruction, and the
`kpmg-deck` default.

Be aware this differs from the supplied QRG, which is written for the
**Diligence+ report template** and says the opposite twice: "All bullets and
sub-bullets are punctuated (including straplines, notes and sources)" and "Full
stops to be used at the end of a sentence". Both can be true because they govern
different deliverables. Decks follow the no-full-stop rule; long-form reports
built on the report template follow the QRG. If a deck is being converted into a
report, the punctuation has to change with it.

**Body paragraphs are not bullets, and they do take a full stop.** The
no-full-stop rule names *bullets*, meaning list items. A prose paragraph in a
read column, a commentary block or a Key findings column is a body paragraph
and is punctuated normally, terminal full stop included.

The distinction is the outline level, not the sentence count. On the 2025
master, levels 0 and 1 are unbulleted paragraphs and level 2 and deeper carry
the bullet glyph. `scan_text.py` reads the level, so a single-sentence body
paragraph is not mistaken for a bullet.

Still unpunctuated, because none of them is a body paragraph: slide titles,
straplines, dark-blue header bars, exhibit titles, exhibit basis lines and the
summary strips on the Key findings layouts.

Notes and sources still end with a full stop in both.

---

## 2. Golden rules

The QRG's own No.1 rule: **be consistent throughout the document.**

| Item | Rule |
|---|---|
| Numbers 1 to 9 | Written in words within text |
| Numbers 10 and above | Written in numbers within text |
| Capitalisation | Only the first letter of a heading is capitalised. Use capitals sparingly |
| Sentence case | The document is in sentence case throughout, not title case |
| Currency | Local currency signs for €, £, $ and ¥. Put the currency in the glossary and stay consistent |
| Million and thousand, body text | €0.1 million or €0.1m; €100 thousand or €100k. Pick one and hold it |
| Million and thousand, tables | €m or €'000. **Never** €Ms, €'000s or €'m |
| Currency spacing | No space between the currency sign and the figure: €1.0 million, not € 1.0 million |
| Currency codes | Space between the code and the figure: GBP 12.1m, USD 12.1m. Use RMB rather than CNY |
| Quotation marks | Only for actual quotes |
| Inverted commas | Used when first defining an acronym, for example capital expenditure ('capex') |
| Terminology | Consistent, per the glossary |
| Square brackets | Run a square bracket search before issue |
| Layout grid | On while drafting, off at final print |
| Reporting periods | Consistent, per the glossary |
| Percentages in tables | Italics. Percentages in body text are not italicised |
| Continuation pages | (Cont.) or (1/2). Be consistent |
| Decimal point | Consistent throughout. Agree €'000 or €m, and one or two decimals, with the team |
| n/a | Write n/a. Never N/A or n.a. in that form: n/a is not applicable, n.a. is not available |
| Slash | No space either side: before/after, not before / after |
| Appendix | Capital A whenever referring to an Appendix |

---

## 3. Find and replace list

Run these before issue.

| Find | Replace with | Why |
|---|---|---|
| "[space]." "[space]," "[space];" | (remove the space) | Common typo before punctuation |
| space hyphen space | space en dash space | Hyphens take no surrounding spaces; an en dash does |
| " (curly double) | ' | Unless an actual quote, in which case italicise the quoted words |
| % | percentage | In text: gross margin percentage, not gross margin % |
| & | and | Not a global change. Acceptable inside company and department names |
| / | / | No spaces either side. Check each instance; sometimes a space or line break is being used to split a paragraph |
| [..] [ ] [xx] [??] | [...] | Missing information is shown as [...]. Unreadable mark-ups become [____] |
| 1 to 10 | one to nine, then 10 | One to nine in full, 10 onward in numerals |
| 1st, 2nd | First, second, third | |
| c. / circa | approximately | Circa only for dates. Approx. acceptable in some circumstances |
| Double space | Single space | Except manual indents in tables. Over 600 hits usually means number formats are wrong |
| eg | e.g. | |
| etc | etc. | |
| ie | i.e. | |
| from / form | (check sense) | Frequent typo |
| N/A or n.a. | n/a | n/a not applicable, n.a. not available |
| vs or vs. | versus | Except legal cases, e.g. Kramer v Kramer |
| Continued | (cont.) | Every continuation page carries it |
| Jan, Feb, Mar | January, February, March | Full dates in text, e.g. 31 March 2023. If shortening to 31 Mar 2023, be consistent |
| Q1, Q2, H1, H2 | 1Q23, 2Q23, 1H23, 2H23 | |
| Can't, isn't | Cannot, is not | |
| FY23 | 2023 | Only use FY[xx] where the financial year does not follow the calendar year |

Also check on every pass: indentation of bullets, line spacing against the
template, and that every financial table, graph and quote carries a source and,
where needed, a note.

---

## 4. Typography and formatting

### Body and headings (report template)

| Element | Specification |
|---|---|
| Main heading | Arial 10pt bold, KPMG Blue. White when sitting on Cobalt Blue shading |
| Sub-heading | Arial 10pt bold italic, KPMG Blue |
| Sub-sub-heading | Arial 10pt italic, KPMG Blue |
| Body text | Arial 10pt, Black, left aligned, hanging from top, 0.2cm left margin, single spacing, 6pt paragraph spacing after |
| Body overflow | Reduce paragraph spacing to 2pt minimum. **Never drop the font below 9pt.** Add pages instead |
| Bullets | Unicode 2022, Black, normal weight |
| Sub-bullets | Unicode 002D, Black, first word lower case unless a proper noun |
| Key or legend for a diagram | Arial 6pt, KPMG Blue. Sits above notes and sources |
| Notes, e.g. (a), (b) | Arial 6pt, KPMG Blue, left aligned, above the source. Single spacing, 2pt before, full stop at end |
| Sources, e.g. (1), (2) | Arial 6pt, KPMG Blue, left aligned, below the notes. Multiple sources separated by semi-colon or numbered. Full stop at end |
| Shaded box text | Arial 8pt bold, KPMG Blue, sits behind the graph |
| Punctuation spacing | One space after a colon, semi-colon, comma or full stop |

### Objects

| Object | Specification |
|---|---|
| Call-out box | 1pt Cobalt Blue line (RGB 30, 73, 226), white fill, single spacing, 2pt before. Arial 7pt Black, middle-centred, 0.15pt internal margins. Size 1.5cm x 4.5cm or 5.5cm. **Make it higher, not wider** |
| Arrows | Smallest arrow head, 1pt line |
| Balls | 0.4 x 0.4, Cobalt Blue fill, no outline, Arial 8pt white, middle-centred |
| Lasso box | 1pt pink square-dot line |
| Photos | 4x3 ratio, correct people-photography blue, sized to match other photos, greyscale where appropriate |

---

## 5. Charts

| Item | Rule |
|---|---|
| Title | Left aligned, no internal margin, Arial 10pt bold, KPMG Blue |
| Graph text | Arial 8pt, Black |
| Data labels | Arial 6pt |
| Legend | Arial 7pt, Black, at the bottom. Show only where there is more than one data series |
| Axes | All axes correctly formatted and labelled |
| Axis labels | Numbers start with a zero, **never a hyphen**. The reverse holds in tables, where a zero is shown as a hyphen |
| Chart size | Set exact dimensions in Shape Format or the Layout tab, never by dragging |
| Quality | Redraw weak diagrams and poor quality graphs. Keep a copy of the original |

---

## 6. Tables

| Item | Rule |
|---|---|
| Alignment | Numbers right aligned, text left aligned or sometimes centred. Column headings bottom aligned. Normal rows centre aligned where wrapping occurs |
| Bold totals | Total rows and total columns bold. **Sub-totals stay unbold** |
| Percentages | Italicised, rows and columns, unless the whole table is percentages. **The percentage column heading is not italicised** |
| Line weights | 0.5 or 1.5 |
| Number formats | £m to one decimal place; £000 to no decimal places; negatives in brackets; percentages to one decimal place in italics. Adjust for materiality |
| Zero | A zero in a table is shown as a hyphen |
| Positives and negatives | In the same table: assets and revenue positive; liabilities and expenses negative |
| Footnotes | Superscript, no space before, e.g. EBITDA⁽ᵃ⁾. In front of a number, written as (a) 123 |
| Margins | Narrow, 0.13cm |
| Heading height | 0.27 inches (0.69cm), which suits 8pt and 9pt type |
| Sizes | Exact dimensions, set in the Layout tab |
| Consistency | Similar tables line up: same column widths, same positions |
| Continuation | Key, notes and source duplicated on continuing slides |

---

## 7. Slide master, guides and theme

### Guides (suggested)

Width +/- 14.20 · Master title +8.30 / +6.80 · Master strapline +6.80 / +5.80 ·
Master text +5.80 / -7.20 · Centre vertical gutter 0.0 / +0.50 / -0.50 · Centre
horizontal content area +0.50 / +0.40 / +0.60 · Notes section +6.80 / +7.80 ·
Section headers and super titles case by case.

### Master styles (suggested)

Master title 1.5cm H x 28.4cm W · Master strapline 1.0cm H x 28.4cm W on the
individual layout slide · Master text 12.6cm H x 28.4cm W · Source and notes
footer 1.0cm H x 14.2cm W, bottom aligned.

### Theme colours

Ten theme colours form the basis of the presentation. PowerPoint generates
"accents" from them automatically. **Accents are not KPMG colours and must not be
treated as shades of them.** The order of colours in the theme determines what
appears on each slide, so a different theme order silently repaints the deck, for
example KPMG Blue becoming purple. It also changes the GSG Powertools side-bar.
Custom colours can be added by editing the `.thmx` XML, up to 50.

### Pitfalls

Incorrect or non-use of the slide master · importing multiple slide masters,
which also inflates file size · not keeping the master clean of redundant themes
· not using exact dimensions.

---

## 8. UK English

Set it properly or it reverts. Select any text or object on a slide, then
Review → Language → Set Proofing Language → select Document and English (United
Kingdom) → OK. Every other method eventually reverts to US English or applies to
some text only. UpSlide has the same function but is less reliable.

Spell check is part of finalisation, not optional. Set the language first, then
search (Ctrl+F) for words containing "z" to catch specialize, criticize and
similar. Copilot is enabled across KPMG China and can be prompted to check
grammar, typos and language, with editing permissions if wanted.

---

## 9. General review checklist

Run when time permits, and **always** before print or a final client version.

- **Acronyms and abbreviations.** All in the glossary. No full stops, no
  apostrophes: KPIs is correct. Possessive apostrophes are the exception
- **Check stamps.** Remove DRAFT from the final print
- **Contents.** Filled in and matching the page and section headings
- **Copyright.** Updated in the footer and on the back page
- **Dates.** Body text 1 January 2023; tables and charts 1 Jan 23. FY23 not
  FY2023. Distinguish FY[xx] from "year ending [xxx]"
- **Glossary.** Alphabetical, sentence case. Add abbreviations found in the text
- **Greyscale.** Flick through in greyscale to catch stray boxes and print issues
- **Key issues boxes.** Removed from appendices
- **Punctuation.** Per section 1: no full stops on deck bullets; the report
  template punctuates bullets, straplines, notes and sources
- **Style check.** PowerPoint: every slide linked to the correct master, incorrect
  masters removed. Word: corrupt styles replaced from the ribbon
- **Telephone numbers.** International format, e.g. +852 xxxx xxxx
- **Point in time versus period of time.** Point in time is "as at [date]". Period
  is "during the period ending [date]". Decide whether the figure is an average
  over a period, a value at a point, or a total over a period
- **Percentage increases.** Movements in percentages are described in percentage
  points, abbreviated pp if defined in the glossary. A move from 30% to 35% is an
  increase of 5 pp, **not 5%**

### Expected as standard

Language set to English UK · document spell-checked and the find-and-replace
searches run · every consultant mark-up, amendment and request checked and 100%
accurate · you are responsible for your own job, including work split with other
operators, and proofing anything you hand back.

### The NO list

No typos · no clip art, except rich images or icons · no pixelated images or
photographs · no layout grids in the final · no messy graphics · no company
logos, the sole exception being client logos with the client's approval confirmed
by the lead partner · no underlining, unless temporarily tracking changes.

### PowerPoint checklist

- All graphics and text positioned within the guides, with limited exceptions
- All diagrams and graphs neat, high quality, consistently sized, in brand colours
- Correct line weights in tables
- Correct font in tables, including colour
- Correct font in charts
- Graph sizes checked
- Notes and Source completed for every table. If the source is a dataroom
  document, give the file reference
- Notes and sources correct and the correct distance from the bottom of the table
- Title slide subheadings correctly formatted where used
- Arrow heads and chevrons correctly sized and consistent
- Appendix, not appendix
- **Never reference page or slide numbers**, because they move. Reference the
  section or sub-section instead

---

## Related

- [[Career/Handover]]
- [[UNIVERSAL — Agent Rules & Standards]]
- [[NME Revenue Pools — Overview]]
- Enforced in part by `Skills/Execute/kpmg-deck/scripts/scan_text.py`
- Applied by the `kpmg-deck` and `pov-analysis` skills
