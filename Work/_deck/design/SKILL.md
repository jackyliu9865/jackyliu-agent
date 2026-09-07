---
name: kpmg-deck
description: "Build PowerPoint decks on the KPMG 2025 brand-refresh slide master — cover, section dividers, key findings, analysis, summary financials, back covers — with the locked palette, 44pt/9pt/8pt/6pt type scale and 2.72cm grid. Use this skill for ANY request to make a deck, slides, a presentation, a pitch, a report-out, or a .pptx, whenever the work is for KPMG or the person has previously used this template — even if they don't name the template, say \"branded\", or mention KPMG in that particular message. Also use it when editing, extending or brand-checking an existing deck built on this master."
---

# KPMG deck builder

Generate decks by filling the real template, not by redrawing it. The bundled
`assets/template.pptx` carries the KPMG Bold/Arial theme, the logo, the footer,
the classification line, the page numbers and 26 layouts on the main master (32 in the file, 6 of them on a second storage master). Add a slide
on a layout and every font, size and colour is inherited correctly with no
styling code at all.

For a McKinsey / BCG / Bain / MBB-quality deck that is **not** on this master
(case, recruiting, board, unnamed strategy work), use **consulting-deck** instead.
That skill builds from a blank 16:9 canvas with action titles and a ghost deck.
Do not redraw the KPMG master in consulting-deck, and do not use this skill for
a non-KPMG deliverable.

Redrawing this look from scratch in pptxgenjs does not work: KPMG Bold isn't
installed, the logo and footer are gone, and the result is a deck that looks
approximately right and is wrong in every detail that a reviewer checks.

## Rule 0: decide which mode you are in, before anything else

House note, 26 August 2026. **Which mode you are in changes what the job is**, and
getting it wrong is the difference between a deck that misquotes a client's
document and a deck that pads a blank page with plausible filler.

| | **Mode A — a document was supplied** | **Mode B — nothing was supplied** |
|---|---|---|
| Trigger | A `.md`, `.docx`, `.pdf`, `.txt`, or pasted text | A topic, a title, a brief, an idea |
| The job is | **Layout.** The thinking is already done | **Research, then layout.** The thinking is yours to do |
| Words | **The document's, word for word.** Change none of them | Yours, and every claim has to be sourced |
| Research | **None.** Do not go and find more | **In depth, and first.** No slide is drafted before the research exists |
| Gate | `qa.content_fidelity(..., mode="verbatim")` returns zero | Every number traceable to a named primary source |

**Neither mode is the light one.** Mode A forbids you from improving anything,
which is harder than it sounds. Mode B has no document to lean on, so the whole
burden of being right falls on the research.

---

### Mode A — a document was supplied

**Use the words in that document, word for word, and change none of them.**

The job is to lay the document out, not to improve it. Do not invent a finding,
sharpen a sentence, add an example, expand an acronym the document abbreviates,
or extend a list to fill a column. **Do not go and research the topic**: the
document is the whole of the input, and anything you find elsewhere is out of
scope even when it is true. If a slide is short, the composition is wrong, not
the content. If the document genuinely does not say something the slide needs,
**say so and ask** rather than filling the gap.

**Get the words out of the document with the tool, not by hand:**

```bash
python3 <skill>/scripts/source_text.py article.docx --notes > source.txt
```

It reads `.md`, `.txt`, `.docx` and `.pdf`, and reaches .docx tables and the
categories and series names inside embedded native charts. **Read the notes it
prints.** Words baked into a picture are pixels: a diagram exported as a PNG, a
chart saved as an image, a scanned PDF. It lists every such part it saw, and the
answer is to read them and transcribe them into the source file under a heading
saying where they came from. That is a deliberate, recorded act. Measured on a
real build: the raw extraction left 63 strings untraceable, and transcribing the
two flagged images brought it to 51.

**Names in a supplied document ship as written.** If the document names a person,
that name goes on the slide, spelled and styled exactly as the document has it.
Removing it is a change to the content, which Mode A forbids, and it is not the
layout agent's call to make: the author already decided. The same holds for a
name the person asks for explicitly. What is never allowed is a name you went and
found yourself, because Mode A forbids the research that would have produced it.

