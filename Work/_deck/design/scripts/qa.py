"""Automated QA gates for a KPMG deck.

the review note, 25 August 2026: the QA checklist has to be incorporated into
the skill, and **the agent should be able to flag or highlight areas where QA
is not met**. So this module does not describe the checklist, it runs it, and
it prints a PASS or FAIL line per gate so nothing is quietly assumed.

The checklist itself is the house-style QRG's section 9 plus the chart and
table rules in sections 4 and 5, held in the vault at
`Career/KPMG House Style — PowerPoint & Report QRG.md`. `references/qa-checklist.md`
records which gates run here and which stay manual, and why.

Gates that cannot be automated honestly (greyscale flick-through, proofing
language, spell check) are printed as MANUAL rather than silently passed. A
gate that reports PASS here really ran.
"""
import re
from collections import OrderedDict

from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Pt

from deckkit import (GRID, DARK_BLUE, KPMG_BLUE, COBALT, PACIFIC, BLUE,
                     LIGHT_BLUE, BLUE_ACCENT1, BLUE_GRAY, AQUA, LIGHT_TURQ,
                     WHITE, GREY, RAG, CHART_SERIES)

# The closed palette, as hex, from references/brand.md. Anything else on a
# slide is off-brand by definition.
PALETTE = {str(c) for c in [
    DARK_BLUE, KPMG_BLUE, COBALT, PACIFIC, BLUE, LIGHT_BLUE, BLUE_ACCENT1,
    BLUE_GRAY, AQUA, LIGHT_TURQ, WHITE] + list(GREY.values()) + list(RAG.values())}
PALETTE |= {"000000", "FFFFFF"}
PALETTE |= {"510DBC", "7213EA", "B497FF", "008E7E", "00C0AE", "7AFFBD",
            "AB0D82", "FD349C", "FFA3DA"}   # reserved accents, on palette

SANCTIONED_PT = {6, 7, 8, 9, 10, 14, 18, 24, 44, 66}

IZE = re.compile(r"\b\w+i[sz]ation\b|\b\w+ize[ds]?\b|\b\w+izing\b", re.I)
# Words ending -size are not -ize Americanisms. Anything built on "size"
# (unsized, downsized, right-sizing, supersize) is correct UK English, and
# flagging it teaches the reader to ignore this gate, which is worse than not
# having it. Fixed 25 Aug 2026 after "unsized" was reported on a live deck.
IZE_OK = re.compile(r"\b\w*(?:siz|priz|seiz)(?:e[ds]?|ing)\b", re.I)
ACRONYM_STOPS = re.compile(r"\b(?:[A-Z]\.){2,}")
# The house rule is that acronyms pluralise without an apostrophe: KPIs, not
# KPI's. A POSSESSIVE acronym is correct English and is not the target, so the
# gate fires only where the apostrophe is doing plural work: an acronym
# followed by a plural verb, or preceded by a number or quantifier.
# Fixed 25 Aug 2026 after "BCT\'s rise was an acquisition" was reported.
ACRONYM_APOS = re.compile(
    r"(?:(?:\b(?:many|several|both|few|all|these|those|two|three|four|five|six|"
    r"seven|eight|nine|ten|\d+)\s+)([A-Z]{2,}'s)\b"
    r"|\b([A-Z]{2,}'s)\s+(?:are|were|have|include|comprise|remain|differ|vary)\b)")
PHONE = re.compile(r"\b(?:\(0?\d{2,4}\)|0\d{2,4})[\s-]?\d{3,4}[\s-]?\d{3,4}\b")
PP_TRAP = re.compile(r"from\s+\d+(?:\.\d+)?%\s+to\s+\d+(?:\.\d+)?%", re.I)
PP_CLAIM = re.compile(r"(increase|decrease|rise|fall|up|down|growth)\w*\s+"
                      r"(?:of\s+|by\s+)?\d+(?:\.\d+)?%", re.I)
DATE_LONG = re.compile(r"\b\d{1,2}\s+(January|February|March|April|May|June|"
                       r"July|August|September|October|November|December)\s+\d{4}\b")


def _iter_text(slide):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                t = "".join(r.text for r in para.runs)
                if t.strip():
                    yield shape, t
        if getattr(shape, "has_table", False):
            for row in shape.table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        yield shape, cell.text


def _iter_runs(slide):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    yield shape, run
        if getattr(shape, "has_table", False):
            for row in shape.table.rows:
                for cell in row.cells:
                    for para in cell.text_frame.paragraphs:
                        for run in para.runs:
                            yield shape, run


def _hex_fills(slide):
    out = []
    for shape in slide.shapes:
        try:
            if shape.fill.type is not None and shape.fill.type == 1:
                out.append((shape.name, str(shape.fill.fore_color.rgb)))
        except (AttributeError, TypeError, ValueError):
            pass
        if getattr(shape, "has_chart", False):
            for ser in shape.chart.series:
                try:
                    out.append((shape.name, str(ser.format.fill.fore_color.rgb)))
                except (AttributeError, TypeError, ValueError):
                    pass
    return out


