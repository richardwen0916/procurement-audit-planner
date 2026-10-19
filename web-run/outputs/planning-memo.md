# Procurement audit: planning memo

*Generated 2026-10-19 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 1, build 1c50332c723c), `auditor-comments.md`, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

## Purpose

Plan an audit of procurement against the Contract Procedure Rules, using risk indicators found by testing the full spend population rather than a small random sample. Each indicator is a pattern to investigate, not a finding of non-compliance by the council, any service or any supplier.
Scope note for the auditor: the internal audit of Personal Budgets (Direct Payments), AUD-16, gave limited assurance and sits in no approved risk, and every sample excludes direct payment narratives; the auditor may add a risk if it should be tested.
Care and education placements are shown separately in the analytics and are exempt from competition under CPR-53; samples draw from general procurement unless a test says otherwise.

## Background

8,534 payments over the publication floor across 3 months were tested against the Rules [metric:$.population.rows_after_exclusions].
Rows excluded as statutory, inter-authority or redacted-payee payments are logged in the analytics [metric:$.population.excluded].

## Scope

The register lists 7 rated risks. The auditor recorded 7 decisions: 7 risks are approved and in scope, and 0 are not.

| ID | Risk | Score | Band | Decision | Auditor comment |
|---|---|---|---|---|---|
| R-01 | Requirements split below the quotation and notice threshold | 20 | Extreme (Red) | approve |  |
| R-02 | Payments clustered just below the quotation threshold | 9 | Medium - High (Amber) | amend | Lower likelihood to 3. 10 payments sit just below £25k against 52 just above (46 vs 52 across all spend), so the data shows no clustering below the threshold. │ │ (12)                        │          │  Keep in scope as a targeted test of the 10 payments. (auditor override applied) |
| R-03 | High-value suppliers with no contract notice found | 20 | Extreme (Red) | approve |  |
| R-04 | Spend continuing after matched contract notices ended | 12 | Medium - High (Amber) | approve |  |
| R-05 | Spend running above the annual rate of the award | 15 | Extreme (Red) | approve |  |
| R-06 | Same supplier, same amount paid more than once within a short period | 12 | Medium - High (Amber) | approve |  |
| R-07 | Waivers, exceptions and award approvals not evidenced | 6 | Moderate | approve |  |

## Approach

Seven risks were rated on the council's own likelihood and impact method and approved by the auditor, who lowered the likelihood of R-02. Each risk is tied to the control the Rules require, a test step and a targeted sample drawn by script from the flagged lists.
Tests for R-03 and R-05 come first in the plan so the split-window test for R-01 skips suppliers already drawn there; the same payments are not tested twice.

The programme holds 10 expected controls and 12 test steps, with 534 sampled transactions worth £24,399,269.38, each traceable to its row in the council's published workbooks (see `audit-program.md` and `outputs/samples/`).

## Rules coverage

19 of 54 rules in `rules.json` are cited by a risk, a control or a test. The remaining 35 are not tested in this audit, for these reasons:

- decision, governance or scope clause outside the spend data; documents are requested under R-07 where they bear on approvals: CPR-01, CPR-02, CPR-03, CPR-04, CPR-05, CPR-17, CPR-18, CPR-40, CPR-41
- tender-process or advertising step; the spend data does not show how a tender was run and the notice export holds publication only: CPR-07, CPR-09, CPR-10, CPR-11, CPR-12, CPR-13, CPR-44
- excluded-contract or Provider Selection Regime route; the spend data does not show which route a payment used, so the approval is requested only through the R-07 document tests: CPR-47, CPR-48
- contract documentation, record-keeping, bond or sealing step; checked from the contract file, not from payments: CPR-20, CPR-21, CPR-22, CPR-24, CPR-25, CPR-26, CPR-27, CPR-28, CPR-29, CPR-30, CPR-31, CPR-32, CPR-33, CPR-34, CPR-35, CPR-36, CPR-37

## Limitations

- The spend data is expenditure over the publication floor only, so split and duplicate counts are lower bounds. Payment dates are payment-run timestamps, not invoice dates.
- The notice export is not a contract register: a supplier with no matching notice may hold an older or unpublished contract. Annualised estimates are distorted by seasonal or one-off spend.
- Statutory-threshold tiers were not tested because the threshold value was not supplied, and no contract register was available, so matching uses published notices only [metric:$.skipped].
- Waivers, approvals and variations are not visible in public data, so those tests rely on documents the client provides.
- The inter-authority and non-procurement payee word lists err in both directions; fieldwork should drop any sampled payee that is a public body or not a purchase.

## Review and sign-off

The challenger's points and their status are in `challenges.md`; points marked *for the auditor* need a decision at sign-off. The QA reviewer's checks and verdict are in `review.md`, which ends with the sign-off block.