Three places a name is legitimate, and one where it never is:

| | Allowed? |
|---|---|
| In the supplied document | **Yes.** Verbatim, unaltered. Mode A requires it |
| Named explicitly by the person | **Yes.** They asked for it |
| An officer, in the company's own published statement about itself | **Yes**, at board or executive level, attributed to the source |
| Anywhere in this skill package | **No.** Never, in any circumstance |

That last row is why `SKILL.md`, the references, the scripts and the bundled
master carry no personal name: the package gets zipped, moved between machines
and handed to other agents, so anything inside it travels. A deliverable is
addressed to someone and stays where it is sent. They are different objects and
the rule for each is different.

**Then prove it:**

```python
qa.content_fidelity(prs, open("source.txt").read())      # mode="verbatim" is the default
```

Every string on a slide must be built from **contiguous runs of words** taken
from the document. Why it is spans rather than a word list, and why deleting
from the middle of a sentence is refused even when every remaining word is the
document's, is in `references/qa-checklist.md`.

| Allowed, because no word changes | Not allowed |
|---|---|
| Re-wrapping across lines | Paraphrase, however slight |
| **Stopping early.** "Payment infrastructure was built" is a legal shortening of "Payment infrastructure was built for humans" | A synonym |
| Joining two runs from **different parts** of the document, reported as a splice so it stays visible | A connective the document never used, including an "and" inserted to join two of its sentences |
| | Expanding an acronym the document abbreviated |
| | Reordering words |
| | **Deleting words from the middle of one sentence**, even a parenthetical |
| | Reassembling the document's vocabulary into a sentence it never wrote |

**The 36-character title box does not license a rewrite.** The answer to a
title that will not fit is a *shortened contiguous run* from the document, not a
new sentence built from its words.

**Punctuation is house style, not content.** `fill()` adds the terminal full
stop a body paragraph takes, in Mode A as in Mode B. Verified 27 August 2026:
`content_fidelity` normalises punctuation out before matching spans, so the
added stop is invisible to the verbatim gate and cannot turn a traceable string
into an untraceable one. If a supplied document's own punctuation has to survive
character for character, pass `fill(..., punctuate=False)` on those slides and
say so in the delivery note.

**One exception, counted rather than failed: exhibit basis lines.** A basis line
states period, units and scope, which is this skill's own required grammar and
not the document's prose, and a document rarely contains one ready-made. They are
listed separately in the report so they can be read by eye. A basis line still
must not assert anything the document does not support.

---

### Mode B — nothing was supplied

**Research first, deck second, and the research has to be real.**

House note, 26 August 2026: a deck built with no input document is not permission to
slack off. A blank page is the harder brief, not the easier one, because nothing
is carrying the argument except what you go and establish.

- **No slide is drafted before the research exists as a file.** The work lands in
  the project's `Research/` folder and stays there afterwards.
- **A verified data register.** Every number in the deck traced to a named
  primary source with its date and where in the document it sits. The standard is
  the `verified-data-booklet` skill; the worked precedent is
  `Asymmetric Warfare/Research/Verified Data Register.md`.
- **Primary sources.** Filings, annual reports, regulators, statistical agencies,
  issuer statements. Not a vendor blog summarising them.
- **No hallucination, and no illustrative numbers passed off as measured.** If it
  cannot be verified it does not go on a slide. A genuinely illustrative figure
  says so in its own source line, and `databooklet.py` classifies it purple
  automatically so it cannot pass for measured data.
- **A thesis, not a topic tour.** The deck argues something and shows the
  mechanism. Section dividers are acts in an argument, not chapter headings.
- **Exhibits from real series.** A page of shapes standing in for data is the
  failure this rule exists to stop.
- **The data booklet is not optional here either**, and in Mode B it is the main
  evidence that the research happened.

`content_fidelity` does not apply in Mode B, because there is no source document
to be faithful to. The discipline that replaces it is the sourcing gate: every
exhibit registered in the booklet, every source line naming a real document, and
`databooklet.check_booklet()` clean.

---

## The rule that applies in both modes

**An exhibit is a native chart, never a picture of one.** House note,
26 August 2026: *"images shouldn't be pictures if possible, instead excel
graph."*