# ---------------------------------------------------------------------------
# Individual gates. Each returns a list of finding strings; empty means PASS.
# ---------------------------------------------------------------------------

def gate_masters(prs):
    """Every slide on the correct master; no stray masters in the file."""
    out = []
    masters = {}
    for n, slide in enumerate(prs.slides, 1):
        m = slide.slide_layout.slide_master
        masters.setdefault(m.name or "master", []).append(n)
    if len(masters) > 1:
        out.append("slides sit on %d different masters: %s. Every slide should "
                   "be on one." % (len(masters), dict(masters)))
    return out


def gate_palette(prs):
    """No colour outside the closed palette."""
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for name, hexv in _hex_fills(slide):
            if hexv.upper() not in PALETTE:
                out.append("slide %d: shape %r is filled #%s, which is not on "
                           "the palette" % (n, name, hexv))
    return out


def gate_type_scale(prs):
    """No hand-set font size outside the sanctioned scale."""
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for shape, run in _iter_runs(slide):
            sz = run.font.size
            if sz is None:
                continue
            if round(sz.pt) not in SANCTIONED_PT:
                out.append("slide %d: %r sets %.0fpt, off the type scale"
                           % (n, shape.name, sz.pt))
    return out


def _has_series_name_labels(ch):
    """True if the chart labels its series on the data itself.

    A line labelled at its own end IS the key, and a better one than a legend,
    so it must satisfy the key gate rather than fail it. Detected from the
    data-label XML rather than from how the chart was built, so a hand-built
    chart gets the same credit.
    """
    from pptx.oxml.ns import qn
    for el in ch._chartSpace.iter(qn('c:showSerName')):
        if el.get('val') in ('1', 'true'):
            return True
    return False


def _visible_series_count(ch):
    """Series the reader can actually see.

    A waterfall is a stacked column whose base series is deliberately
    invisible. Counting it would demand a key for a colour nobody sees.
    """
    from pptx.oxml.ns import qn
    n = 0
    for ser in ch.series:
        spPr = ser._element.find(qn('c:spPr'))
        if spPr is not None and spPr.find(qn('a:noFill')) is not None:
            continue
        n += 1
    return n


def gate_chart_legend(prs):
    """Colour that encodes anything carries a key. House note, 25 Aug 2026.

    A key can be a legend, or direct labels on the marks. What is not
    acceptable is two visible series and no way to tell which is which.
    """
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not getattr(shape, "has_chart", False):
                continue
            ch = shape.chart
            n_ser = _visible_series_count(ch)
            if "#" in (shape.name or ""):
                continue          # one panel of a small-multiples row; the
                                  # row carries a single shared key
            if n_ser > 1 and not ch.has_legend and not _has_series_name_labels(ch):
                out.append("slide %d: chart %r has %d series and no key, so "
                           "its colours mean nothing to the reader"
                           % (n, shape.name, n_ser))
            if ch.has_legend:
                try:
                    if ch.legend.font.size and ch.legend.font.size > Pt(8):
                        out.append("slide %d: legend is %.0fpt; the QRG says 7pt"
                                   % (n, ch.legend.font.size.pt))
                except AttributeError:
                    pass
    return out


def gate_rag_key(prs):
    """A traffic-light chip is meaningless without a stated scale."""
    out = []
    rag_hexes = {str(v).upper() for v in RAG.values()}
    for n, slide in enumerate(prs.slides, 1):
        chips = [nm for nm, h in _hex_fills(slide) if h.upper() in rag_hexes]
        if not chips:
            continue
        text = " ".join(t for _s, t in _iter_text(slide)).lower()
        explained = ("red is" in text or "red =" in text
                     or "traffic-light" in text or "traffic light" in text)
        if not explained:
            out.append("slide %d: %d traffic-light chip(s) with no key. State "
                       "what red, amber and green mean in the note, or drop "
                       "the colour" % (n, len(chips)))
    return out


def gate_exhibit_grammar(prs):
    """Every chart carries an exhibit title and a basis line."""
    out = []
    for n, slide in enumerate(prs.slides, 1):
        charts = [s for s in slide.shapes if getattr(s, "has_chart", False)]
        if not charts:
            continue
        names = {s.name for s in slide.shapes}
        if not any(x == "EXHIBIT_TITLE" or x.startswith("EXHIBIT_TITLE")
                   for x in names):
            out.append("slide %d: chart with no exhibit title. The finding goes "
                       "above the plot in 10pt bold KPMG Blue" % n)
        if not any(x.startswith("EXHIBIT_BASIS") for x in names):
            out.append("slide %d: chart with no basis line. State the period, "
                       "the units and which axis carries what" % n)
    return out


def gate_sources(prs):
    """Every table, chart and quoted figure carries a source."""
    out = []
    for n, slide in enumerate(prs.slides, 1):
        name = slide.slide_layout.name.lower()
        if "cover" in name or "divider" in name:
            continue
        has_ex = any(getattr(s, "has_chart", False)
                     or getattr(s, "has_table", False) for s in slide.shapes)
        if not has_ex:
            continue
        texts = [t for _s, t in _iter_text(slide)]
        if not any(t.strip().lower().startswith(("source", "note:", "sources"))
                   for t in texts):
            out.append("slide %d: exhibit with no source line" % n)
    return out


