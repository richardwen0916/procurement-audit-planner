# Procurement risk register (West Berkshire Council)

**Revision 1** · build `0dcdcc47e846` · built 2026-10-16T16:26:05
Inputs: analytics.json (2026-10-15T15:55:20), history.json (2026-10-15), rules.json, risk-ratings.json.

## Revision 1: changes since revision 0

Applied auditor decisions on register rev 0 (build 7e7648b89f26): eight risks approved unchanged, R-08 likelihood raised by auditor override.

| Risk | Field | From | To | Auditor decision | Auditor comment | Override |
|---|---|---|---|---|---|---|
| R-08 | likelihood.score | 2 | 3 | Amend (R-08) | Raise likelihood to 3: awards above £500,000 are rare but carry the highest stakes. | **Auditor override** |
| R-08 | likelihood.justification | text revised | text revised | Amend (R-08) | Raise likelihood to 3: awards above £500,000 are rare but carry the highest stakes. |  |

Approved without change: R-01, R-02, R-03, R-04, R-05, R-06, R-07, R-09.

## Method

Scored on the council's own method: likelihood 1–5 × impact 1–5 from the risk-management-strategy-2024-27.pdf (Table 2 likelihood, Table 1 impact, Figure 1 matrix, Table 4 bands). Score = likelihood × impact, which every printed cell of Figure 1 equals.
Assessment level: **actual** (current likelihood and impact, based on mitigation action already put in place but excluding further mitigation action planned).

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
- Corporate Risk Register threshold conflicts: used **5.13 Table 4** (score 15 or above), because that table defines the bands and their escalation. Not used: 6.3 Figure 4 (score 9 or above). Risks that qualify only under the unused reading are marked †.
- Impact £ bands share endpoints (£17,500, £175,000, £500,000, £2,000,000). Convention used: a value equal to a shared endpoint goes to the higher band, unless the higher band is printed as strictly greater ('>'), when it stays in the lower band.

Discrepancies recorded in history.json for this document. Scores and labels are read only from Table 1, Table 2, Figure 1 and Table 4, so any discrepancy not resolved above does not change a score:

- DSC-01 (4.3): Prose labels Medium as (2); Table 1 prints Medium as 3.
- DSC-02 (Table 1): Financial % bands overlap: Major 0.25%-1% vs Medium 0.1%-0.3%. £ bands share endpoints (£500k, £175k, £17.5k, £2m) with no stated inclusive/exclusive rule.
- DSC-03 (Table 1, Personal / Staff or Customers column): Personal/Staff column for Minor (2) and Negligible (1) contains financial-loss text (£1,000+ / up to £1,000) separate from the Financial column.
- DSC-04 (Table 4 vs Figure 1 p.18): Table 4 names the 8-12 band 'Medium - High (Amber)'; Figure 1 labels those cells 'High'. Moderate (4-6) row prints no RAG colour.
- DSC-05 (Figure 4 vs Table 4 p.19): Corporate Risk Register inclusion: Figure 4 says score 9 or above; Table 4 says 15-25 'Add to Corporate Risk Register'; 6.3 says Extreme (Red) risks are considered for Directorate or Corporate register.
- DSC-06 (5.10 vs Table 3): Reputation appetite is set as 'Open', but the first sentence uses wording of the Table 3 'Cautious' cell ('Little chance of significant repercussions'); the paragraph later says the Council is seeking an open reputational risk.
- DSC-07 (6.3): Typo 'extrene' for 'Extreme' as printed.
- DSC-08 (Objective after 5.18): p.20 objective says 'increased risk appetite'; p.9 objective says 'changed risk appetite'.
- DSC-10 (5.8): Appetite is identified by shading in Table 3, which is not recoverable from the text; levels recorded from 5.10 only. Compliance is 'Flexible/Open' (between two columns).

## Summary

