# Audit program

*Generated 2026-10-16 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 1, build 0dcdcc47e846), `auditor-comments.md` by Richard Wen dated 2026-10-16, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

9 risks in scope, 10 controls, 15 tests, 385 sampled transactions. Samples are drawn by the builder from `analytics-full/` by the recipe stated under each test, and every transaction is listed with its workbook row.


## R-03: High-value suppliers with no contract notice found [20 (Extreme; Extreme (Red))]

**Audit objective.** Conclude whether the council's largest suppliers with no matching contract notice are paid under a competed, written and registered contract or a properly approved framework call-off.

**C-03.1. Expected control.** Spend at or above the quotation band rests on a written contract let by the competition the Rules require for its value, after a recorded check of the supplier's suitability and financial standing, or on a Purchasing Scheme call-off with recorded advice and Monitoring Officer approval. [CPR-54, CPR-55, CPR-56, CPR-57, CPR-32, CPR-27, CPR-60, CPR-09] Owner: Relevant Service Director.

**T-03.1. Test.** For each sampled supplier, obtain the contract or call-off covering the sampled payments and the competition evidence for its value tier: Portal quotations for goods or services, or for works, concession or light touch contracts below the tender band; a full tender above it; or the Purchasing Scheme advice and approval. Inspect the recorded pre-award check of the supplier's suitability and financial standing. Pass: a written contract or call-off covering the payments, let by the route its value and type require, with the suitability check recorded before award. [CPR-54, CPR-55, CPR-57, CPR-32, CPR-60, metric:$.tests.off_contract.headline_unmatched_general_procurement.suppliers, CPR-09]  
**Evidence to inspect:** Signed contract or call-off, tender or quotation record, framework access advice and Monitoring Officer approval, pre-award supplier suitability and financial standing check  
**Sample:** 10 items from `off-contract.csv`, where match_class = none, dominant_tag = general_procurement, largest annualised_estimate first, 3 payments per supplier, excluding supplier_norm matching /\b(?:COUNCIL|CNCL|NHS|POLICE|FIRE AND RESCUE|FIRE AUTHORITY|HMRC|WALLET|PREPAID|PAYPOINT)\b/; 30 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:793` | 2026-07-13 | VolkerHighways Ltd | £998,987.64 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:603` | 2026-07-28 | VolkerHighways Ltd | £855,750.25 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:684` | 2026-06-22 | VolkerHighways Ltd | £366,872.38 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:2196` | 2026-05-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,201,856.40 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:2146` | 2026-06-29 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,180,425.32 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3194` | 2026-07-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £1,803,783.32 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:2144` | 2026-06-25 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:2216` | 2026-06-03 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:3789` | 2026-07-29 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:665` | 2026-05-15 | The Better Group Ltd | £64,500.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:666` | 2026-05-15 | The Better Group Ltd | £58,833.00 | Adult Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:670` | 2026-06-01 | The Better Group Ltd | £48,784.37 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 6 | `Over500_2026_P02_-_published.xlsx:2200` | 2026-05-13 | Livity Life Ltd | £135,591.03 | Finance, Property & Procurement |
| 6 | `Over500_2026_P03_-_published.xlsx:3087` | 2026-06-17 | Livity Life Ltd | £127,886.78 | Finance, Property & Procurement |
| 6 | `Over500_2026_P04_-_published.xlsx:3310` | 2026-07-13 | Livity Life Ltd | £50,961.45 | Finance, Property & Procurement |
| 7 | `Over500_2026_P04_-_published.xlsx:784` | 2026-07-10 | E W BEARD LTD | £64,202.50 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:674` | 2026-05-20 | E W BEARD LTD | £60,039.70 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:675` | 2026-05-20 | E W BEARD LTD | £55,594.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:183` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £73,296.50 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:203` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £26,085.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:208` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £17,607.50 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:661` | 2026-06-08 | ANDY AND ES LIMITED | £59,335.72 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:1283` | 2026-07-15 | ANDY AND ES LIMITED | £56,941.82 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:670` | 2026-05-13 | ANDY AND ES LIMITED | £54,881.31 | Education & SEND |
| 10 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 10 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 10 | `Over500_2026_P04_-_published.xlsx:533` | 2026-07-28 | Elior UK PLC | £23,173.08 | Adult Social Care |

**C-03.2. Expected control.** Every contract award is notified to the Service Lead for Commissioning and Procurement and entered on the published contract register. [CPR-34, CPR-07] Owner: Service Lead for Commissioning and Procurement.

**T-03.2. Test.** Obtain the contract register. For each near-miss name candidate, confirm whether the supplier paid is the supplier on the candidate notice; for every supplier sampled in this risk, confirm the contract appears on the register. Pass: identity confirmed or rejected with evidence, and each contract registered. [CPR-34, CPR-07, metric:$.tests.off_contract.per_match_class.near_contain.suppliers, metric:$.tests.off_contract.per_match_class.near_ratio.suppliers]  
**Evidence to inspect:** Contract register entries, award notifications to Procurement, supplier master data  
**Sample:** 6 items from `off-contract.csv`, where match_class = ['near_ratio', 'near_contain'], largest annualised_estimate first, 1 payments per supplier, (only 6 available); 6 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:173` | 2026-05-26 | Glen Cleaning Company Ltd | £5,829.96 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:247` | 2026-07-09 | BAILEYS OF NEWBURY | £6,592.17 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:278` | 2026-07-14 | D J TRAVEL | £7,035.00 | Adult Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:817` | 2026-06-01 | Swan Advocacy | £7,178.24 | Adult Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:232` | 2026-07-10 | Kennet & Avon Group | £2,970.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:297` | 2026-07-08 | POTTINGER'S HIRE SERVICE | £1,981.67 | Education & SEND |


## R-08: Contract awards not approved at the required level [9 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether contract awards are approved at the delegated level set for their value, including Key Decision status for the highest tiers.

