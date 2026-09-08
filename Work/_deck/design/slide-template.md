---
type: house-file
purpose: routes a deck type to its slide master
applies_to: Report, Proposal, Talkbook
last_updated: 2026-09-08
---

# Layout — which master for which deck

Read [[START-HERE]] first. This file answers one question: **which slide master
does this deck type build on.**

## Routing

| Deck type | Master | Build call | Closer |
|---|---|---|---|
| **Report** — client deliverable | KPMG 2025 brand-refresh master, the one `assets/specimen-deck.pptx` demonstrates | `new_deck()` | `Back Cover_Report` |
| **Report** — publication | Same master | `new_deck()` | `Back Cover_Publications` |
| **Proposal** | Same master | `new_deck()` | `Back Cover_Proposal` |
| **Talkbook** | **Placeholder.** A template is to be supplied | — | Undecided |

## The trap: never build from the specimen

`assets/specimen-deck.pptx` and `assets/template.pptx` carry the **same master**.
Verified 31 August 2026 by comparing both layout sets: 32 layouts each, identical
names, no difference either way. The specimen is that master with 28 demonstration
slides on it; the template is that master cleaned to zero slides.

**Open the template, never the specimen.** `new_deck()` already does this.

The specimen's 28 slides cross-link. Deleting them leaves orphan relationships
that collide with new slides, and PowerPoint then reports the file as corrupt.
`SKILL.md` states this directly. A build that starts from the specimen produces a
file the client cannot open.

| Use the specimen for | Never |
|---|---|
| Looking at what a layout does before choosing it | As the starting file |
| Lifting a pre-formatted table out of | Deleting its slides to make room for yours |
| Checking density and restraint against your own draft | |

## Layout entry points per deck type

The master is shared, so the deck types differ in **which layouts they open with
and close on**, rather than in the master itself.

| | Report (client) | Report (publication) | Proposal |
|---|---|---|---|
| Cover | `Cover page` | `Cover page` | `Cover page` |
| Cover letter | `Transmittal Letter` | — | `Transmittal Letter` |
| Contents | `Title only_Blank` | `Title only_Blank` | `Title only_Blank` |
| Section break | `Section divider`, then `Subsection divider` | Same | Same |
| Body | Placeholder layouts, bullets | `Title only_Blank` with `exhibits.*`, prose | `Key findings_*` blocks, `Two Columns Text` |
| Closer | `Back Cover_Report` | `Back Cover_Publications` | `Back Cover_Proposal` |

Which body layouts each type draws on, and why the two Report variants differ, is
in [[Report]] and [[Proposal]].

**Never author on** a layout named `FOR REFERENCE_` or containing
`DO NOT delete`. Those are parts bins for the UpSlide add-in. Twenty-six of the
32 are authoring layouts; the placeholder idx map for each is in
`references/layouts.md`.

## Talkbook — placeholder

**Blocked until a template is supplied.** Drop it in `Talkbook/` and this table
gets filled in.

The current master will not serve. It fixes 9pt body across 12.60 cm of content
height for documents read alone, and the package forbids overriding the type
scale. It also carries no talkbook closer: the three back covers are Report,
Proposal and Publications.

Until the template arrives, a live-presented deck built on this master is a
report being presented. Say that rather than calling it a talkbook. See
[[Talkbook]].

## Related

- [[START-HERE]]
- [[Report]]
- [[Proposal]]
- [[Talkbook]]
