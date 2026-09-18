#!/usr/bin/env python3
"""Reconcile a brokerage holding/transaction extract against a KICS export.

Usage:
    python scripts/reconcile.py input.json                 # print result as JSON
    python scripts/reconcile.py input.json --save-state    # also write state/last_check.json

The input schema is documented in assets/input_template.json and references/conventions.md.
This module is pure logic: no Excel, no I/O beyond reading the input and writing state.
build_databook.py imports `reconcile()` from here, so the numbers on the spreadsheet and the
numbers in the chat answer can never disagree.
"""

import json
import sys
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent.parent / "state" / "last_check.json"


# --------------------------------------------------------------------------- helpers
def norm(ticker) -> str:
    """Normalise an identifier for matching.

    Numeric codes are zero-padded to 6 digits ('217' -> '000217') because Excel, PDFs and
    fund platforms disagree about leading zeros. Anything with a letter in it (HK0194,
    ISINs) is upper-cased and left alone.
    """
    s = str(ticker).strip().replace(" ", "")
    if s.isdigit():
        return s.zfill(6)
    return s.upper()


def _rows(data, key):
    return data.get(key) or []


def kics_tickers(snapshot, profile):
    """Tickers on one KICS snapshot belonging to `profile`.

    Rows with no profile field are treated as in scope: single-profile exports do not
    carry the column. Rows naming a different person are out of scope.
    """
    out = {}
    for r in snapshot.get("rows", []):
        p = (r.get("profile") or profile or "").strip()
        if profile and p and p != profile:
            continue
        out[norm(r["id"])] = r
    return out


# --------------------------------------------------------------------------- main logic
def reconcile(data: dict) -> dict:
    profile = data.get("profile") or ""
    snaps = data.get("kics_snapshots") or []
    if not snaps:
        raise SystemExit("input needs at least one entry in kics_snapshots")

    current = snaps[-1]
    previous = snaps[-2] if len(snaps) > 1 else None

    cur = kics_tickers(current, profile)
    prev = kics_tickers(previous, profile) if previous else {}
    ever = set(cur)
    for s in snaps:
        ever |= set(kics_tickers(s, profile))

    holdings = _rows(data, "holdings")
    held = {}
    for h in holdings:
        held[norm(h["ticker"])] = h

    txns = _rows(data, "transactions")
    traded = []
    for t in txns:
        n = norm(t["ticker"])
        if n not in traded:
            traded.append(n)

    names = {}
    for h in holdings:
        names.setdefault(norm(h["ticker"]), h.get("name", ""))
    for t in txns:
        names.setdefault(norm(t["ticker"]), t.get("name", ""))
    for t, r in cur.items():
        names.setdefault(t, r.get("name", ""))

    # ---------------- classify every ticker we know about
    lines = []
    for t in sorted(set(held) | set(traded) | set(cur)):
        in_hold = t in held
        in_txn = t in traded
        on_kics = t in cur
        was_on_kics = t in ever

        if in_hold and not on_kics:
            action, severity = "ADD", "exception"
            why = "Held at the cut-off date but not declared on KICS."
        elif in_txn and not in_hold and not on_kics and not was_on_kics:
            action, severity = "ADD", "exception"
            why = ("Traded during the period and never declared on any KICS export, even though the "
                   "position has since been closed.")
        elif in_txn and not in_hold and not on_kics and was_on_kics:
            action, severity = "NONE", "explained"
            why = "Disposed during the period and de-registered from KICS afterwards."
        elif on_kics and not in_hold and not in_txn:
            action, severity = "REMOVE?", "tidy-up"
            why = ("Declared on KICS but not held at the cut-off date and not traded in the period — "
                   "stale declaration. Over-declaration is not a breach; confirm the position is not "
                   "held elsewhere before removing.")
        elif on_kics and not in_hold and in_txn:
            action, severity = "NONE", "explained"
            why = "Sold during the period; still declared. Remove once the disposal is settled if KICS should show live positions only."
        else:
            action, severity = "NONE", "ok"
            why = "Held and declared."

        lines.append({
            "ticker": t,
            "name": names.get(t, ""),
            "in_holding": in_hold,
            "in_txn": in_txn,
            "on_kics_current": on_kics,
            "on_kics_previous": (t in prev) if previous else None,
            "action": action,
            "severity": severity,
            "why": why,
            "value": held.get(t, {}).get("value"),
        })

    to_add = [l for l in lines if l["action"] == "ADD"]
    to_remove = [l for l in lines if l["action"] == "REMOVE?"]
    exceptions = [l for l in lines if l["severity"] == "exception"]

    result = {
        "profile": profile,
        "as_of": data.get("as_of"),
        "period": {"from": data.get("period_from"), "to": data.get("as_of")},
        "counts": {
            "holdings": len(held),
            "transactions": len(txns),
            "traded_tickers": len(traded),
            "kics_current": len(cur),
            "kics_rows_total": len(current.get("rows", [])),
        },
        "current_snapshot": current.get("label"),
        "previous_snapshot": previous.get("label") if previous else None,
        "lines": lines,
        "to_add": to_add,
        "to_remove": to_remove,
        "exceptions": exceptions,
        "clear": len(exceptions) == 0,
        "expected_kics_after_action": sorted((set(cur) | {l["ticker"] for l in to_add})
                                             - {l["ticker"] for l in to_remove}),
    }

    if previous:
        result["movement"] = verify_movement(prev, cur, data)
    return result


def verify_movement(prev: dict, cur: dict, data: dict) -> dict:
    """Round 2: what actually changed between the previous and current KICS export."""
    added = sorted(set(cur) - set(prev))
    removed = sorted(set(prev) - set(cur))
    expected = data.get("expected_after_last_check") or {}
    exp_add = {norm(t) for t in expected.get("add", [])}
    exp_remove = {norm(t) for t in expected.get("remove", [])}

    return {
        "added": added,
        "removed": removed,
        "expected_add_done": sorted(exp_add & set(added)),
        "expected_add_missing": sorted(exp_add - set(cur)),
        "expected_remove_done": sorted(exp_remove & set(removed)),
        "expected_remove_outstanding": sorted(exp_remove & set(cur)),
        "unrequested_changes": sorted((set(added) - exp_add) | (set(removed) - exp_remove)),
    }


def save_state(result: dict, data: dict) -> Path:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "profile": result["profile"],
        "last_checked": result["as_of"],
        "current_snapshot": result["current_snapshot"],
        "holdings": sorted({norm(h["ticker"]) for h in _rows(data, "holdings")}),
        "expected_after_last_check": {
            "add": [l["ticker"] for l in result["to_add"]],
            "remove": [l["ticker"] for l in result["to_remove"]],
        },
        "expected_kics_after_action": result["expected_kics_after_action"],
        "databook": data.get("databook_out"),
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return STATE_PATH


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = reconcile(data)
    if "--save-state" in sys.argv:
        save_state(result, data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