**C-08.1. Expected control.** Each award is made only under a decision within the Scheme of Delegation at the Appendix A tier for its total contract value, with the written procurement report and board approval where required, and taken as a Key Decision where the value requires it. Works contracts estimated above the bond level without a performance bond carry a written risk assessment approved by the Service Director for Finance and Property. [CPR-02, CPR-04, CPR-49, CPR-50, CPR-51, CPR-52, CPR-28, CPR-42] Owner: Relevant Service Director.

**T-08.1. Test.** For each sampled tender-tier window, identify the contract the payments fall under and its total contract value; obtain the award decision and check it against the Appendix A tier, the written procurement report and Key Decision status. For works contracts, check that a performance bond is held or that a written risk assessment approved by the Service Director for Finance and Property is on the contract file. Pass: an award decision at or above the required level, dated before the contract, and a bond or approved risk assessment for works contracts. The Appendix A tier is set from the Threshold values in force, which the council must supply. [CPR-04, CPR-51, CPR-52, CPR-42, CPR-56, metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows]  
**Evidence to inspect:** Award decision record, delegated decision or Executive report, written procurement report, Forward Plan or Key Decision record, performance bond or bond risk assessment and its approval  
**Sample:** 3 items from `split-purchases.csv`, where threshold = 500000, dominant_tag = general_procurement, largest window_total first, largest 3 payments per item, (only 3 available); 9 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:699` | 2026-06-08 | VolkerHighways Ltd | £329,988.88 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:701` | 2026-06-09 | VolkerHighways Ltd | £307,338.45 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:729` | 2026-06-08 | VolkerHighways Ltd | £299,416.56 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:684` | 2026-06-22 | VolkerHighways Ltd | £366,872.38 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:619` | 2026-07-15 | VolkerHighways Ltd | £195,182.14 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:795` | 2026-07-14 | VolkerHighways Ltd | £161,847.24 | Environment |
| 3 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 3 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 3 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |

