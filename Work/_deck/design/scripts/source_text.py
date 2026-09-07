#!/usr/bin/env python3
"""Pull the words out of a supplied source document, and say what it could not.

Added 26 August 2026, on house instruction: **when a document is supplied,
the deck uses the words in that document and does not change them.** That rule
is only enforceable if there is one honest answer to "what words were supplied",
so this produces it, and `qa.content_fidelity(mode="verbatim")` checks the deck
against it.

    python3 scripts/source_text.py article.docx > source.txt
    python3 scripts/source_text.py paper.pdf --notes

Handles `.md`, `.txt`, `.docx` and `.pdf`. Returns every run of text it can
reach, including .docx tables and the categories and series names inside
embedded native charts, because on a real build the exhibit data lived in
`word/charts/chart1.xml` and nowhere else.

**What it cannot reach, and why that matters.** Text baked into a picture is
pixels. A diagram exported as a PNG, a chart saved as an image, a scanned PDF:
the words are in the document and not in this output, so a deck that reproduces
them faithfully will be reported as unfaithful. `notes()` lists every image and
unreadable part it saw, and the answer is to transcribe them by hand and append
them to the extracted text under a heading that says where they came from. That
is a deliberate, recorded act. Silently letting the gate pass them is not.
"""
import argparse
import os
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
C_NS = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

SUPPORTED = (".md", ".txt", ".markdown", ".docx", ".pdf")


class Extraction:
    """The words, and an honest account of what was left behind."""

    def __init__(self, text, gaps=(), source=""):
        self.text = text
        self.gaps = list(gaps)
        self.source = source

    def __str__(self):
        return self.text

    def report(self, stream=sys.stderr):
        n_words = len(self.text.split())
        print("  source: %s" % os.path.basename(self.source), file=stream)
        print("  extracted: %d words" % n_words, file=stream)
        if self.gaps:
            print("  NOT extracted, %d item(s) — transcribe these by hand and "
                  "append them, or the fidelity gate will fail text that IS in "
                  "the document:" % len(self.gaps), file=stream)
            for g in self.gaps:
                print("   ! %s" % g, file=stream)
        else:
            print("  no unreadable parts", file=stream)


# ---------------------------------------------------------------------------
# Plain text and Markdown
# ---------------------------------------------------------------------------

# Markdown footnote references, `[^ep]`, `[^roic]`. They are citation markers,
# the same thing a superscript run is in Word, and left in they break an
# otherwise perfect quote: "destroyed economic value[^ep] for four consecutive
# years" stops matching a deck that quotes the sentence exactly. Added
# 26 August 2026. The footnote DEFINITIONS are left in place, because their
# text is part of the document and a deck may legitimately quote it.
MD_FOOTNOTE_REF = re.compile(r"\[\^[^\]\s]+\](?!:)")


def _from_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    return Extraction(MD_FOOTNOTE_REF.sub("", raw), [], path)


# ---------------------------------------------------------------------------
# Word
# ---------------------------------------------------------------------------

def _docx_chart_text(zf, name):
    """Category names and series names from an embedded native chart."""
    out = []
    try:
        root = ET.fromstring(zf.read(name))
    except (KeyError, ET.ParseError):
        return out
    for ser in root.findall(".//" + C_NS + "ser"):
        tx = ser.find(".//" + C_NS + "tx//" + C_NS + "v")
        if tx is not None and tx.text:
            out.append(tx.text)
        for pt in ser.findall(".//" + C_NS + "cat//" + C_NS + "pt/" + C_NS + "v"):
            if pt.text:
                out.append(pt.text)
    return out


def _from_docx(path):
    gaps, parts = [], []
    try:
        import docx                                    # noqa: F401
    except ImportError:
        return Extraction("", ["python-docx is not installed, so nothing was "
                               "read: pip3 install --user python-docx"], path)
    from docx import Document

    doc = Document(path)
    for p in doc.paragraphs:
        # Superscript runs are citation markers, not prose. Left in, they turn
        # "...in five years.3" into the words "in five years 3", and a deck
        # quoting that sentence perfectly then fails the verbatim gate on a
        # footnote number. Detected by formatting rather than by pattern, so a
        # real figure in the prose is never stripped.
        txt = "".join(r.text for r in p.runs if not r.font.superscript) \
            if p.runs else p.text
        if txt.strip():
            parts.append(txt)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                if cell.text.strip():
                    parts.append(cell.text)

    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        for n in sorted(names):
            if n.startswith("word/charts/chart") and n.endswith(".xml"):
                got = _docx_chart_text(zf, n)
                if got:
                    parts.append(" ".join(got))
        images = [n for n in names if n.startswith("word/media/")]
        for n in sorted(images):
            gaps.append("%s is a picture. Any words inside it are pixels, not "
                        "text. Read it and transcribe them." % posixpath.basename(n))
        embedded = [n for n in names if n.startswith("word/embeddings/")]
        for n in sorted(embedded):
            gaps.append("%s is an embedded object and was not opened. If it "
                        "carries figures the deck uses, open it and record "
                        "them." % posixpath.basename(n))
    return Extraction("\n".join(parts), gaps, path)


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def _from_pdf(path):
    gaps, pages = [], []
    reader = None
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
    except ImportError:
        try:
            from PyPDF2 import PdfReader          # older name, same job
            reader = PdfReader(path)
        except ImportError:
            return Extraction("", ["no PDF reader installed: pip3 install "
                                   "--user pypdf"], path)
    for i, page in enumerate(reader.pages, 1):
        try:
            txt = page.extract_text() or ""
        except Exception as exc:                   # a bad page is not fatal
            txt = ""
            gaps.append("page %d could not be read: %r" % (i, exc))
        if txt.strip():
            pages.append(txt)
        else:
            gaps.append("page %d yielded no text. It is probably a scan or an "
                        "image; the words on it have to be transcribed by hand"
                        % i)
    return Extraction("\n".join(pages), gaps, path)


# ---------------------------------------------------------------------------

def extract(path):
    """Extraction for one supplied document."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".txt", ".markdown"):
        return _from_text(path)
    if ext == ".docx":
        return _from_docx(path)
    if ext == ".pdf":
        return _from_pdf(path)
    raise ValueError(
        "unsupported source %r. This reads %s. A .doc or .pages file has to be "
        "saved as .docx first; a .pptx source is read with slides_to_md.py"
        % (ext, ", ".join(SUPPORTED)))


def extract_many(paths):
    """One Extraction covering several supplied documents."""
    texts, gaps = [], []
    for p in paths:
        e = extract(p)
        texts.append(e.text)
        gaps.extend("%s: %s" % (os.path.basename(p), g) for g in e.gaps)
    return Extraction("\n".join(texts), gaps, ", ".join(
        os.path.basename(p) for p in paths))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", nargs="+")
    ap.add_argument("--notes", action="store_true",
                    help="print the extraction report to stderr")
    args = ap.parse_args(argv)
    e = extract_many(args.source)
    sys.stdout.write(e.text)
    if args.notes or e.gaps:
        print("", file=sys.stderr)
        e.report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