| Risk | Title | L | I | Score | Matrix (Fig. 1) | Band (Table 4) | Corporate register | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Requirements split below the quotation threshold | 4 | 5 | **20** | Extreme | Extreme (Red) | yes | Approved |
| R-03 | High-value suppliers with no contract notice found | 4 | 5 | **20** | Extreme | Extreme (Red) | yes | Approved |
| R-05 | Spend above the award's annual rate | 3 | 5 | **15** | Extreme | Extreme (Red) | yes | Approved |
| R-02 | Payments clustered just below the quotation threshold | 4 | 3 | **12** | High | Medium - High (Amber) | † 6.3 Figure 4 | Approved |
| R-04 | Spend continuing after every matched contract notice ended | 3 | 4 | **12** | High | Medium - High (Amber) | † 6.3 Figure 4 | Approved |
| R-06 | Same supplier paid the same amount within seven days | 4 | 3 | **12** | High | Medium - High (Amber) | † 6.3 Figure 4 | Approved |
| R-08 | Contract awards not approved at the required level | 3 | 3 | **9** | High | Medium - High (Amber) | † 6.3 Figure 4 | Approved |
| R-07 | Waivers and exceptions to competition not approved and documented | 2 | 3 | **6** | Moderate | Moderate (not printed) | no | Approved |
| R-09 | Placement exemption applied without recorded reasons or board approval | 2 | 2 | **4** | Moderate | Moderate (not printed) | no | Approved |

† Qualifies for the Corporate Risk Register only under the reading not used (see Scoring-method conflicts).

## R-01: Requirements split below the quotation threshold

**Risk.** Related payments to one supplier within a short window may together reach a threshold that each single payment stays under, so the Portal quotation requirements of CPR-54 and CPR-55 may not be applied, contrary to the anti-splitting rule CPR-12.

**Likelihood: 4 (Almost Certain).** Rubric L4. 64 general-procurement supplier windows of 30 days combine payments each under the threshold to a total at or above it [M1], an indicator that CPR-12 may not operate.

**Impact: 5 (Critical), financial.** The flagged general-procurement windows total £3,442,571.49 in the three-month window [M2].

**Score: 4 × 5 = 20** · Matrix: Extreme · Band: Extreme (Red) · Escalation: Add to Corporate Risk Register and mitigation action. · Response: Allocate to Executive Director to oversee and Service Director implement agreed actions.

**Evidence.**

- Tier tested: £25,000.00, the App B quotation band CPR-54; the auditor has not yet confirmed this tier for the test.
- Lower tier (single quote, CPR-53): 108 general-procurement windows totalling £293,334.13 [M3].
- Tender tier (CPR-56): 3 general-procurement windows totalling £5,133,960.69 [M4].
- Placements shown separately and not counted: 178 windows, exempt from competition under CPR-63.
- Statutory-threshold tiers were not tested because the threshold values are not supplied: STATUTORY_THRESHOLD_GOODS_SERVICES is null (auditor has not supplied it); no statutory-threshold band tested. A skipped test is not a zero.
- Payments of the publication floor or less are not published, so the count is a lower bound [M5]; recurring periodic charges can also form windows.
- The last Contract Letting audit gave Reasonable Assurance AUD-01; not adverse, so no uplift.

**Proposed focus.** Take the largest general-procurement windows and establish whether each is one requirement; for those that are, seek the Portal quotation evidence required by CPR-54 or an approved waiver under CPR-19.

**Sources.**