# A capitalised word that is not opening a sentence is a name, and a name is
# spelled the way its owner spells it. Added 25 August 2026 after the gate
# failed a deck over "Monetization Gateway", which is Cloudflare's product.
# Renaming a real product to satisfy a house style rule is a factual error, and
# a worse one than the style slip it would fix. This is the same principle
# `gate_acronyms` already applies to quoted document titles: UK English governs
# OUR prose, not someone else's name for their own thing.
_SENTENCE_START = re.compile(r"(?:^|[.!?:;]\s+|\n\s*|[\u2022\-\u2013]\s*)$")


def _is_proper_noun(text, match):
    """True if this word is capitalised and not opening a sentence."""
    word = match.group(0)
    if not word[:1].isupper():
        return False
    return not _SENTENCE_START.search(text[:match.start()])


def gate_uk_english(prs, allow=()):
    """Flag -ize/-ization Americanisms in our own prose.

    `allow` takes any further words to exempt, for the case a lower-case term
    of art genuinely has to keep its US spelling.
    """
    allowed = {w.lower() for w in allow}
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for _s, t in _iter_text(slide):
            for m in IZE.finditer(t):
                w = m.group(0)
                if IZE_OK.fullmatch(w) or "is" in w[-5:].lower():
                    continue
                if w.lower() in allowed or _is_proper_noun(t, m):
                    continue
                if re.search(r"iz", w, re.I):
                    out.append("slide %d: %r is US spelling" % (n, w))
    return out


_QUOTED = re.compile(r"['\u2018\u2019\u201c\u201d\"][^'\u2018\u2019\u201c\u201d\"]{6,}?"
                     r"['\u2018\u2019\u201c\u201d\"]")


def _quoted_spans(text):
    """Character ranges inside quotation marks.

    A cited document title is reproduced as its publisher wrote it. House style
    governs our prose, not someone else's title, so 'The U.S. Budgetary Costs
    of the Post-9/11 Wars' is correct as printed and must not be silently
    corrected into a misquotation. Added 25 Aug 2026.
    """
    return [(m.start(), m.end()) for m in _QUOTED.finditer(text)]


def gate_acronyms(prs):
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for _s, t in _iter_text(slide):
            spans = _quoted_spans(t)
            for pat, msg in ((ACRONYM_STOPS, "acronym with full stops"),
                             (ACRONYM_APOS, "acronym with an apostrophe; KPIs, not KPI's")):
                for m in pat.finditer(t):
                    if any(a <= m.start() and m.end() <= b for a, b in spans):
                        continue          # inside a quoted title, left as published
                    out.append("slide %d: %s: %r" % (n, msg, m.group(0)))
                    break
    return out


def gate_percentage_points(prs):
    """A move from 30% to 35% is 5 pp, never 5%."""
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for _s, t in _iter_text(slide):
            if PP_TRAP.search(t) and PP_CLAIM.search(t) and " pp" not in t:
                out.append("slide %d: percentage move described in %% rather "
                           "than pp: %r" % (n, t[:90]))
    return out


def gate_phone(prs):
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for _s, t in _iter_text(slide):
            if PHONE.search(t) and "+" not in t:
                out.append("slide %d: telephone number not in international "
                           "format: %r" % (n, PHONE.search(t).group(0)))
    return out


def gate_footprint(prs):
    """Content must stop at the content floor; the source strip is not content.

    Three limits, and conflating them is what made this gate wrong twice:
      * content ends at GRID["no_content_below"], the content floor
      * the source strip runs from 16.32 to 17.32 and legitimately sits below
        that floor, because that is where the master puts placeholder idx 17
      * the master's own "no content below this line" marker is lower still

    So idx 17, idx 18 and a hand-drawn EXHIBIT_SOURCE are furniture, held to
    the strip rather than to the content floor. Cover, divider and transmittal
    layouts are fixed master artwork and are skipped entirely: an earlier
    version flagged the template's own cover placeholder, which is proof the
    threshold was being applied to the wrong things.

    Tables are the case that matters for the content floor, because PowerPoint
    grows their rows to fit and reports nothing about it, so their height is
    estimated from the text rather than read off the shape.
    """
    from deckkit import table_height
    out = []
    limit = GRID["no_content_below"]
    strip_floor = GRID["source_strip_y"] + GRID["source_strip_h"]
    for n, slide in enumerate(prs.slides, 1):
        lname = (slide.slide_layout.name or "").lower()
        if "cover" in lname or "divider" in lname or "transmittal" in lname:
            continue
        for shape in slide.shapes:
            try:
                is_ph = shape.is_placeholder
                idx = shape.placeholder_format.idx if is_ph else None
            except (AttributeError, ValueError):
                is_ph, idx = False, None
            name = shape.name or ""
            try:
                if shape.top is None:
                    continue
                top_cm = shape.top / 360000.0
                h_cm = (shape.height or 0) / 360000.0
            except (AttributeError, TypeError):
                continue

            if idx in (17, 18) or name == "EXHIBIT_SOURCE":
                if top_cm + h_cm > strip_floor + 0.15:
                    out.append(
                        "slide %d: %r ends at y %.2f cm, past the bottom of the "
                        "source strip at %.2f" % (n, name, top_cm + h_cm,
                                                  strip_floor))
                continue

            if top_cm > limit:
                out.append("slide %d: %r starts at y %.2f cm, below the "
                           "content floor at %.2f" % (n, name, top_cm, limit))
                continue
            if getattr(shape, "has_table", False):
                tbl = shape.table
                rows = [[c.text for c in r.cells] for r in tbl.rows]
                widths = [col.width / 360000.0 for col in tbl.columns]
                h_cm = table_height(rows, sum(widths), widths)
            bottom = top_cm + h_cm
            if bottom > limit + 0.15:
                out.append(
                    "slide %d: %r ends at y %.2f cm, past the content floor at "
                    "%.2f. %s" % (n, name, bottom, limit,
                                  "A table grows its rows to fit, so the height "
                                  "on the shape is not the height on the page. "
                                  "Split it or cut words."
                                  if getattr(shape, "has_table", False)
                                  else "Move it up or shrink it."))
    return out


