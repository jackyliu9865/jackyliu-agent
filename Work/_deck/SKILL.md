---
name: kpmg-deck
description: "Build PowerPoint decks on the KPMG 2025 brand-refresh slide master — cover, section dividers, key findings, analysis, summary financials, back covers — with the locked palette, 44pt/9pt/8pt/6pt type scale and 2.72cm grid. Use this skill for ANY request to make a deck, slides, a presentation, a pitch, a report-out, or a .pptx, whenever the work is for KPMG or the person has previously used this template — even if they don't name the template, say \"branded\", or mention KPMG in that particular message. Also use it when editing, extending or brand-checking an existing deck built on this master."
---

# Decks — start here

**Any PowerPoint task starts here, and this is the only entry point.** The job is
one thing: turn supplied content into a coherent deck. Follow the six steps in
order. Do not skip ahead.

For an MBB-quality deck that is **not** on the KPMG master (case, recruiting,
board, unnamed strategy work), use **consulting-deck** instead.

---

## The pipeline

### 1. Read the input

| Input | How to read it |
|---|---|
| `.md`, `.txt` | Read directly |
| `.docx`, `.pdf`, `.pptx` | `python3 design/scripts/source_text.py <file> --notes > source.txt` |

**Read the notes it prints.** Words baked into an image are pixels and do not
extract. Transcribe those by hand under a heading saying where they came from.

**The supplied content is the content.** Use its words. Do not improve a
sentence, invent a finding, expand an acronym it abbreviated, or research the
topic to add more. If the content does not say something a slide needs, **ask**.

The operative rules — what counts as a legal shortening, why deleting
mid-sentence is refused, how names are handled — are in
`design/references/content-rules.md`. Read it before drafting.

→ *Exit: every word that will appear on a slide exists in the source.*

### 2. Confirm purpose and audience → pick the template

**Ask the user. Do not assume.**

- What is this deck for?
- Who reads it, and are they in the room or reading it alone?

| Purpose | Folder | Lead file | `kind` |
|---|---|---|---|
| Client deliverable, read without a presenter | `Report/` | [[Report]] | `report` |
| Published thought leadership | `Report/` | [[Report]], publication variant | `publication` |
| Sells an engagement | `Proposal/` | [[Proposal]] — **not written, ask** | `proposal` |
| Presented live | `Talkbook/` | [[Talkbook]] — **blocked, ask** | `talkbook` |

Read the lead file for the chosen type before going on. Where it says *not
written*, stop and ask rather than borrowing another type in silence.

→ *Exit: the user has confirmed purpose, audience and template.*

### 3. Agree the length and the outline

**Ask for a target slide count.** Then write the outline: a numbered list, one
line per slide stating **the message of that slide**.

**Stop. Show the outline. Wait for an explicit go.**

Structural problems cost minutes here and hours after the build.

→ *Exit: the user has said go on the outline.*

### 4. One planning file per slide

Write `plan/01-<slug>.md` … `plan/NN-<slug>.md` in the engagement folder. One
file per slide, each carrying:

```markdown
# Slide 07 — <the message, as a sentence>

**Message.** The one assertion this slide makes. If there are two, split it.
**Layout.** The named master layout, from design/references/layouts.md
**Composition.** Where things sit: exhibit left 13.70, read right at 17.43, etc.
**Content.** The text for each placeholder, taken from the source.
**Exhibit.** Chart type, series, basis line, and the source of the numbers.
**Icons / graphics.** What and why, or "none".
```

Build one representative slide from its plan, show it, and wait for a go before
building the rest. Never the cover, which hides layout problems.

→ *Exit: every slide has a plan file, and one built slide is approved.*

### 5. One build file for the deck

Consolidate the plans into `deck.md`: the whole deck in order, slide by slide,
with the exact layout name and the exact placeholder content. This is the single
spec the build script is written from.

Then write and run the build script per `design/references/build-api.md`.
`deckkit` for placeholders, `exhibits.chart_exhibit()` for anything with a
number. **Open the deck with `new_deck(kind=...)`** from the table in step 2, so
the deck-type gates run.

→ *Exit: `save()` returns without raising.*

### 6. Coherence check before delivery

**The failure this step exists to catch is a set of correct slides that is not a
deck.** Run all of it:

- **Does it argue one thing?** Read the titles alone, top to bottom. They should
  read as a single argument. If they read as a list of topics, the deck is
  scattered.
