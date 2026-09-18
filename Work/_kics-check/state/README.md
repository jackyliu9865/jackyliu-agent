`last_check.json` is written by `reconcile.py --save-state`. It carries forward:

- `last_checked` — the cut-off date of the last check; the next period's transaction
  records must start here, or trades in the gap go unseen.
- `expected_after_last_check` — the adds and removes requested, so round 2 can verify
  the user actually made them.
- `expected_kics_after_action` — what the next KICS export should contain.

It holds tickers and dates only. No names, account numbers or ID numbers.
