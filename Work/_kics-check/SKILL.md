---
name: kics-check
description: >
  Reconcile personal investment holdings and transactions against a KICS (compliance
  platform) portfolio export, then tell the user exactly what to add to or remove from
  KICS, and re-verify once they supply a refreshed export. Use this skill whenever the
  user provides a holding statement as at a date plus transaction records, together with
  a KICS / platform holdings report, or asks to "check my KICS", "check the investment
  declaration", "which ticker is not on the platform", "I've updated KICS, check again",
  or to roll the investment check databook forward to a new period. Also use it when
  they hand over a fresh KICS export referring to a check done earlier.
---

# KICS declaration check

Three populations, one question: **is everything the person holds or has traded
declared on KICS?**

| Population | What it is | Where it comes from |
|---|---|---|
| **Holding** | Positions as at a cut-off date | Broker/platform asset certificate |
| **Txn** | Trades between the last-checked date and that cut-off | Broker/platform transaction detail |
| **KICS** | What the person has declared to the firm | KICS portfolio holdings export (PDF) |

The check runs in two rounds. Round 1 finds the gaps and produces an action list.
Round 2 verifies the user actually made those changes and nothing else moved.

## Round 1 — check and instruct

1. **Read the inputs.** Holdings, transactions and the KICS export may arrive as PDFs,
   spreadsheets or pasted text. Extract them into one `input.json`
   (schema: `assets/input_template.json`).
2. **Check period continuity.** `period_from` must be the `last_checked` date in
   `state/last_check.json` (if a prior check exists). If the transaction records start
   later than that, say so — trades in the gap are invisible to the check. Do not
   silently proceed.
3. **Run the reconciliation:**
   ```bash
   python scripts/reconcile.py input.json --save-state
   python scripts/build_databook.py input.json -o Investment_check.xlsx
   ```
   `build_databook.py` calls the same `reconcile()` function, so the workbook and your
   chat answer can never disagree.
4. **Report** using the wording rules below, and give the user the action list.

## Round 2 — verify the updated export

The user comes back with a refreshed KICS PDF. Do **not** just diff the two exports —
re-run the whole check against the new export, and additionally verify the movement.

1. Append the new export to `kics_snapshots` (the last entry is always the current one;
   earlier entries become the superseded tabs).
2. Copy `expected_after_last_check` from `state/last_check.json` into the input so the
   movement check knows what was asked for.
3. Set `prior_databook` to the round 1 workbook so the period rolls forward into the
   same file rather than starting a new one.
4. Re-run both scripts. Confirm four things explicitly:
   - every requested **add** now appears (`expected_add_missing` is empty);
   - every requested **remove** is gone (`expected_remove_outstanding` is empty);
   - any **unrequested** change is explained (`unrequested_changes`) — a removal the user
     made on their own initiative is usually fine, but it must be named, not glossed over;
   - the full check now returns `clear: true`.

If something is still outstanding, say what remains and stop. Do not describe the check
as cleared while `exceptions` is non-empty.

## Decision table

This is the whole of the logic. It lives in `scripts/reconcile.py`; keep the two in step.

| In Holding | In Txn | On current KICS | Verdict | Colour |
|---|---|---|---|---|
| yes | — | yes | OK | green |
| yes | — | **no** | **ADD** — held but undeclared | red |
| no | yes | no, and never on any export | **ADD** — traded but never declared | red |
| no | yes | no, but on an earlier export | Disposed in period, de-registered — no action | amber |
| no | yes | yes | Sold in period, still declared — remove once settled | amber |
| no | no | yes | **REMOVE?** — stale declaration | amber |

Only the red rows are exceptions. Over-declaration is untidy, not a breach: always
propose removals as a question, because the person may hold that position through
another broker that this statement does not cover.

## Wording rules

- Lead with the answer: the ticker(s) to add, then the ticker(s) to consider removing.
  Name the fund, the date acquired and the value, so the user can act without reopening
  the file.
- Keep red and amber distinct in prose too. "One exception, plus eleven stale lines you
  may want to tidy" — not "twelve problems".
- State what the check does **not** cover: whether pre-clearance was required before a
  trade, and any account the supplied statements do not include. Flag the pre-clearance
  question when a ticker was undeclared from its purchase date; do not answer it.
- Never give investment advice, and never comment on the merits of the holdings. This is
  a completeness check against a declaration, nothing more.

## Data handling

- **Identifiers are text.** Normalise with `norm()`: numeric codes zero-pad to six digits
  (`217` → `000217`), alphanumeric IDs (`HK0194`) are upper-cased and left alone. Every
  match is on the normalised value. Never let Excel or `json` turn a code into an integer
  on the way in.
- **Never infer a ticker from a fund name.** Chinese and English names for the same fund
  differ across the two systems, and share classes (A/C) differ by one character. If a
  line has no identifier, ask.
- **Profiles.** A KICS "All Holdings" export can carry several people. Set `profile` and
  tag each row; out-of-scope rows are greyed on the tab and excluded from matching via
  `COUNTIFS`. Never let another profile's ticker satisfy a check.
- **Do not persist personal identifiers.** ID card numbers, account numbers and the
  person's name beyond the profile label have no place in the databook, the state file or
  memory. Tickers, values and dates are what the check needs.

## Databook conventions

See `references/conventions.md` for the full layout, formula and formatting rules.
In short: newest period at the front, older periods below an `Archive>>` divider, blue
for keyed figures, black for formulas, red/amber/green as in the decision table, and
no spilled array formulas (`UNIQUE`, `FILTER`, `XLOOKUP`) anywhere — de-duplicate in
Python instead, or the file breaks the moment it is recalculated outside modern Excel.

## Local use (Jacky's vault)

- The skill lives at `~/Documents/jacky-agent/Work/_kics-check/`.
  `~/.claude/skills/kics-check` symlinks to it. Edit the vault copy only.
- Run the scripts by absolute path from any working directory:
  `python3 ~/.claude/skills/kics-check/scripts/reconcile.py <input.json>`.
- Each period's files go to `~/Documents/jacky-agent/Work/KICS check/`:
  - `input_<as_of>.json` for the extracted input;
  - `Investment_check.xlsx` for the one rolling databook (set it as both
    `prior_databook` and `databook_out` from the second period onward);
  - `evidence/` for extraction records.
- Source PDFs stay where the user saved them. Reference them by path in `*_source`.
- `state/last_check.json` stays in the skill folder. Read it before every round 1.
- Only run `--save-state` on real inputs. The example input overwrites the live state.

## Files

```
kics-check/
  SKILL.md
  scripts/reconcile.py        core logic + state; run standalone for a fast answer
  scripts/build_databook.py   Excel databook; imports reconcile()
  assets/input_template.json  annotated schema
  assets/example_input.json   tiny worked example (synthetic tickers)
  references/conventions.md   workbook layout, formulas, gotchas
  state/last_check.json       written by --save-state; carries the date forward
```
