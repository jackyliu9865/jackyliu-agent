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


## Second pass: dated notes removed, markdown tightened

User instruction. Stripped provenance dates from every markdown file in
`Work/_deck/` and tightened prose. `Sessions/` untouched — dated records by
design.

Two kinds of dated note were mixed together, and a blind strip would have
deleted content:
- Pure provenance ("Added 21 August 2026 on the reviewer's instruction") — cut
- Correction records carrying live facts ("Corrected 21 August 2026: ... where
  this table and an inch figure disagree, this table wins") — date cut, rule kept

`brand.md` was rewritten in full (288 -> 209) because it also duplicated the font
install and verification section that `environment.md` now owns more accurately.
The dense reference files were edited surgically rather than rewritten, since
gate-by-gate detail is their value.

Verified after each file by extracting hex values, API names, decimal
measurements and file paths from the pristine tag and diffing against the new
version. Three real losses were caught and restored:
- `deckkit.shade()` had been shortened to `shade()`
- `brand.md`'s cross-reference to `layouts.md` for narrative pages
- `fonts.check_not_tracked()` and the font licence note, dropped from
  `environment.md` in an earlier edit this session

Remaining date strings are all content: data years in exhibit examples, the
date-format table in `house-style-qrg.md`, "KPMG 2025 brand-refresh", and
`last_checked` in `environment.md`, which the file tells the reader to check.

Totals across the folder: 17 files changed, 734 insertions, 961 deletions.
`doctor.py` ready to build, deck rebuilds clean, no new broken wikilinks.

## Third pass: deck-type profile made machine-readable

Assessed a suggested restructure. Most of it was already in place; the router
thinning was done this session (527 -> 75 lines) and `brand.md` was already the
single copy.

**Rejected: `profiles.json` carrying margins and grid per deck type.** Those do
not vary. The master splits by type in two places only, the back cover and the
front matter, and the package treats an explicit size on placeholder text as a
bug. Per-type margins would encode a distinction that does not exist. The
prose-to-code concern it raised is also already solved by `deckkit.GRID`.

**Built the real version instead.** What genuinely varies by type is which
layouts a deck opens and closes with, and nothing checked it.

- `deckkit.DECK_TYPES` — four kinds (report, publication, proposal, talkbook),
  each with its closer. `ALL_CLOSERS` derived from it
- `new_deck(kind=...)` stamps the type and rejects an unknown kind
- Three gates in `qa`: deck opens on `Cover page`, ends on its own back cover,
  carries no other type's back cover anywhere
- Undeclared kind skips all three and reports INFO, so fixtures and partial
  builds are unaffected

Proved against six scenarios: correct deck passes; wrong closer caught by two
gates; foreign closer mid-deck caught; missing cover caught; undeclared kind
reports INFO; talkbook correctly expects no closer.

**One regression found and fixed.** The cover gate initially fired
unconditionally and broke the package's own selftest, whose fixture legitimately
starts on `Title only_Blank`. Made it conditional on a declared kind. Selftest
back to **0 findings across 27 gates**, up from 23.

Also caught while checking: `brand.md` said the no-content marker is at y 17.45
while `deckkit.GRID["no_content_below"]` is 16.33. Both numbers are real - the
caption box is at 17.45, confirmed in the master XML, and the line it labels is
at 16.33. The wording invited reading 17.45 as the limit, which lets content sit
on the footer. Clarified.

Docs updated: `slide-template.md`, `build-api.md`, `START-HERE.md` step 5.
`build.py` now declares `kind="report"`.

## Fourth pass: SKILL.md moved out of the package

User asked whether `SKILL.md` should sit under `_deck/` rather than `design/`,
since it routes the whole deck task. Yes, and the fix was larger than a move.

There were two entry points with names that did not say which was which:
`START-HERE.md` routed the task, `design/SKILL.md` mapped the package. Merged
into one `Work/_deck/SKILL.md` carrying the registration frontmatter, the
six-step pipeline and the package map. Both old files deleted.

Symlink repointed: `~/.claude/skills/kpmg-deck -> Work/_deck`. Registration needs
`SKILL.md` at the symlink root, so the skill is now the deck capability rather
than the imported package.

`slide-template.md` also lifted out of `design/`. **The vendor tree now carries no
house markdown at all** - only upstream files plus our edits to `references/` and
`scripts/`. `design/SKILL.md` was the most-conflicted file against
`kpmg-deck-pristine` at 558 lines changed, and it is gone from the merge surface.

Thirteen references re-pointed. Wikilinks use `[[SKILL|the pipeline]]`, since a
bare `[[SKILL]]` reads badly in prose.

Verified: skill re-registered from the new root, `doctor.py` ready to build
through the symlink, selftest 0 findings across 27 gates, template rebuilds
clean, no broken wikilinks. `AGENTS.md` re-pointed.