- **Does each slide follow from the last?** A slide that could sit anywhere
  belongs nowhere.
- **Is the layout varied?** Every slide on one layout wastes the template.
- **Is anything said twice?** Merge it.
- **Is anything missing between two slides?** The reader should never have to
  make a leap the deck did not make.
- **Do the section dividers mark acts in the argument**, rather than chapter
  headings?
- **QA**, per `design/references/qa-checklist.md`: `qa.report()`,
  `scan_text.py`, `validate_pptx.py`, and `qa.content_fidelity()` returning
  zero.
- **The seven per-slide checks** in `design/references/design-principles.md` §7.

→ *Exit: the deck reads as one document, and every check that can run has run.*

---

## Where things go

| Item | Path |
|---|---|
| Extracted source | `Work/<Engagement>/source.txt` |
| Per-slide plans | `Work/<Engagement>/plan/` |
| Build spec and script | `Work/<Engagement>/deck.md`, `build.py` |
| The deck and its data booklet | `Work/<Engagement>/` — a deck ships as two files |
| Figure traces and renders | `Work/<Engagement>/evidence/` |
| Session note | `Sessions/YYYY-MM-DD <slug>.md`, opened at the start |

Use the engagement code name where one exists. `save()` takes a path relative to
the project folder.

## Reference, when you need it

Read the file that answers the question in front of you.

| Question | File |
|---|---|
| What a finished page looks like | `design/references/visual-reference/` — **look at the pages** |
| How to compose a slide | `design/references/design-principles.md` |
| Which layout, which placeholder idx | `design/references/layouts.md` |
| Anything carrying a number | `design/references/exhibits.md` |
| A colour or size literal | `design/references/brand.md` |
| What the words may be, and how to prove it | `design/references/content-rules.md` |
| Writing the build script | `design/references/build-api.md` |
| Wording and punctuation | `design/references/house-style-qrg.md` |
| The QA pass and what each gate fails on | `design/references/qa-checklist.md` |
| Which master each deck type uses | [[slide-template]] |
| What works on this Mac | [[environment]] |

**Assets**, all under `design/assets/`:

- `template.pptx` — the cleaned master, zero slides. `new_deck()` opens it
- `specimen-deck.pptx` — the 28-slide sample. For looking at and for lifting
  pre-formatted tables. **Never a starting point**; see [[slide-template]]
- `fonts/` — the nine brand faces

## `design/` is a local fork

`design/` is the imported `kpmg-deck` package, now **edited in place** and
version-controlled with the vault. Fix things there directly rather than
recording an override elsewhere.

The unmodified import is tagged **`kpmg-deck-pristine`**. To take an upstream
update:

```bash
git checkout -b upstream kpmg-deck-pristine
```

Drop the new package into `Work/_deck/design/`, commit, then merge into `main`.
Git resolves everything upstream changed that was not touched here, and raises a
conflict only where both moved.

**House changes inside `design/`**, so a merge conflict is recognisable:

| Change | Why |
|---|---|
| `SKILL.md` deleted | Its workflow and reference index competed with this file. The package map lives here now |
| `references/content-rules.md`, `references/build-api.md` added | The content and API rules extracted out of the old `SKILL.md` |
| `references/*.md` — dated provenance notes stripped | House note dates carried no information the rule did not |
| `scripts/deckkit.py` — `DECK_TYPES`, `new_deck(kind=...)` | Per-type closers made machine-readable |
| `scripts/qa.py` — three deck-type gates | Cover, closer, and no foreign back cover |
| `scripts/doctor.py:54` | Printed `pip3 install --user pptx`; the package is `python-pptx` |
| Cite KPMG's own thought leadership | `design-principles.md` §6 forbids it. It is a legitimate source for its own data |
| Use the 38 reference pages freely | `visual-reference/` marks them restricted |

Everything else in `design/` is upstream. `design/README.txt` describes the
package's original portable install, which this fork has superseded.

## Sources and citation

| Source | Analysis | Name it in the deck |
|---|---|---|
| KPMG publications | Yes | Yes |
| Competitor consultancy output | Yes, background and craft | No |
| Primary, government, regulator, filings | Yes | Yes, preferred |

Use everything in `design/` freely — reference pages, specimen, master, fonts.

## Related

- [[Report]] · [[Proposal]] · [[Talkbook]]
- [[slide-template]] · [[environment]]
