---
date: 2026-08-31
agent: claude-code
status: done
started: 2026-08-31 16:34
ended: 2026-08-31 16:40
engagement: _deck trial
---

# Report template trial run

## Goal

First end-to-end run of the deck workflow. Build a structural template deck for
the Report type and prove the pipeline works.

## Declarations

- **Mode:** neither A nor B in the strict sense. No document was supplied, and a
  structural template carries no claims to research. **No real figures go in it.**
  Any number is visibly illustrative and its basis line says so, per §6 of
  `AGENTS.md` and the illustrative-data rule in `SKILL.md`.
- **Deck type:** Report, client variant. Closer `Back Cover_Report`.
- **Master:** KPMG 2025 brand-refresh, opened via `new_deck()` on
  `assets/template.pptx`. Never the specimen.

## Plan

1. Probe the real placeholder maps -> verify: idx numbers printed from the template
2. Write one build script -> verify: it runs clean
3. Build -> verify: `save()` returns without raising
4. QA steps 1-3 -> verify: zero findings
5. Steps 4-5 -> blocked, no soffice/pdftoppm. Report the gap

## Outcome

Built. `Work/_deck/Report/template/report-template.pptx`, 11 slides, plus
`report-template-databook.xlsx`. Reproducible from `build.py`.

QA steps 1-3 clean. Steps 4-5 not run: no soffice, no pdftoppm. The deck is
unverified visually and the font resolution is unproved.

### Gates that fired, and what they caught

| Gate | Finding |
|---|---|
| Title budget | Three titles over 36 chars. Shortened |
| Strapline | `Key findings_2 columns` has no idx 18. Needed `strapline()`, which falls back to a drawn box |
| `check_booklet` | Chart C1 registered with no source. Passed `source=` with `draw_source=False` so the source line stays on idx 17 |
| `gate_rag_key` | Two RAG chips with no key |

`gate_rag_key` is brittle and worth knowing: it string-matches for `red is`,
`red =`, `traffic-light` or `traffic light`. "Rating scale: red high, amber
medium, green low" fails it. Phrasing recorded as a comment in `build.py`.

`databooklet.write()` takes a path first, not the presentation. `SKILL.md`
implies otherwise.

### Deviation from the Report profile

Contents built on `One Column Text` rather than `Title only_Blank`.
`Title only_Blank` carries a title and nothing else, so a contents list means
hand-placing a box. `One Column Text` gives a real body placeholder and a source
line. Propose amending `Report.md` front matter.


## Font failure and fix — 1 September 2026

The trial run's real finding. Titles rendered in Helvetica despite every gate
passing.

Traced the chain first and cleared the deck: slide title carries no explicit
font, layout does not override, master titleStyle is `+mj-lt`, `theme1`
majorFont is `KPMG Bold`. The build was correct throughout.

**Root cause: `com.apple.quarantine` on all nine faces.** Downloaded from Notion,
stamped by Gatekeeper. macOS silently refuses to activate a quarantined font, so
Font Book copied files in, saw the filename, and never activated. `atsutil
databases -removeUser` failed because no font registry existed to remove.

Fix, both steps needed:
- `xattr -d com.apple.quarantine` on `~/Library/Fonts/*.ttf` and the vault copies
- `killall fontd`

Now resolving: `KPMG Bold -> postscript=KPMG-Bold family=KPMG`. system_profiler
went from 0 KPMG entries to 55, families `KPMG` and `KPMG Logo`.

Cleaned up three byte-identical `KPMG-BOLD_2/_3/_4.ttf` left by Font Book's
"Keep Both".

**Standing lesson: `doctor.py`'s font check is a directory listing and gives a
false green.** It said `9 faces` and `ready to build` the entire time. Recorded
in `environment.md`.

Deck rebuilt clean after the fix. QA 1-3 pass, theme confirmed asking for
`KPMG Bold`.