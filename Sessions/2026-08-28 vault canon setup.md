---
date: 2026-08-28
agent: claude-code
status: active
started: 2026-08-28
ended:
engagement: vault-setup
---

# Vault canon setup

## Goal

Establish the master agent rule file before building any workflow. Split the
vault into work and personal. Personal stays empty.

## Decisions

- Scope: whole Mac. `~/.claude/CLAUDE.md` symlinks to the vault `AGENTS.md`.
- Writing voice: full canon inherited from the reference file, including
  ASD-STE100, the banned vocabulary and the banned structures.
- Deck gate: two gates. Outline, then one slide, then wait.

## Source

Reference file `~/Downloads/AGENTS.md`, a sanitised template from the user's
manager. Dropped from it: the `~/Skills` monorepo, website deploy rules, the
KeePassXC secret store, cmux handoff spawning, cross-tool Codex awareness, the
multi-vault tier table and the vault-search MCP. None of that infrastructure
exists on this Mac.

## Added beyond the reference

- §6 Data integrity. The output carries figures a reader acts on.
- §7 Confidentiality. Member returns and unpublished drafts.
- Deck and report production section, routing to `kpmg-deck`, `kpmg-wgl` and
  `dataviz`.

## Correction applied

User corrected the preamble: Deal Advisory and Strategy Advisory consultant at
KPMG. The role change propagated to §7 Confidentiality, which now covers
price-sensitive transaction material, deal code names, external lookups and
clean-team restrictions. Engagement folders now use the deal code name.

## Second correction

User edited the preamble directly. Dropped the `kpmg-wgl` routing. Loosened §7
into three tiers: open by default for web search, market data and public filings
including by company name; ask first for raw client document upload and external
publishing; fixed prohibition on disclosing an unannounced transaction outward.
User accepts the research tradeoff explicitly.

## kpmg-deck skill reviewed

Source: `~/Downloads/kpmg-deck-3/`. Mature package. SKILL.md 527 lines, 2,264
lines of references, 20 scripts, 38 rendered reference pages, bundled master and
nine KPMG faces.

Finding that changes the design: the master splits by deck type in two places
only, the back cover (`Back Cover_Report` / `_Proposal` / `_Publications`) and
the Transmittal Letter. Type scale, grid and palette are global in
`references/brand.md`, and the skill forbids overriding them. The per-type files
therefore become deck-type profiles carrying layout repertoire and section
skeleton.

Environment: installed python-pptx 1.0.2, openpyxl 3.1.5, python-docx, pypdf.
`doctor.py` now reports ready to build.

Defects and blockers recorded:
- `doctor.py` line 54 prints `pip3 install --user pptx`. Correct package is
  `python-pptx`. Its name-mapping dict covers `docx` and misses `pptx`.
- No `soffice`, no `pdftoppm`, no Homebrew. QA steps 4 and 5 cannot run, so no
  deck can be visually verified or its font resolution proved.
- Vault has Obsidian Sync enabled. `assets/fonts/` holds nine Commercial Type
  faces licensed to KPMG. The skill must stay outside the vault.

## Deck profiles — slice written

Publication folded into Report as a variant on user instruction. Three profiles,
not four.

Skill copied to `~/.claude/skills/kpmg-deck`, outside the synced vault. `doctor.py`
reports ready to build from the new location, and the skill is now registered.

Written as the thin slice, awaiting go:
- `Work/_workflow/branding/base.md`
- `Work/_workflow/branding/report.md`

Design point recorded: the client and publication variants differ in more than
the back cover. Client builds on the placeholder layouts with bullets;
publication builds on `Title only_Blank` with `exhibits.*` furniture and prose,
using compositions A to D. Building a publication from `Analysis_Horizontal` is
the failure the skill was corrected for on 26 August 2026.

All API names and geometry cited in the profile verified against source:
`gate_exhibit_width` qa.py:916, `commentary` exhibits.py:315, `drop`
deckkit.py:371, `shade` deckkit.py:395, and `TL` exhibits.py:68 giving plot_w
13.70, read_x 17.43, read_w 13.70.

Held back at the gate: `proposal.md`, `talkbook.md`, and the pointer from
`AGENTS.md` to this folder.

## Skill moved into the vault

User instruction: the entire skill, fonts included, inside the vault. Canonical
copy now at `Work/_workflow/kpmg-deck/`, with `~/.claude/skills/kpmg-deck`
symlinked to it. Verified: `doctor.py` reports ready to build through the
symlink, and the skill still registers with Claude Code.

Correction to the concern raised earlier. Obsidian Sync is enabled as a plugin
with no remote configured, so nothing is uploading. Connected, it is end-to-end
encrypted to the user's own devices, which matches the README's permitted
internal use. The real exposure is git, which is the scenario the boss's file
described. Added a vault-root `.gitignore` excluding `**/assets/fonts/` and every
`.ttf` so the faces stay out of any repository this vault later becomes.

`base.md` updated for the new paths and the licence position.

## Folder restructure

User: `branding/` and `kpmg-deck/` overlapped, and the reading order for a PPT
task was unclear. Combined into one folder, `Work/_deck/`.