def gate_draft_stamp(prs):
    """The master's DRAFT banner has to come off a final deck."""
    seen, masters = set(), []
    for slide in prs.slides:
        m = slide.slide_layout.slide_master
        if id(m) not in seen:
            seen.add(id(m))
            masters.append(m)
    for master in masters:
        for shape in master.shapes:
            if shape.has_text_frame and "DRAFT" in shape.text_frame.text.upper():  # noqa
                return ["INFO: the master carries a DRAFT FOR DISCUSSION "
                        "banner, so every slide shows it. Correct for a draft. "
                        "For a final version it comes off in the master, never "
                        "covered with a white box"]
    return []


GATES = OrderedDict([
    ("Correct master, no strays", gate_masters),
    ("Closed palette only", gate_palette),
    ("Type scale", gate_type_scale),
    ("Colour carries a key", gate_chart_legend),
    ("Traffic lights have a scale", gate_rag_key),
    ("Exhibit title and basis", gate_exhibit_grammar),
    ("Every exhibit sourced", gate_sources),
    ("UK English", gate_uk_english),
    ("Acronyms", gate_acronyms),
    ("Percentage points", gate_percentage_points),
    ("Telephone format", gate_phone),
    ("Nothing below the line", gate_footprint),
    ("Draft stamp", gate_draft_stamp),
])

MANUAL = [
    "Greyscale flick-through, to catch stray boxes and print problems",
    "Proofing language set to English (United Kingdom) via Review, Language, "
    "Set Proofing Language, Document",
    "Spell check run after the language is set",
    "Contents page filled in and matching the section headings",
    "Copyright year updated in the footer and on the back page",
    "Key issues boxes removed from the appendices",
    "Glossary alphabetical, sentence case, holding every abbreviation used",
]


def report(prs, *, booklet_problems=None, verbose=True):
    """Run every gate. Returns {gate name: [findings]}; empty list is a pass."""
    results = OrderedDict()
    for name, fn in GATES.items():
        try:
            results[name] = fn(prs)
        except Exception as exc:               # a broken gate must not pass
            results[name] = ["gate errored: %r" % (exc,)]
    if booklet_problems is not None:
        results["Charts linked to the booklet"] = list(booklet_problems)

    if verbose:
        width = max(len(k) for k in results) + 2
        print("\n  QA gates")
        for name, findings in results.items():
            info = findings and all(str(f).startswith("INFO") for f in findings)
            status = ("PASS" if not findings
                      else "INFO" if info else "FAIL (%d)" % len(findings))
            print("   %-*s %s" % (width, name, status))
            for f in findings:
                print("      ! %s" % f)
        print("\n  Manual, not automatable, still required before issue:")
        for m in MANUAL:
            print("   - %s" % m)
    return results


# Exhibit furniture: the skill's own grammar rather than the document's prose.
# A basis line states period, units and scope; a KPI basis does the same for a
# headline number; a reference-line label names a hurdle; a panel title names a
# panel. A supplied document almost never contains these ready-made, and
# demanding that "USD billions, FY25" be a verbatim quote from an article is
# not a standard anyone can meet. They are reported separately so they can be
# read by eye, and they still must not assert anything the document does not
# support. Broadened 26 August 2026 from EXHIBIT_BASIS alone, after a finished
# deck's axis labels and unit declarations were being reported as paraphrase.
FURNITURE = ("EXHIBIT_BASIS", "KPI_BASIS", "EXHIBIT_REFLABEL", "EXHIBIT_KEY",
             "PANEL_TITLE", "SHAREBAR_CAP", "DUMBBELL_CAT", "DUMBBELL_VALUE",
             "AXIS_LABEL", "CHART_PARAM")


def _norm_words(s):
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()