A native chart carries an embedded Excel workbook, so a reader can open Edit
Data and check the numbers, the palette and type scale are inherited from the
master, and it prints and reflows at any size. A pasted image has none of that.
`qa.gate_no_picture_exhibits` fails any picture bigger than about 2.6 cm on both
sides; icons are the exception and are small. A diagram is drawn with real
shapes, which is how the x402 payment cycle page is built.

**This applies to what is inside the chart as well.** The categories in the
sheet must be the real categories. To thin a crowded axis use
`exhibits.label_every(chart, n)`, which sets `c:tickLblSkip` and leaves every
category name in the data. Do **not** blank unwanted labels by substituting
empty or whitespace strings: those go straight into the embedded workbook and
into the data booklet, so the axis reads correctly while Edit Data shows empty
cells. `exhibits.sparse_labels()` did exactly that and now raises.

*LibreOffice ignores `c:tickLblSkip` and draws every label, so the render pass
cannot confirm this one. PowerPoint implements it. Same class as the `INSET`
note in `references/exhibits.md`: judge label thinning in PowerPoint, not in the
render. The element order inside `c:catAx` is a strict schema sequence
(`lblOffset, tickLblSkip, tickMarkSkip, noMultiLvlLbl`) and PowerPoint enforces
it, so run the pptx skill's XSD validator after touching axis XML — the bundled
structural validator does not check sequence order.*



**Every chart links to the data booklet.** Added 25 August 2026 on the owner's
instruction. Build charts with `exhibits.chart_exhibit()`, which registers its
numbers as it draws, then write the booklet with `databooklet.write()` and gate
it with `databooklet.check_booklet()`. A deck ships as two files: the .pptx and
the .xlsx. A chart whose numbers are not in the booklet is a build error.

## Workflow

00. **Decide the mode, per Rule 0 above, and say which one you are in.** A
   document was supplied, or it was not. In **Mode A** the next step is
   `source_text.py`, and no research happens at all. In **Mode B** the next step
   is the research file, and no slide is drafted until it exists. Everything
   below applies to both.
0. **Look at `references/visual-reference/` first.** Thirty-eight rendered pages
   from three finished decks built on this master: Capital Allocator's Market,
   The New Machine Economy, Asymmetric Warfare. **That is the target.** The
   written rules below describe those pages and did not, on their own, make
   anyone produce them, because a rule you read is not a page you have seen.
   Read `00 — Visual Reference Index.md` for the four page compositions and
   then look at the JPGs. Compare your own render against them at the end.
   *(Added 26 August 2026, after a POV deck built entirely from
   `Analysis_Horizontal` came back with "why doesn't this look like the other
   outputs?". It did not, because the DD placeholder layouts are a different
   document shape from published thought leadership, and nothing in the skill
   showed the difference.)*
0a. **Read `references/design-principles.md`.** It covers the artboard, the
   grid, the composition patterns, minimal text and the seven checks per slide. It is
   the difference between a designed deck and a generated one, and it is the fix for
   the most common failure: every slide poured into the same layout with half a
   column left empty.
0b. **Read `references/exhibits.md` before any slide carrying a number.**
   KPMG runs on graphing and data-heavy analysis, and that file is the exhibit
   grammar taken from three published thought-leadership decks. A deck of text
   blocks with two charts in it is the failure this skill was corrected for on
   25 August 2026.
1. **Read `references/layouts.md`** and pick a layout per content section. Vary
   them — a deck where every slide is `One Column Text` wastes the template.
   The DD master's layouts are the starting point, not the ceiling: published
   TL pages are built on `Title only_Blank` with `exhibits.*` furniture, which
   is how the same master carries a due-diligence readout and a data-heavy
   publication without either looking like the other.
2. **Read `references/brand.md`** before writing any colour or size literal.
   **Measurements are in centimetres** (house standard, 21 August 2026);
   `deckkit` exports `CM` and a `GRID` dict of the guides in cm.
3. Write one Python script that builds the whole deck with
   `scripts/deckkit.py` for placeholders and `scripts/exhibits.py` for every
   exhibit.
