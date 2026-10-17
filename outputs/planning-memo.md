# Procurement audit: planning memo

*Generated 2026-10-16 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 1, build 0dcdcc47e846), `auditor-comments.md` by Richard Wen dated 2026-10-16, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

## Purpose

This audit seeks assurance that the council's Contract Procedure Rules operate over its purchasing: that requirements are valued as a whole before a route is chosen, that competition, waivers, extensions and variations carry the approvals the Rules require, and that payments rest on written evidence. The analytics surface risk indicators to investigate, not findings: each pattern below has legitimate explanations, and the tests ask whether the expected control was in place.
Grants are out of scope: the auditor recorded that they are not rated in this register and will be covered by a separate review.

## Background

The full published expenditure population from 2026-05-01 to 2026-07-31 (3 months) was analysed: 8,534 payments worth £66,778,104.78 after statutory, redacted and inter-authority payments were set aside [metric:$.population.rows_after_exclusions].
General procurement accounts for 2,126 payments worth £28,318,367.76 to 518 suppliers; care and education placements, exempt from competition under App C row F, for £30,571,711.30 [metric:$.population.tags.general_procurement.gbp].
Headline indicators in general procurement: 64 supplier windows of thirty days where payments each under the quotation threshold together reach it; 186 suppliers at or above the publication threshold with no exact match to a live contract notice; 8 of 19 eligible suppliers paid at or above 1.25 times the award's annual rate; 7 suppliers paid after every matched notice ended; 35 same-amount groups on different payment runs within seven days; and 10 payments just below the quotation threshold.
The last Contract Letting and Accounts Payable audits gave Reasonable Assurance; no repeat adverse finding raised any rating.

## Scope

The register lists 9 rated risks. The auditor recorded 9 decisions by Richard Wen dated 2026-10-16: 9 risks are approved and in scope, and 0 are not.

| ID | Risk | Score | Band | Decision | Auditor comment |
|---|---|---|---|---|---|
| R-01 | Requirements split below the quotation threshold | 20 | Extreme (Red) | approve |  |
| R-02 | Payments clustered just below the quotation threshold | 12 | Medium - High (Amber) | approve |  |
| R-03 | High-value suppliers with no contract notice found | 20 | Extreme (Red) | approve |  |
| R-04 | Spend continuing after every matched contract notice ended | 12 | Medium - High (Amber) | approve |  |
| R-05 | Spend above the award's annual rate | 15 | Extreme (Red) | approve |  |
| R-06 | Same supplier paid the same amount within seven days | 12 | Medium - High (Amber) | approve |  |
| R-07 | Waivers and exceptions to competition not approved and documented | 6 | Moderate | approve |  |
| R-08 | Contract awards not approved at the required level | 9 | Medium - High (Amber) | amend | Raise likelihood to 3: awards above £500,000 are rare but carry the highest stakes. (auditor override applied) |
| R-09 | Placement exemption applied without recorded reasons or board approval | 4 | Moderate | approve |  |

## Approach

The Rules were turned into testable rules with clause references; Python tested the whole population against them; past audit coverage was read from Governance Committee papers. Risks were rated on the council's own likelihood and impact scale, and the auditor approved all nine, raising the likelihood of R-08 by override.
For each approved risk the programme names the control the Rules require, cites the rule, and sets a test step with the evidence to inspect. Samples are targeted, not random: each is drawn by the builder from the flagged list behind the risk's metric, largest value first, sized by score (ten items for a score of nine or more, five below), general procurement only except where the risk concerns placements. Split windows and duplicate groups are drawn whole so each can be judged as one requirement. Tests that rest on council records alone (waivers, award approvals) pair a log request with a targeted sample.
Fieldwork order: R-01, R-03 and R-05 first (Extreme band), then the Amber risks, then R-07 and R-09. The programme lists R-03 and R-08 first so that the split-purchase sample skips suppliers whose contracts those tests already pull.

The programme holds 10 expected controls and 15 test steps, with 385 sampled transactions worth £20,889,335.84, each traceable to its row in the council's published workbooks (see `audit-program.md` and `outputs/samples/`).

## Rules coverage

35 of 64 rules in `rules.json` are cited by a risk, a control or a test. The remaining 29 are not tested in this audit, for these reasons:

- sets a duty outside the approved risks (social value record, budget provision); neither is visible in the spend data: CPR-01, CPR-03
- transparency or reporting duty; the published spend data is itself the expenditure publication, and no approved risk addresses tender publication or monthly board reporting: CPR-05, CPR-06, CPR-08
- applies above the statutory threshold, whose value was not supplied, so it cannot be tied to the spend data: CPR-10, CPR-11, CPR-13, CPR-46
- conduct of a tender (portal security, late tenders, opening, evaluation, award criteria); no approved risk addresses tender conduct: CPR-14, CPR-15, CPR-16, CPR-17, CPR-18
- record-retention period; checked only incidentally when documents are requested: CPR-29
- contract drafting, sealing, indemnities, bonds, insurance and Counsel: legal formalities no approved risk addresses: CPR-33, CPR-35, CPR-36, CPR-37, CPR-38, CPR-39, CPR-40, CPR-41, CPR-43, CPR-44, CPR-45, CPR-47, CPR-48
- Provider Selection Regime records; no approved risk addresses health-care provider selection: CPR-59

## Limitations

- Only payments over the publication floor are published, so split-purchase and duplicate counts are lower bounds [metric:$.tests.split_purchases.caveat].
- Contract notices are not a contract register: no register was supplied, so 'no notice found' and 'notice ended' are indicators only, and suppliers below the publication threshold are never questioned on this basis [metric:$.tests.off_contract.scope_note].
- Annualised figures scale the window by 4 and are distorted by seasonal or one-off spend; award values may be estimates or maxima [metric:$.tests.spend_vs_award.caveat].
- Supplier matching to contract notices uses normalised names only, because the spend data carries no company number [metric:$.matching.companies_house_matching]; the spend-versus-award test covers only 19 eligible suppliers, those on one live single-supplier notice with a positive value [metric:$.tests.spend_vs_award.parameters.eligibility].
- Statutory-threshold tiers were not tested because the threshold values were not supplied; the auditor has not yet confirmed the quotation tier used. The award-tier and board-approval grading in T-08.1, T-08.2 and T-09.1 depends on the Threshold values in force, requested on the PBC list.
- Payment dates are payment-run timestamps, not invoice dates.
- The inter-authority word list both sets aside some non-public suppliers and misses some public bodies with abbreviated names, so the headline unmatched count includes a few public bodies; samples leave out council, NHS, police and fire payees by name pattern.
- Approvals of waivers, awards, extensions and variations are held only in council records, so their tests depend on the PBC list.
- CPR-19 and CPR-20 name different approvers for a waiver; until the auditor settles which applies, T-07.1 records the approver against both and refers any approval meeting only one rule to the auditor.

## Review and sign-off

The challenger's points and their status are in `challenges.md`; points marked *for the auditor* need a decision at sign-off. The QA reviewer's checks and verdict are in `review.md`, which ends with the sign-off block.