- CPR-54: clause App B row B1, p.12: goods or services, total value exclusive of VAT £25,000 or more and less than the Threshold
- CPR-55: clause App B row B2, p.12: works, concession or light touch contracts, total value exclusive of VAT £25,000 or more and less than £500,000
- CPR-12: clause 6.16, p.5: any contract or requirement
- CPR-53: clause App B row A, p.12: total value exclusive of VAT above £1,000 and less than £25,000
- CPR-56: clause App B row C, p.12: works, concession or light touch contracts, total value exclusive of VAT above £500,000 and less than the Threshold (works/concessions or light touch threshold as applicable)
- CPR-63: clause App C row F, p.15: specified individual social care placements and packages (items a–f)
- CPR-19: clause 7.2 (7.2.1–7.2.2), p.6: contract with a value of more than £24,999.99 where competition is excepted or waived
- AUD-01: Contract Letting (completed audit), Reasonable Assurance, period to 2025-03-31 [audit-completed-work-2024-25-annual.pdf p.1]
- M1: `$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows` = 64
- M2: `$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp` = £3,442,571.49
- M3: `$.tests.split_purchases.by_threshold.1000.headline_general_procurement` = {"gbp":293334.13,"suppliers":80,"windows":108}
- M4: `$.tests.split_purchases.by_threshold.500000.headline_general_procurement` = {"gbp":5133960.69,"suppliers":2,"windows":3}
- M5: `$.tests.split_purchases.caveat` = payments of £500 or less are not published, so these counts are lower bounds; periodic care fees legitimately recur

## R-03: High-value suppliers with no contract notice found

**Risk.** Suppliers whose annualised spend reaches the publication threshold may be paid without a competed, published and registered contract, so the requirements of CPR-54, CPR-57 and the contract-register notification of CPR-34 may not operate.

**Likelihood: 4 (Almost Certain).** Rubric L4. 186 general-procurement suppliers at or above the publication threshold have no exact name match to an active Contracts Finder notice [M1]. No notice found is an indicator to investigate, not evidence that no contract exists.

**Impact: 5 (Critical), financial.** Their annualised estimate is £98,553,147.20 [M2], scaled from the three-month window and distorted by seasonal or one-off spend.

**Score: 4 × 5 = 20** · Matrix: Extreme · Band: Extreme (Red) · Escalation: Add to Corporate Risk Register and mitigation action. · Response: Allocate to Executive Director to oversee and Service Director implement agreed actions.

**Evidence.**

- No council contract register was supplied, so matching used published notices only: data/contract-register.csv absent: matching uses Contracts Finder notices only [M3].
- Exact matches: 40 suppliers; near-miss names for the auditor to confirm: 2 by similarity and 4 by containment, never counted as matches [M4].
- Spend data carries no company number, so matching is on normalised names only [M5].
- Placements shown separately: 303 unmatched suppliers, expected to have few notices under CPR-63.
- Publication threshold used: £25,000.00; suppliers below it are not classed and must not be questioned on this basis [M6]. The auditor has not yet confirmed this tier.
- The inter-authority exclusion has a known limitation: inter_authority supplier regex is a fixed word list; it can catch non-public bodies whose name contains e.g. COUNTY (see spend-excluded.csv) [M7]. At least one excluded supplier has been identified as not a public body, so its spend sits outside this test.
- The register-publication duty CPR-07 cannot be checked because no register was supplied.

**Proposed focus.** Request the council's contract register and, for the largest unmatched general-procurement suppliers, the contract or framework call-off and the competition evidence required by CPR-54 or CPR-57; confirm or reject each near-miss name match.

**Sources.**