4. Write the data booklet with `scripts/databooklet.py`.
5. Run the QA pass below, then `scripts/qa.py`. Fix what they find. **In Mode A
   that includes `qa.content_fidelity(prs, source)` returning zero**; in Mode B
   it includes `databooklet.check_booklet()` clean and every source line naming
   a real document.
6. Render every page and look at it. `check()` cannot see composition.

### Building

```python
import sys; sys.path.insert(0, "<path-to-this-skill>/scripts")
from deckkit import *

prs = new_deck()

s = add(prs, "Cover page")
fill(s, title="Project Falcon",
        ph11=["Commercial due diligence", "", "12 August 2026"],
        ph13="KPMG. Make the Difference.")

s = add(prs, "One Column Text")
fill(s, title="Revenue grew but mix deteriorated",
        ph18="Growth is real; margin quality is not.",
        ph56=[("Headline", 0), ("Revenue rose 14% CAGR FY22–FY25.", 1)]
             + bullets(["Volume contributed 9pp of the 14pp.",
                        "Price/mix contributed 5pp, all from one contract."]),
        ph17="Source: Management accounts, KPMG analysis")

save(prs, "falcon.pptx")   # relative to the project folder; never a machine-absolute path
```

`fill()` keys are `ph<idx>` and the idx numbers come from
`references/layouts.md` — they differ between layouts. Values are a string, a
list of strings, or a list of `(text, level)` tuples. `bullets(items)` builds
the tuple list for you.

Levels are 0-based and the master assigns each one a job: **0 and 1** are
unbulleted paragraphs, **2 and deeper** carry the bullet glyph at increasing
indents. So a lead-in with bullets under it is
`[("Headline", 0)] + bullets([...])`.

The master makes level 0 bold, but every content layout overrides that back to
regular, so a lead-in won't look like a heading on its own. If you need one to
stand out, put the emphasis in the header bar (`Analysis_*` idx 54, the Key
findings bars) rather than bolding body text by hand.

If a layout isn't in `references/layouts.md`, or you want to confirm one that
is, `probe("Two Columns Text")` prints its real placeholder map — idx, type and
geometry — straight from the template.

Helpers: `note()` for the source line, `strapline()` for the key message,
`rag(slide, idx, "red"|"amber"|"green")` for traffic-light chips, `table()` for
brand-formatted tables (**cm by default**, `units="in"` for the old behaviour).

### Charts and tables

Build every exhibit with `exhibits.chart_exhibit()`, never `deckkit.chart()`
directly: the former registers its numbers so `databooklet.check_booklet()` can
prove the chart traces to the booklet, and an unregistered chart is a build
error.

Full signatures, every argument and the geometry, are in
**`references/exhibits.md`**. Read it before any slide carrying a number.


### House style

Non-negotiable, and enforced: `qa.gate_house_style` runs the QRG find-and-replace
list over every string on every slide, and `save()` raises on a finding.

The full rules are bundled at **`references/house-style-qrg.md`**; deck-side
typography, colour and table formatting are in **`references/brand.md`**. Read
whichever governs what you are about to write.

The four that catch people most often: **no full stops on bullets, but body
paragraphs do take one**, **sentence case** not title case, **numbers one to
nine in words**, and a percentage move is in **percentage points**, never per
cent.

On that first one, added 27 August 2026 on house instruction: the rule names
*bullets*, meaning list items, and a prose paragraph is not a bullet. `fill()`
and `exhibits.commentary()` now add the terminal full stop to body paragraphs
for you, and leave bullets, header bars, summary strips, straplines, source
lines and cover text alone. Notes and sources still take a full stop as they
always did. `scripts/test_punctuation.py` asserts the whole matrix; run it after
touching `deckkit._is_prose_body`.


### The rules that matter most

- **Never assign `text_frame.text`.** It collapses the placeholder to one
  unstyled run and takes the inherited brand formatting with it. `deckkit`
  writes runs individually; if you go around it, do the same.
- **Never set a font size, face or colour on placeholder text.** Inheritance
  already gives you the right one. An explicit `Pt(14)` on body text is a bug,
  not a preference.
- **Only palette colours**, and only in their assigned role. See
  `references/brand.md`. RAG red/amber/green are for status ratings and nothing
  else.
- **9pt body is correct.** Dense is the house style. If content doesn't fit,
  cut it or split the slide; don't shrink boxes or grow type.
