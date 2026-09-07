"""Write the data booklet that every chart in the deck traces back to.

House instruction, 25 August 2026: **all graphs created should link to the
accompanying databooklet.** So the booklet is not an optional companion, it is
the source of record, and `check_booklet()` fails a deck that draws a chart
from a number the booklet does not hold.

Every exhibit built through `exhibits.py` registers its numbers as it is drawn,
so the booklet is written FROM the deck rather than maintained beside it. That
removes the failure mode where the two drift apart.

Cell colours follow the house data standard:
    yellow  input          green  formula
    blue    primary source purple secondary / market source
    orange  caveat or open item
"""
import os
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import exhibits

FILL = {
    "input":     PatternFill("solid", fgColor="FFF2CC"),
    "formula":   PatternFill("solid", fgColor="E2EFDA"),
    "primary":   PatternFill("solid", fgColor="DDEBF7"),
    "secondary": PatternFill("solid", fgColor="E4D9F2"),
    "caveat":    PatternFill("solid", fgColor="FCE4D6"),
}
HEADER_FILL = PatternFill("solid", fgColor="0C233C")
HEADER_FONT = Font(name="Arial", size=9, bold=True, color="FFFFFF")
BODY_FONT = Font(name="Arial", size=9)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# A source string that names a document, an issuer or a database is primary.
# One that says "estimate", "analysis" or "illustrative" is not, and the
# booklet has to say so rather than presenting it as measured.
_SECONDARY = re.compile(r"estimat|analysis|illustrat|assum|indicative|model",
                        re.I)


def classify(source):
    if not source:
        return "caveat"
    return "secondary" if _SECONDARY.search(source) else "primary"


def _sheet(wb, name, headers, widths):
    ws = wb.create_sheet(name) if wb.sheetnames != ["Sheet"] else wb.active
    ws.title = name
    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="bottom", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = "A2"
    return ws


def write(path, *, deck_name=None, notes=None, registry=None):
    """Write the booklet. Returns (path, chart_count, row_count)."""
    reg = exhibits.REGISTRY if registry is None else registry
    wb = Workbook()

    idx = _sheet(wb, "Index",
                 ["Chart_ID", "Slide", "Kind", "Exhibit title", "Basis",
                  "Units", "Source", "Source type"],
                 [26, 7, 14, 46, 46, 14, 60, 13])
    for r, ex in enumerate(reg, start=2):
        kind_of_source = classify(ex["Source"])
        values = [ex["Chart_ID"], ex["Slide"], ex["Kind"], ex["Title"],
                  ex["Basis"], ex["Units"], ex["Source"], kind_of_source]
        for c, v in enumerate(values, 1):
            cell = idx.cell(row=r, column=c, value=v)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=c in (4, 5, 7))
            if c == 7:
                cell.fill = FILL[kind_of_source]

    data = _sheet(wb, "Chart_Data",
                  ["Chart_ID", "Series", "Category", "Value", "Units",
                   "Source"],
                  [26, 34, 30, 14, 14, 60])
    r = 2
    for ex in reg:
        for row in ex["Rows"]:
            values = [row["Chart_ID"], row["Series"], row["Category"],
                      row["Value"], row["Units"], row["Source"]]
            for c, v in enumerate(values, 1):
                cell = data.cell(row=r, column=c, value=v)
                cell.font = BODY_FONT
                cell.border = BORDER
                if c == 4:
                    cell.fill = FILL["input"]
                    cell.alignment = Alignment(horizontal="right")
                elif c == 6:
                    cell.fill = FILL[classify(row["Source"])]
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
            r += 1
    row_count = r - 2

    key = _sheet(wb, "Read me", ["Item", "Meaning"], [34, 88])
    lines = [
        ("Deck", deck_name or os.path.basename(path)),
        ("Chart_ID", "Matches the shape name EXHIBIT::<Chart_ID> on the slide. "
                     "Every chart in the deck appears here; a chart that does "
                     "not is a build error, not an omission."),
        ("Basis", "Period, units, scope, and which axis carries what. An "
                  "exhibit with no basis is a chart the reader cannot check."),
        ("Yellow cell", "Input. A number typed in, not derived."),
        ("Green cell", "Formula. Derived from other cells in this booklet."),
        ("Blue cell", "Primary source: a filing, an issuer statement, a named "
                      "database."),
        ("Purple cell", "Secondary or market source, an estimate, or an "
                        "illustrative model. Not measured data."),
        ("Orange cell", "Caveat or open item. Unsourced, and must be resolved "
                        "before the deck goes anywhere."),
    ]
    for i, (k, v) in enumerate(lines + list(notes or []), start=2):
        for c, val in enumerate((k, v), 1):
            cell = key.cell(row=i, column=c, value=val)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
    wb.save(path)
    return path, len(reg), row_count


def check_booklet(prs, registry=None, verbose=True):
    """Every chart on every slide must trace to a booklet entry.

    Catches the two ways the link breaks: a chart drawn with raw
    `deckkit.chart()` so it never registered, and a registry entry whose
    exhibit was removed from the deck.
    """
    reg = exhibits.REGISTRY if registry is None else registry
    known = {ex["Chart_ID"] for ex in reg}
    problems, seen = [], set()

    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            is_chart = getattr(shape, "has_chart", False)
            if not is_chart:
                continue
            name = shape.name or ""
            if not name.startswith("EXHIBIT::"):
                problems.append(
                    "slide %d: chart %r is not linked to the data booklet. "
                    "Build it with exhibits.chart_exhibit() rather than "
                    "deckkit.chart(), so its numbers register." % (n, name))
                continue
            cid = name.split("::", 1)[1].split("#", 1)[0]
            seen.add(cid)
            if cid not in known:
                problems.append(
                    "slide %d: chart id %r has no booklet entry" % (n, cid))

    for ex in reg:
        if ex["Kind"] in ("dumbbell", "small_multiples"):
            continue
        if ex["Chart_ID"] not in seen:
            problems.append(
                "booklet holds %r but no chart on any slide carries it; the "
                "exhibit was removed or rebuilt" % ex["Chart_ID"])
    for ex in reg:
        if not ex["Source"]:
            problems.append("booklet entry %r has no source" % ex["Chart_ID"])
        if not ex["Basis"]:
            problems.append("booklet entry %r has no basis line" % ex["Chart_ID"])

    if verbose:
        for p in problems:
            print("  !", p)
        if not problems:
            print("  booklet: clean (%d exhibits linked)" % len(reg))
    return problems
