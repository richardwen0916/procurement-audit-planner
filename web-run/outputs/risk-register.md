# Procurement risk register (West Berkshire Council)

**Revision 1** · build `1c50332c723c` · built 2026-10-19T06:31:01
Inputs: analytics.json (2026-10-19T05:44:46), history.json (2026-10-19), rules.json, risk-ratings.json.

## Revision 1: changes since revision 0

Applied auditor decisions of 2026-10-19.

| Risk | Field | From | To | Auditor decision | Auditor comment | Override |
|---|---|---|---|---|---|---|
| R-02 | likelihood.score | 4 | 3 | Amend (R-02) | Lower likelihood to 3. 10 payments sit just below £25k against 52 just above (46 vs 52 across all spend), so the data shows no clustering below the threshold. │ │ (12)                        │          │  Keep in scope as a targeted test of the 10 payments. | **Auditor override** |
| R-02 | likelihood.justification | text revised | text revised | Amend (R-02) | Lower likelihood to 3. 10 payments sit just below £25k against 52 just above (46 vs 52 across all spend), so the data shows no clustering below the threshold. │ │ (12)                        │          │  Keep in scope as a targeted test of the 10 payments. |  |

Approved without change: R-01, R-03, R-04, R-05, R-06, R-07.

## Method

Scored on the council's own method: likelihood 1–5 × impact 1–5 from the risk-management-strategy-2024-27.pdf (Table 2 likelihood, Table 1 impact, Figure 1 matrix, Table 4 bands). Score = likelihood × impact, which every printed cell of Figure 1 equals.
Assessment level: **actual** (current likelihood and impact, based on mitigation already in place, excluding further planned action).

Likelihood rubric (applied by the risk-assessor, checked by the builder against the cited count):

| Row | Score | Evidence |
|---|---|---|
| L1 | 1 | full-population test found 0 instances in general procurement |
| L2 | 2 | no public-data test can measure the risk (rated Unlikely, never Rare) |
| L3 | 3 | test found 1–9 instances |
| L4 | 4 | test found 10 or more instances |
| L5 | 5 | an open agreed action states the control is not operating |

A repeat finding (a past audit on the same theme with an adverse opinion) raises likelihood by one point, capped at 5, and is stated on the risk.

These are **risk indicators to investigate**, not findings of non-compliance or wrongdoing by the council, any service or any supplier.

### Scoring-method conflicts

How the builder resolved conflicts in the method (one reading used, the other marked):

- Band names differ between the matrix (Figure 1) and the band table (Table 4): Figure 1 'High' = Table 4 'Medium - High'. The register shows both: *Matrix* is the Figure 1 label, *Band* the Table 4 level.
- Table 4 prints no RAG colour name for 'Moderate'; shown as 'not printed'.
- Corporate Risk Register threshold conflicts: used **5.13, Table 4** (score 15 or above), because that table defines the bands and their escalation. Not used: 6.3, Figure 4 (score 9 or above). Risks that qualify only under the unused reading are marked †.
- Impact £ bands share endpoints (£17,500, £175,000, £500,000, £2,000,000). Convention used: a value equal to a shared endpoint goes to the higher band, unless the higher band is printed as strictly greater ('>'), when it stays in the lower band.

Discrepancies recorded in history.json for this document. Scores and labels are read only from Table 1, Table 2, Figure 1 and Table 4, so any discrepancy not resolved above does not change a score:

- DSC-01 (4.3 / Table 1): None
- DSC-02 (5.13 Table 4 vs 6.3 Figure 4): None
- DSC-03 (Table 1): None
- DSC-04 (Table 4 vs Figure 1): None
- DSC-05 (6.3): None
- DSC-06 (Table 2): None
- DSC-07 (5.8 Table 3 vs 4.3 Table 1): None

## Summary

| Risk | Title | L | I | Score | Matrix (Fig. 1) | Band (Table 4) | Corporate register | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Requirements split below the quotation and notice threshold | 4 | 5 | **20** | Extreme | Extreme (Red) | yes | Approved |
| R-03 | High-value suppliers with no contract notice found | 4 | 5 | **20** | Extreme | Extreme (Red) | yes | Approved |
| R-05 | Spend running above the annual rate of the award | 3 | 5 | **15** | Extreme | Extreme (Red) | yes | Approved |
| R-04 | Spend continuing after matched contract notices ended | 3 | 4 | **12** | High | Medium - High (Amber) | † 6.3, Figure 4 | Approved |
| R-06 | Same supplier, same amount paid more than once within a short period | 4 | 3 | **12** | High | Medium - High (Amber) | † 6.3, Figure 4 | Approved |
| R-02 | Payments clustered just below the quotation threshold | 3 | 3 | **9** | High | Medium - High (Amber) | † 6.3, Figure 4 | Approved |
| R-07 | Waivers, exceptions and award approvals not evidenced | 2 | 3 | **6** | Moderate | Moderate (not printed) | no | Approved |

