kpmg-deck — install, move, and prove it works
=============================================
Read SKILL.md to build a deck. Read this once per machine.

FIRST THING TO RUN
    python3 scripts/doctor.py

It checks the interpreter, both dependencies, the master, all nine faces, the
house style QRG and the render toolchain, then reports what is missing and what
you lose without it. Exit 0 means ready.

## Self-contained, and what that means

Audited and closed 25 August 2026, on house instruction. The test is: unzip
the skill onto a machine that has never seen the vault, build a deck, and get a
brand-correct .pptx with the titles in KPMG Bold.

**What ships inside the skill:** the cleaned master (`assets/template.pptx`), the
specimen deck, all nine KPMG faces, every reference file, **the full house-style
QRG**, and **the .pptx validator**. Nothing in `scripts/` reads a vault path.

**What does not, and cannot:** `soffice` and `pdftoppm`. They are binaries, they
are not ours to redistribute, and they are needed only to *look at* the result,
not to build it. `doctor.py` reports them as optional and says what you lose.

Two holes were open until this audit and both are now closed:

- **The house style lived only in the vault.** This file used to say outright
  that the QRG "has to travel with the vault, not the package". It is now
  mirrored at `references/house-style-qrg.md`, with the vault note still the
  authority and `doctor.py` reporting drift between them.
- **The QA pass borrowed another skill and a second interpreter.** Validation
  ran `validate.py` from the **pptx** skill, which needs `defusedxml` and Python
  3.10+, so on stock macOS (3.9.6) it meant installing `uv`, building a 3.12
  virtualenv and pip-installing into it before the documented QA step would run
  at all. `scripts/validate_pptx.py` replaces it: standard library only, runs on
  the interpreter already there, and gates the build the same way.


## Moving the skill to another machine

Two halves, because they travel differently.

**Git carries the skill, never the fonts.** `assets/fonts/` is in `.gitignore`
and has never been committed to any branch, verified with
`git log --all -- '*.ttf'`. A clone alone therefore builds decks in Arial.

**`scripts/package.py` carries both.** It writes a single archive holding the
skill and all nine faces, to an off-vault location so it cannot be swept into a
commit:

```bash
python3 scripts/package.py

## Fonts deploy themselves

Added 25 August 2026. The skill carries all nine KPMG faces in `assets/fonts/`
and installs any the machine is missing the first time `new_deck()` runs, on
macOS, Windows or Linux. Clone the skill, build a deck, and the titles come out
in KPMG Bold. There is no per-machine font checklist any more.

**The binaries are never committed.** They are licensed to KPMG by Commercial
Type and the vault this skill lives in pushes to GitHub, so `assets/fonts/` is
in `.gitignore`. `fonts.check_not_tracked()` runs on demand and fails loudly if
a future .gitignore edit ever makes them tracked, because the next push would
then redistribute a commercial licence. Self-contained on disk is the goal;
redistribution is not, and the two are not the same thing.

On a machine with neither the bundle nor the licensed source, `ensure_installed()`
seeds from `~/Library/Application Support/Artemis/fonts-vendor/kpmg/` if it is
there, and otherwise says so and lets the deck build in Arial. It is never
fatal: a deck that builds with a warning beats a deck that does not build, and
the render-time font probe catches the substitution either way.

**Everything is in centimetres.** Set 25 August 2026. A call that passes inches without `units="in"` builds a table about 2.5x too small, so this is a correctness rule, not a preference.
`deckkit` exports `CM` and `GRID`; `exhibits` exports `TL` for the
exhibit-plus-read geometry measured off the published decks. No function in
`exhibits.py` accepts inches.


NAMES
No personal name appears anywhere in this package, and none should be added.
Names in a DELIVERABLE are governed by the rule under Mode A in SKILL.md:
supplied content and explicit instruction allow them, research does not.
