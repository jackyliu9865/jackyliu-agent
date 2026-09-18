#!/usr/bin/env python3
"""Build (or roll forward) the KICS check databook.

Usage:
    python scripts/build_databook.py input.json [-o out.xlsx] [--no-recalc]

Reads the same input.json as reconcile.py. If input.json names a `prior_databook`, that file
is copied and the previous period's tabs are pushed below the `Archive>>` divider, so one
workbook carries every period ever checked.

Tab layout produced (newest first):
    Summary @ <as_of>
    KICS list @ <current label>      <- current export, drives every conclusion
    KICS list @ <previous label>      <- superseded export, kept for the audit trail
    Holding @ <as_of>
    Txn <from>-<to>
    Archive>>
    ... prior periods, untouched ...
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reconcile import kics_tickers, norm, reconcile  # noqa: E402

FONT = "Arial"
H_FONT = Font(name=FONT, bold=True, size=10, color="FFFFFF")
H_FILL = PatternFill("solid", fgColor="4F5B66")
BODY = Font(name=FONT, size=10)
BLUE = Font(name=FONT, size=10, color="0000FF")       # keyed from a source document
GREY = Font(name=FONT, size=10, color="808080")
NOTE = Font(name=FONT, size=9, italic=True, color="595959")
TITLE = Font(name=FONT, bold=True, size=13)
SUB = Font(name=FONT, bold=True, size=11)
BOLD = Font(name=FONT, size=10, bold=True)
THIN = Side(style="thin", color="BFBFBF")
BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
AMBER = PatternFill("solid", fgColor="FFF2CC")
RED_FILL = PatternFill("solid", fgColor="FFC7CE")
RED_FONT = Font(name=FONT, size=10, color="9C0006", bold=True)
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")
GREY_FILL = PatternFill("solid", fgColor="EDEDED")


def compact(d: str) -> str:
    return (d or "").replace("-", "").replace("/", "")


def header(ws, row, labels, start_col=1):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font, c.fill, c.border = H_FONT, H_FILL, BD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def flag_rules(ws, rng):
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=["0"],
                                                  fill=RED_FILL, font=RED_FONT))
    ws.conditional_formatting.add(rng, CellIsRule(operator="greaterThanOrEqual", formula=["1"],
                                                  fill=GREEN_FILL))


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


def build(data: dict, out_path: Path, recalc: bool = True) -> dict:
    res = reconcile(data)
    profile = data.get("profile") or ""
    as_of = data["as_of"]
    snaps = data["kics_snapshots"]
    current, previous = snaps[-1], (snaps[-2] if len(snaps) > 1 else None)

    PM = f"KICS list @ {current['label']}"[:31]
    AM = f"KICS list @ {previous['label']}"[:31] if previous else None
    HOLD = f"Holding @ {compact(as_of)}"[:31]
    TXN = f"Txn {compact(data.get('period_from'))}-{compact(as_of)}"[:31]
    SUMM = f"Summary @ {compact(as_of)}"[:31]

    prior = data.get("prior_databook")
    if prior and Path(prior).exists():
        shutil.copy(prior, out_path)
        wb = load_workbook(out_path)
        for name in (SUMM, PM, AM, HOLD, TXN):
            if name and name in wb.sheetnames:
                del wb[name]
    else:
        wb = Workbook()
        wb.remove(wb.active)
    if "Archive>>" not in wb.sheetnames:
        wb.create_sheet("Archive>>")

    holdings = data.get("holdings") or []
    txns = data.get("transactions") or []
    uniq = []
    for t in txns:
        if norm(t["ticker"]) not in uniq:
            uniq.append(norm(t["ticker"]))
    by_ticker = {l["ticker"]: l for l in res["lines"]}

    # ---------------------------------------------------------------- KICS current
    ws = wb.create_sheet(PM)
    ws["A1"] = f"KICS platform holdings list @ {current['label']}  —  CURRENT"
    ws["A1"].font = TITLE
    ws["A2"] = (f"Source: {current.get('source','(source document)')}"
                + (f", printed {current['printed']}" if current.get("printed") else "")
                + (f". Export covers more than one profile; only the {profile} lines are in scope."
                   if any(r.get("profile") and r["profile"] != profile for r in current["rows"]) else "."))
    ws["A2"].font = NOTE
    header(ws, 4, ["ID (Text)", "Profile", "Check is in Holding?", "Check is in Txn?",
                   "Name (per KICS)", "Entry type", "Acquisition date", "Status(es)"], start_col=2)
    for i, r in enumerate(current["rows"]):
        row = 5 + i
        in_scope = not r.get("profile") or r["profile"] == profile
        c = ws.cell(row=row, column=2, value=norm(r["id"]))
        c.number_format, c.font = "@", BLUE
        ws.cell(row=row, column=3, value=r.get("profile", profile)).font = BLUE
        if in_scope:
            ws.cell(row=row, column=4, value=f"=COUNTIF('{HOLD}'!$B:$B,$B{row})")
            ws.cell(row=row, column=5, value=f"=COUNTIF('{TXN}'!$E:$E,$B{row})")
        else:
            for col in (4, 5):
                ws.cell(row=row, column=col, value="n/a").font = GREY
        ws.cell(row=row, column=6, value=r.get("name", "")).font = BLUE
        ws.cell(row=row, column=7, value=r.get("entry_type", "")).font = BLUE
        ws.cell(row=row, column=8, value=r.get("acquired", "")).font = BLUE
        ws.cell(row=row, column=9, value=r.get("status", "")).font = BLUE
    pm_last = 4 + len(current["rows"])
    for row in ws.iter_rows(min_row=5, max_row=pm_last, min_col=2, max_col=9):
        for c in row:
            c.border = BD
            if c.font.color is None or c.font.color.rgb not in ("000000FF", "00808080"):
                c.font = BODY
            c.alignment = Alignment(horizontal="left" if c.column == 6 else "center")
    for i, r in enumerate(current["rows"]):
        if r.get("profile") and r["profile"] != profile:
            for col in range(2, 10):
                ws.cell(row=5 + i, column=col).fill = GREY_FILL
    flag_rules(ws, f"D5:E{pm_last}")
    ws.cell(row=pm_last + 2, column=2, value=(
        "Grey rows belong to another profile and are excluded from the matching. A zero on an in-scope "
        "line means the position is not held at the cut-off date and was not traded in the period — "
        "over-declaration, not a breach; see the Summary tab for the proposed tidy-up.")).font = NOTE
    widths(ws, {"A": 2, "B": 13, "C": 12, "D": 18, "E": 16, "F": 62, "G": 11, "H": 15, "I": 13})
    ws.freeze_panes = "B5"

    # ---------------------------------------------------------------- KICS superseded
    if previous:
        ws = wb.create_sheet(AM)
        ws["A1"] = f"KICS platform holdings list @ {previous['label']}  —  SUPERSEDED"
        ws["A1"].font = TITLE
        ws["A2"] = (f"Source: {previous.get('source','(source document)')}. Kept as the evidence base for the "
                    f"exceptions first raised; superseded by the {current['label']} export on the CURRENT tab.")
        ws["A2"].font = NOTE
        header(ws, 4, ["ID (Text)", "Profile", f"Still on KICS @ {current['label']}?",
                       "Name (per KICS)", "Acquisition date", "Status(es)"], start_col=2)
        for i, r in enumerate(previous["rows"]):
            row = 5 + i
            c = ws.cell(row=row, column=2, value=norm(r["id"]))
            c.number_format = "@"
            c.font = BLUE
            ws.cell(row=row, column=3, value=r.get("profile", profile)).font = BLUE
            ws.cell(row=row, column=4, value=f"=COUNTIF('{PM}'!$B:$B,$B{row})")
            ws.cell(row=row, column=5, value=r.get("name", "")).font = BLUE
            ws.cell(row=row, column=6, value=r.get("acquired", "")).font = BLUE
            ws.cell(row=row, column=7, value=r.get("status", "")).font = BLUE
        am_last = 4 + len(previous["rows"])
        for row in ws.iter_rows(min_row=5, max_row=am_last, min_col=2, max_col=7):
            for c in row:
                c.border = BD
                if c.font.color is None or c.font.color.rgb != "000000FF":
                    c.font = BODY
                c.alignment = Alignment(horizontal="left" if c.column == 5 else "center")
        ws.conditional_formatting.add(f"D5:D{am_last}", CellIsRule(operator="equal", formula=["0"], fill=AMBER))
        ws.cell(row=am_last + 2, column=2, value=(
            "Amber = the line was removed between the two exports. Check each removal against the Summary tab: "
            "a removal that was asked for is fine, an unrequested one is not.")).font = NOTE
        widths(ws, {"A": 2, "B": 13, "C": 12, "D": 24, "E": 62, "F": 15, "G": 13})
        ws.freeze_panes = "B5"

    # ---------------------------------------------------------------- Holdings
    ws = wb.create_sheet(HOLD)
    ws["A1"] = f"Holdings @ {as_of} — checked to KICS"
    ws["A1"].font = TITLE
    ws["A2"] = f"Source: {data.get('holdings_source','(holding statement)')}."
    ws["A2"].font = NOTE
    cols = ["Holding (Num)", "Holding (Text)", "Name", "Check is in Txn?",
            f"On KICS @ {previous['label']}" if previous else "On KICS (prior)",
            f"On KICS @ {current['label']}", "Units", "NAV", "Value", "Conclusion"]
    header(ws, 4, cols)
    for i, h in enumerate(holdings):
        row = 5 + i
        t = norm(h["ticker"])
        if t.isdigit():
            ws.cell(row=row, column=1, value=int(t)).font = BLUE
            ws.cell(row=row, column=2, value=f'=TEXT(A{row},"000000")')
        else:
            ws.cell(row=row, column=1, value=t).font = BLUE
            ws.cell(row=row, column=2, value=f"=A{row}")
        ws.cell(row=row, column=3, value=h.get("name", "")).font = BLUE
        ws.cell(row=row, column=4, value=f"=COUNTIF('{TXN}'!$E:$E,$B{row})")
        ws.cell(row=row, column=5,
                value=(f"=COUNTIF('{AM}'!$B:$B,$B{row})" if previous else "n/a"))
        if not previous:
            ws.cell(row=row, column=5).font = GREY
        ws.cell(row=row, column=6,
                value=f"=COUNTIFS('{PM}'!$B:$B,$B{row},'{PM}'!$C:$C,\"{profile}\")")
        ws.cell(row=row, column=7, value=h.get("units")).font = BLUE
        ws.cell(row=row, column=8, value=h.get("nav")).font = BLUE
        ws.cell(row=row, column=9, value=h.get("value")).font = BLUE
        # Round 1 has no prior export, so "newly added" cannot be derived.
        ws.cell(row=row, column=10, value=(
            f'=IF(F{row}=0,"ADD TO KICS",IF(E{row}=0,"Now declared (newly added)","OK"))' if previous
            else f'=IF(F{row}=0,"ADD TO KICS","OK")'))
    hold_last = 4 + len(holdings)
    ws.cell(row=hold_last + 1, column=3, value="Total").font = BOLD
    tot = ws.cell(row=hold_last + 1, column=9, value=f"=SUM(I5:I{hold_last})")
    tot.font, tot.number_format = BOLD, "#,##0.00"
    ws.cell(row=hold_last + 1, column=10,
            value=f'=COUNTIF(J5:J{hold_last},"ADD TO KICS")&" exception(s)"').font = BOLD
    for row in ws.iter_rows(min_row=5, max_row=hold_last, min_col=1, max_col=10):
        for c in row:
            c.border = BD
            if c.font.color is None or c.font.color.rgb not in ("000000FF", "00808080"):
                c.font = BODY
            if c.column in (1, 2, 4, 5, 6, 10):
                c.alignment = Alignment(horizontal="center")
            if c.column in (7, 9):
                c.number_format = "#,##0.00"
            if c.column == 8:
                c.number_format = "0.0000"
    flag_rules(ws, f"D5:F{hold_last}")
    ws.conditional_formatting.add(f"J5:J{hold_last}", CellIsRule(
        operator="equal", formula=['"ADD TO KICS"'], fill=RED_FILL, font=RED_FONT))
    ws.conditional_formatting.add(f"J5:J{hold_last}", CellIsRule(
        operator="equal", formula=['"Now declared (newly added)"'], fill=GREEN_FILL))
    ws.cell(row=hold_last + 3, column=1, value=(
        "\"Check is in Txn?\" = 0 means the position was not traded in the period — expected for long-held "
        "positions, never an exception. The CURRENT KICS column decides the conclusion; the superseded column "
        "is kept to show the movement between exports.")).font = NOTE
    widths(ws, {"A": 12, "B": 16, "C": 38, "D": 15, "E": 19, "F": 19, "G": 12, "H": 10, "I": 13, "J": 26})
    ws.freeze_panes = "A5"

    # ---------------------------------------------------------------- Transactions
    ws = wb.create_sheet(TXN)
    ws["A1"] = f"Transactions {data.get('period_from')} – {as_of} — checked to KICS"
    ws["A1"].font = TITLE
    ws["A2"] = (f"Source: {data.get('transactions_source','(transaction statement)')}. Column E de-duplicates "
                "column C outside Excel, so the unique list does not depend on a spill formula.")
    ws["A2"].font = NOTE
    header(ws, 4, ["Txn date", "Txn List", "Txn to Text", "Txn type"], start_col=1)
    header(ws, 4, ["Unique Ticker", "Fund name", "Is in Holding?",
                   f"On KICS @ {previous['label']}" if previous else "On KICS (prior)",
                   f"On KICS @ {current['label']}", "Conclusion"], start_col=5)
    for i, t in enumerate(txns):
        row = 5 + i
        n = norm(t["ticker"])
        ws.cell(row=row, column=1, value=t.get("date", "")).font = BLUE
        if n.isdigit():
            ws.cell(row=row, column=2, value=int(n)).font = BLUE
            ws.cell(row=row, column=3, value=f'=IF(ISBLANK(B{row})=FALSE,TEXT(B{row},"000000"),"")')
        else:
            ws.cell(row=row, column=2, value=n).font = BLUE
            ws.cell(row=row, column=3, value=f"=B{row}")
        ws.cell(row=row, column=4, value=t.get("type", "")).font = BLUE
    for i, t in enumerate(uniq):
        row = 5 + i
        c = ws.cell(row=row, column=5, value=t)
        c.number_format = "@"
        ws.cell(row=row, column=6, value=by_ticker.get(t, {}).get("name", ""))
        ws.cell(row=row, column=7, value=f"=COUNTIF('{HOLD}'!$B:$B,$E{row})")
        ws.cell(row=row, column=8, value=(f"=COUNTIF('{AM}'!$B:$B,$E{row})" if previous else "n/a"))
        ws.cell(row=row, column=9,
                value=f"=COUNTIFS('{PM}'!$B:$B,$E{row},'{PM}'!$C:$C,\"{profile}\")")
        # Round 1 has no prior export, so "disposed, de-registered" cannot be derived.
        ws.cell(row=row, column=10, value=(
            f'=IF(I{row}>0,"OK",IF(G{row}>0,"ADD TO KICS",'
            f'IF(H{row}>0,"Disposed in period, de-registered","ADD TO KICS — traded, never declared")))'
            if previous else
            f'=IF(I{row}>0,"OK",IF(G{row}>0,"ADD TO KICS","ADD TO KICS — traded, never declared"))'))
    txn_last, uniq_last = 4 + len(txns), 4 + len(uniq)
    for row in ws.iter_rows(min_row=5, max_row=txn_last, min_col=1, max_col=4):
        for c in row:
            c.border = BD
            if c.font.color is None or c.font.color.rgb != "000000FF":
                c.font = BODY
            c.alignment = Alignment(horizontal="center" if c.column != 4 else "left")
    for row in ws.iter_rows(min_row=5, max_row=uniq_last, min_col=5, max_col=10):
        for c in row:
            c.border = BD
            c.font = GREY if c.value == "n/a" else BODY
            c.alignment = Alignment(horizontal="left" if c.column == 6 else "center")
    flag_rules(ws, f"G5:I{uniq_last}")
    for txt in ('"ADD TO KICS"', '"ADD TO KICS — traded, never declared"'):
        ws.conditional_formatting.add(f"J5:J{uniq_last}", CellIsRule(
            operator="equal", formula=[txt], fill=RED_FILL, font=RED_FONT))
    ws.conditional_formatting.add(f"J5:J{uniq_last}", CellIsRule(
        operator="equal", formula=['"Disposed in period, de-registered"'], fill=AMBER))
    ws.cell(row=txn_last + 2, column=1, value=(
        f"{len(txns)} transactions in the period; {len(uniq)} distinct tickers after de-duplication.")).font = NOTE
    widths(ws, {"A": 12, "B": 11, "C": 12, "D": 12, "E": 13, "F": 38, "G": 16, "H": 19, "I": 19, "J": 34})
    ws.freeze_panes = "A5"

    # ---------------------------------------------------------------- Summary
    ws = wb.create_sheet(SUMM)
    ws["A1"] = f"Personal investment declaration check — {as_of}"
    ws["A1"].font = TITLE
    ws["A2"] = f"{profile} — brokerage account vs KICS declared holdings"
    ws["A2"].font = Font(name=FONT, size=10, italic=True)

    ws["A4"] = "Conclusion"
    ws["A4"].font = SUB
    if res["clear"]:
        verdict = (f"Cleared. All {res['counts']['holdings']} holdings at {as_of} and all "
                   f"{res['counts']['traded_tickers']} tickers traded in the period are declared on the "
                   f"{current['label']} KICS export. No exceptions.")
    else:
        verdict = (f"{len(res['exceptions'])} exception(s) to clear. See the action list below; each one is also "
                   f"flagged red on the Holding and Txn tabs.")
    ws["A5"] = verdict
    ws["A5"].font = BODY
    ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A5:F6")
    ws["A5"].fill = GREEN_FILL if res["clear"] else RED_FILL

    ws["A8"] = "Sources"
    ws["A8"].font = SUB
    header(ws, 9, ["Population", "Source document", "As at / period", "Lines"])
    src = [("KICS list — current", current.get("source", ""), current["label"],
            f"{res['counts']['kics_current']} in scope / {res['counts']['kics_rows_total']} total")]
    if previous:
        src.append(("KICS list — superseded", previous.get("source", ""), previous["label"],
                    len(previous["rows"])))
    src += [
        ("Holding", data.get("holdings_source", ""), as_of, res["counts"]["holdings"]),
        ("Txn (raw / unique)", data.get("transactions_source", ""),
         f"{data.get('period_from')} – {as_of}",
         f"{res['counts']['transactions']} / {res['counts']['traded_tickers']}"),
    ]
    for i, row in enumerate(src):
        for j, v in enumerate(row):
            c = ws.cell(row=10 + i, column=1 + j, value=v)
            c.font, c.border = BODY, BD
            c.alignment = Alignment(horizontal="center" if j == 3 else "left", wrap_text=True)
    r = 10 + len(src) + 1

    ws.cell(row=r, column=1, value="Action list — what to change on KICS").font = SUB
    header(ws, r + 1, ["Action", "Ticker", "Name", "Value", "Why"])
    rr = r + 2
    actions = ([("ADD", l) for l in res["to_add"]] + [("REMOVE?", l) for l in res["to_remove"]])
    if not actions:
        c = ws.cell(row=rr, column=1, value="No changes required — KICS agrees with the account.")
        c.font, c.border, c.fill = BODY, BD, GREEN_FILL
        ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=5)
        rr += 1
    else:
        for act, l in actions:
            ws.cell(row=rr, column=1, value=act)
            ws.cell(row=rr, column=2, value=l["ticker"]).number_format = "@"
            ws.cell(row=rr, column=3, value=l["name"])
            ws.cell(row=rr, column=4, value=l.get("value"))
            ws.cell(row=rr, column=5, value=l["why"])
            for col in range(1, 6):
                c = ws.cell(row=rr, column=col)
                c.font, c.border = BODY, BD
                c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(row=rr, column=4).number_format = "#,##0.00"
            fill = RED_FILL if act == "ADD" else AMBER
            ws.cell(row=rr, column=1).fill = fill
            ws.row_dimensions[rr].height = 34
            rr += 1
    rr += 1

    if res.get("movement"):
        m = res["movement"]
        ws.cell(row=rr, column=1, value=f"Movement since the {previous['label']} export").font = SUB
        rr += 1
        header(ws, rr, ["Change", "Tickers", "Requested?"])
        rr += 1
        rows = [
            ("Added", ", ".join(m["added"]) or "none",
             "yes" if not (set(m["added"]) - set(m["expected_add_done"])) else "CHECK — includes unrequested lines"),
            ("Removed", ", ".join(m["removed"]) or "none",
             "yes" if not (set(m["removed"]) - set(m["expected_remove_done"])) else "CHECK — includes unrequested lines"),
            ("Still outstanding", ", ".join(m["expected_add_missing"] + m["expected_remove_outstanding"]) or "none",
             "—"),
        ]
        for row in rows:
            for j, v in enumerate(row):
                c = ws.cell(row=rr, column=1 + j, value=v)
                c.font, c.border = BODY, BD
                c.alignment = Alignment(wrap_text=True, vertical="top")
            if row[0] != "Still outstanding" and row[2].startswith("CHECK"):
                ws.cell(row=rr, column=3).fill = AMBER
            if row[0] == "Still outstanding" and row[1] != "none":
                ws.cell(row=rr, column=2).fill = RED_FILL
            rr += 1
        rr += 1

    ws.cell(row=rr, column=1, value="Check totals (live formulas)").font = SUB
    rr += 1
    checks = [
        ("Holdings not on KICS", f'=COUNTIF(\'{HOLD}\'!$J:$J,"ADD TO KICS")&" of {len(holdings)} holdings"'),
        ("Traded tickers not on KICS",
         f'=COUNTIF(\'{TXN}\'!$J:$J,"ADD TO KICS")+COUNTIF(\'{TXN}\'!$J:$J,"ADD TO KICS — traded, never declared")'
         f'&" of {len(uniq)} traded tickers"'),
        ("Newly declared since last export",
         f'=COUNTIF(\'{HOLD}\'!$J:$J,"Now declared (newly added)")&" holding(s)"'),
    ]
    for lab, f in checks:
        ws.cell(row=rr, column=1, value=lab).font = BODY
        c = ws.cell(row=rr, column=2, value=f)
        c.font, c.fill = BODY, AMBER
        rr += 1
    rr += 1
    ws.cell(row=rr, column=1, value=(
        "Legend: blue text = keyed from a source document · black = formula · red = exception · "
        "amber = explained difference or proposed tidy-up · grey = out of scope.")).font = NOTE
    widths(ws, {"A": 26, "B": 30, "C": 40, "D": 14, "E": 60, "F": 20})

    # ---------------------------------------------------------------- order & save
    order = [SUMM, PM] + ([AM] if AM else []) + [HOLD, TXN, "Archive>>"]
    wb._sheets = [wb[n] for n in order if n in wb.sheetnames] + \
                 [s for s in wb._sheets if s.title not in order]
    wb.save(out_path)

    if recalc:
        recalculate(out_path)
    return res


def recalculate(path: Path) -> None:
    """openpyxl writes formulas with no cached value; LibreOffice fills them in.

    Without this, anything that reads cached values (pandas, a previewer, a phone) sees blanks.
    Silently skipped if soffice is not installed — Excel will calculate on open.
    """
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        print("note: soffice not found, skipping recalculation (Excel will calculate on open)")
        return
    out_dir = path.parent / "_recalc"
    out_dir.mkdir(exist_ok=True)
    subprocess.run([exe, "--headless", "--convert-to", "xlsx", "--outdir", str(out_dir), str(path)],
                   check=True, capture_output=True, timeout=180)
    produced = out_dir / path.name
    if produced.exists():
        shutil.move(str(produced), str(path))
    shutil.rmtree(out_dir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--no-recalc", action="store_true")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out = Path(args.output or data.get("databook_out") or "Investment_check.xlsx")
    res = build(data, out, recalc=not args.no_recalc)
    print(json.dumps({
        "databook": str(out),
        "clear": res["clear"],
        "add": [l["ticker"] for l in res["to_add"]],
        "remove": [l["ticker"] for l in res["to_remove"]],
        "movement": res.get("movement"),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