† Qualifies for the Corporate Risk Register only under the reading not used (see Scoring-method conflicts).

## R-01: Requirements split below the quotation and notice threshold

**Risk.** Related payments to one supplier may together reach a threshold that each single payment stays under, so the quotation and Portal requirements of CPR-43 may not have been applied, contrary to the anti-splitting rule CPR-08.

**Likelihood: 4 (Almost Certain).** Rubric L4. 64 supplier windows in general procurement combine to reach the threshold within 30 days [M1]. Counts are lower bounds because payments at or below the publication floor are not published. No adverse past audit on this theme, so no uplift.

**Impact: 5 (Critical), financial.** The flagged windows total £3,442,571.49 in the period [M2].

**Score: 4 × 5 = 20** · Matrix: Extreme · Band: Extreme (Red) · Escalation: Add to Corporate Risk Register and mitigation action. · Response: Allocate to Executive Director to oversee and Service Director implement agreed actions.

**Evidence.**

- Placements shown separately: 178 windows, exempt from competition under CPR-53.
- Windows may reflect legitimate recurring services; each is an indicator to test, not a finding.

**Proposed focus.** Test the largest general-procurement windows for a single underlying requirement and for the quotation evidence required by CPR-43.

**Sources.**

- CPR-43: clause App B row B1, p.12: goods or services contract, total value £25,000 or more and less than the Threshold
- CPR-08: clause 6.16, p.5: any contract
- CPR-53: clause App C row F, p.15: social care services listed in row F (a–f)
- CPR-42: clause App B row A, p.12: total value exclusive of VAT above £1,000 and less than £25,000
- M1: `$.tests.split_purchases.by_threshold.25000.headline_general_procurement` = {"gbp":3442571.49,"suppliers":42,"windows":64}
- M2: `$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp` = £3,442,571.49

## R-03: High-value suppliers with no contract notice found

**Risk.** Suppliers whose annualised spend reaches the publication threshold may have no matching published contract notice, so competition and publication under CPR-43, CPR-46 and CPR-06 may not have been followed, or the contract may sit outside the notice export.

**Likelihood: 4 (Almost Certain).** Rubric L4. 186 general-procurement suppliers at or above the threshold have no matching active notice [M1]. The notice export is not a contract register, so many may hold unpublished or older contracts [M2].

**Impact: 5 (Critical), financial.** The annualised estimate for these suppliers is £98,553,147.20 [M3]; seasonal or one-off spend distorts annualisation.

**Score: 4 × 5 = 20** · Matrix: Extreme · Band: Extreme (Red) · Escalation: Add to Corporate Risk Register and mitigation action. · Response: Allocate to Executive Director to oversee and Service Director implement agreed actions.

**Evidence.**

- Exact notice matches: 40 suppliers; near-name candidates: 2 by ratio and 4 by containment, for the auditor to confirm.
- Care and education placements (303 unmatched suppliers) are excluded from the count; they are exempt under CPR-53.
- Contract register: data/contract-register.csv absent: matching uses Contracts Finder notices only

**Proposed focus.** Obtain the contract file or exception record for the largest unmatched general-procurement suppliers and confirm the route to market.

**Sources.**

