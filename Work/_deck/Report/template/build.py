"""Report template deck — structural skeleton for the Report profile.

Trial run of the deck workflow, 31 August 2026.

NO REAL FIGURES. Every number here is illustrative and says so in its own basis
line, per §6 of AGENTS.md and the illustrative-data rule in SKILL.md. This file
is a layout template; it is not evidence of anything.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "design", "scripts"))

from deckkit import (new_deck, add, fill, bullets, note, strapline, drop,
                     shade, save, rag, table, CM, GRID)
import exhibits as ex
import qa, databooklet

prs = new_deck()

# ---------------------------------------------------------------- front matter
s = add(prs, "Cover page")
fill(s, title="[Project name]",
        ph11=["[Engagement type]", "", "[Date]"],
        ph13="KPMG. Make the Difference.")

s = add(prs, "Transmittal Letter")
fill(s, ph14="[Client name]\n[Addressee and title]\n[Address]",
        ph15="[Date]",
        ph10=["[Opening paragraph. States what was engaged, under what terms of "
              "reference, and over what period]",
              "[Second paragraph. States the basis of preparation and the "
              "limitations the reader must carry into the findings]"],
        ph11=["[Third paragraph. States what the reader should do with this "
              "document and who to contact]",
              "[Closing and signature block]"])

s = add(prs, "One Column Text")
fill(s, title="Contents",
        ph18="[Strapline. One line stating what this document argues]",
        ph56=[("Section", 0)]
             + bullets(["1. Executive summary",
                        "2. Scope and basis of preparation",
                        "3. Findings by workstream",
                        "4. Financial analysis",
                        "5. Key risks",
                        "6. Recommendations",
                        "7. Appendices"], level=3),
        ph17="Source: KPMG analysis")

# ------------------------------------------------------------------- section 1
s = add(prs, "Section divider")
fill(s, title="1. Executive summary")

s = add(prs, "One Column Text")
fill(s, title="[Finding, never the topic]",
        ph18="[Strapline sharpens the finding into one assertion]",
        ph56=[("[Lead-in, bold. The single sentence a reader keeps]", 0),
              ("[Supporting sentence. The subject is the company, the market or "
               "the number, never the analysis]", 1)]
             + bullets(["[Each bullet is a full sentence carrying one point]",
                        "[Never more than about six in a block]",
                        "[A bullet of three words is a label pretending to be "
                        "a point]"]),
        ph17="Source: [Document, page, line]. KPMG analysis")

# ---------------------------------------------------------- findings with RAG
s = add(prs, "Key findings_2 columns")
fill(s, title="[Finding, both columns]",
        ph54="[Workstream one]",
        ph74="[Workstream two]",
        ph56=[("[Finding]", 0),
              ("[What was observed, and the number that carries it]", 1)],
        ph76=[("[Finding]", 0),
              ("[What was observed, and the number that carries it]", 1)],
        ph55="[Recommendation, not a restatement of the finding]",
        ph75="[Recommendation, not a restatement of the finding]",
        # gate_rag_key string-matches for "red is" / "traffic light".
        # Phrase the scale this way or the gate fails the build.
        ph17="Source: [Document, page]. Traffic light: red is high risk, amber "
             "is medium, green is low. KPMG analysis")
strapline(s, "[Strapline. One assertion covering both workstreams]")
rag(s, 72, "amber")
rag(s, 77, "green")

# ------------------------------------------------------------ exhibit page
s = add(prs, "Analysis_Horizontal")
drop(s, 54, 55)
fill(s, title="[What the exhibit proves]",
        ph18="[Strapline. The so-what of the exhibit]",
        ph56=[("Reading the exhibit", 0),
              ("[Prose, short paragraphs, one idea each. The read reaches the "
               "bottom of the page or the composition is wrong]", 1),
              ("[Second paragraph. Numbers do the work: state the movement and "
               "its driver]", 1)])
ex.chart_exhibit(
    s, "column",
    ["FY22", "FY23", "FY24", "FY25"],
    [("[Series A]", [100, 108, 121, 138]),
     ("[Series B]", [100, 104, 103, 111])],
    title="[Exhibit title, stating what this shows]",
    basis="ILLUSTRATIVE ONLY. Indexed to 100 at FY22. Not measured data",
    chart_id="C1",
    source="Source: ILLUSTRATIVE. This exhibit carries no measured data",
    draw_source=False,
    left=GRID["left"], top=3.73, width=13.70, height=9.00,
    legend=True)
note(s, "Source: ILLUSTRATIVE. This exhibit carries no measured data")

# ------------------------------------------------------- financial summary
s = add(prs, "Summary Financials_5 blocks")
fill(s, title="[The financial finding]",
        ph18="[Strapline. What the five blocks add up to]",
        ph10="[Revenue]", ph12="[Gross margin]", ph14="[EBITDA]",
        ph15="[Working capital]", ph16="[Net debt]",
        ph17="Source: ILLUSTRATIVE. Management accounts [period]. KPMG analysis")

# ------------------------------------------------------------------- section 2
s = add(prs, "Section divider")
fill(s, title="2. Basis of preparation")

s = add(prs, "One Column Text")
fill(s, title="[Basis, limitations and reliance]",
        ph18="[Strapline stating the single largest limitation]",
        ph56=[("Basis of preparation", 0),
              ("[What the work was based on, over what period, and what was "
               "excluded from scope]", 1),
              ("Reliance", 0),
              ("[Who may rely on this document and on what terms]", 1)],
        ph17="Source: Engagement letter dated [date]")

s = add(prs, "Back Cover_Report")

# ------------------------------------------------------------------------- out
save(prs, "report-template.pptx")
databooklet.write("report-template-databook.xlsx",
                  deck_name="Report template")
print("booklet check:", databooklet.check_booklet(prs) or "clean")
print("built: report-template.pptx")
