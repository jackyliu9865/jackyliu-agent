# Databook conventions

One workbook carries every period ever checked. Newest at the front, history below the
`Archive>>` divider, never a second file.

## Tab order

```
Summary @ <as_of>                 conclusion, sources, action list, movement, live check totals
KICS list @ <current label>       the export that drives every conclusion
KICS list @ <previous label>      superseded export, kept as the audit trail (round 2 onward)
Holding @ <as_of>                 one row per position
Txn <from>-<to>                   raw transactions on the left, unique tickers on the right
Archive>>                         empty divider sheet
<prior period tabs>               untouched — never edit a closed period
```

## Column layout

**Holding tab** — `A` ticker (numeric), `B` ticker as text, `C` name, `D` in Txn?,
`E` on prior KICS?, `F` on current KICS?, `G` units, `H` NAV, `I` value, `J` conclusion.
`B` is the key every other tab matches on.

**Txn tab** — `A` date, `B` ticker (numeric), `C` ticker as text, `D` type; then the
unique block: `E` unique ticker, `F` name, `G` in Holding?, `H` on prior KICS?,
`I` on current KICS?, `J` conclusion. **Column E is the unique-ticker column** — other
tabs point at `$E:$E`, so do not move it.

**KICS tab** — `B` ticker as text, `C` profile, `D` in Holding?, `E` in Txn?, `F` name,
`G` entry type, `H` acquisition date, `I` status.

## Formulas

- Text key: `=TEXT(A5,"000000")`. Keeps `217` and `000217` matching.
- Presence: `=COUNTIF('Holding @ 20260914'!$B:$B,$E5)` — whole-column ranges so a row
  added later is picked up.
- Profile-scoped presence: `=COUNTIFS('KICS list @ X'!$B:$B,$B5,'KICS list @ X'!$C:$C,"Name")`.
  Use this against any multi-profile export; plain `COUNTIF` would let another person's
  ticker satisfy the check.
- Conclusion: nested `IF` over the check columns, never a hardcoded verdict, so the cell
  re-derives if a source row is corrected.

## Formatting

| Meaning | Style |
|---|---|
| Keyed from a source document | blue text `0000FF` |
| Formula | black |
| Exception | red fill `FFC7CE`, bold dark red text |
| Explained difference / proposed tidy-up | amber fill `FFF2CC` |
| Matched / cleared | green fill `C6EFCE` |
| Out of scope (other profile) | grey fill `EDEDED` |

Arial 10 throughout, header row 4 in white-on-slate with wrap, freeze panes below the
header, a source note under the title, and an explanatory note under each table saying
what a zero in a check column does and does not mean.

## Gotchas

- **No spilled array formulas.** `UNIQUE`, `FILTER`, `SORT`, `XLOOKUP` evaluate to
  `#NAME?` or silently truncate once the file is recalculated outside modern Excel.
  De-duplicate in Python and write literal values. If an inherited file contains one,
  replace it with its own cached output and note the change on the tab.
- **openpyxl writes no cached values.** Recalculate (LibreOffice headless, handled by
  `build_databook.py`) or every formula reads back blank to anything but Excel.
- **A green recalc is not a correct check.** It proves the formulas evaluate. Verify a
  few conclusions against the source documents by eye before reporting.
- **Never edit an archived period.** If an old conclusion was wrong, add a note on the
  current Summary tab; the archive is evidence of what was concluded at the time.
