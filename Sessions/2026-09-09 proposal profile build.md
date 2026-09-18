---
date: 2026-09-09
agent: claude-code
status: done
started: 2026-09-09
ended: 2026-09-09
engagement: _deck
---

# Proposal profile build

## Goal

Write `Work/_deck/Proposal/Proposal.md` as a lean lead file routing to one md
per proposal section, grounded in four reference proposals the user supplied.

## Constraints carried in

- The four reference decks are pursuit material. Client names and personal
  names stay out of every file written in `_deck/`. `content-rules.md` forbids
  a personal name anywhere in the package.
- Thin-slice gate: analyse all four, propose the structure, write the lead file
  and one section as the slice, wait for go on the rest.

## Plan

1. Inventory all four decks: layouts, titles, slide counts -> verify: table
2. Extract text and read section structure -> verify: common skeleton found
3. Identify what varies vs what is fixed across the four
4. Write Proposal.md + one section file -> verify: wikilinks resolve
5. Wait for go

## Findings from the four references

All four are on the **pre-2025 master** (`Title Only`, `5_Divider with image`,
`Back Cover dark Gradient`). Not the master the pipeline builds on. Profile maps
old layouts to new.

**Roughly seven pages in ten are hand-composed on `Title Only`.** Placeholder
layouts carry the CVs and little else. The profile is written as page recipes.

Skeleton, ten sections. Fixed: summary is always slide 2, one team page titled
"Your committed core team", fee estimate is always two pages and always last
before appendices, CVs on Two Column Text in the appendix, back cover with
disclaimer. Order of Credentials / Team / Scope varies across the four.

Fee page anatomy: left paragraph, right fee table (Service | Fee basis | Low |
High) plus a rate card (Grade | Fee USD), caveat line, footnote. Page 2 is fee
assumptions in two columns. The opening sentence is identical in three of four.

## Written

- `Proposal/Proposal.md` — lean lead, skeleton, routing to nine section files
- `Proposal/sections/summary.md` — the slice

All eight remaining sections written on go: understanding, approach,
credentials, team, scope, timetable, fees, closing. Ten files in `Proposal/`,
every wikilink resolves.

One leak caught by the names sweep: `understanding.md` used a real client as the
naming-convention example. Placeholdered. Re-sweep clean.

Boilerplate captured verbatim from the references, where three of four agree:
the fee opening paragraph, the fee caveat, the fee footnote, the five fee
assumptions, the timetable caveat, and the three back-cover disclaimer
paragraphs. The two references disagree on the entity wording; the file names
the current form.

Rates deliberately excluded from `fees.md`. The two references differ by roughly
a fifth on every grade; a rate carried forward is a wrong rate. §6.

## Environment regression found and fixed

Homebrew's Python 3.14.7 shadowed stock 3.9.6; `python3 build.py` broke.
Installed the five packages into the brew interpreter's user site with the PEP
668 override. Selftest passes 0/27 on 3.14.7. Recorded in `environment.md`.

## Outcome

Done. `Proposal/Proposal.md` plus nine section files under `sections/`,
grounded in four reference proposals read page by page. `SKILL.md` routing
updated from *not written* to routing. Ready for a first proposal build.
