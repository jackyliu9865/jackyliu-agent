---
tags: [note, skills, kpmg-deck, content]
---

# Content rules — turning supplied content into slide text

**Read this at step 1 of the pipeline in `SKILL.md`, before drafting a single
line.** These are write-time rules. `qa-checklist.md` covers what the
gates check afterwards and why they are shaped as they are.

The house workflow always supplies content: a `.md`, a `.pdf`, a `.docx`,
another deck, or pasted text. **The job is layout. The thinking is already
done.**

## The rule everything else follows from

**Use the words in that document, word for word, and change none of them.**

Do not invent a finding, sharpen a sentence, add an example, expand an acronym
the document abbreviates, or extend a list to fill a column. **Do not go and
research the topic**: the document is the whole of the input, and anything found
elsewhere is out of scope even when it is true.

If a slide is short, **the composition is wrong and the content is right**. If
the document genuinely does not say something a slide needs, **say so and ask**
rather than filling the gap.

## Get the words out with the tool

```bash
python3 design/scripts/source_text.py article.docx --notes > source.txt
```

It reads `.md`, `.txt`, `.docx` and `.pdf`, and reaches `.docx` tables and the
categories and series names inside embedded native charts.

**Read the notes it prints.** Words baked into a picture are pixels: a diagram
exported as a PNG, a chart saved as an image, a scanned PDF. It lists every such
part it saw. Read those and transcribe them into the source file under a heading
saying where they came from — a deliberate, recorded act. Measured on a real
build: raw extraction left 63 strings untraceable, and transcribing the two
flagged images brought it to 51.

## What counts as faithful

Every string on a slide must be built from **contiguous runs of words** taken
from the document.

| Allowed, because no word changes | Not allowed |
|---|---|
| Re-wrapping across lines | Paraphrase, however slight |
| **Stopping early.** "Payment infrastructure was built" is a legal shortening of "Payment infrastructure was built for humans" | A synonym |
| Joining two runs from **different parts** of the document, reported as a splice so it stays visible | A connective the document never used, including an "and" inserted to join two of its sentences |
| | Expanding an acronym the document abbreviated |
| | Reordering words |
| | **Deleting words from the middle of one sentence**, even a parenthetical |
| | Reassembling the document's vocabulary into a sentence it never wrote |

Why it is spans rather than a word list, and why deleting from the middle is
refused even when every remaining word is the document's, is in
`qa-checklist.md`.

**The 36-character title box does not license a rewrite.** The answer to a title
that will not fit is a *shortened contiguous run* from the document, never a new
sentence assembled from its words.

## Punctuation is house style

`fill()` adds the terminal full stop a body paragraph takes. `content_fidelity`
normalises punctuation out before matching spans, so the added stop is invisible
to the verbatim gate and cannot turn a traceable string into an untraceable one.

Where a supplied document's own punctuation has to survive character for
character, pass `fill(..., punctuate=False)` on those slides and say so in the
delivery note.

**One exception, counted rather than failed: exhibit basis lines.** A basis line
states period, units and scope. That is this package's required grammar rather
than the document's prose, and a document rarely carries one ready-made. They
are listed separately in the report so they can be read by eye. A basis line
still must not assert anything the document does not support.

## Names

**A name in the supplied document ships as written**, spelled and styled exactly
as the document has it. Removing it is a change to the content, and it is not
the layout agent's call: the author already decided. The same holds for a name
the user asks for explicitly.

**A name found by research is never allowed**, because the research that would
have produced it is itself out of scope.

| | Allowed? |
|---|---|
| In the supplied document | **Yes.** Verbatim, unaltered |
| Named explicitly by the user | **Yes.** They asked for it |
| An officer, in the company's own published statement about itself | **Yes**, at board or executive level, attributed to the source |
| Anywhere in this package's own files | **No.** Never, in any circumstance |

That last row holds because the package travels between machines and to other
agents. A deliverable is addressed to someone and stays where it is sent.

## Prove it

```python
qa.content_fidelity(prs, open("source.txt").read())   # mode="verbatim" is the default
```

**Zero findings, or the deck does not ship.**

## Exhibits: native charts only

**An exhibit is a native chart, never a picture of one.**

A native chart carries an embedded Excel workbook, so a reader can open Edit Data
and check the numbers; the palette and type scale are inherited from the master;
and it prints and reflows at any size. A pasted image has none of that.
`qa.gate_no_picture_exhibits` fails any picture bigger than about 2.6 cm on both
sides. Icons are the exception and are small. A diagram is drawn with real
shapes.

**This applies inside the chart as well.** The categories in the sheet must be
the real categories. To thin a crowded axis use `exhibits.label_every(chart, n)`,
which sets `c:tickLblSkip` and leaves every category name in the data. Do **not**
blank unwanted labels with empty or whitespace strings: those go straight into
the embedded workbook and the data booklet, so the axis reads correctly while
Edit Data shows empty cells. `exhibits.sparse_labels()` did exactly that and now
raises.

*LibreOffice ignores `c:tickLblSkip` and draws every label, so the render pass
cannot confirm this one. PowerPoint implements it. Judge label thinning in
PowerPoint. The element order inside `c:catAx` is a strict schema sequence
(`lblOffset, tickLblSkip, tickMarkSkip, noMultiLvlLbl`) and PowerPoint enforces
it, so validate after touching axis XML — the bundled structural validator does
not check sequence order.*

## Every chart links to the data booklet

Build charts with `exhibits.chart_exhibit()`, which registers its numbers as it
draws. Write the booklet with `databooklet.write()` and gate it with
`databooklet.check_booklet()`.

**A deck ships as two files: the `.pptx` and the `.xlsx`.** A chart whose numbers
are not in the booklet is a build error.

## Related

- [[qa-checklist]] — what the gates check, and why
- [[build-api]] — how to place the content once it is written
- [[exhibits]] — exhibit grammar and chart signatures
- [[house-style-qrg]] — wording and punctuation