def _longest_prefix(words, haystack, start=0):
    """How many words from `start` appear as one contiguous run in the source."""
    lo, hi = 0, len(words) - start
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if " " + " ".join(words[start:start + mid]) + " " in haystack:
            lo = mid
        else:
            hi = mid - 1
    return lo


# How far apart two source runs must be before joining them counts as quoting
# two places rather than deleting words from one sentence. In words.
ELISION_GAP = 12


def _span_cover(words, haystack, min_span):
    """Cover `words` with contiguous source runs, and locate each in the source.

    Returns a list of (length, source_start_word, source_end_word), or None if
    some word cannot begin a run of at least `min_span` words. Greedy is right:
    a longer first run can never force a worse cover, because any later word is
    still free to start its own run.

    The source positions are what let the caller tell a **splice** (two runs
    quoted from different parts of the document, which changes no words) from
    an **elision** (words deleted from the middle of one sentence, which can
    invert its meaning). Added 26 August 2026 after the gate passed "Existing
    payment rails have native concept of delegated machine authority", which is
    the source sentence with "no" removed and says the opposite of it.
    """
    hay_words = haystack.split()
    spans, i = [], 0
    while i < len(words):
        k = _longest_prefix(words, haystack, i)
        if k < min_span:
            return None
        run = words[i:i + k]
        # Every place this run occurs; the caller assumes the worst of them.
        starts = [j for j in range(len(hay_words) - k + 1)
                  if hay_words[j:j + k] == run]
        spans.append((k, starts))
        i += k
    return spans


def _classify_cover(spans):
    """'splice' if the runs come from different places, 'elision' if not.

    Fail-safe: where a run occurs more than once, the arrangement that looks
    most like an elision is the one assumed, because a machine cannot tell a
    harmlessly dropped parenthetical from a dropped negation.
    """
    prev_ends = [j + spans[0][0] for j in spans[0][1]]
    for k, starts in spans[1:]:
        gaps = [s - e for e in prev_ends for s in starts if s >= e]
        if gaps and min(gaps) <= ELISION_GAP:
            return "elision"
        prev_ends = [j + k for j in starts]
    return "splice"


def content_fidelity(prs, allowed_text, *, mode="verbatim", ignore=(),
                     min_chars=12, max_spans=2, min_span=4, verbose=True):
    """Prove the deck says only what the supplied document said.

    Review note, 25 August 2026: the AI must stick to the input content without
    revising it. House note, 26 August 2026, sharpening it: **when a document is
    supplied, use the words in that document word for word and change none of
    them.**

    Two modes, and the difference is the whole point.

    `mode="verbatim"` — **the default, and what a supplied source requires.**
    Every string on a slide must be built from *contiguous runs of words* taken
    from the source. Re-wrapping is fine. Stopping early is fine: "Payment
    infrastructure was built" is a legal shortening of "Payment infrastructure
    was built for humans", because no word changed and none moved. Joining two
    sentences the document wrote is fine, and is reported as a splice so it can
    be seen. What fails is paraphrase, a synonym, a connective the document
    never used, an expanded acronym, and words reassembled into a sentence the
    document never wrote.

    `mode="words"` — the old bag-of-words check: every word must appear
    somewhere in the source, in any order. **Too weak for a supplied document**,
    and kept only for the case where the person asked you to write the content
    and the document is background rather than script. It cannot tell a
    quotation from a collage of the document's own vocabulary.

    `max_spans` and `min_span` set what counts as a splice rather than a
    collage: by default a string may be assembled from at most two source runs
    of at least four words each. `max_spans=1` is the pure form, every string a
    single unbroken quote.

    **Exhibit basis lines are counted separately, not failed.** A basis line
    states period, units and scope, which is this skill's own required grammar
    (`references/exhibits.md`) rather than the document's prose, and a document
    rarely contains one ready-made. They are listed so they can be checked by
    eye, because a basis line still must not assert anything the source does
    not support.

    Returns the genuine failures. Splices and basis lines are reported and not
    returned, so a clean run means nothing was paraphrased.
    """
    haystack = " " + " ".join(_norm_words(allowed_text)) + " "
    haystack_words = set(haystack.split())
    skip = tuple(s.lower() for s in ignore) + (
        "kpmg", "document classification", "draft for discussion",
        "source:", "sources:", "note:", "make the difference")
    if mode not in ("verbatim", "words"):
        raise ValueError("mode is 'verbatim' or 'words', got %r" % mode)

    problems, splices, bases = [], [], []
    checked = 0
    for n, slide in enumerate(prs.slides, 1):
        for shape, t in _iter_text(slide):
            low = t.strip().lower()
            if len(low) < min_chars or any(s in low for s in skip):
                continue
            words = _norm_words(t)
            if not words:
                continue
            checked += 1
            is_basis = (getattr(shape, "name", "") or "").startswith(FURNITURE)
            phrase = " " + " ".join(words) + " "
            if phrase in haystack:
                continue                      # one unbroken quote: always fine

            if mode == "words":
                missing = [w for w in words if w not in haystack_words]
                if missing:
                    problems.append("slide %d: %r introduces %s"
                                    % (n, t[:70], ", ".join(sorted(set(missing))[:6])))
                continue

            cover = _span_cover(words, haystack, min_span)
            if cover is not None and len(cover) <= max_spans:
                kind = _classify_cover(cover)
                lengths = [k for k, _ in cover]
                if kind == "splice":
                    splices.append("slide %d: %r joins %d source runs %s"
                                   % (n, t[:60], len(cover), lengths))
                    continue
                problems.append(
                    "slide %d: %r drops words from the middle of one source "
                    "sentence (runs %s). Deleting mid-sentence can invert the "
                    "meaning, so quote the shorter unbroken run instead"
                    % (n, t[:70], lengths))
                continue

            k = _longest_prefix(words, haystack)
            detail = ("is not in the source at all" if k == 0 else
                      "stops matching after %d word(s), at %r"
                      % (k, " ".join(words[k:k + 4])))
            (bases if is_basis else problems).append(
                "slide %d: %r %s" % (n, t[:70], detail))

    if verbose:
        label = "verbatim spans" if mode == "verbatim" else "vocabulary only"
        print("  content fidelity (%s): %d string(s) checked" % (label, checked))
        if splices:
            print("   %d spliced from source spans, legal but worth an eye:"
                  % len(splices))
            for x in splices[:8]:
                print("     - %s" % x)
            if len(splices) > 8:
                print("     - ... %d more" % (len(splices) - 8))
        if bases:
            print("   %d exhibit furniture string(s) — basis lines, units and "
                  "axis labels, this skill's grammar not the document's "
                  "prose:" % len(bases))
            for x in bases[:6]:
                print("     - %s" % x)
            if len(bases) > 6:
                print("     - ... %d more" % (len(bases) - 6))
        if problems:
            print("   %d NOT traceable to the source:" % len(problems))
            for x in problems:
                print("   ! %s" % x)
        else:
            print("   nothing paraphrased")
    return problems