**T-08.2. Test.** For each sampled supplier with a matching notice and a large annualised estimate, obtain the award decision for the noticed contract and check it as in T-08.1. Pass: award approved at the Appendix A tier for the contract's total value. The tier is set from the Threshold values in force. [CPR-49, CPR-50, CPR-51, CPR-28, metric:$.tests.off_contract.per_match_class.exact.suppliers]  
**Evidence to inspect:** Contract notice, award decision record, written procurement report, Key Decision record where applicable  
**Sample:** 7 items from `off-contract.csv`, where match_class = exact, dominant_tag = general_procurement, annualised_estimate ≥ 500000, largest annualised_estimate first, 1 payments per supplier, excluding suppliers and rows already drawn in T-08.1, (only 7 available); 7 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:437` | 2026-05-20 | Newbury & District Ltd | £60,797.19 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:669` | 2026-05-26 | ASCIA CONSTRUCTION LIMITED | £332,579.29 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:905` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £129,125.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P03_-_published.xlsx:2130` | 2026-06-09 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 5 | `Over500_2026_P04_-_published.xlsx:450` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £9,615.23 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:321` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,074.00 | Education & SEND |
| 7 | `Over500_2026_P04_-_published.xlsx:260` | 2026-07-13 | BROADWAY CARS | £5,487.69 | Education & SEND |


## R-01: Requirements split below the quotation threshold [20 (Extreme; Extreme (Red))]

**Audit objective.** Conclude whether related purchases from one supplier are aggregated and valued as one requirement before the procurement route is chosen, so that the quotation requirements apply where the combined value reaches them.

**C-01.1. Expected control.** Requirements are valued in total and not split or disaggregated; where the combined value reaches the quotation band, invitations to quote go via the Procurement Portal to at least three sources, the payments are call-offs under a written contract or Purchasing Scheme let by the route the total value requires, or an approved waiver is held. [CPR-12, CPR-54, CPR-55, CPR-30, CPR-60] Owner: Relevant Service Director.

**T-01.1. Test.** For each sampled window, obtain the orders and invoices behind the payments and establish whether they relate to one requirement. Where they do, obtain the Portal quotation record (at least three invitations), the written contract or Purchasing Scheme call-off the payments fall under with its award route, or an approved waiver. Pass: separate requirements evidenced; or quotation evidence, a contract or call-off let by the route its total value requires, or a waiver held for the combined value. Suppliers already drawn in T-03.1 and T-08.1 are left out here: their windows are judged on the contract evidence those tests obtain. [CPR-12, CPR-54, CPR-19, CPR-60, metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows]  
**Evidence to inspect:** Purchase orders, invoices, requirement specification, Procurement Portal quotation record, contract or Purchasing Scheme call-off and its award record, waiver approval where relevant  
**Sample:** 10 items from `split-purchases.csv`, where threshold = 25000, dominant_tag = general_procurement, largest window_total first, one item per supplier_norm, excluding supplier_norm matching /\b(?:COUNCIL|CNCL|NHS|POLICE|FIRE AND RESCUE|FIRE AUTHORITY|HMRC|WALLET|PREPAID|PAYPOINT)\b/, narratives matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/, excluding suppliers and rows already drawn in T-03.1, T-08.1; 149 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:268` | 2026-06-01 | Newbury & District Ltd | £13,826.61 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:357` | 2026-06-01 | Newbury & District Ltd | £6,349.35 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:171` | 2026-06-02 | Newbury & District Ltd | £10,529.33 | Education & SEND |
| 1 | `Over500_2026_P03_-_published.xlsx:336` | 2026-06-02 | Newbury & District Ltd | £9,861.00 | Education & SEND |
| 1 | `Over500_2026_P03_-_published.xlsx:341` | 2026-06-02 | Newbury & District Ltd | £794.67 | Education & SEND |
| 1 | `Over500_2026_P03_-_published.xlsx:264` | 2026-06-12 | Newbury & District Ltd | £6,331.70 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:269` | 2026-06-12 | Newbury & District Ltd | £14,852.00 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:176` | 2026-06-30 | Newbury & District Ltd | £7,785.00 | Education & SEND |
| 1 | `Over500_2026_P03_-_published.xlsx:213` | 2026-06-30 | Newbury & District Ltd | £8,312.63 | Education & SEND |
| 1 | `Over500_2026_P03_-_published.xlsx:251` | 2026-06-30 | Newbury & District Ltd | £627.37 | Education & SEND |
| 1 | `Over500_2026_P03_-_published.xlsx:274` | 2026-06-30 | Newbury & District Ltd | £13,663.85 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:359` | 2026-06-30 | Newbury & District Ltd | £5,921.50 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:360` | 2026-06-30 | Newbury & District Ltd | £4,465.96 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:181` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £1,197.90 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:183` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £8,226.54 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:195` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £730.27 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:196` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £862.12 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:245` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £1,214.56 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:246` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £4,549.40 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:253` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £2,118.96 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:300` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £999.32 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:301` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £1,039.14 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:302` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £7,911.27 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:309` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £2,974.60 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:450` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £9,615.23 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:451` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £574.66 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:452` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £9,483.38 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:459` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £2,312.52 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:192` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £6,662.12 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:197` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £614.96 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:198` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £2,504.93 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:249` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £6,927.61 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:250` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £3,831.07 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:305` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £7,986.00 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:310` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £1,784.39 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:311` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £1,947.39 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:456` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £8,097.04 | Education & SEND |
| 2 | `Over500_2026_P04_-_published.xlsx:460` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £726.00 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:1287` | 2026-07-13 | Roadside Technologies Ltd | £10,298.22 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:1288` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:598` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:601` | 2026-07-13 | Roadside Technologies Ltd | £9,103.64 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:733` | 2026-07-13 | Roadside Technologies Ltd | £11,188.22 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:734` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:735` | 2026-07-13 | Roadside Technologies Ltd | £21,000.00 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:740` | 2026-07-13 | Roadside Technologies Ltd | £9,103.64 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:789` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:597` | 2026-07-30 | Roadside Technologies Ltd | £1,000.00 | Environment |
| 4 | `Over500_2026_P02_-_published.xlsx:265` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,912.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:380` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,448.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:381` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,716.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:382` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,596.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:383` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,210.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:384` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,156.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:385` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,324.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:241` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,288.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:242` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £693.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:266` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,092.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:289` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,980.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:290` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,288.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:387` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,590.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:388` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,576.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:389` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,744.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:390` | 2026-05-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,079.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:251` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £742.50 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:283` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,340.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:284` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £3,120.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:294` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,244.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:422` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,910.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:423` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,622.86 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:424` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,940.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:425` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,550.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:426` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,227.50 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:427` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,925.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:428` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,745.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:429` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,608.00 | Education & SEND |
| 4 | `Over500_2026_P02_-_published.xlsx:430` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,187.50 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:164` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,380.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:184` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,490.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:228` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,775.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:229` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,760.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:255` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,710.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:333` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,380.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:346` | 2026-06-05 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,310.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:240` | 2026-05-12 | BROADWAY CARS | £1,213.33 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:288` | 2026-05-12 | BROADWAY CARS | £2,426.67 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:364` | 2026-05-12 | BROADWAY CARS | £3,747.69 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:367` | 2026-05-12 | BROADWAY CARS | £2,800.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:368` | 2026-05-12 | BROADWAY CARS | £2,100.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:369` | 2026-05-12 | BROADWAY CARS | £3,640.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:371` | 2026-05-12 | BROADWAY CARS | £2,240.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:372` | 2026-05-12 | BROADWAY CARS | £3,640.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:245` | 2026-05-13 | BROADWAY CARS | £2,076.67 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:297` | 2026-05-13 | BROADWAY CARS | £1,148.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:314` | 2026-05-13 | BROADWAY CARS | £595.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:391` | 2026-05-13 | BROADWAY CARS | £1,785.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:394` | 2026-05-13 | BROADWAY CARS | £3,220.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:395` | 2026-05-13 | BROADWAY CARS | £3,640.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:396` | 2026-05-13 | BROADWAY CARS | £3,010.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:403` | 2026-05-26 | BROADWAY CARS | £3,000.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:404` | 2026-05-26 | BROADWAY CARS | £4,015.38 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:249` | 2026-05-27 | BROADWAY CARS | £1,300.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:250` | 2026-05-27 | BROADWAY CARS | £2,225.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:292` | 2026-05-27 | BROADWAY CARS | £2,600.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:299` | 2026-05-27 | BROADWAY CARS | £1,230.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:326` | 2026-05-27 | BROADWAY CARS | £595.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:410` | 2026-05-27 | BROADWAY CARS | £2,400.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:411` | 2026-05-27 | BROADWAY CARS | £2,250.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:412` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:414` | 2026-05-27 | BROADWAY CARS | £3,220.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:415` | 2026-05-27 | BROADWAY CARS | £1,785.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:416` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:418` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:419` | 2026-05-27 | BROADWAY CARS | £3,010.00 | Education & SEND |
| 6 | `Over500_2026_P03_-_published.xlsx:688` | 2026-06-01 | R&A Haines Building Contractors | £20,332.89 | Development & Housing |
| 6 | `Over500_2026_P03_-_published.xlsx:733` | 2026-06-01 | R&A Haines Building Contractors | £9,666.85 | Development & Housing |
| 6 | `Over500_2026_P03_-_published.xlsx:709` | 2026-06-09 | R&A Haines Building Contractors | £5,487.25 | Development & Housing |
| 6 | `Over500_2026_P03_-_published.xlsx:740` | 2026-06-30 | R&A Haines Building Contractors | £16,600.00 | Development & Housing |
| 6 | `Over500_2026_P03_-_published.xlsx:742` | 2026-06-30 | R&A Haines Building Contractors | £18,707.55 | Development & Housing |
| 7 | `Over500_2026_P03_-_published.xlsx:2392` | 2026-06-17 | Triple Value Impact | £10,787.00 | Chief Executive |
| 7 | `Over500_2026_P03_-_published.xlsx:2393` | 2026-06-17 | Triple Value Impact | £13,110.00 | Chief Executive |
| 7 | `Over500_2026_P03_-_published.xlsx:641` | 2026-06-17 | Triple Value Impact | £13,275.00 | Chief Executive |
| 7 | `Over500_2026_P03_-_published.xlsx:642` | 2026-06-17 | Triple Value Impact | £6,612.00 | Chief Executive |
| 7 | `Over500_2026_P03_-_published.xlsx:649` | 2026-06-18 | Triple Value Impact | £24,244.00 | Chief Executive |
| 8 | `Over500_2026_P03_-_published.xlsx:173` | 2026-06-16 | SOUTHERN COACH LINES LTD | £4,043.93 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:174` | 2026-06-16 | SOUTHERN COACH LINES LTD | £6,304.46 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:175` | 2026-06-16 | SOUTHERN COACH LINES LTD | £6,754.78 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:179` | 2026-06-16 | SOUTHERN COACH LINES LTD | £819.72 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:211` | 2026-06-16 | SOUTHERN COACH LINES LTD | £6,588.28 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:216` | 2026-06-16 | SOUTHERN COACH LINES LTD | £765.07 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:217` | 2026-06-16 | SOUTHERN COACH LINES LTD | £604.54 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:218` | 2026-06-16 | SOUTHERN COACH LINES LTD | £647.72 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:250` | 2026-06-16 | SOUTHERN COACH LINES LTD | £1,020.72 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:338` | 2026-06-16 | SOUTHERN COACH LINES LTD | £4,332.78 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:180` | 2026-06-17 | SOUTHERN COACH LINES LTD | £1,268.05 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:219` | 2026-06-17 | SOUTHERN COACH LINES LTD | £1,093.63 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:220` | 2026-06-17 | SOUTHERN COACH LINES LTD | £1,358.63 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:248` | 2026-06-17 | SOUTHERN COACH LINES LTD | £7,058.87 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:249` | 2026-06-17 | SOUTHERN COACH LINES LTD | £6,213.45 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:339` | 2026-06-17 | SOUTHERN COACH LINES LTD | £6,657.26 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:2189` | 2026-05-20 | ARDENT | £9,343.75 | Environment |
| 9 | `Over500_2026_P02_-_published.xlsx:2190` | 2026-05-21 | ARDENT | £5,908.50 | Environment |
| 9 | `Over500_2026_P02_-_published.xlsx:2191` | 2026-05-21 | ARDENT | £7,956.00 | Environment |
| 9 | `Over500_2026_P02_-_published.xlsx:2192` | 2026-05-21 | ARDENT | £11,692.50 | Environment |
| 9 | `Over500_2026_P02_-_published.xlsx:761` | 2026-05-28 | ARDENT | £8,541.25 | Environment |
| 9 | `Over500_2026_P03_-_published.xlsx:696` | 2026-06-16 | ARDENT | £11,188.00 | Environment |
| 10 | `Over500_2026_P03_-_published.xlsx:667` | 2026-06-09 | Home Front Ltd | £17,160.76 | Community Services |
| 10 | `Over500_2026_P03_-_published.xlsx:679` | 2026-06-25 | Home Front Ltd | £15,875.26 | Community Services |
| 10 | `Over500_2026_P03_-_published.xlsx:697` | 2026-06-25 | Home Front Ltd | £17,160.76 | Community Services |


