---
type: deck-profile
deck_type: proposal
kind: proposal
status: drafted
---

# Deck profile — Proposal

Read [[SKILL|the pipeline]] first. This file is the skeleton and the router;
each section has its own file under `sections/`.

A proposal sells an engagement. It is read by a buyer comparing three firms,
skimmed first and read closely in two or three places: the summary, the scope,
and the fee. Everything else earns its place by being short.

**Evidence base.** Four KPMG Hong Kong deal and strategy proposals, read page
by page. Every rule below is something all four do, or a
variation the four show between them. Client names and personal names do not
appear in this folder.

## Settled

| | |
|---|---|
| `kind` | `proposal` — `new_deck(kind="proposal")` turns on the deck-type gates |
| Closer | `Back Cover_Proposal` |
| Mode | A. The pursuit team supplies the content; this profile lays it out |

## Before the outline: ask which sections to include

**Every section is optional. Always ask the user which to include before
writing the outline.** Put the list below to them and take their selection. Do
not assume a section is wanted because every reference carried it.

The summary page then carries one column per chosen section, in the chosen
order, and the deck-type gates check only the cover and the closer.

## Skeleton

Ten sections, in the majority order the references use. **Length follows from
the sections chosen and the depth the content needs.** Each section file states
the page shape that section takes.

| # | Section | File |
|---|---|---|
| 1 | Cover | — `Cover page` |
| 2 | Summary of our proposal | [[summary]] |
| 3 | Understanding | [[understanding]] |
| 4 | Our approach | [[approach]] |
| 5 | Credentials | [[credentials]] |
| 6 | Your KPMG team | [[team]] |
| 7 | Proposed scope of work | [[scope]] |
| 8 | Timetable | [[timetable]] |
| 9 | Fee estimate | [[fees]] |
| 10 | Appendices and back cover | [[closing]] |

Where a section is included, it opens on a `Section divider`, except the cover,
the summary and the back cover.

**Where the order varies.** Three of four put Credentials and Team before Scope.
One folds Team into the Understanding section and pairs it with "Why KPMG". One
inserts a twelve-page outside-in market view between Understanding and Scope.
The summary page's column order follows whichever order the deck uses.

## What the references are built on

**Roughly seven pages in ten are hand-composed on a blank title-only layout.**
Placeholder layouts carry the CVs and little else. A proposal is a set of page
recipes rather than a set of filled placeholders, and the section files are
written as recipes.

The references sit on the pre-2025 master. This profile maps them onto the 2025
master the pipeline builds on:

| Reference layout | Build on |
|---|---|
| `Title Only` | `Title only_Blank`, or `Title Only_strapline` where the page carries an assertion |
| `Two Column Text` | `Two Columns Text` |
| `One Column Text` | `One Column Text` |
| `Divider with image` | `Section divider` |
| `Subsection divider` | `Subsection divider` |
| `TITLE SLIDE Left Horizontal Window` | `Cover page` |
| `Back Cover dark Gradient` | `Back Cover_Proposal` |

## Density

Dense, in the report style: 9pt body, full sentences, tables carrying the scope.
The exception is the summary page, whose five columns each carry two to four
sentences and nothing more.

Numbered continuation titles are the norm for anything longer than a page:
`Financial due diligence (3/6)`, `Fee estimate (2/2)`.

## Boilerplate

Three things repeat across all four with near-identical wording and belong in a
house file rather than being retyped: the fee opening sentence, the fee
assumptions page, and the back-cover disclaimer. [[fees]] and [[closing]] carry
the wording.

## Related

- [[SKILL|the pipeline]] · [[slide-template]] · [[environment]]
- [[Report]] · [[Talkbook]]
