---
date: 2026-09-08
agent: claude-code
status: done
started: 2026-09-08
ended: 2026-09-08
engagement: _deck
---

# SKILL.md restructure

## Goal

User has decided to stop treating `design/` as untouchable. Break `SKILL.md`
(527 lines) into routing files and remove its overlap with `START-HERE.md`.

## Decision recorded

Forking the package loses upstream fixes on re-import. Mitigated with a vendor
branch: `kpmg-deck-pristine` tags the unmodified import at `af01e5f`. A future
re-import branches from the tag, drops the new package in, and merges to `main`,
so git resolves everything upstream changed that we did not touch.

## Plan

1. Tag pristine -> verify: `git tag -l` shows it, diff against `design/` empty
2. `references/content-rules.md` -> verify: written, Mode A rules moved
3. `references/build-api.md` -> verify: written, API moved
4. Trim `SKILL.md` to a router -> verify: skill still registers, line count down
5. Consequential edits to START-HERE, environment, slide-template -> verify: no
   stale "never patch" text
6. Fix `doctor.py:54` -> verify: prints `python-pptx`
7. Final -> verify: `doctor.py` ready to build, all wikilinks resolve

## Outcome

Done. `SKILL.md` 527 -> 75 lines, now a map with no process authority.

| Moved to | Lines |
|---|---|
| `references/content-rules.md` (new, 154) | Mode A operative rules, native-chart rule, booklet-link rule |
| `references/build-api.md` (new, 156) | Building, charts, house style, rules that matter most, own shapes, modules, traps |
| `references/qa-checklist.md` (existing) | Nothing moved. It already carried the runbook and the fidelity rationale; the `SKILL.md` copy was deleted |
| `environment.md` (existing) | Nothing moved. Already more accurate than the `What you need installed` table, which was deleted |
| `START-HERE.md` (existing) | Nothing moved. Its six steps replace `SKILL.md`'s `Workflow` |

Deleted outright: `Mode B` (34 lines, never applies now input is always supplied)
and `Installing, moving and proving the package` (53 lines, `README.txt` keeps
it).

**Fork made survivable.** `kpmg-deck-pristine` tags the unmodified import at
`af01e5f`; diff against `design/` was empty, confirming the baseline is clean. A
re-import branches from the tag, drops the new package in, and merges to `main`.
`START-HERE.md` carries the procedure and a table of every house change so a
merge conflict is recognisable.

`doctor.py:54` patched: the name-mapping dict now covers `pptx -> python-pptx`.

Consequential edits: `START-HERE.md` precedence section replaced by the fork
policy, pipeline steps 1/5/6 re-pointed at the new files, reference table
expanded to 12 rows; `environment.md` known-defect section rewritten as fixed;
`slide-template.md` re-import warning dropped.

Verified: skill still registers, `doctor.py` reports ready to build, the report
template still builds clean with the booklet linked. The 18 unresolved wikilinks
are pre-existing, inside imported reference files, pointing at the author's own
vault.

Not committed. The vendor-branch strategy needs these changes committed to work.
