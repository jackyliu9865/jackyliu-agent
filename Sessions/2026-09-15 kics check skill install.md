---
date: 2026-09-15
agent: claude-code
status: done
started: 2026-09-15 10:40
ended: 2026-09-15 10:45
engagement: _kics-check
---

# KICS check skill install

## Goal

Move the `kics-check` skill pack from `~/Downloads/kics-check/` into the vault as a local agentic workflow for regular use.

## Actions

- Copied pack to `Work/_kics-check/`. Left out the empty `{scripts,assets,references,state}` folder (failed brace expansion).
- Symlinked `~/.claude/skills/kics-check` -> `Work/_kics-check/`, same pattern as `kpmg-deck`.

- Added "Local use" section to `Work/_kics-check/SKILL.md`: script paths, run folder `Work/KICS check/`, state-file caution.
- Test: ran `assets/example_input.json` in the scratchpad without `--save-state`. Verdicts: 000111 OK, 000222 OK, 000333 ADD, 000444 explained, 000555 REMOVE?. Databook built, LibreOffice recalc filled cached values.

## Open points

- Holding tab conclusion says "Now declared (newly added)" on OK lines in round 1 (no prior export): column E is a hardcoded 0. Reported, not fixed.
- `assets/input_template.json` carries a real profile name in its example row. Reported, not fixed.
- Git: databooks and inputs in `Work/KICS check/` carry personal holdings. `.gitignore` decision pending.

## Fixes (user said "fix")

- `scripts/build_databook.py`: if there is no prior export, Holding column E shows "n/a" and the conclusion is `=IF(F=0,"ADD TO KICS","OK")`. Round 2 logic is unchanged.
- `assets/input_template.json`: real profile name replaced with "A Person".
- `.gitignore`: added `Work/KICS check/` and `Work/_kics-check/state/last_check.json`.
- Verified: round 1 example gives OK, OK, ADD TO KICS. Synthetic round 2 gives OK, OK, Now declared, with `clear: true` and no unrequested changes. `git check-ignore` confirms both paths.

## Fix 2 (user said "fix")

- Txn tab, round 1: column H shows grey "n/a". The conclusion leaves out the "disposed, de-registered" branch, because that branch needs a prior export.
- Grey font now shows. The Holding and Txn formatting loops had reset it to black.
- Verified: round 1 Txn J gives 000333 ADD TO KICS, 000444 OK, 000111 OK. Round 2 (000444 removed) gives 000444 "Disposed in period, de-registered". Both rounds agree with `reconcile()`.

## Outcome

Skill installed and registered. Example run passes. All open points closed.