## R-05: Spend above the award's annual rate [15 (Extreme; Extreme (Red))]

**Audit objective.** Conclude whether spend running above a contract's awarded annual rate is within the priced scope or covered by an approved variation.

**C-05.1. Expected control.** A variation of scope receives prior written approval of the Monitoring Officer and S151 Officer below the Threshold, or of the relevant board on their recommendation above it. [CPR-62] Owner: Monitoring Officer and S151 Officer.

**T-05.1. Test.** For each sampled supplier, obtain spend to date under the contract from the supplier ledger and compare it with the Awarded Value and the contract term, pro rata to date. Where spend to date exceeds the award's rate, check for a variation of scope approved at the level CPR-62 sets before the excess arose. Pass: spend to date within the award, or any excess covered by a dated, approved variation. [CPR-62, metric:$.tests.spend_vs_award.flagged_ratio_ge_threshold]  
**Evidence to inspect:** Supplier ledger spend to date on the contract, contract and pricing schedule, variation records and approvals, board reports where above the Threshold  
**Sample:** 8 items from `spend-vs-award.csv`, where ratio ≥ 1.25, largest ratio first, all payments per supplier, (only 8 available); 31 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:905` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £129,125.00 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:492` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £91,629.15 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:487` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £52,054.00 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:494` | 2026-07-24 | NEC SOFTWARE SOLUTIONS UK LIMITED | £15,094.00 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:488` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £13,063.00 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:906` | 2026-07-28 | NEC SOFTWARE SOLUTIONS UK LIMITED | £3,750.00 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:493` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £3,000.00 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:489` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £2,771.89 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:427` | 2026-07-21 | NEC SOFTWARE SOLUTIONS UK LIMITED | £2,119.68 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:904` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £1,776.85 | Finance, Property & Procurement |
| 2 | `Over500_2026_P03_-_published.xlsx:396` | 2026-06-10 | BookingLab Limited | £24,000.00 | Transformation, Customer & ICT |
| 3 | `Over500_2026_P03_-_published.xlsx:384` | 2026-06-04 | Exacom Systems Ltd | £12,105.85 | Development & Housing |
| 4 | `Over500_2026_P04_-_published.xlsx:1276` | 2026-07-22 | WCL UK Ltd (Trading as Everything ICT) | £102,882.78 | Education & SEND |
| 5 | `Over500_2026_P03_-_published.xlsx:276` | 2026-06-30 | SMS-Environmental Ltd | £2,070.00 | Adult Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:365` | 2026-07-09 | SMS-Environmental Ltd | £1,335.60 | Adult Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:29` | 2026-06-22 | SMS-Environmental Ltd | £1,175.00 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:17` | 2026-05-28 | SMS-Environmental Ltd | £1,129.15 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:19` | 2026-05-27 | SMS-Environmental Ltd | £759.16 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:55` | 2026-05-27 | SMS-Environmental Ltd | £715.00 | Finance, Property & Procurement |
| 5 | `Over500_2026_P04_-_published.xlsx:80` | 2026-07-06 | SMS-Environmental Ltd | £575.00 | Development & Housing |
| 6 | `Over500_2026_P02_-_published.xlsx:460` | 2026-05-20 | Softcat Ltd | £8,979.02 | Education & SEND |
| 6 | `Over500_2026_P03_-_published.xlsx:375` | 2026-06-17 | Softcat Ltd | £2,025.98 | Transformation, Customer & ICT |
| 7 | `Over500_2026_P03_-_published.xlsx:371` | 2026-06-08 | IDOX SOFTWARE LTD | £48,579.20 | Community Services |
| 7 | `Over500_2026_P02_-_published.xlsx:462` | 2026-05-20 | IDOX SOFTWARE LTD | £2,647.21 | Development & Housing |
| 8 | `Over500_2026_P03_-_published.xlsx:2130` | 2026-06-09 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 8 | `Over500_2026_P04_-_published.xlsx:3181` | 2026-07-22 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 8 | `Over500_2026_P02_-_published.xlsx:2160` | 2026-05-12 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 8 | `Over500_2026_P02_-_published.xlsx:2161` | 2026-05-13 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 8 | `Over500_2026_P02_-_published.xlsx:2162` | 2026-05-27 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 8 | `Over500_2026_P03_-_published.xlsx:3080` | 2026-06-25 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 8 | `Over500_2026_P04_-_published.xlsx:3781` | 2026-07-20 | TWO SAINTS LTD | £27,147.69 | Development & Housing |


## R-02: Payments clustered just below the quotation threshold [12 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether single payments just below the quotation threshold reflect requirements whose estimated total value was correctly below it.

**C-02.1. Expected control.** The estimated total value of each requirement is recorded before the route is chosen, and requirements valued at or above the quotation band follow the Portal quotation process. [CPR-54, CPR-55, CPR-53, CPR-30] Owner: Relevant Service Director.

**T-02.1. Test.** For each sampled payment, obtain the order and the recorded estimate of the requirement's total value, and check for other orders for the same requirement. Pass: a documented estimate below the quotation band and at least one quote, or quotation evidence where the total reaches it. Read results against the above-band comparator. [CPR-54, CPR-53, metric:$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement.count, metric:$.tests.threshold_clustering.by_threshold.25000.above_band_comparator.count]  
**Evidence to inspect:** Purchase order, recorded value estimate, quotation(s), related orders for the same requirement  
**Sample:** 9 items from `threshold-clustering.csv`, where threshold = 25000, tag = general_procurement, largest Net amount first, excluding supplier_norm matching /\b(?:COUNCIL|CNCL|NHS|POLICE|FIRE AND RESCUE|FIRE AUTHORITY|HMRC|WALLET|PREPAID|PAYPOINT)\b/, (only 9 available); 9 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:1281` | 2026-07-29 | The Better Group Ltd | £24,476.02 | Adult Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:649` | 2026-06-18 | Triple Value Impact | £24,244.00 | Chief Executive |
| 3 | `Over500_2026_P02_-_published.xlsx:560` | 2026-05-12 | DevComms South East Ltd | £24,227.07 | Development & Housing |
| 4 | `Over500_2026_P03_-_published.xlsx:13` | 2026-06-01 | The Better Group Ltd | £24,088.98 | Children's Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:396` | 2026-06-10 | BookingLab Limited | £24,000.00 | Transformation, Customer & ICT |
| 6 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 7 | `Over500_2026_P03_-_published.xlsx:683` | 2026-06-08 | VolkerHighways Ltd | £23,591.22 | Environment |
| 8 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:533` | 2026-07-28 | Elior UK PLC | £23,173.08 | Adult Social Care |

**T-02.2. Test.** For each sampled payment just below the single-quote threshold, obtain the order, the recorded estimate of the requirement's value and other orders to the same supplier for the same requirement. Pass: at least one quote held where the requirement's total value is above the single-quote threshold, as CPR-53 requires. [CPR-53, metric:$.tests.threshold_clustering.by_threshold.1000.below_band_by_tag.general_procurement.count, metric:$.tests.threshold_clustering.by_threshold.1000.above_band_comparator.count]  
**Evidence to inspect:** Purchase order, recorded value estimate, quotation, related orders to the same supplier  
**Sample:** 10 items from `threshold-clustering.csv`, where threshold = 1000, tag = general_procurement, largest Net amount first, one item per supplier_norm, excluding supplier_norm matching /\b(?:COUNCIL|CNCL|NHS|POLICE|FIRE AND RESCUE|FIRE AUTHORITY|HMRC|WALLET|PREPAID|PAYPOINT)\b/, Narrative matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:34` | 2026-05-08 | BERKSHIRE MECHANICAL SERVICES | £1,000.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:597` | 2026-07-30 | Roadside Technologies Ltd | £1,000.00 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:1006` | 2026-07-14 | Becky Turner | £1,000.00 | Adult Social Care |
| 4 | `Over500_2026_P04_-_published.xlsx:613` | 2026-07-16 | ALAN FULLER | £1,000.00 | Community Services |
| 5 | `Over500_2026_P04_-_published.xlsx:535` | 2026-07-16 | BCJD Ltd | £1,000.00 | Adult Social Care |
| 6 | `Over500_2026_P04_-_published.xlsx:3787` | 2026-07-15 | VolkerHighways Ltd | £1,000.00 | Environment |
| 7 | `Over500_2026_P04_-_published.xlsx:300` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £999.32 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:209` | 2026-06-04 | Sikandar Hayat t/a Prompt Cars | £996.43 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:341` | 2026-05-01 | Go Green Taxis Ltd | £995.95 | Education & SEND |
| 10 | `Over500_2026_P03_-_published.xlsx:17` | 2026-06-30 | PHF Training | £995.00 | Community Services |


