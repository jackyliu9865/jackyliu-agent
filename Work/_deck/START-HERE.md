---
type: entry-point
applies_to: every PowerPoint task
last_updated: 2026-08-30
---

# Decks — start here

**Any PowerPoint task starts at this file.** It routes you. It contains no brand
values and no build instructions, because those live in `design/` and restating
them here would create a second source that drifts.

## Precedence

**Where this file and `design/` disagree, this file wins.** `design/` is an
imported package written for a different house; its rules are the default, and
the overrides recorded here are standing. Recorded overrides:

| `design/` says | This file says |
|---|---|
| `design-principles.md` §6: never cite KPMG's own thought leadership in a client-facing deliverable, "not negotiable" | **Cite it.** A KPMG published report is a legitimate source for its own data. See *Sources and citation* below |
| `visual-reference/`: the 38 pages are private work product, restricted | Use them freely for every deck. The restriction on publishing them outward stands under §7 of `AGENTS.md`, which already covers it |

Never patch `design/` to close a disagreement. Record the override here instead,
because the package can be replaced wholesale by a newer version and a local edit
would be lost.

**House files kept inside `design/`.** These are yours and a re-import deletes
them. Restore from the vault afterwards.

| File | Holds |
|---|---|
| `design/layout.md` | Which slide master each deck type builds on |

## How this folder is split

**Who owns it** decides where a fact belongs.

| | `design/` | `Report/` `Proposal/` `Talkbook/` |
|---|---|---|
| Scope | Design and build, every deck type | One deck type |
| Owner | Imported package. Replaceable wholesale | Yours |
| Edit it? | **Never.** Edits are lost on the next import | Yes |
| Holds | Brand, type, grid, layouts, composition rules, exhibit grammar, house style, QA gates, the build API, the master, the nine fonts, 38 rendered reference pages | Section skeleton, layout repertoire, density, default mode, and any master or sample for that one type |
| Answers | *How does a KPMG slide work?* | *What does a Jacky report look like?* |

A value that exists in `design/` is **cited**, never copied. House decisions that
apply to every deck type go in **this file**, under *Precedence* or the sections
below.

**One folder per deck type**, each with a lead file of the same name as its entry
point. Anything specific to that type lives in its folder: its own master, sample
decks, worked examples, boilerplate.

## Reading order for a deck task

Read in this order. Stop when you have what the task needs.

| # | Read | When |
|---|---|---|
| 1 | `AGENTS.md` (vault root) | Always. Loaded automatically |
| 2 | **This file** | Always |
| 3 | [[slide-template]] | Always, before opening any file. Which master this deck type builds on |
| 4 | `<Type>/<Type>.md` — the lead file in `Report/`, `Proposal/` or `Talkbook/` | Always, once the type is chosen. Read the whole folder if it holds more |
| 5 | `design/references/visual-reference/` | Always, before laying out a data slide. **Look at the pages**, do not only read the index |
| 6 | `design/references/design-principles.md` | Always. How to compose a slide, and the seven checks |
| 7 | `design/references/exhibits.md` | Before any slide carrying a number |
| 8 | `design/references/layouts.md` | When choosing a layout or hand-placing on one |
| 9 | `design/references/brand.md` | Before writing any colour or size literal |
| 10 | `design/references/house-style-qrg.md` | Before any client-facing wording |
| 11 | `design/SKILL.md` | For the build API and the five-step QA pass |
| 12 | `environment.md` | Before claiming any QA step passed |

## Two things to declare before building

**1. The mode.** Rule 0 of `design/SKILL.md`, and it changes what the job is.

| | Mode A | Mode B |
|---|---|---|
| Trigger | A document was supplied | A topic or a brief |
| The job | Layout. The thinking is done | Research first, then layout |
| Words | The document's, word for word | Yours, every claim sourced |
| Gate | `qa.content_fidelity(..., mode="verbatim")` returns zero | Verified data register, `databooklet.check_booklet()` clean |

**2. The deck type.** Then go to that folder and read its lead file.

| Deck | Folder | Lead file | Back cover | State |
|---|---|---|---|---|
| Client deliverable, read without a presenter | `Report/` | [[Report]] | `Back Cover_Report` | Drafted |
| Published thought leadership | `Report/` | [[Report]], publication variant | `Back Cover_Publications` | Drafted |
| Sells an engagement | `Proposal/` | [[Proposal]] | `Back Cover_Proposal` | **Not written** |
| Presented live | `Talkbook/` | [[Talkbook]] | Undecided | **Blocked**, awaiting a layout |

Say both out loud before the first slide. Where the lead file says *not written*,
stop and ask rather than borrowing another type in silence.

## The two gates

From §5 of `AGENTS.md`. Both apply to every deck.

1. **Outline gate.** Storyline and a numbered slide list, one line stating the
   message of each slide. Stop. Wait for an explicit go.
2. **Slice gate.** One representative body slide, built and rendered. Never the
   cover, which hides layout problems. Stop. Wait for an explicit go.

No layout is invented after the slice gate. A slide that will not fit an approved
layout comes back to the user.

## Where output goes

| Item | Path |
|---|---|
| The deck | `Work/<Engagement>/` |
| Data booklet (`.xlsx`) | Beside the deck. A deck ships as two files |
| Figure traces, renders, extraction records | `Work/<Engagement>/evidence/` |
| Mode B research | `Work/<Engagement>/Research/` |
| Session note | `Sessions/YYYY-MM-DD <slug>.md`, opened at the start |

Use the engagement code name in the folder and the file name where one exists.
`save()` takes a path relative to the project folder, never a machine-absolute
one.

## Sources and citation

§7 of `AGENTS.md` governs confidentiality. This section governs what may be used
and what may be named.

**Use everything in `design/` freely.** The 38 rendered reference pages, the
specimen deck, the master and the nine fonts exist to make the output better, and
the agent draws on all of them without restriction and without asking. Look at
the reference pages before every data slide.

| Source | Use for analysis | Name it in the deck |
|---|---|---|
| KPMG published reports and thought leadership | Yes | **Yes.** Cite it like any other publication |
| Competitor consultancy output | **Yes**, for background and for craft | No |
| Primary, government, agency, regulator, filings | Yes | Yes. Preferred |
| Vendor blogs summarising a primary source | Read, then go to the primary | Cite the primary instead |

One craft point on the first row. A KPMG publication is a sound source for its
own data, and it is weak as independent corroboration of a KPMG claim. Where a
government or regulator series says the same thing, cite that as well.

## Where the package is

`Work/_deck/design/` is the canonical copy of the `kpmg-deck` package.
`~/.claude/skills/kpmg-deck` is a symlink to it, so Claude Code finds it and
there is one copy to maintain.

## Related

- [[slide-template]]
- [[Report]]
- [[Proposal]]
- [[Talkbook]]
- [[environment]]
