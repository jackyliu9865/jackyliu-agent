#!/usr/bin/env python3
"""Exercise every exhibit type the skill offers, then gate the result.

Run it after any change to deckkit, exhibits, databooklet, qa or icons:

    python3 scripts/selftest.py [outdir]

It builds a deck using all of them, writes the booklet, runs every gate and
prints what failed. It is deliberately not a unit test: the failure mode this
skill has is visual and structural, so the artefact has to be produced.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from deckkit import (new_deck, add, fill, note, strapline, save, check, GRID,
                     drop, shade,
                     DARK_BLUE, PACIFIC, COBALT, KPMG_BLUE, LIGHT_BLUE, GREY)
import exhibits as ex
import databooklet
import icons
import qa

# Where an exhibit needs the wide split, its commentary must move with it.
# Mixing the two geometries is what puts a callout on top of a paragraph.
W = ex.TL   # the master column; TL_WIDE crosses the slide centre line

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets")
SRC = "Source: Self-test fixture, KPMG analysis."

ex.reset_registry()
prs = new_deck()

# 1. Column exhibit with the full five-part grammar
s = add(prs, "Title only_Blank")
fill(s, title="Column exhibit and a read")
strapline(s, "Every chart carries a title, a basis line, a key and a source.")
ex.chart_exhibit(s, "column", ["2021", "2022", "2023", "2024", "2025"],
                 [("Revenue", [54.0, 58.2, 61.1, 63.0, 64.8]),
                  ("EBITDA", [4.1, 4.6, 5.2, 5.7, 6.3])],
                 title="EBITDA grew faster than revenue in four of five years",
                 basis="2021-2025, USD billion", units="USD bn", source=SRC,
                 chart_id="SELFTEST_COLUMN", height=10.4)
ex.commentary(s, ["Revenue compounded at 4.7% while EBITDA compounded at 11.3%",
                  "The gap is mix, not price",
                  "Two contracts carry the whole of the margin improvement"],
              heading="What the chart shows")

# 2. Dumbbell
s = add(prs, "Title only_Blank")
fill(s, title="Dumbbell: level and movement")
strapline(s, "Two marks per category show where each sector sits and how far it moved.")
ex.dumbbell(s, [("Real estate", -7.0, -0.3), ("Energy", -6.2, 0.8),
                ("Industrials", -1.4, 0.2), ("Materials", -2.2, 1.3),
                ("Utilities", -1.3, 1.7), ("Financials", 0.2, 0.8),
                ("Health care", -0.4, 1.8), ("Staples", 4.5, 6.6)],
            title="Only three sectors cleared their hurdle in both years",
            basis="Return on capital minus cost of capital, 2020 and 2025, %",
            label_a="2020", label_b="2025", source=SRC,
            chart_id="SELFTEST_DUMBBELL", ref_value=0.0,
            ref_label="Cost of capital", left=W["plot_x"],
            width=W["plot_w"], height=9.6)
ex.commentary(s, ["The vertical rule is the hurdle, not zero growth",
                  "A sector left of it destroyed value in that year"],
              left=W["read_x"], width=W["read_w"])

# 3. Combo, columns on the left axis and markers on the right
s = add(prs, "Title only_Blank")
fill(s, title="Combo: two units, one exhibit")
strapline(s, "Columns carry the level, detached markers carry the rate.")
ex.combo_exhibit(s, ["Mexico", "Vietnam", "India", "Malaysia", "Brazil",
                     "Thailand", "Indonesia", "Turkey"],
                 [("2025 exports", [660, 450, 435, 330, 320, 310, 280, 265])],
                 [("2018-2025 export CAGR", [0.041, 0.128, 0.058, 0.062,
                                             0.061, 0.049, 0.066, 0.055])],
                 title="Export growth is fastest where the base is smallest",
                 basis="2018-2025, USD billion (column, LHS) and % (dot, RHS)",
                 source=SRC, chart_id="SELFTEST_COMBO", height=10.0)
ex.commentary(s, ["Vietnam grew three times faster than Mexico from a base "
                  "two thirds the size",
                  "The marker series is deliberately not a line, because the "
                  "categories are not ordered in time"])

# 4. Bubble
s = add(prs, "Title only_Blank")
fill(s, title="Bubble: a third variable in size")
strapline(s, "Size carries export value, colour carries the group, both are keyed.")
ex.bubble_exhibit(s, [
    ("Emerging manufacturing hubs",
     [(32.5, 16.0, 40, "Vietnam"), (21.0, 13.5, 12, "Cambodia"),
      (9.8, 8.4, 90, "India"), (4.2, 8.7, 55, "Indonesia"),
      (3.9, 5.0, 45, "Malaysia"), (6.1, 3.4, 60, "Brazil")]),
    ("Other economic blocs",
     [(9.5, 14.0, 600, "Greater China"), (2.6, 3.3, 420, "EU"),
      (2.2, 2.6, 380, "USA"), (3.6, 2.4, 190, "Mexico")])],
    title="Export growth and GDP growth move together, to a point",
    basis="2000-2025, times growth, bubble size is 2025 export value",
    source=SRC, chart_id="SELFTEST_BUBBLE", height=10.0)
ex.commentary(s, ["The largest blocs cluster at the origin",
                  "Growth multiples are a small-base effect above 20 times"])

# 5. Small multiples, one shared key
s = add(prs, "Title only_Blank")
fill(s, title="Small multiples on one scale")
strapline(s, "Three panels, one scale, one key, so the eye compares rather than converts.")
y = ex.multiples_head(s, group_id="SELFTEST_SM",
                      title="The mix shifted the same way in every region",
                      basis="2021-2025, share of revenue, %", source=SRC,
                      left=W["plot_x"], width=W["plot_w"])
y = ex.key(s, [("Legacy", GREY[4]), ("Digital", KPMG_BLUE)], top=y,
       left=W["plot_x"])
panels = ex.small_multiples(s, 3, top=y, left=W["plot_x"],
                            width=W["plot_w"])
data = {"Asia": [[52, 48, 45, 41, 38], [48, 52, 55, 59, 62]],
        "Europe": [[61, 58, 55, 52, 50], [39, 42, 45, 48, 50]],
        "Americas": [[47, 45, 42, 40, 37], [53, 55, 58, 60, 63]]}
for (x, w), (region, vals) in zip(panels, data.items()):
    ex.panel_title(s, region, x, y, w)
    ex.chart_exhibit(s, "column_stacked_100", ["21", "22", "23", "24", "25"],
                     [("Legacy", vals[0]), ("Digital", vals[1])],
                     title="", basis=None, left=x, top=y + 0.50, width=w,
                     height=8.2, legend=False, data_labels=False,
                     group="SELFTEST_SM", panel=region,
                     value_labels=(region == "Asia"),
                     colours=[GREY[4], KPMG_BLUE])
ex.exhibit_source(s, SRC, left=W["plot_x"], width=W["plot_w"],
                  top=GRID["content_bottom"] - 0.6)
ex.commentary(s, ["Digital passed half of revenue in Asia in 2023 and in "
                  "Europe in 2025",
                  "The panels share one scale, one key and one source",
                  "Value-axis labels appear on the first panel only"],
              top=y, left=W["read_x"], width=W["read_w"])

# 6. Share bar, KPI band, key features and icons
s = add(prs, "Title only_Blank")
fill(s, title="Bands, shares and vector icons")
strapline(s, "Furniture the published decks use to close a page.")
ex.kpi_band(s, [("55%", "of positive economic profit",
                 "Top 20 firms, 2025"),
                ("4.9%", "incremental return on new capital",
                 "2015-2025 average"),
                ("7.9%", "weighted cost of capital",
                 "2025, market weighted")], top=3.85, height=2.20)
y = ex.share_bar(s, [("40.1%", 40.1, "Top 10"), ("14.9%", 14.9, "Next 10"),
                     ("45.0%", 45.0, "Other 637 value creators")],
                 top=6.60, caption="Cumulative share of all positive economic "
                                   "profit companies, %",
                 left=GRID["left"], width=GRID["content_w"])
ex.key_features(s, [("+100 USD billion", "of 2024 total export, or strong "
                                         "export growth"),
                    ("Labour-intensive focus", "Limited ownership of core "
                                               "technologies"),
                    ("Geographic advantage", "Strategically located within "
                                             "global trade routes"),
                    ("Members of FTAs", "Benefit from tariff advantages "
                                        "through trade agreements")],
                heading="Key features", top=y + 0.55, height=3.10)
for i, nm in enumerate(["cost", "time", "target", "growth"]):
    try:
        icons.place(s, nm, GRID["left"] + i * 2.2, 14.4, 1.0, colour=KPMG_BLUE)
    except RuntimeError as exc:
        print("  icons skipped:", exc)
        break
ex.exhibit_source(s, SRC)

# 7. Data table as an exhibit
s = add(prs, "Title only_Blank")
fill(s, title="A table is an exhibit too")
strapline(s, "Titled, based, banded, sourced, and sized to its rows.")
ex.data_table(s, [["Sector", "2024", "2025", "Change (pp)"],
                  ["Financials", "12.4", "13.1", "+0.7"],
                  ["Industrials", "8.9", "8.2", "(0.7)"],
                  ["Technology", "17.2", "19.6", "+2.4"],
                  ["Materials", "6.1", "5.8", "(0.3)"],
                  ["Utilities", "4.4", "4.9", "+0.5"]],
              title="Technology widened its lead while industrials slipped",
              basis="Return on invested capital, 2024 and 2025, %",
              source=SRC, slot="half_left")
ex.commentary(s, ["Only technology improved by more than one percentage point",
                  "Industrials and materials both went backwards",
                  "Row height comes from the row count, not from stretching to "
                  "fill a box",
                  "Numeric columns right-align and keep a gap from the next "
                  "column"],
              left=W["read_x"], width=W["read_w"])

os.makedirs(OUT, exist_ok=True)
# 8. Line with end labels, on a log scale
s = add(prs, "Title only_Blank")
fill(s, title="Line, labelled at its own end")
strapline(s, "A legend the eye has to travel to is a tax on every reader.")
ex.line_exhibit(s, ["2015", "2017", "2019", "2021", "2023", "2025"],
                [("Attacker cost per effect", [1000, 620, 300, 140, 70, 40]),
                 ("Defender cost per intercept", [1800, 1850, 1900, 1950,
                                                  2000, 2100])],
                title="The two curves separated by two orders of magnitude",
                basis="2015-2025, indexed cost per unit of effect, log scale",
                units="index", source=SRC, chart_id="SELFTEST_LINE",
                log=True, height=10.4, colours=[PACIFIC, DARK_BLUE],
                slot="half_left")
ex.commentary(s, ["Each line carries its own name and final value",
                  "A log axis is disclosed in the basis line, because the "
                  "reader otherwise misreads the gaps",
                  "Bars are never put on a log axis: length encodes value and "
                  "a log axis has no zero"],
              heading="Why end labels",
              left=W["read_x"], width=W["read_w"])

# 9. Waterfall and a ranked bar with one focal mark
s = add(prs, "Title only_Blank")
fill(s, title="Bridge and ranked comparison")
strapline(s, "A decomposition above, a ranking with one accent below.")
ex.waterfall(s, [("2021 margin", 12.4), ("Price", 2.1), ("Mix", -1.6),
                 ("Input cost", -2.8), ("Volume", 1.2), ("Opex", 0.9)],
             title="Input cost took more than price and volume put back",
             basis="2021 to 2025, EBITDA margin, percentage points",
             units="pp", source=SRC, chart_id="SELFTEST_WATERFALL",
             left=GRID["left"], width=GRID["col2_w"], height=5.6, draw_source=False,
             number_format="0.0")
ex.sorted_bar(s, [("Alpha", 14.2), ("Bravo", 9.8), ("Charlie", 22.6),
                  ("Delta", 6.1), ("Echo", 17.3)],
              title="Charlie carries the position the slide is about",
              basis="2025, revenue, USD billion", units="USD bn",
              highlight="Charlie", source=SRC, chart_id="SELFTEST_SORTED",
              left=GRID["left"], top=10.30, width=GRID["col2_w"], height=5.0,
              number_format="0.0")
ex.commentary(s, ["The waterfall is a stacked column with an invisible base, "
                  "so it stays a native editable chart",
                  "The ranked bar sorts by value and spends the one accent "
                  "colour on the category the slide is actually about",
                  "Everything else is neutral, because colour everywhere is "
                  "colour nowhere"])

# --- the master's own narrative page, with its unused chips taken off -------
# Added 25 August 2026. `1_Key findings_3 columns` is what a three-column
# narrative page should sit on: fixed body boxes and a summary strip per column
# fill the page by design, where hand-built columns leave a third of it empty.
# It ships a red RAG chip and a grey "Value" chip per column, and both have to
# be dealt with: drop() takes them off, shade() puts the master's Grey 5 back
# behind the summary strips the "Value" chip was anchoring.
s = add(prs, "1_Key findings_3 columns")
fill(s, title="Narrative pages go on this layout",
     ph54="Fixed boxes", ph57="Summary strips", ph61="No stray chips",
     ph64=[("The body box is 9.30 by 10.10 cm and the same on every column, so "
            "three columns of unequal prose still line up", 1)],
     ph65=[("The strip along the bottom carries the column's takeaway, which is "
            "what stops a short column reading as an unfinished one", 1)],
     ph66=[("An unused placeholder is not free: a red chip that encodes nothing "
            "is decoration, and gate_rag_key fails it", 1)],
     ph55="Fixed geometry beats hand-built columns",
     ph59="The takeaway sits in the strip, not in the prose",
     ph63="Drop what the slide does not use",
     ph17="Source: kpmg-deck self-test.")
strapline(s, "drop() takes the unused chips off and shade() restores the "
             "master's Grey 5 behind the summary strips")
drop(s, 72, 73, 74, 52, 56, 60)
shade(s, 55, 59, 63)

# --- a long series, labelled sparsely --------------------------------------
# Every point plotted, four labels printed. Blanks are runs of zero-width
# spaces: unique, so PowerPoint does not collapse them, and invisible, so the
# axis does not grow a row of tick stubs.
_QTRS = ["Q%d %d" % (q, y) for y in range(2021, 2026) for q in range(1, 5)]
_VALS = [round(8.9 + 0.62 * i + (1.4 if i > 15 else 0), 2)
         for i in range(len(_QTRS))]
s = add(prs, "Title only_Blank")
fill(s, title="A long series needs few labels")
strapline(s, "Twenty quarters plotted and four labelled, which is the only way "
             "a dense time series stays readable at 8pt")
_sp = ex.line_exhibit(
    s, _QTRS, [("Series", _VALS)],
    title="Sparse category labels keep a twenty-point series legible",
    basis="Illustrative series, units, Q1 2021 – Q4 2025",
    units="units", source="Source: kpmg-deck self-test, illustrative.",
    chart_id="selftest_sparse", slot="half_left", number_format="0.0",
    plot_rect=(0.07, 0.03, 0.82, 0.86))
ex.label_every(_sp, 4)          # one label a year, real quarters in the data
ex.commentary(s, [
    "label_every() prints one label in four and keeps every category name in "
    "the data, so Edit Data in PowerPoint still shows the real quarters",
    "The first version of this blanked the unwanted names with zero-width "
    "spaces, which made the axis read correctly and wrote empty category cells "
    "into the chart's own workbook",
    "A chart is only an Excel graph if its data is the real data, which is why "
    "sparse_labels() now raises rather than warns",
    "plot_rect pins the plot area, so a chart with many categories cannot be "
    "squashed into the top of its own frame by the renderer",
], heading="Thin the labels, not the data")

out_pptx = os.path.abspath(os.path.join(OUT, "selftest.pptx"))
out_xlsx = os.path.abspath(os.path.join(OUT, "selftest-databooklet.xlsx"))

print("\n  deckkit.check()")
problems = check(prs)
prs.save(out_pptx)

path, n_charts, n_rows = databooklet.write(
    out_xlsx, deck_name="kpmg-deck self-test")
print("\n  booklet: %d exhibits, %d data rows -> %s"
      % (n_charts, n_rows, os.path.basename(path)))
bp = databooklet.check_booklet(prs)
results = qa.report(prs, booklet_problems=bp)

# INFO findings are notes, not failures. Counting them meant a clean run
# reported "1 finding" forever, which trains the reader to ignore the number.
fails = sum(1 for v in results.values() for f in v
            if not str(f).startswith("INFO")) + len(problems)
import validate_pptx
print("\n  validate_pptx (bundled, stdlib only)")
struct = validate_pptx.validate(
    out_pptx, os.path.join(os.path.dirname(OUT), "assets", "template.pptx")
    if os.path.isdir(os.path.join(os.path.dirname(OUT), "assets"))
    else os.path.join(OUT, "template.pptx"))
fails += len(struct)

print("\n  self-test: %d finding(s) across %d gates" % (fails, len(results) + 2))
print("  deck:    %s" % out_pptx)
print("  booklet: %s" % out_xlsx)
sys.exit(0)
