---
name: kpmg-deck
description: "Build PowerPoint decks on the KPMG 2025 brand-refresh slide master — cover, section dividers, key findings, analysis, summary financials, back covers — with the locked palette, 44pt/9pt/8pt/6pt type scale and 2.72cm grid. Use this skill for ANY request to make a deck, slides, a presentation, a pitch, a report-out, or a .pptx, whenever the work is for KPMG or the person has previously used this template — even if they don't name the template, say \"branded\", or mention KPMG in that particular message. Also use it when editing, extending or brand-checking an existing deck built on this master."
---

# KPMG deck builder

> **This file is a map. The process lives elsewhere.**
> **Any deck task starts at `Work/_deck/START-HERE.md`**, which carries the
> six-step pipeline from supplied content to a finished deck. Do not follow a
> workflow from this file; it no longer has one.

Generate decks by filling the real template, never by redrawing it. The bundled
`assets/template.pptx` carries the KPMG Bold/Arial theme, the logo, the footer,
the classification line, the page numbers and 26 authoring layouts on the main
master (32 in the file, 6 of them on a second storage master). Add a slide on a
layout and every font, size and colour is inherited correctly with no styling
code at all.

Redrawing this look from scratch does not work: KPMG Bold is not applied, the
logo and footer are gone, and the result is approximately right and wrong in
every detail a reviewer checks.

For an MBB-quality deck that is **not** on this master (case, recruiting, board,
unnamed strategy work), use **consulting-deck**. Do not use this package for a
non-KPMG deliverable.

## Where everything is

**Process and routing** — outside this package, in the vault:

| File | Answers |
|---|---|
| `Work/_deck/START-HERE.md` | The six-step pipeline. **Start here** |
| `Work/_deck/Report/`, `Proposal/`, `Talkbook/` | What each deck type looks like |
| `Work/_deck/design/slide-template.md` | Which master each deck type builds on |
| `Work/_deck/environment.md` | What works on this Mac, what is blocked, and the deps |

**Craft and API** — in `references/`, roughly in reading order:

| File | Read it |
|---|---|
| `visual-reference/` | **First.** 38 rendered pages from three finished decks: the target |
| `design-principles.md` | **Second.** Artboard, grid, the four page compositions, the seven per-slide checks |
| `content-rules.md` | Before drafting any slide text: what the words may be, and how to prove it |
| `exhibits.md` | Before any slide with a number: exhibit grammar, which chart answers which question, full signatures |
| `layouts.md` | Choosing a layout, placeholder idx numbers, box geometry, traps |
| `brand.md` | Palette, type scale, the cm grid, table rules |
| `build-api.md` | Writing the build script: `deckkit`, `exhibits`, the modules, the rules that matter most |
| `house-style-qrg.md` | Before any client-facing deck |
| `qa-checklist.md` | The QA pass, what each gate fails on, and what stays manual |

**Assets:**

- `assets/template.pptx` — the cleaned master, zero slides. `new_deck()` opens it
- `assets/specimen-deck.pptx` — the 28-slide sample. For looking at and for
  lifting pre-formatted tables. **Never a starting point**; see [[slide-template]]
- `assets/fonts/` — the nine brand faces
- `scripts/source_text.py` — step 1 of the pipeline, for `.docx`, `.pdf`, `.pptx`

`README.txt` covers installing the package on another machine and proving it
works.

## Local fork

This package is edited in place and version-controlled with the vault. The
unmodified import is tagged `kpmg-deck-pristine`. To take an upstream update:
branch from that tag, drop the new package in, commit, and merge to `main`, so
git resolves everything upstream changed that was not touched here.

## Related

- [[content-rules]] · [[build-api]] · [[qa-checklist]]
- [[00 — Visual Reference Index]]
- [[slide-template]]