- **Nothing below the source strip at y 16.32cm** — that's the footer zone and the master says so.
- **Fill the strapline and the source line.** Every content layout has both
  because the house style demands an assertion and a provenance on each slide.
- Don't open `assets/specimen-deck.pptx` as a starting point. Its 28 sample
  slides cross-link, and deleting them leaves orphans that collide with new
  slides and make PowerPoint report the file as corrupt. `new_deck()` already
  opens the cleaned template. The specimen deck is for looking at.

### Adding your own shapes

Sometimes a layout gives you a blank region (`Title only_Blank`, the chart half
of `Analysis_Horizontal`). Shapes you add there are yours to style, so apply the
brand yourself: Arial, 9pt body / 8pt in tables, palette fills, `margin: 0`
equivalents via cell/text insets, and stay inside the grid columns listed in
`references/brand.md`. Charts go in as native PowerPoint charts with
`CHART_SERIES` colours in order — never as images.

**Place them in centimetres.** `deckkit` exports `CM` (alias of `pptx.util.Cm`)
and `GRID`, a dict of every guide in cm, so a shape on the second column of a
two-column split is `CM(GRID["col2_x"])` rather than a retyped inch literal.
`table()` now takes cm by default; pass `units="in"` for the old behaviour.
`in2cm()` and `cm2in()` are there for converting a value read off the template.

## QA (required)

Run all five, in order. Each one catches what the one before it cannot.

```bash
# 1. structural + brand + house style, in-process. save() RAISES on a finding.
python3 -c "import qa, databooklet; qa.report(prs, booklet_problems=databooklet.check_booklet(prs))"

# 2. every string, as a separate gate that exits 1
python3 <skill>/scripts/scan_text.py out.pptx          # --dump to read every string

# 3. the file itself: parts, relationships, layouts, masters
python3 <skill>/scripts/validate_pptx.py out.pptx --original <skill>/assets/template.pptx

# 4. the font, verified by RENDERING, never by listing the fonts folder
soffice --headless --convert-to pdf out.pptx --outdir .
python3 -c "import re,io;print(sorted(set(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+#,\-_]+)', io.open('out.pdf','rb').read()))))"

# 5. rasterise and LOOK at every page
pdftoppm -jpeg -r 90 out.pdf page
```

**Step 4 passes only if `KPMG-Bold` comes back alongside the Arial faces.** Arial
alone means the font is not resolving and every title in the deck is wrong.

**Step 5 cannot be automated.** `check()` sees geometry, not composition. Run the
seven per-slide design checks in `references/design-principles.md` section 7:
title states a finding, one argument per slide, no column a third empty, on the
grid, every colour means something, sourced with bars from zero, content reaching
past y 11 cm.

**Fix findings; never pass `verify=False` to get round them.** Each one is a
defect that shows on the rendered slide. What each gate means, what it costs and
why it exists is in `references/qa-checklist.md`.

**Never report a check you did not run.** If a binary is missing, say the render
pass was skipped and why. A deck that only had `check(prs)` run on it has not
been visually checked.

### What you need installed

| Piece | Needed for | Get it |
|---|---|---|
| `python-pptx` | **Everything.** `deckkit` imports it | `pip3 install --user python-pptx` |
| `openpyxl` | The data booklet | `pip3 install --user openpyxl` |
| `soffice` | Steps 4 and 5, SVG icon fallbacks | `brew install --cask libreoffice` |
| `pdftoppm` | Step 5 page images | `brew install poppler` |

Nothing else. The master, all nine faces, every reference, the house-style QRG
and the .pptx validator ship inside the skill. Run `python3 scripts/doctor.py`
to confirm on any machine.


## The modules

| Module | What it is for |
|---|---|
| `deckkit` | Placeholders, tables, the grid, `save()`. The base layer |
| `exhibits` | Every exhibit type, the slot system, the read column. **Use this for anything with a number in it** |
| `qa` | The gate set. `qa.report()` returns findings per gate |
| `databooklet` | Writes the booklet and proves every chart links to it |
| `icons` | SVG icons that stay vector and recolourable |
| `fonts` | Installs the nine faces on a new machine |
| `scan_text`, `validate_pptx`, `doctor`, `package`, `selftest`, `slides_to_md` | QA, diagnosis and moving the skill |

