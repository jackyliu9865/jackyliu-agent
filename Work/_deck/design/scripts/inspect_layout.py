#!/usr/bin/env python3
"""Print the placeholder map for template layouts.

The idx numbers are not consistent across layouts — 'Key findings_2 columns'
puts its second column at idx 74/75/76 while '1_Key findings_3 columns' (note the leading 1_) puts its
second at 57/59/65. Guessing produces slides with content in the wrong box, so
read the map for the layout you are about to use.

    python3 scripts/inspect_layout.py                     # list every layout
    python3 scripts/inspect_layout.py "Key findings_2 columns"
    python3 scripts/inspect_layout.py --all               # every map, long

Output columns: idx, role, position/size in CENTIMETRES (the house unit; the
template itself is authored in inches), inherited size + colour.
"""
import os
import sys

from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "template.pptx")

# What each recurring idx is for. Roles repeat across layouts even when the
# numbers move, so this is keyed on the placeholder's inherited geometry role.
ROLE_BY_SIZE = [
    (0.24, "section header bar — 9pt bold WHITE on Dark Blue"),
    (0.39, "strapline / source line"),
    (0.16, "RAG chip — recolour only, no text"),
    (0.20, "'Read more' button — 8pt bold Dark Blue on Light Blue"),
    (0.75, "summary / recommendation box"),
    (0.74, "summary / recommendation box"),
]

FIXED_ROLES = {
    17: "source / footnote — 6pt, bottom of content area",
    18: "strapline — 9pt bold Pacific Blue, under the title",
}


def role_for(shape):
    idx = shape.placeholder_format.idx
    if idx in FIXED_ROLES:
        return FIXED_ROLES[idx]
    if shape.height is None:
        return ""
    h = round(Emu(shape.height).cm, 2)
    w = round(Emu(shape.width).cm, 2) if shape.width else 0
    if h == 0.2 and w == 0.71:
        return "'Read more' button — 8pt bold Dark Blue on Light Blue"
    if w == 0.47:
        return "Value/SPA rating chip — 9pt bold Dark Blue on Grey 5"
    for height, role in ROLE_BY_SIZE:
        if h == height:
            return role
    if h > 1.0:
        return "body copy — 9pt Arial, levels 2-4 bulleted"
    return ""


def show(lay):
    print("\n%s" % lay.name.strip())
    print("-" * max(30, len(lay.name)))
    rows = []
    for shape in lay.placeholders:
        pf = shape.placeholder_format
        idx = pf.idx
        if shape.left is None:
            geo = "inherits from master"
        else:
            geo = "%5.2f,%5.2f  %5.2f x %-5.2f" % (
                Emu(shape.left).cm, Emu(shape.top).cm,
                Emu(shape.width).cm, Emu(shape.height).cm)
        label = "title" if str(pf.type).startswith("TITLE") or \
            str(pf.type).startswith("CENTER_TITLE") else "ph%d" % idx
        rows.append((idx if label != "title" else -1, label, geo, role_for(shape)))
    for _, label, geo, role in sorted(rows):
        print("  %-7s %-28s %s" % (label, geo, role))


def main():
    prs = Presentation(TEMPLATE)
    layouts = [l for m in prs.slide_masters for l in m.slide_layouts]
    args = sys.argv[1:]
    if not args:
        print("Layouts in template.pptx (pass a name for its placeholder map):\n")
        for lay in layouts:
            n = len(lay.placeholders)
            print("  %-42s %2d placeholders" % (lay.name.strip(), n))
        return
    if args[0] == "--all":
        for lay in layouts:
            show(lay)
        return
    want = args[0].strip().lower().lstrip("0123456789_")
    hits = [l for l in layouts if want in l.name.strip().lower()]
    if not hits:
        print("No layout matching %r. Run with no arguments to list them." % args[0])
        sys.exit(1)
    for lay in hits:
        show(lay)


if __name__ == "__main__":
    main()