## R-04: Spend continuing after every matched contract notice ended [12 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether payments to suppliers whose matched contract notices had ended are covered by an approved extension or a new contract.

**C-04.1. Expected control.** Each contract extension is approved by the S151 Officer before the extended period begins; otherwise a new contract is let. [CPR-61] Owner: S151 Officer.

**T-04.1. Test.** For each sampled supplier, obtain the contract under which the sampled payments were made. If it is an extension, check for S151 Officer approval dated before the extended period began; if a new contract, check it on the register. Pass: a dated approval or a current contract covering the payments. Suppliers below the publication threshold are not sampled, consistent with the scope note. [CPR-61, metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement]  
**Evidence to inspect:** Current contract or extension, S151 Officer approval and its date, contract register entry  
**Sample:** 4 items from `expired-notice-spend.csv`, where dominant_tag = general_procurement, at_or_above_publication_threshold = True, largest total_gbp first, 3 payments per supplier, (only 4 available); 8 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:704` | 2026-06-16 | Hope & Clay (Construction) Ltd | £91,306.75 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:58` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £8,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:42` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £6,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:279` | 2026-06-09 | BERKSHIRE MECHANICAL SERVICES | £5,585.00 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:467` | 2026-05-08 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:531` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:721` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £1,365.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:459` | 2026-05-15 | CACI Limited | £12,071.67 | Children's Social Care |