# ---------------------------------------------------------------------------
# Overlap detection, added 25 August 2026.
#
# House note: "your graphs are overlapping". They were, repeatedly, and I had been
# catching them by eye off a render, which is why they kept coming back. A
# geometric check is not a nicety here, it is the only reliable method.
#
# The rule is not "nothing may overlap". A callout deliberately sits on top of
# its chart. What must never happen is two pieces of TEXT sharing the same
# pixels, or an exhibit crossing into the commentary column.
# ---------------------------------------------------------------------------

EMU_CM = 360000.0


def _rect(shape):
    try:
        if None in (shape.left, shape.top, shape.width, shape.height):
            return None
        return (shape.left / EMU_CM, shape.top / EMU_CM,
                shape.width / EMU_CM, shape.height / EMU_CM)
    except (AttributeError, TypeError):
        return None


def _intersect(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    y = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    return x * y


def _has_visible_text(shape):
    try:
        return shape.has_text_frame and bool(shape.text_frame.text.strip())
    except AttributeError:
        return False


def _is_container(shape):
    """Charts, tables and pictures legitimately have things drawn over them."""
    return (getattr(shape, "has_chart", False)
            or getattr(shape, "has_table", False))


def gate_overlap(prs, tolerance=0.12):
    """Two text shapes must not share the same space.

    `tolerance` is a centimetre slack on each edge, because adjacent boxes that
    merely touch are not a defect.
    """
    out = []
    for n, slide in enumerate(prs.slides, 1):
        items = []
        for shape in slide.shapes:
            r = _rect(shape)
            if r is None:
                continue
            items.append((shape, r, _has_visible_text(shape),
                          _is_container(shape)))
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                sa, ra, ta, ca = items[i]
                sb, rb, tb, cb = items[j]
                if not (ta and tb):
                    continue          # at least one carries no text
                if ca or cb:
                    continue          # a callout over its own chart is intended
                shrunk_a = (ra[0] + tolerance, ra[1] + tolerance,
                            max(ra[2] - 2 * tolerance, 0.01),
                            max(ra[3] - 2 * tolerance, 0.01))
                area = _intersect(shrunk_a, rb)
                smaller = min(ra[2] * ra[3], rb[2] * rb[3]) or 1.0
                if area / smaller > 0.03:
                    out.append(
                        "slide %d: %r overlaps %r by %.0f%% of the smaller "
                        "shape (%.1f cm2)"
                        % (n, sa.name, sb.name, 100 * area / smaller, area))
    return out


def gate_column_bleed(prs, read_left=17.43, tolerance=0.15):
    """Nothing from the left column may cross into the commentary column.

    This is the specific failure that produced a callout printed over a
    paragraph: an annotation positioned off the plot rather than inside it.
    """
    out = []
    for n, slide in enumerate(prs.slides, 1):
        read = [s for s in slide.shapes
                if (s.name or "") in ("COMMENTARY", "HEADER_BAR")
                and (_rect(s) or (0,))[0] >= read_left - 1.0]
        if not read:
            continue
        edge = min((_rect(s)[0] for s in read))
        for shape in slide.shapes:
            r = _rect(shape)
            if r is None or shape in read:
                continue
            name = shape.name or ""
            if not (name.startswith("EXHIBIT_") or _is_container(shape)):
                continue
            # Horizontal extent alone is not a bleed. The source line spans the
            # full page width by design and sits on the strip BELOW the
            # commentary, so it never touches it. Only flag a shape that
            # crosses the column edge AND shares vertical space with the read.
            v_overlap = any(
                min(r[1] + r[3], _rect(t)[1] + _rect(t)[3]) - max(r[1], _rect(t)[1]) > 0.1
                for t in read if _rect(t))
            if (r[0] + r[2] > edge + tolerance and r[0] < edge and v_overlap):
                out.append(
                    "slide %d: %r runs to %.2f cm, past the commentary column "
                    "edge at %.2f cm, at the same height as the read"
                    % (n, name, r[0] + r[2], edge))
    return out


def gate_house_style(prs):
    """The QRG find-and-replace list, applied to every string on every slide.

    Wired into the report on 26 August 2026. `scan_text.py` has carried these
    patterns since the skill was written, but only as a separate command, so a
    build that ran `qa.report()` and nothing else never saw them. On the first
    finished deck it was pointed at afterwards it found a real one: a source
    line reading "FY2019–25", where the QRG wants the FY[xx] form. A check that
    exists but is not in the pass everybody runs is a check that does not exist.

    Structural findings (title length, empty strapline or source, unfilled
    placeholders) stay with `deckkit.check()` rather than being reported twice.
    """
    try:
        from scan_text import HOUSE_STYLE
    except ImportError as exc:
        return ["gate could not load scan_text: %r" % (exc,)]
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for _shape, t in _iter_text(slide):
            for pattern, msg in HOUSE_STYLE:
                if pattern.search(t):
                    out.append("slide %d: %s: %r" % (n, msg, t[:60]))
                    break
    return out


def gate_no_picture_exhibits(prs, max_icon_cm=2.60):
    """An exhibit is a native chart, never a picture of one.

    House note, 26 August 2026: **"images shouldn't be pictures if possible, instead
    excel graph."** The skill has said so in prose since it was written and
    nothing enforced it, which is the same gap that let the house-style list sit
    outside the QA pass.

    A native chart carries an embedded workbook, so the reader can open Edit
    Data, the numbers can be checked, the palette and type scale are inherited,
    and it reflows and prints at any size. A pasted image of a chart has none of
    that: it cannot be checked, it cannot be corrected, and it goes blurry on a
    projector.

    Icons are the legitimate exception and are small, so anything at or below
    `max_icon_cm` on both sides passes. Everything larger has to justify itself:
    a chart is rebuilt with `exhibits.chart_exhibit()`, and a diagram is drawn
    with real shapes, which is how the x402 payment cycle is built.
    """
    out = []
    for n, slide in enumerate(prs.slides, 1):
        lname = (slide.slide_layout.name or "").lower()
        if "cover" in lname or "divider" in lname:
            continue                     # master artwork, not ours
        for shape in slide.shapes:
            if shape.shape_type != MSO_SHAPE_TYPE.PICTURE:
                continue
            try:
                w, h = shape.width / 360000.0, shape.height / 360000.0
            except TypeError:
                continue
            if w <= max_icon_cm and h <= max_icon_cm:
                continue                 # an icon
            out.append(
                "slide %d: %r is a picture %.1f x %.1f cm. An exhibit is a "
                "native chart with its own workbook, not an image of one; a "
                "diagram is drawn with shapes. Rebuild it with "
                "exhibits.chart_exhibit()" % (n, shape.name, w, h))
    return out


GATES["Exhibits are charts, not pictures"] = gate_no_picture_exhibits


GATES["House style, find and replace"] = gate_house_style


GATES["No text overlapping text"] = gate_overlap
GATES["Nothing bleeds into the read column"] = gate_column_bleed


# ---------------------------------------------------------------------------
# Exhibit width discipline, added 25 August 2026.
#
# House note, on a chart drawn 20.40 cm wide from the left margin: "Obviously over
# the middle line and wrong format." That was right, and it had already been said
# once: "graphs should generally be aligned to the left margins and at 13.7cm
# wide situationally... The standard should still be the standard."
#
# A 20.40 cm exhibit at the left margin ends at 23.13 cm and crosses the
# slide's vertical centre at 16.94. The master's column is 13.70 and ends at
# 16.43, stopping short of centre by design. There are exactly two legitimate
# exhibit widths on this master, and anything between them is drift.
# ---------------------------------------------------------------------------

SLIDE_CENTRE = 33.87 / 2.0
LEGAL_WIDTHS = (13.70, 28.40)     # one master column, or the full content width


def gate_exhibit_width(prs, tolerance=0.35):
    """An exhibit is one column wide or full content width. Nothing between.

    Also catches the specific symptom: a left-aligned exhibit whose right edge
    crosses the slide's vertical centre without being full width.
    """
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not (getattr(shape, "has_chart", False)
                    or getattr(shape, "has_table", False)):
                continue
            # One panel of a small-multiples row is not an exhibit in its own
            # right: the row occupies the slot, the panels divide it. Their
            # width is deliberately narrower than a column.
            if "#" in (shape.name or ""):
                continue
            r = _rect(shape)
            if r is None:
                continue
            left, width, right = r[0], r[2], r[0] + r[2]
            if any(abs(width - w) <= tolerance for w in LEGAL_WIDTHS):
                continue
            near = min(LEGAL_WIDTHS, key=lambda w: abs(width - w))
            crosses = (left < SLIDE_CENTRE < right
                       and abs(width - 28.40) > tolerance)
            out.append(
                "slide %d: %r is %.2f cm wide%s. Use %.2f cm, one master "
                "column, or %.2f cm, the full content width"
                % (n, shape.name, width,
                   ", crossing the slide centre line at %.2f" % SLIDE_CENTRE
                   if crosses else "", 13.70, 28.40))
            del near
    return out


GATES["Exhibit width on the grid"] = gate_exhibit_width


def gate_exhibit_slot(prs):
    """Every exhibit occupies a named page slot.

    House note, 25 August 2026: "It either is half page, 1/4 page, full page, or 2
    on 1 page." So an exhibit does not get an arbitrary rectangle. It fills a
    fraction of the content zone taken off the master's own guides, and this
    fails anything placed between them.

    This supersedes the width-only check: a slot constrains height and vertical
    position too, which is what stops two stacked exhibits sitting at 5.03 and
    11.05 instead of on the half-height line at 10.13.
    """
    from exhibits import in_slot
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not (getattr(shape, "has_chart", False)
                    or getattr(shape, "has_table", False)):
                continue
            # One panel of a small-multiples row is not an exhibit in its own
            # right: the row occupies the slot, the panels divide it. Their
            # width is deliberately narrower than a column.
            if "#" in (shape.name or ""):
                continue
            r = _rect(shape)
            if r is None:
                continue
            if in_slot(r) is None:
                out.append(
                    "slide %d: %r at %.2f, %.2f cm, %.2f x %.2f cm is not in a "
                    "page slot. Use slot= with full, half_top, half_bottom, "
                    "half_left, half_right or a quarter"
                    % (n, shape.name, r[0], r[1], r[2], r[3]))
    return out


GATES["Exhibit fills a page slot"] = gate_exhibit_slot


def gate_text_overflow(prs, tolerance=0.12):
    """Text must fit the box it is drawn in.

    Added 25 August 2026 after a wrapped exhibit title printed its second line
    over its own basis line. The geometric overlap gate could not see it: the
    shape rectangles did not overlap, the TEXT overflowed its rectangle and
    printed on top of whatever sat beneath. Estimating the wrap is the only way
    to catch this class, and it is the same class as the table-height problem.
    """
    from exhibits import est_text_height
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not (shape.has_text_frame and shape.text_frame.text.strip()):
                continue
            if getattr(shape, "has_chart", False) or getattr(shape, "has_table", False):
                continue
            r = _rect(shape)
            if r is None or r[2] <= 0 or r[3] <= 0:
                continue
            try:
                runs = [rn for p in shape.text_frame.paragraphs for rn in p.runs]
                if not runs:
                    continue
                size = runs[0].font.size
                bold = bool(runs[0].font.bold)
            except (AttributeError, IndexError):
                continue
            if size is None:
                continue          # inherited from the master; not ours to judge
            needed = 0.0
            for p in shape.text_frame.paragraphs:
                t = "".join(rn.text for rn in p.runs)
                if t.strip():
                    needed += est_text_height(t, r[2], size.pt, bold)
            if needed > r[3] + tolerance:
                out.append(
                    "slide %d: %r holds %.2f cm of text in a %.2f cm box, so it "
                    "prints outside and over whatever is beneath: %r"
                    % (n, shape.name, needed, r[3],
                       shape.text_frame.text.strip()[:60]))
    return out


GATES["Text fits its box"] = gate_text_overflow


def gate_exhibit_title_length(prs):
    """An exhibit title is one line at the width it is drawn.

    A wrapped title is not just heavy to read, it pushes the plot down and eats
    the slot's budget. The finding still has to be a sentence, so the fix is a
    shorter sentence, not a smaller font.
    """
    from exhibits import est_lines, EXHIBIT_TITLE_PT
    out = []
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if (shape.name or "") != "EXHIBIT_TITLE":
                continue
            r = _rect(shape)
            if r is None:
                continue
            text = shape.text_frame.text.strip()
            lines = est_lines(text, r[2], EXHIBIT_TITLE_PT, bold=True)
            if lines > 1:
                per_line = int(r[2] / (0.530 * EXHIBIT_TITLE_PT * 2.54 / 72.0))
                out.append(
                    "slide %d: exhibit title wraps to %d lines at %.2f cm. "
                    "Budget is about %d characters, this is %d: %r"
                    % (n, lines, r[2], per_line, len(text), text[:70]))
    return out


GATES["Exhibit title fits one line"] = gate_exhibit_title_length