The cut that removes the overlap is ownership. `skill/` is imported and never
edited, so a local patch is lost on the next import. `profiles/` is the user's
own decisions and cites the skill rather than restating it. `START-HERE.md` is
the single entry point and carries the numbered reading order.

`base.md` dissolved into `START-HERE.md` plus `environment.md`. Environment split
out because it is volatile and START-HERE should stay stable.

`AGENTS.md` now points at `Work/_deck/START-HERE.md` for any PowerPoint task.

Symlink re-pointed to `Work/_deck/skill`; doctor verified through it.

## Citation rules loosened

User instruction. The confidentiality section in `START-HERE.md` was constraining
output quality.

- Reference pages, specimen, master and fonts are now used freely, without
  restriction and without asking.
- Competitor output: usable for background analysis and for craft, never named in
  a deck.
- KPMG publications: now citable in a deck. This overrides
  `skill/references/design-principles.md` §6, which bans it and calls the ban
  non-negotiable.

That conflict exposed a structural gap: nothing said which file wins. Added a
**Precedence** section to `START-HERE.md` stating that this folder overrides
`skill/`, with a table of recorded overrides, and forbidding local patches to
`skill/` since an import would lose them.

Font licence fact moved out of the router into `environment.md`, where it is a
fact rather than a rule.

## Category folders

User instruction: one folder per deck type, routed from `START-HERE.md`. The
`profiles/` container is gone; the three folders sit directly under `Work/_deck/`
so the routing is one hop.

```
Work/_deck/
├── START-HERE.md
├── environment.md
├── Report/Report.md        drafted
├── Proposal/Proposal.md    stub, not written
├── Talkbook/Talkbook.md    stub, blocked on a layout
├── skill/
└── deck-workflow-map.html
```

Convention: folder name matches its lead file, so `[[Report]]` resolves and the
folder holds anything specific to that type - its own master, samples,
boilerplate.

Stubs written rather than empty folders, so routing does not dead-end and no
agent invents a profile. Each stub lists what must be decided before it can be
written. All wikilinks verified to resolve.

## Design layer collapsed into the package

Superseded within the session. User: use the skill folder as the design folder,
delete the separate one. `skill/` renamed to `design/`; the `design/` folder
written earlier deleted with its two files.

Net simplification. Fonts returned to `design/assets/fonts/` as a real folder, so
`fonts.py` resolves `BUNDLED` natively and **the only modification to the package
is gone**. Symlink re-pointed to `Work/_deck/design`; doctor verified.

Back to two layers: `design/` is imported and never edited, the category folders
are the user's. House decisions that span all three types live in
`START-HERE.md`, under Precedence or its own sections, rather than in a third
folder.

Paths swept across `START-HERE.md`, `Report.md`, `environment.md`, `AGENTS.md`
and `.gitignore`. All wikilinks resolve.

The `deck-workflow-map.html` thinking artefact was removed by the user at some
point before this change. Not recreated.

### Superseded: design layer added

User instruction: a `design/` folder governing all three deck categories, with
subfolders per design element, starting with the fonts.

```
Work/_deck/
├── START-HERE.md
├── environment.md
├── design/
│   ├── Design.md
│   └── typography/
│       ├── Typography.md
│       └── fonts/          nine faces, canonical
├── Report/ Proposal/ Talkbook/
└── skill/
```

Three layers now: `skill/` is the engine, `design/` is cross-category, the
category folders are per-type.

Font move required care. `fonts.py:27` resolves `BUNDLED` to
`<skill>/assets/fonts` and installs from it on the first `new_deck()` call, so a
plain move would have left every deck building in Arial. Canonical copy now in
`design/typography/fonts/`, with `skill/assets/fonts` a symlink to it. Verified:
nine faces resolve, `doctor.py` still reports ready to build.

That symlink is the only modification to `skill/`. Recorded in the START-HERE
precedence section; `Typography.md` carries the command to restore it after a
re-import.

`Design.md` states what the folder must never become: a copy of `brand.md`. It
holds shared assets, house overrides and additions only, and points at the skill
for everything else. `colour/`, `grid/` and `exhibits/` deliberately not created,
since an empty folder that only points at the skill is worse than no folder.

`.gitignore` updated for both font paths. All wikilinks resolve.

## layout.md written

`design/layout.md` routes deck type to slide master. Report and Proposal build on
the KPMG 2025 master; Talkbook is a placeholder pending a template.

Verified before writing: `specimen-deck.pptx` and `template.pptx` carry the
identical 32-layout set, no difference either way. The specimen is that master
with 28 demo slides; the template is it cleaned to zero.

So the file routes to the master and records the trap. `SKILL.md` forbids opening
the specimen as a starting file - its 28 slides cross-link and deleting them
leaves orphans that make PowerPoint report the file corrupt. `new_deck()` opens
`template.pptx`. The specimen stays the visual reference and the parts bin for
lifting pre-formatted tables.

This is a house file inside an imported package, so a re-import deletes it. Added
a **House files kept inside `design/`** table to the START-HERE precedence
section, replacing the "carries no modifications" line. Reading order now has
`layout.md` at step 3, before any file is opened.

Naming note: `design/layout.md` sits near `design/references/layouts.md`, which
is the package's placeholder idx map. Different files, one letter apart.

## Open

- First workflow not yet built. Target is PPT deck production.

## Outcome