## R-06: Same supplier paid the same amount within seven days [12 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether same-amount payments to one supplier on different payment runs within seven days each rest on their own written evidence of purchase.

**C-06.1. Expected control.** Every payment is supported by its own written or electronic evidence of purchase (order and invoice), so a repeat invoice is detected before payment. [CPR-31]

**T-06.1. Test.** For each sampled group, match every payment to its invoice and order and compare invoice numbers, dates and the goods or services supplied. Pass: distinct invoices for distinct supplies. Refer any payment without its own evidence for recovery review. [CPR-31, metric:$.tests.duplicates.tiers.different_time.by_dominant_tag.general_procurement.groups]  
**Evidence to inspect:** Invoices, purchase orders, goods-received records, supplier statements, any accounts-payable duplicate-check report or exception log covering the sampled payments  
**Sample:** 10 items from `duplicates.csv`, where tier = different_time, dominant_tag = general_procurement, largest gbp_beyond_first first, one item per supplier_norm; 27 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:3308` | 2026-07-15 | VolkerHighways Ltd | £101,925.86 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:618` | 2026-07-17 | VolkerHighways Ltd | £101,925.86 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:2160` | 2026-05-12 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 2 | `Over500_2026_P02_-_published.xlsx:2161` | 2026-05-13 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 3 | `Over500_2026_P04_-_published.xlsx:598` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:734` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:789` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:1288` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 4 | `Over500_2026_P04_-_published.xlsx:259` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:264` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:474` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:8` | 2026-05-13 | Pavillion Publishing and Media Ltd | £9,084.60 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:643` | 2026-05-14 | Pavillion Publishing and Media Ltd | £9,084.60 | Executive Director People - Children's Services |
| 6 | `Over500_2026_P02_-_published.xlsx:187` | 2026-05-11 | CONNICK TREE CARE | £1,009.40 | Environment |
| 6 | `Over500_2026_P02_-_published.xlsx:188` | 2026-05-14 | CONNICK TREE CARE | £1,009.40 | Environment |
| 6 | `Over500_2026_P02_-_published.xlsx:191` | 2026-05-21 | CONNICK TREE CARE | £1,009.40 | Environment |
| 6 | `Over500_2026_P02_-_published.xlsx:197` | 2026-05-28 | CONNICK TREE CARE | £1,009.40 | Environment |
| 6 | `Over500_2026_P03_-_published.xlsx:144` | 2026-06-04 | CONNICK TREE CARE | £1,009.40 | Environment |
| 6 | `Over500_2026_P03_-_published.xlsx:141` | 2026-06-10 | CONNICK TREE CARE | £1,009.40 | Environment |
| 7 | `Over500_2026_P03_-_published.xlsx:459` | 2026-06-25 | LOCAL GOVERNMENT PROPERTY CONSULTANTS (LGPC) | £4,925.00 | Finance, Property & Procurement |
| 7 | `Over500_2026_P03_-_published.xlsx:467` | 2026-06-25 | LOCAL GOVERNMENT PROPERTY CONSULTANTS (LGPC) | £4,925.00 | Finance, Property & Procurement |
| 8 | `Over500_2026_P03_-_published.xlsx:431` | 2026-06-17 | BRITISH TELECOM | £4,364.06 | Transformation, Customer & ICT |
| 8 | `Over500_2026_P03_-_published.xlsx:427` | 2026-06-17 | BRITISH TELECOM | £4,364.06 | Transformation, Customer & ICT |
| 9 | `Over500_2026_P04_-_published.xlsx:467` | 2026-07-09 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:266` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:838` | 2026-07-14 | AMR CONSULT LTD | £2,665.27 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:635` | 2026-07-14 | AMR CONSULT LTD | £2,665.27 | Education & SEND |

**T-06.2. Test.** For each sampled placement group, match every payment to its invoice and the placement agreement or care package, and compare the period, client reference and service each invoice covers. Pass: each payment covers a distinct period or service under the agreement. Regular periodic fees evidenced by the agreement pass; refer any payment without its own evidence for recovery review. [CPR-31, metric:$.tests.duplicates.tiers.different_time.by_dominant_tag.care_or_education_placement.groups]  
**Evidence to inspect:** Invoices, placement agreements or care package records, payment schedules (personal details redacted), any accounts-payable duplicate-check report or exception log covering the sampled payments  
**Sample:** 10 items from `duplicates.csv`, where tier = different_time, dominant_tag = care_or_education_placement, largest gbp_beyond_first first, one item per supplier_norm; 79 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:2164` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2165` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2166` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2167` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2189` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2190` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2311` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3106` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3107` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2169` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2170` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2312` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2313` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3109` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2173` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2195` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2315` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2316` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2317` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3110` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3111` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2175` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2176` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2199` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2200` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2201` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3112` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3113` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2177` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2203` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2204` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2321` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2322` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:2323` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3114` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P03_-_published.xlsx:3115` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,337.45 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2242` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2243` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2247` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2249` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2252` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2253` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2255` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2257` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2260` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P02_-_published.xlsx:2263` | 2026-05-21 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2157` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2158` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:3102` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2159` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:3103` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2306` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2266` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2267` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2269` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P04_-_published.xlsx:3064` | 2026-07-16 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:3091` | 2026-07-22 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:3084` | 2026-07-24 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:3087` | 2026-07-31 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:2008` | 2026-06-16 | Care Services To You | £23,989.77 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:1931` | 2026-06-16 | Care Services To You | £23,989.77 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:3044` | 2026-06-22 | Care Services To You | £23,989.77 | Children's Social Care |
| 7 | `Over500_2026_P02_-_published.xlsx:2092` | 2026-05-26 | Amegreen Childrens Services | £34,431.08 | Children's Social Care |
| 7 | `Over500_2026_P02_-_published.xlsx:2105` | 2026-05-27 | Amegreen Childrens Services | £34,431.08 | Children's Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:1716` | 2026-06-24 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:2958` | 2026-06-24 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:2979` | 2026-07-01 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:2319` | 2026-07-08 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:2346` | 2026-07-08 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:2348` | 2026-07-08 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:2985` | 2026-07-08 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:2423` | 2026-07-15 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:3029` | 2026-07-15 | Affinity Trust Support Ltd | £3,960.00 | Adult Social Care |
| 9 | `Over500_2026_P03_-_published.xlsx:1440` | 2026-06-24 | LIAISE LODDON LTD | £14,721.68 | Adult Social Care |
| 9 | `Over500_2026_P03_-_published.xlsx:1514` | 2026-06-24 | LIAISE LODDON LTD | £14,721.68 | Adult Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:2179` | 2026-07-01 | LIAISE LODDON LTD | £14,721.68 | Adult Social Care |
| 10 | `Over500_2026_P02_-_published.xlsx:2234` | 2026-05-11 | The Unicorn School | £13,771.00 | Education (DSG Funded) & Other Education Grants |
| 10 | `Over500_2026_P02_-_published.xlsx:2235` | 2026-05-11 | The Unicorn School | £13,771.00 | Education (DSG Funded) & Other Education Grants |
| 10 | `Over500_2026_P02_-_published.xlsx:2236` | 2026-05-11 | The Unicorn School | £13,771.00 | Education (DSG Funded) & Other Education Grants |


## R-07: Waivers and exceptions to competition not approved and documented [6 (Moderate; Moderate)]

**Audit objective.** Conclude whether waivers and exceptions to competition are approved in advance at the level the Rules require, documented, reported and recorded by the S151 Officer.

**C-07.1. Expected control.** Each waiver or exception is approved in advance by the Monitoring Officer and/or S151 Officer at the level set for its value, fully documented, supported by a written exception report to the relevant board, and recorded by the S151 Officer; exclusions under Procurement Legislation have prior Monitoring Officer approval. [CPR-19, CPR-20, CPR-21, CPR-22, CPR-23, CPR-24, CPR-25, CPR-26, CPR-58] Owner: S151 Officer and Monitoring Officer.

**T-07.1. Test.** Obtain the waiver and exception log for the spend window and select entries across the value tiers. For each, record the approver against both CPR-19 (Executive Director and/or Chief Executive) and CPR-20 (Monitoring Officer and/or S151 Officer), and check the written exception report, board approval where required, and the S151 Officer's record. Pass: all elements present, dated before the contract, and the approval meets both rules; refer any approval that meets only one rule to the auditor. [CPR-19, CPR-20, CPR-21, CPR-22, CPR-23, CPR-25, CPR-26]  
**Evidence to inspect:** Waiver and exception log, approvals, exception reports, board minutes, S151 Officer records  
**Sample:** document test: entries selected from the waiver and exception log the council provides; no published transaction identifies a waiver

**T-07.2. Test.** For each sampled supplier with no notice found and not already sampled under R-03, ask whether a waiver or exception covers the spend; where one does, test it as in T-07.1 and check it appears in the log. Pass: a contract let by competition, or a logged and approved waiver. [CPR-19, CPR-24, metric:$.tests.off_contract.headline_unmatched_general_procurement.suppliers]  
**Evidence to inspect:** Contract or waiver record for the sampled suppliers, waiver and exception log  
**Sample:** 5 items from `off-contract.csv`, where match_class = none, dominant_tag = general_procurement, largest annualised_estimate first, 1 payments per supplier, excluding supplier_norm matching /\b(?:COUNCIL|CNCL|NHS|POLICE|FIRE AND RESCUE|FIRE AUTHORITY|HMRC|WALLET|PREPAID|PAYPOINT)\b/, main_narrative matching /Contribution|External audit|Allowances|Direct Payment/, excluding suppliers and rows already drawn in T-03.1; 5 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:738` | 2026-05-20 | ANCHOR PIPEWORK LIMITED | £33,148.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P03_-_published.xlsx:730` | 2026-06-23 | SCOTTISH & SOUTHERN | £101,258.24 | Environment |
| 3 | `Over500_2026_P02_-_published.xlsx:478` | 2026-05-20 | Education Software Solutions Limited | £95,536.35 | Transformation, Customer & ICT |
| 4 | `Over500_2026_P02_-_published.xlsx:178` | 2026-05-27 | Continental Landscapes Ltd | £67,604.74 | Environment |
| 5 | `Over500_2026_P03_-_published.xlsx:2148` | 2026-06-12 | Bloom Procurement Services Ltd | £100,210.53 | Transformation, Customer & ICT |


## R-09: Placement exemption applied without recorded reasons or board approval [4 (Moderate; Moderate)]

**Audit objective.** Conclude whether care and education placements relying on the App C row F exemption have recorded reasons for the choice of provider and, above the Threshold, board approval.

**C-09.1. Expected control.** The reasons for the choice of provider are recorded on the individual's case notes, and where the annual or total value exceeds the Threshold the relevant board approves the exemption. [CPR-63, CPR-64] Owner: Service Directors.

**T-09.1. Test.** For each sampled placement payment, identify the placement and inspect the case-note record of the reasons for the provider chosen; where the arrangement's value exceeds the Threshold, obtain the board approval. Pass: reasons recorded, and board approval where required. Whether board approval is required is set from the Threshold values in force, which the council must supply. [CPR-63, CPR-64, metric:$.population.tags.care_or_education_placement.gbp]  
**Evidence to inspect:** Case-note extract of provider-choice reasons (personal details redacted), placement agreement, board approval  
**Sample:** 5 items from `high-value-suppliers.csv`, where dominant_tag = care_or_education_placement, largest annualised_estimate first, 2 payments per supplier; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:1850` | 2026-07-08 | BUPA Care Services | £10,400.00 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:1039` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 2 | `Over500_2026_P04_-_published.xlsx:2320` | 2026-07-08 | Affinity Trust Support Ltd | £28,512.00 | Adult Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:1628` | 2026-06-24 | Affinity Trust Support Ltd | £26,394.66 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:2171` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2172` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:823` | 2026-05-13 | RUSKIN MILL TRUST | £179,236.76 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:1822` | 2026-05-13 | RUSKIN MILL TRUST | £151,859.86 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:2095` | 2026-05-26 | Amegreen Childrens Services | £36,705.55 | Children's Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:3080` | 2026-07-17 | Amegreen Childrens Services | £36,705.55 | Children's Social Care |