Each module's own docstring is the reference for its API;
**`references/exhibits.md`** carries the exhibit grammar in full.


### Installing, moving and proving the package

`python3 scripts/doctor.py` checks every piece and says what is missing.
`python3 scripts/package.py` wraps the skill and the nine faces into one archive
for another machine. **`README.txt` carries both in full**, plus how the fonts
deploy themselves and what "self-contained" is tested to mean.

The short version: the master, all nine faces, every reference, the house-style
QRG and the .pptx validator ship inside this folder. `soffice` and `pdftoppm` do
not, are not ours to redistribute, and are needed only to look at output rather
than build it.


### Traps

Layout-specific gotchas, each with what it costs and how to avoid it, are in
**`references/layouts.md`** under *Traps found building on this master*. Read it
before hand-placing anything on a layout you have not used.



# -> ~/Library/Application Support/Artemis/kpmg-deck-dist/kpmg-deck-<date>.zip
```

Unzip on the new machine, symlink it into `~/.claude/skills/kpmg-deck`, and
build. `new_deck()` installs the faces on first run.

**Verified 25 August 2026, twice.** The archive was extracted to a clean
directory outside the vault and run from there on **stock macOS Python 3.9.6**,
with no virtualenv and without the pptx skill on the path:

- `doctor.py` — every required piece present, and the font probe came back
  `KPMG-Bold` rather than Arial
- `selftest.py` — **0 findings across 23 gates**, including the bundled
  structural validator
- `validate_pptx.py` — clean against a real 16-slide deck built elsewhere

`grep -rl "PA. Record"` over the extracted bundle returns two files and neither
is a dependency: `package.py`'s install instructions use it as an example path,
and `doctor.py` uses it for the optional house-style drift check, which reports
"vault note not on this machine" and carries on.

**The fonts travel, and this was proved rather than assumed.** The archive
carries all nine faces including `KPMGLOGO1.ttf`, which is a separate family and
which a `KPMG-*.ttf` glob misses. `ensure_installed()` was then run against a
temporary font directory with the off-vault vendor path disabled, so the bundle
was the only possible source: **9 faces installed, 0 already present, and every
one byte-identical (SHA-256) to the copies in `~/Library/Fonts`.**

One honest limit on that: the render probe returning `KPMG-Bold` was measured on
a machine where the faces were already installed, so it proves the faces render,
not that a never-seen-them machine renders. The chain is proved in links instead
— the bundle holds the right bytes, `ensure_installed()` puts them in the user
font directory on a machine that lacks them, and PowerPoint and LibreOffice
resolve them once they are there. Short of uninstalling the faces from this
machine, that is as far as the proof goes.

**Internal use across your own devices only.** Handing the archive to anyone
outside KPMG redistributes a Commercial Type licence.


## Reference files

Read in this order. The first two decide what you build; the rest are read while
building it.

| File | Read it |
|---|---|
| `references/visual-reference/` | **First.** 38 rendered pages from three finished decks: the target |
| `references/design-principles.md` | **Second.** Artboard, grid, the four page compositions, the seven per-slide checks |
| `references/exhibits.md` | Before any slide with a number: exhibit grammar, which chart answers which question, full signatures |
| `references/layouts.md` | Choosing a layout, placeholder idx numbers, box geometry, traps |
| `references/brand.md` | Palette, type scale, the cm grid, table rules |
| `references/house-style-qrg.md` | Before any client-facing deck. Bundled verbatim; the vault note stays the authority and `doctor.py` reports drift |
| `references/qa-checklist.md` | What each gate fails on, what stays manual, and why |

`assets/template.pptx` is the cleaned master, zero slides.
`assets/specimen-deck.pptx` is the 28-slide sample, for lifting pre-formatted
tables out of. `scripts/source_text.py` is Mode A's first step.


## Related

- [[house-style-qrg]]
- [[00 — Visual Reference Index]]
- [[SKILLS — Library Index]]
- [[consulting-deck]]
- [[UNIVERSAL — Agent Rules & Standards]]
- [[Projects Index]]