- CPR-43: clause App B row B1, p.12: goods or services contract, total value £25,000 or more and less than the Threshold
- CPR-46: clause App B row D, p.12: goods and services, works, concession or light touch contract above the Threshold
- CPR-06: clause 6.10, p.4: contract opportunity above the relevant Procurement Legislation threshold
- CPR-53: clause App C row F, p.15: social care services listed in row F (a–f)
- CPR-54: clause App C note, p.15: any exemption applied; contract with annual or total value of more than the Threshold
- M1: `$.tests.off_contract.headline_unmatched_general_procurement` = {"annualised_estimate_gbp":98553147.2,"suppliers":186}
- M2: `$.contracts` = {"active_in_window":62,"caveat":"contracts.csv holds published *notices*, not a contract register. It holds awards published on Contracts Finder in roughly t…
- M3: `$.tests.off_contract.headline_unmatched_general_procurement.annualised_estimate_gbp` = £98,553,147.20

## R-05: Spend running above the annual rate of the award

**Risk.** Annualised payments above the award's annual rate may indicate scope or value growth without the variation approvals of CPR-51 and CPR-52.

**Likelihood: 3 (Likely).** Rubric L3. 8 of 19 eligible suppliers exceed the flag ratio of 1.25 [M1]. Variation approvals are not visible in public data. No adverse past audit on this theme, so no uplift.

**Impact: 5 (Critical), financial.** The flagged annualised estimate is £2,946,603.88 [M2].

**Score: 3 × 5 = 15** · Matrix: Extreme · Band: Extreme (Red) · Escalation: Add to Corporate Risk Register and mitigation action. · Response: Allocate to Executive Director to oversee and Service Director implement agreed actions.

**Evidence.**

- Awarded values may be estimates or maxima and periods may include extensions, so a high ratio is an indicator only.

**Proposed focus.** Compare payments with the contract value and obtain variation approvals for the flagged suppliers.

**Sources.**

- CPR-51: clause App C row E, p.14: variation of scope of an existing contract where the contract provides for it or the Procurement Legislation permits; value below the Threshold
- CPR-52: clause App C row E, p.14: variation of scope of an existing contract (as above); value greater than the Threshold
- M1: `$.tests.spend_vs_award.parameters` = {"award_annual_rate":"Awarded Value / contract years (end - start days / 365.25)","eligibility":"exact name match; supplier on exactly one active notice; tha…
- M2: `$.tests.spend_vs_award.flagged_annualised_estimate_gbp` = £2,946,603.88

## R-04: Spend continuing after matched contract notices ended

**Risk.** Payments may continue after the only matching contract notice ended without the S151 Officer approval of an extension required by CPR-50; a newer contract may exist without a notice.

**Likelihood: 3 (Likely).** Rubric L3. 7 general-procurement suppliers were paid in the window with every matched notice ended [M1]. Extension approvals are not visible in public data. No adverse past audit on this theme, so no uplift.

**Impact: 4 (Major), financial.** The annualised estimate for these suppliers is £761,467.68 [M2].

**Score: 3 × 4 = 12** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Of these, 4 are at or above the publication threshold.
- Notices hold dates only; extension options are not in the export, so some may be approved extensions.

**Proposed focus.** Request extension approvals under CPR-50 or the replacement contract for each supplier.

**Sources.**

- CPR-50: clause App C row D, p.14: extension to an existing contract where the contract provides for the extension
- M1: `$.tests.expired_notice_spend.by_dominant_tag` = {"agency_staff":0,"care_or_education_placement":0,"general_procurement":7,"grant":0,"premises_non_procurement":0}
- M2: `$.tests.expired_notice_spend.annualised_estimate_gbp` = £761,467.68

## R-06: Same supplier, same amount paid more than once within a short period

**Risk.** Repeat payments of an identical amount to one supplier within a short period may indicate duplicate payment, and purchase evidence required by CPR-23 may not support each payment.

**Likelihood: 4 (Almost Certain).** Rubric L4. 35 general-procurement groups were paid at different timestamps within 7 days [M1]. A past Accounts Payable audit gave a non-adverse opinion AUD-15, so no uplift. No rule specifically requires duplicate-payment checks; the rating rests on the metric.

**Impact: 3 (Medium), financial.** Amounts beyond the first payment total £299,374.24 [M1].

**Score: 4 × 3 = 12** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Same-timestamp batch groups (general procurement): 33, a lower-signal tier.
- Recurring charges of equal value are common; counts are lower bounds.

**Proposed focus.** Trace the largest groups to invoices and confirm each payment was for a separate supply.

**Sources.**

- CPR-23: clause 10.1, p.8: all purchases
- AUD-15: Accounts Payable (completed audit), Reasonable Assurance, period to 2025-12-31 [audit-completed-work-2025-26-q3.pdf p.1]
- M1: `$.tests.duplicates.tiers.different_time.by_dominant_tag` = {"agency_staff":{"gbp_beyond_first":0.0,"groups":0},"care_or_education_placement":{"gbp_beyond_first":2880203.06,"groups":204},"general_procurement":{"gbp_be…

## R-02: Payments clustered just below the quotation threshold

**Risk.** A concentration of single payments just under the threshold may indicate values being kept below the point at which CPR-43 applies.

**Likelihood: 3 (Likely).** Rubric L4. 10 general-procurement payments sit in the band just below the threshold [M1], against 52 in the comparator band just above it across all spend [M2]. No adverse past audit on this theme, so no uplift. Auditor amendment (comment of 2026-10-19): likelihood lowered because the below-band count is not higher than the count just above the threshold, so the data shows no clustering below the threshold; kept in scope as a targeted test of the payments in the band.

**Impact: 3 (Medium), financial.** The clustered general-procurement payments total £239,427.82 [M3].

**Score: 3 × 3 = 9** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Below-band payments across all spend tags: 46; the statutory-threshold tiers were not tested: STATUTORY_THRESHOLD_GOODS_SERVICES is null (auditor has not supplied it); no statutory-threshold band tested

**Proposed focus.** Review the quotation evidence for the largest payments in the band and whether they relate to a larger requirement.

**Sources.**

- CPR-43: clause App B row B1, p.12: goods or services contract, total value £25,000 or more and less than the Threshold
- CPR-42: clause App B row A, p.12: total value exclusive of VAT above £1,000 and less than £25,000
- CPR-08: clause 6.16, p.5: any contract
- M1: `$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement` = {"count":10,"gbp":239427.82}
- M2: `$.tests.threshold_clustering.by_threshold.25000.above_band_comparator` = {"count":52,"gbp":1366203.77}
- M3: `$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement.gbp` = £239,427.82

*Builder warnings: 3 (see build output).*

## R-07: Waivers, exceptions and award approvals not evidenced

**Risk.** Exceptions to the Rules and contract awards may lack the written approvals required by CPR-14, CPR-19 and CPR-39. Public spend data cannot show approvals or waivers.

**Likelihood: 2 (Unlikely).** Rubric L2. No public-data test can observe waivers or award approvals, so this is rated on the rule CPR-14 and the data gap, not on a count. Absence of evidence is not evidence of absence. The notice export records publication only, not approvals [M1]; history.json lists no agreed actions on this control, so L5 is not met.

**Impact: 3 (Medium), compliance.** Table 1 compliance descriptor for this score: 'Reasonable possibility of successful legal challenge. Reasonable possibility of regulatory interest.' Awards without the approvals of CPR-39 could attract challenge THM-04. *Table 1 compliance descriptor for 3: "Reasonable possibility of successful legal challenge. Reasonable possibility of regulatory interest.".*

**Score: 2 × 3 = 6** · Matrix: Moderate · Band: Moderate (not printed) · Escalation: None · Response: Monitor risk

**Evidence.**

- Contract notices in the export: 141, which is a publication record, not an approvals record.

**Proposed focus.** Request the exception register and award decision records and test a sample against CPR-19 and CPR-39.

**Sources.**

- CPR-14: clause 7.3, p.6: any waiver or exception to the Rules
- CPR-19: clause 7.5.3, p.7: any exception or waiver
- CPR-39: clause App A row 2, p.11: total contract value above the relevant threshold and less than £500,000
- CPR-15: clause 7.4.1, p.6: exception for contract up to the Threshold
- CPR-16: clause 7.4.2, p.6: exception for contract above the relevant Threshold and up to £500,000
- CPR-38: clause App A row 1, p.11: total contract value up to the relevant Threshold
- THM-04: compliance (legal) risk appetite, high value transactions [risk-management-strategy-2024-27.pdf p.17]
- M1: `$.contracts` = {"active_in_window":62,"caveat":"contracts.csv holds published *notices*, not a contract register. It holds awards published on Contracts Finder in roughly t…

## Auditor decisions

Record one decision per risk in `outputs/auditor-comments.md`: **Approve**, **Amend** (with a comment) or **Reject** (out of scope). Decided: 7 of 7.

| Risk | Decision | Comment |
|---|---|---|
| R-01 | Approve |  |
| R-02 | Amend | Lower likelihood to 3. 10 payments sit just below £25k against 52 just above (46 vs 52 across all spend), so the data shows no clustering below the threshold. │ │ (12)                        │          │  Keep in scope as a targeted test of the 10 payments. |
| R-03 | Approve |  |
| R-04 | Approve |  |
| R-05 | Approve |  |
| R-06 | Approve |  |
| R-07 | Approve |  |