**T-09.2. Test.** For each sampled placement payment just below the quotation threshold, identify the placement and its package value, and inspect the case-note record of the reasons for the provider chosen; where the arrangement's annual or total value exceeds the Threshold, obtain the board approval. Pass: reasons recorded, and board approval where required. Whether board approval is required is set from the Threshold values in force, which the council must supply. [CPR-63, CPR-64, metric:$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.care_or_education_placement.count]  
**Evidence to inspect:** Case-note extract of provider-choice reasons (personal details redacted), placement agreement or care package record showing its value, board approval  
**Sample:** 5 items from `threshold-clustering.csv`, where threshold = 25000, tag = care_or_education_placement, largest Net amount first, one item per supplier_norm, excluding suppliers and rows already drawn in T-09.1; 5 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:2307` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £24,788.75 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:1660` | 2026-06-24 | FOCUS SUPPORT LTD | £24,719.02 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:2106` | 2026-06-30 | Unity Residential Care Services | £24,587.49 | Children's Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2265` | 2026-05-22 | ACORN CARE & EDUCATION LTD | £24,578.67 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P02_-_published.xlsx:2268` | 2026-05-26 | Huckleberry House | £24,453.39 | Education (DSG Funded) & Other Education Grants |


## Prepared-by-client (PBC) request list

Derived from the test steps above. Each item names the tests that need it.

| # | Risk | Item requested | For tests |
|---|---|---|---|
| 1 | R-03 | Contract register (all contracts in progress and awarded) | T-03.1, T-03.2 |
| 2 | R-03 | Contracts or call-offs and competition evidence for the sampled suppliers | T-03.1 |
| 3 | R-03 | Supplier master data for the near-miss name candidates | T-03.2 |
| 4 | R-08 | Award decision records and written procurement reports for the contracts behind the sampled windows | T-08.1 |
| 5 | R-08 | Performance bond or approved bond risk assessment for works contracts behind the sampled windows | T-08.1 |
| 6 | R-08 | Threshold values in force in the spend window (goods and services, works and concessions, light touch) | T-08.1, T-08.2 |
| 7 | R-08 | Award decision records for the noticed contracts of the suppliers sampled in T-08.2 | T-08.2 |
| 8 | R-08 | Scheme of Delegation and nominations in writing in force in the spend window | T-08.2 |
| 9 | R-01 | Purchase orders and invoices for the sampled split-purchase windows | T-01.1 |
| 10 | R-01 | Procurement Portal quotation records for the sampled windows | T-01.1 |
| 11 | R-01 | Contracts or Purchasing Scheme call-offs the sampled window payments fall under | T-01.1 |
| 12 | R-01 | Waiver and exception log for the spend window | T-01.1 |
| 13 | R-05 | Supplier ledger spend to date on each sampled contract | T-05.1 |
| 14 | R-05 | Contracts, pricing schedules and variation approvals for the sampled suppliers | T-05.1 |
| 15 | R-05 | Threshold values in force in the spend window (goods and services, works and concessions, light touch) | T-05.1 |
| 16 | R-02 | Purchase orders, value estimates and quotations for the sampled near-threshold payments | T-02.1 |
| 17 | R-02 | Purchase orders, value estimates and quotes for the sampled single-quote-tier payments | T-02.2 |
| 18 | R-04 | Current contracts or extensions and S151 Officer extension approvals for the sampled suppliers | T-04.1 |
| 19 | R-06 | Invoices and purchase orders for every payment in the sampled same-amount groups | T-06.1 |
| 20 | R-06 | Any accounts-payable duplicate-check report or exception log covering the sampled payments | T-06.1, T-06.2 |
| 21 | R-06 | Invoices and placement agreements for every payment in the sampled placement same-amount groups | T-06.2 |
| 22 | R-07 | Waiver and exception log for the spend window | T-07.1 |
| 23 | R-07 | Approvals, exception reports and S151 Officer records for the selected log entries | T-07.1 |
| 24 | R-07 | Contract or waiver record for the suppliers sampled in T-07.2 | T-07.2 |
| 25 | R-09 | Case-note extracts of provider-choice reasons for the sampled placement payments | T-09.1 |
| 26 | R-09 | Board approvals of Appendix C exemptions above the Threshold | T-09.1 |
| 27 | R-09 | Threshold values in force in the spend window (goods and services, works and concessions, light touch) | T-09.1 |
| 28 | R-09 | Case-note extracts and placement agreements or care package records for the sampled near-threshold placement payments | T-09.2 |
