---
type: proposal-section
section: 10
---

# Appendices and back cover

**Every reference ends the same way**: a `Section divider` titled *Appendices*,
the CVs, any supporting analysis, then `Back Cover_Proposal`. Eight to fifteen
pages, most of them CVs.

## Appendices

**CVs first.** One `Two Columns Text` page per person, in the format in [[team]].
Where the appendix carries more than CVs, a `Subsection divider` opens each
part: *Appendix A: Team's CV*, *Appendix B: Budget*.

**Supporting analysis second**, where the pursuit produced any. Seen across the
references:

| Appendix | Shape |
|---|---|
| *Budget* | The detailed build-up behind the fee page |
| *Key value drivers of Target's business (1/6)…* | Prose on `One Column Text`, continued |
| *Benchmarking analysis (1/3)…* | Exhibits on `One Column Text` |
| *Integration blueprint*, *People strategy*, *Technology integration strategy* | Each on its own subsection divider, one to three pages |
| *A set of analytic methods mapped to your value levers* | One diagram page |

Supporting analysis is where the outside-in work goes when the body would
otherwise run long. It is read by the buyer's team rather than the buyer.

## Back cover

`Back Cover_Proposal`. On the pre-2025 master this carried contacts and a
disclaimer; on the 2025 master the layout is fixed artwork with no placeholders,
so contacts and disclaimer are hand-placed if the layout leaves room, or go on a
final `Title only_Blank` page before it.

| Element | Geometry on the reference |
|---|---|
| Lead | y 3.70 — *"The contacts at KPMG in connection with this proposal are:"* |
| Contacts | y 6.90, 6.60 cm per block, three to five across, each with a photo at y 4.90 — name, title and workstream, *T:*, *E:* |
| Social line | y 10.10 to 11.60 — *kpmg.com/cn/socialmedia* |
| Disclaimer | y 10.60 to 12.40, full width, 6pt |

**The disclaimer is boilerplate in three paragraphs.** The engagement-letter
paragraph:

> *This proposal is made by KPMG Advisory (Hong Kong) Limited, a Hong Kong
> limited liability company and a member firm of the KPMG network of independent
> member firms affiliated with KPMG International Cooperative ("KPMG
> International"), a Swiss entity, and is in all respects subject to the
> negotiation, agreement and signing of a specific engagement letter or
> contractual terms and to the satisfactory completion of our applicable client
> and engagement acceptance procedures, including conflict of interest checks.
> KPMG International provides no client services. No member firm has any
> authority to obligate or bind KPMG International or any other member firm
> vis-à-vis third parties, nor does KPMG International have any such authority to
> obligate or bind any member firm.*

The confidentiality paragraph, with the client named:

> *This document has been prepared specifically for [Client]. It contains
> confidential or proprietary KPMG information, the disclosure of which would
> provide a competitive advantage to others. It is not to be used or duplicated
> for any purpose other than to evaluate KPMG and is not to be disclosed or
> referred to, in whole or in part, without our prior written consent. The
> restriction pertains to all data throughout the entire document.*

The trademark and copyright lines:

> *The KPMG name and logo are trademarks used under license by the independent
> member firms of the KPMG global organisation.*
>
> *© [year] KPMG Advisory (Hong Kong) Limited, a Hong Kong (SAR) limited
> liability company and a member firm of the KPMG global organisation of
> independent member firms affiliated with KPMG International Limited ("KPMG
> International"), a private English company limited by guarantee. All rights
> reserved. Printed in Hong Kong (SAR).*

The two references disagree on the entity wording — *KPMG International
Cooperative, a Swiss entity* against *KPMG International Limited, a private
English company limited by guarantee*. The second is the current form. Use it.

## Conventions

- The contacts are the engagement lead and the workstream leads, the same people
  as the front of the team page
- The year in the copyright line is the year of issue, checked at delivery
- The client is named in the confidentiality paragraph even where the deal is
  code-named elsewhere, because the document is addressed to them

## Checks

- Every CV in the appendix belongs to someone on the team page or named as an
  SME in the scope
- The disclaimer carries the current entity wording
- The deck ends on `Back Cover_Proposal`. `qa.gate_deck_type_closer` enforces it
  once `new_deck(kind="proposal")` is declared

## Related

- [[Proposal]] · [[team]] · [[fees]]
