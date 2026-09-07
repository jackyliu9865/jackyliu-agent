"""Prove the house punctuation rule across every element type.

Bullets take no full stop; body paragraphs do. House instruction, 27 August
2026. This asserts the outcome for a cover subtitle, a divider, level 0/1
paragraphs, level 2 bullets, header bars, summary strips, straplines, exhibit
titles, commentary headings and the read column, on the layouts that carry
each. Run after any change to `_is_prose_body` or `add_full_stop`.

    python3 scripts/test_punctuation.py

Machine-independent: it derives its own location rather than hardcoding a path.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import new_deck, add, fill, bullets, note, strapline, drop, shade, save
import exhibits as ex
from pptx import Presentation

prs = new_deck(); ex.reset_registry()

s = add(prs, "Cover page")
fill(s, title="A cover", ph11=["A cover subtitle", "27 August 2026"],
     ph13="KPMG. Make the Difference.")
drop(s, 12)

s = add(prs, "Section divider")
fill(s, title="A divider")

s = add(prs, "One Column Text")
fill(s, title="Mixed body content",
     ph56=[("A lead-in paragraph at level zero", 0),
           ("A body paragraph at level one", 1)]
          + bullets(["A bullet at level two", "Another bullet"]))
strapline(s, "A strapline states the argument")
note(s, "Source: A named document, 2026.")

s = add(prs, "Analysis_Horizontal")
fill(s, title="Analysis layout",
     ph54="A header bar", ph55="Chart goes here",
     ph56=["A commentary paragraph beside the exhibit"])
strapline(s, "Another strapline")
note(s, "Source: Another named document, 2026.")

s = add(prs, "Key findings_2 columns")
fill(s, title="Key findings layout",
     ph54="Left header bar", ph56=["Left body paragraph"], ph55="Left summary strip",
     ph74="Right header bar", ph76=["Right body paragraph"], ph75="Right summary strip")
strapline(s, "A third strapline")
note(s, "Source: A third named document, 2026.")
drop(s, 72, 77, 52, 73); shade(s, 55, 75)

s = add(prs, "Title only_Blank")
fill(s, title="A hand-built page")
strapline(s, "A fourth strapline")
ex.exhibit_head(s, "An exhibit title", "Basis line, units and period.")
ex.commentary(s, ["A read-column paragraph", "A second read-column paragraph"],
              heading="A commentary heading")
ex.exhibit_source(s, "Source: A fourth named document, 2026.")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "assets", "punctuation-test.pptx")
save(prs, OUT, verify=False)

EXPECT = {
    "A cover subtitle": False, "27 August 2026": False,
    "A lead-in paragraph at level zero": True,
    "A body paragraph at level one": True,
    "A bullet at level two": False, "Another bullet": False,
    "A strapline states the argument": False,
    "A header bar": False, "Chart goes here": False,
    "A commentary paragraph beside the exhibit": True,
    "Left header bar": False, "Left body paragraph": True,
    "Left summary strip": False,
    "Right header bar": False, "Right body paragraph": True,
    "Right summary strip": False,
    "An exhibit title": False, "A commentary heading": False,
    "A read-column paragraph": True, "A second read-column paragraph": True,
}
seen, fails = {}, []
for n, sl in enumerate(Presentation(OUT).slides, 1):
    for sh in sl.shapes:
        if not sh.has_text_frame: continue
        for p in sh.text_frame.paragraphs:
            t = "".join(r.text for r in p.runs).strip()
            if not t: continue
            base = t[:-1] if t.endswith(".") else t
            if t in EXPECT:
                base = t
            if base in EXPECT:
                got = t.endswith(".")
                seen[base] = got
                if got != EXPECT[base]:
                    fails.append((base, EXPECT[base], got, sh.name))
missing = [k for k in EXPECT if k not in seen]
print("checked %d of %d cases" % (len(seen), len(EXPECT)))
for m in missing: print("  NOT FOUND:", m)
for b, want, got, nm in fails:
    print("  WRONG [%s] %r want full stop=%s got=%s" % (nm, b, want, got))
ok = not fails and not missing
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