- CPR-54: clause App B row B1, p.12: goods or services, total value exclusive of VAT £25,000 or more and less than the Threshold
- CPR-57: clause App B row D, p.12: goods, services, works, concession or light touch contracts, total value exclusive of VAT above the Threshold
- CPR-34: clause 10.4, p.8: award of every contract
- CPR-63: clause App C row F, p.15: specified individual social care placements and packages (items a–f)
- CPR-07: clause 5.2.1, p.3: all contracts in progress and awarded
- CPR-55: clause App B row B2, p.12: works, concession or light touch contracts, total value exclusive of VAT £25,000 or more and less than £500,000
- M1: `$.tests.off_contract.headline_unmatched_general_procurement.suppliers` = 186
- M2: `$.tests.off_contract.headline_unmatched_general_procurement.annualised_estimate_gbp` = £98,553,147.20
- M3: `$.tests.off_contract.caveat` = contracts.csv holds published *notices*, not a contract register. It holds awards published on Contracts Finder in roughly the last five years. A contract aw…
- M4: `$.matching.note` = near matches are candidates for the auditor to confirm and are never counted as matches
- M5: `$.matching.companies_house_matching` = not possible: spend data carries no company number
- M6: `$.tests.off_contract.scope_note` = Only suppliers at or above the publication threshold are classed; Contracts Finder does not carry smaller awards, so results must never be used to question s…
- M7: `$.population.excluded.inter_authority.reason` = Payments to other public bodies (councils, NHS, police, fire, HMRC, government departments) or joint arrangements are not competitive procurement (Private Co…

## R-05: Spend above the award's annual rate

**Risk.** Annualised spend well above a contract's awarded annual rate may indicate a variation of scope without the approvals required by CPR-62.

**Likelihood: 3 (Likely).** Rubric L3. 8 of 19 eligible suppliers have an annualised estimate at or above 1.25 times the award's annual rate [M1].

**Impact: 5 (Critical), financial.** Annualised estimate for the flagged suppliers: £2,946,603.88 [M2].

**Score: 3 × 5 = 15** · Matrix: Extreme · Band: Extreme (Red) · Escalation: Add to Corporate Risk Register and mitigation action. · Response: Allocate to Executive Director to oversee and Service Director implement agreed actions.

**Evidence.**

- Award values may be estimates or maxima and spend may relate to other arrangements; a high ratio is an indicator only [M3].
- Eligibility is narrow (one live single-supplier notice with a positive value), so the test covers few suppliers [M4].
- Contract management is a named source of risk in the council's strategy RT-12.

**Proposed focus.** For each flagged supplier, compare spend with the contract's priced scope and look for a variation approved by the Monitoring Officer and S151 Officer, or by the relevant board, as CPR-62 requires.

**Sources.**

- CPR-62: clause App C row E, p.14: variation of scope of an existing contract (provided for in the contract or permitted by Procurement Legislation)
- RT-12: source of risk: contracts & partnerships – contractor failure, procurement contract and relationship management [risk-management-strategy-2024-27.pdf p.33]
- M1: `$.tests.spend_vs_award.flagged_ratio_ge_threshold` = 8
- M2: `$.tests.spend_vs_award.flagged_annualised_estimate_gbp` = £2,946,603.88
- M3: `$.tests.spend_vs_award.caveat` = Award values may be estimates or maxima, contract periods may include optional extensions, and spend may relate to other arrangements; a high ratio is an ind…
- M4: `$.tests.spend_vs_award.parameters.eligibility` = exact name match; supplier on exactly one active notice; that notice single-supplier with Awarded Value > 0 and both dates present

## R-02: Payments clustered just below the quotation threshold

**Risk.** Single payments falling just below the quotation threshold may indicate requirements valued or invoiced to stay under it, so the competition steps of CPR-54 and CPR-55 may not be applied.

**Likelihood: 4 (Almost Certain).** Rubric L4. 10 general-procurement payments fall in the band just below the threshold [M1] set by CPR-54.

**Impact: 3 (Medium), financial.** Those payments total £239,427.82 in the window [M2].

**Score: 4 × 3 = 12** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Band tested: 0.9*T to T with the threshold at £25,000.00; the auditor has not yet confirmed this tier.
- Comparator, all tags: 46 payments in the band below against 52 in the band above [M3]. Clustering is read against this comparator, not from the count alone.
- Placements shown separately: 30 payments, exempt under CPR-63.
- Lower tier (CPR-53): 88 general-procurement payments just below that threshold [M4].
- No general-procurement payments fall just below the higher tiers [M5]; statutory tiers were skipped (STATUTORY_THRESHOLD_GOODS_SERVICES is null (auditor has not supplied it); no statutory-threshold band tested).

**Proposed focus.** For the flagged general-procurement payments, obtain the requirement's estimated total value and check whether it was a single requirement that should have followed CPR-54; read the result against the above-band comparator.

**Sources.**

- CPR-54: clause App B row B1, p.12: goods or services, total value exclusive of VAT £25,000 or more and less than the Threshold
- CPR-55: clause App B row B2, p.12: works, concession or light touch contracts, total value exclusive of VAT £25,000 or more and less than £500,000
- CPR-63: clause App C row F, p.15: specified individual social care placements and packages (items a–f)
- CPR-53: clause App B row A, p.12: total value exclusive of VAT above £1,000 and less than £25,000
- M1: `$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement.count` = 10
- M2: `$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement.gbp` = £239,427.82
- M3: `$.tests.threshold_clustering.by_threshold.25000.above_band_comparator.count` = 52
- M4: `$.tests.threshold_clustering.by_threshold.1000.below_band_by_tag.general_procurement.count` = 88
- M5: `$.tests.threshold_clustering.by_threshold.500000.below_band_by_tag.general_procurement.count` = 0

## R-04: Spend continuing after every matched contract notice ended

**Risk.** Suppliers paid in the spend window whose only matched notices had already ended may be paid under an extension without the S151 Officer approval required by CPR-61.

**Likelihood: 3 (Likely).** Rubric L3. 7 general-procurement suppliers were paid in the window although every exact-matched notice ended before it began [M1]; a newer contract may exist with no notice.

**Impact: 4 (Major), financial.** Annualised estimate for these suppliers: £761,467.68 [M2]; window spend £190,366.92.

**Score: 3 × 4 = 12** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Of these, 4 suppliers are at or above the publication threshold [M3].
- Notices are not a register; extensions and replacement contracts may be unpublished [M4].
- Contract management and contractor delivery are a named source of risk in the council's strategy RT-12.

**Proposed focus.** For each flagged supplier, obtain the current contract and any extension, and check for S151 Officer approval under CPR-61 dated before the extended period began.

**Sources.**

- CPR-61: clause App C row D, p.14: extension to an existing contract that provides for such extension
- RT-12: source of risk: contracts & partnerships – contractor failure, procurement contract and relationship management [risk-management-strategy-2024-27.pdf p.33]
- M1: `$.tests.expired_notice_spend.by_dominant_tag.general_procurement` = 7
- M2: `$.tests.expired_notice_spend.annualised_estimate_gbp` = £761,467.68
- M3: `$.tests.expired_notice_spend.at_or_above_publication_threshold.suppliers` = 4
- M4: `$.tests.expired_notice_spend.caveat` = contracts.csv holds published *notices*, not a contract register. It holds awards published on Contracts Finder in roughly the last five years. A contract aw…

## R-06: Same supplier paid the same amount within seven days

**Risk.** Payments of identical amounts to one supplier within seven days on separate payment runs may indicate a duplicate payment or a purchase without its own written evidence CPR-31.

**Likelihood: 4 (Almost Certain).** Rubric L4. 35 general-procurement groups of same-amount payments fall on two or more payment runs within seven days [M1], the higher-signal tier, against the written-evidence rule CPR-31.

**Impact: 3 (Medium), financial.** Value beyond the first payment in each group: £299,374.24 [M2], the most that could be recoverable if every repeat were a duplicate.

**Score: 4 × 3 = 12** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Same-run groups (lower signal, typical of a batch of equal invoices): 33 in general procurement [M3].
- Placements shown separately: 204 different-run groups, where periodic fees legitimately recur.
- Payments at or below the publication floor are not published, so counts are lower bounds [M4].
- The last Accounts Payable audit gave Reasonable Assurance AUD-15; not adverse, so no uplift.

**Proposed focus.** For the different-run general-procurement groups, match each payment to its invoice and order to confirm separate supplies, and check any confirmed duplicate for recovery.

**Sources.**

- CPR-31: clause 10.1, p.8: every purchase
- AUD-15: Accounts Payable (completed audit), Reasonable Assurance, period to 2025-12-31 [audit-completed-work-2025-26-q3.pdf p.1]
- M1: `$.tests.duplicates.tiers.different_time.by_dominant_tag.general_procurement.groups` = 35
- M2: `$.tests.duplicates.tiers.different_time.by_dominant_tag.general_procurement.gbp_beyond_first` = £299,374.24
- M3: `$.tests.duplicates.tiers.same_timestamp.by_dominant_tag.general_procurement.groups` = 33
- M4: `$.tests.duplicates.caveat` = payments of £500 or less are not published, so counts are lower bounds

## R-08: Contract awards not approved at the required level

**Risk.** Contract awards may be made without the delegated authority, board report or Key Decision that Appendix A and CPR-04 require for their value.

**Likelihood: 3 (Likely).** Rubric L2. No public-data test can measure award approvals: they are held only in council records CPR-50, so the risk is rated on the rule and the gap CPR-04. The rubric row is L2; the score is raised to Likely by auditor override, per the auditor's comment: "Raise likelihood: awards above £500,000.00 are rare but carry the highest stakes."

**Impact: 3 (Medium), compliance.** An award above the Key Decision level not taken as a Key Decision CPR-04 fits Table 1 Medium: reasonable possibility of successful legal challenge. *Table 1 compliance descriptor for 3: "Reasonable possibility of successful legal challenge. Reasonable possibility of regulatory interest.".*

**Score: 3 × 3 = 9** · Matrix: High · Band: Medium - High (Amber) · Escalation: Seek assurance that identified controls are effective · Response: Allocate to Service Director to put in place Controls Assurance.

**Evidence.**

- Context: 3 general-procurement supplier windows exceed the tender tier within thirty days [M1], indicating arrangements whose value may require a Key Decision.
- The Appendix A tiers for awards between the threshold and the Key Decision level depend on the statutory threshold, which is not supplied (STATUTORY_THRESHOLD_GOODS_SERVICES is null (auditor has not supplied it); no statutory-threshold band tested).
- The last Contract Letting audit gave Reasonable Assurance AUD-01; not adverse, so no uplift.

**Proposed focus.** For a sample of awards in the period, including the arrangements behind the tender-tier windows, check the approval record against the value tier in CPR-49 to CPR-52 and Key Decision status under CPR-04.

**Sources.**

- CPR-04: clause 4.3, p.3: contract award with a value over £500,000
- CPR-50: clause App A row 2, p.11: Total Contract Value above the relevant threshold and less than £500,000
- CPR-49: clause App A row 1, p.11: Total Contract Value up to the relevant Threshold
- CPR-52: clause App A row 4, p.11: Total Contract Value £2.5million or more (cell text: in excess of £2.5million)
- CPR-51: clause App A row 3, p.11: Total Contract Value above £500,000 and less than £2.5million
- AUD-01: Contract Letting (completed audit), Reasonable Assurance, period to 2025-03-31 [audit-completed-work-2024-25-annual.pdf p.1]
- M1: `$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows` = 3

## R-07: Waivers and exceptions to competition not approved and documented

**Risk.** Competition may be waived or excepted without the advance approval, written exception report and S151 Officer record that CPR-20, CPR-25 and CPR-26 require.

**Likelihood: 2 (Unlikely).** Rubric L2. No public-data test can measure this control: waivers are held only in council records CPR-24, so it is rated on the rule and the gap, not on observed data CPR-26.

**Impact: 3 (Medium), compliance.** An unapproved waiver removes competition the Rules require above the quotation band CPR-19; this fits Table 1 Medium: reasonable possibility of successful legal challenge. *Table 1 compliance descriptor for 3: "Reasonable possibility of successful legal challenge. Reasonable possibility of regulatory interest.".*

**Score: 2 × 3 = 6** · Matrix: Moderate · Band: Moderate (not printed) · Escalation: None · Response: Monitor risk

**Evidence.**

- The Rules name different approvers for exceptions (Executive Director or Chief Executive in CPR-19; Monitoring Officer or S151 Officer only in CPR-20); the auditor should confirm which applies.
- Unmatched high-value suppliers ([M1]) are a population in which waivers, if any, would be found.

**Proposed focus.** Obtain the waiver and exception log for the spend window and test a sample for advance approval, a written exception report and the S151 Officer's record under CPR-26; cross-check against the unmatched high-value suppliers.

**Sources.**

- CPR-20: clause 7.3, p.6: any waiver or exception to these Rules
- CPR-25: clause 7.5.2, p.6: exception or waiver for a contract where competition is not excluded by Procurement Legislation
- CPR-26: clause 7.5.3, p.7: every exception or waiver
- CPR-24: clause 7.5.1, p.6: every exception or waiver
- CPR-19: clause 7.2 (7.2.1–7.2.2), p.6: contract with a value of more than £24,999.99 where competition is excepted or waived
- M1: `$.tests.off_contract.headline_unmatched_general_procurement.suppliers` = 186

## R-09: Placement exemption applied without recorded reasons or board approval

**Risk.** Care and education placements are exempt from competition only where the reasons for the choice of provider are recorded CPR-63 and, above the threshold, the relevant board approves CPR-64; these records may be missing.

**Likelihood: 2 (Unlikely).** Rubric L2. No public-data test can measure this control: the reasons sit in individual case notes CPR-63 and board approvals in council records CPR-64. Personal Budgets (Direct Payments) received Limited Assurance AUD-16, but direct payments are funds given to individuals to arrange their own support, not a provider chosen by the council under this exemption, so the theme differs and no uplift is applied.

**Impact: 2 (Minor), compliance.** A missing case-note reason is a record gap on an exempt purchase CPR-63; this fits Table 1 Minor: low possibility of legal challenge, low possibility of regulatory interest. *Table 1 compliance descriptor for 2: "Low possibility of legal challenge. Low possibility regulatory interest".*

**Score: 2 × 2 = 4** · Matrix: Moderate · Band: Moderate (not printed) · Escalation: None · Response: Monitor risk

**Evidence.**

- Scale: placement spend in the window is £30,571,711.30 across 361 suppliers [M1], and placements dominate the split-purchase and duplicate flags [M2].
- The last audit of residential and nursing care purchasing gave Reasonable Assurance AUD-18; not adverse, so no uplift.

**Proposed focus.** For a sample of placement suppliers, check the case-note record of provider choice under CPR-63 and, where the annual value is above the threshold, the board approval under CPR-64.

**Sources.**

- CPR-63: clause App C row F, p.15: specified individual social care placements and packages (items a–f)
- CPR-64: clause App C closing note, p.15: any contract where an Appendix C exemption is applied, with annual or total value more than the Threshold
- AUD-16: Personal Budgets (Direct Payments) (completed audit), Limited Assurance, period to 2025-12-31 [audit-completed-work-2025-26-q3.pdf p.1]
- AUD-18: Purchase of Residential and Nursing Care Provision (completed audit), Reasonable Assurance, period to 2025-12-31 [audit-completed-work-2025-26-q3.pdf p.1]
- M1: `$.population.tags.care_or_education_placement.gbp` = £30,571,711.30
- M2: `$.tests.split_purchases.by_threshold.25000.placement_separately.windows` = 178

*Builder warnings: 1 (see build output).*

## Auditor decisions

Record one decision per risk in `outputs/auditor-comments.md`: **Approve**, **Amend** (with a comment) or **Reject** (out of scope). Decided: 9 of 9.

| Risk | Decision | Comment |
|---|---|---|
| R-01 | Approve |  |
| R-02 | Approve |  |
| R-03 | Approve |  |
| R-04 | Approve |  |
| R-05 | Approve |  |
| R-06 | Approve |  |
| R-07 | Approve |  |
| R-08 | Amend | Raise likelihood to 3: awards above £500,000 are rare but carry the highest stakes. |
| R-09 | Approve |  |
