# Audit program

*Generated 2026-10-19 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 1, build 1c50332c723c), `auditor-comments.md`, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

7 risks in scope, 10 controls, 12 tests, 534 sampled transactions. Samples are drawn by the builder from `analytics-full/` by the recipe stated under each test, and every transaction is listed with its workbook row.


## R-03: High-value suppliers with no contract notice found [20 (Extreme; Extreme (Red))]

**Audit objective.** Conclude whether high-value suppliers with no matching notice were procured through the route the Rules require for their value.

**C-03.1. Expected control.** Contracts at or above the quotation threshold are procured through the Portal quotation route, and above the Threshold by full tender with a Contract Details Portal notice. [CPR-43, CPR-46, CPR-06] Owner: Service Director.

**T-03.1. Test.** For each sampled supplier obtain the contract file or exception record and confirm the quotation or tender route, the notice, and that the annual value fits the route used. A pass is a documented route that matches the value, or a contract outside the notice export. [CPR-43, CPR-46, CPR-06, metric:$.tests.off_contract.headline_unmatched_general_procurement.suppliers]  
**Evidence to inspect:** Contract file, quotations or tender record, Portal and notice references, exception record  
**Sample:** 10 items from `off-contract.csv`, where dominant_tag = general_procurement, match_class = none, largest annualised_estimate first, 5 payments per supplier, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, main_narrative matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/; 44 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:793` | 2026-07-13 | VolkerHighways Ltd | £998,987.64 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:603` | 2026-07-28 | VolkerHighways Ltd | £855,750.25 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:684` | 2026-06-22 | VolkerHighways Ltd | £366,872.38 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:699` | 2026-06-08 | VolkerHighways Ltd | £329,988.88 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:709` | 2026-05-05 | VolkerHighways Ltd | £311,353.42 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:2196` | 2026-05-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,201,856.40 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:2146` | 2026-06-29 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,180,425.32 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3194` | 2026-07-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £1,803,783.32 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:2144` | 2026-06-25 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:2216` | 2026-06-03 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:3789` | 2026-07-29 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:3311` | 2026-07-29 | Millbrook Healthcare Limited | £33,611.35 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:665` | 2026-05-15 | The Better Group Ltd | £64,500.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:666` | 2026-05-15 | The Better Group Ltd | £58,833.00 | Adult Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:670` | 2026-06-01 | The Better Group Ltd | £48,784.37 | Adult Social Care |
| 4 | `Over500_2026_P04_-_published.xlsx:783` | 2026-07-29 | The Better Group Ltd | £48,518.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:667` | 2026-05-19 | The Better Group Ltd | £41,125.00 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:654` | 2026-05-27 | SoftwareONE UK Ltd | £1,759.34 | Transformation, Customer & ICT |
| 6 | `Over500_2026_P02_-_published.xlsx:2200` | 2026-05-13 | Livity Life Ltd | £135,591.03 | Finance, Property & Procurement |
| 6 | `Over500_2026_P03_-_published.xlsx:3087` | 2026-06-17 | Livity Life Ltd | £127,886.78 | Finance, Property & Procurement |
| 6 | `Over500_2026_P04_-_published.xlsx:3310` | 2026-07-13 | Livity Life Ltd | £50,961.45 | Finance, Property & Procurement |
| 6 | `Over500_2026_P04_-_published.xlsx:3197` | 2026-07-13 | Livity Life Ltd | £46,409.47 | Finance, Property & Procurement |
| 6 | `Over500_2026_P02_-_published.xlsx:2199` | 2026-05-13 | Livity Life Ltd | £42,882.27 | Finance, Property & Procurement |
| 7 | `Over500_2026_P04_-_published.xlsx:784` | 2026-07-10 | E W BEARD LTD | £64,202.50 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:674` | 2026-05-20 | E W BEARD LTD | £60,039.70 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:675` | 2026-05-20 | E W BEARD LTD | £55,594.00 | Education & SEND |
| 7 | `Over500_2026_P03_-_published.xlsx:664` | 2026-06-10 | E W BEARD LTD | £38,672.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:672` | 2026-05-20 | E W BEARD LTD | £36,170.52 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:183` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £73,296.50 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:203` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £26,085.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:208` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £17,607.50 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:162` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £9,944.00 | Education & SEND |
| 8 | `Over500_2026_P04_-_published.xlsx:220` | 2026-07-21 | Sikandar Hayat t/a Prompt Cars | £3,743.00 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:661` | 2026-06-08 | ANDY AND ES LIMITED | £59,335.72 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:1283` | 2026-07-15 | ANDY AND ES LIMITED | £56,941.82 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:670` | 2026-05-13 | ANDY AND ES LIMITED | £54,881.31 | Education & SEND |
| 10 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 10 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 10 | `Over500_2026_P04_-_published.xlsx:533` | 2026-07-28 | Elior UK PLC | £23,173.08 | Adult Social Care |
| 10 | `Over500_2026_P03_-_published.xlsx:433` | 2026-06-17 | Elior UK PLC | £18,592.30 | Adult Social Care |
| 10 | `Over500_2026_P02_-_published.xlsx:525` | 2026-05-13 | Elior UK PLC | £18,371.14 | Adult Social Care |

**C-03.2. Expected control.** Spend with a social care placement provider is supported by a record of the reasons for choice of provider. [CPR-53, CPR-54] Owner: Service Director.

**T-03.2. Test.** For a sample of placement providers with no matching notice, obtain the record of reasons for the choice of provider and confirm it exists. [CPR-53, CPR-54, metric:$.contracts.active_in_window]  
**Evidence to inspect:** Provider choice record, placement agreement  
**Sample:** 5 items from `off-contract.csv`, where dominant_tag = care_or_education_placement, match_class = none, largest annualised_estimate first, 3 payments per supplier, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/; 15 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:1850` | 2026-07-08 | BUPA Care Services | £10,400.00 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:1039` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:1043` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 2 | `Over500_2026_P04_-_published.xlsx:2320` | 2026-07-08 | Affinity Trust Support Ltd | £28,512.00 | Adult Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:1628` | 2026-06-24 | Affinity Trust Support Ltd | £26,394.66 | Adult Social Care |
| 2 | `Over500_2026_P04_-_published.xlsx:2239` | 2026-07-01 | Affinity Trust Support Ltd | £24,926.00 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:2171` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2172` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P03_-_published.xlsx:2191` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:823` | 2026-05-13 | RUSKIN MILL TRUST | £179,236.76 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:1822` | 2026-05-13 | RUSKIN MILL TRUST | £151,859.86 | Adult Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:802` | 2026-06-02 | RUSKIN MILL TRUST | £122,817.82 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:2095` | 2026-05-26 | Amegreen Childrens Services | £36,705.55 | Children's Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:3080` | 2026-07-17 | Amegreen Childrens Services | £36,705.55 | Children's Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:2088` | 2026-05-22 | Amegreen Childrens Services | £35,636.36 | Children's Social Care |


## R-05: Spend running above the annual rate of the award [15 (Extreme; Extreme (Red))]

**Audit objective.** Conclude whether spend above the annual rate of an award was covered by the variation approvals the Rules require.

**C-05.1. Expected control.** Variations to scope or value are approved in writing before they take effect, by the officers named for the value band. [CPR-51, CPR-52] Owner: Monitoring Officer and S151 Officer.

**T-05.1. Test.** For each sampled supplier obtain the contract, its variation approvals and the payment history, and compare cumulative payments with the award value over the contract term. A pass is an approved variation or an award value that explains the payments. [CPR-51, CPR-52, metric:$.tests.spend_vs_award.flagged_annualised_estimate_gbp]  
**Evidence to inspect:** Contract, variation approvals, award report, payment ledger  
**Sample:** 8 items from `spend-vs-award.csv`, where dominant_tag = general_procurement, ratio ≥ 1.25, largest ratio first, all payments per supplier, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, main_narrative matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/, (only 8 available); 31 transactions

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


## R-04: Spend continuing after matched contract notices ended [12 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether payments after a matched notice ended were covered by an approved extension or a replacement contract.

**C-04.1. Expected control.** Extensions to an existing contract are approved by the S151 Officer where the contract provides for the extension. [CPR-50] Owner: S151 Officer.

**T-04.1. Test.** For each sampled supplier obtain the extension approval or the replacement contract and confirm it covers the payment dates. A pass is an approved extension or a contract in force. [CPR-50, metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement]  
**Evidence to inspect:** Extension approval, replacement contract, notice record  
**Sample:** 4 items from `expired-notice-spend.csv`, where dominant_tag = general_procurement, at_or_above_publication_threshold = True, largest annualised_estimate first, 5 payments per supplier, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, main_narrative matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/, (only 4 available); 12 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:704` | 2026-06-16 | Hope & Clay (Construction) Ltd | £91,306.75 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:58` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £8,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:42` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £6,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:279` | 2026-06-09 | BERKSHIRE MECHANICAL SERVICES | £5,585.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:52` | 2026-06-09 | BERKSHIRE MECHANICAL SERVICES | £4,000.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:374` | 2026-07-03 | BERKSHIRE MECHANICAL SERVICES | £3,400.00 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:467` | 2026-05-08 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:531` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:721` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £1,365.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:1309` | 2026-07-15 | G7 BUSINESS SOLUTIONS LIMITED | £1,365.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P02_-_published.xlsx:762` | 2026-05-19 | G7 BUSINESS SOLUTIONS LIMITED | £910.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:459` | 2026-05-15 | CACI Limited | £12,071.67 | Children's Social Care |


## R-01: Requirements split below the quotation and notice threshold [20 (Extreme; Extreme (Red))]

**Audit objective.** Conclude whether payment windows that together reach the threshold were treated as one requirement and purchased by the route the Rules require.

**C-01.1. Expected control.** Requirements are aggregated before the route to market is chosen, and no contract is artificially split to avoid the Rules. [CPR-08, CPR-43] Owner: Service Director.

**T-01.1. Test.** For each sampled window obtain the orders, quotes and contract entries and decide whether the payments were one requirement. Where they were call-offs under a written contract or Purchasing Scheme (CPR-49) record that as a pass route; otherwise check the quotation evidence for the combined value. [CPR-08, CPR-49, metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows]  
**Evidence to inspect:** Purchase orders, quotations, contract register entry, written contract or Purchasing Scheme terms  
**Sample:** 10 items from `split-purchases.csv`, where dominant_tag = general_procurement, threshold = 25000, largest window_total first, one item per supplier_norm, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, narratives matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/, excluding suppliers and rows already drawn in T-03.1, T-05.1; 149 transactions

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

**C-01.2. Expected control.** Purchases of the lower band are supported by at least one quote from an appropriate source, and a combined requirement reaching the quotation threshold by Portal invitations to at least three suppliers. [CPR-43, CPR-42] Owner: Service Director.

**T-01.2. Test.** For each sampled window at the lower threshold obtain the quote evidence and confirm at least one quote from an appropriate source is on file; where the combined value reaches the quotation threshold, also confirm Portal invitations to at least three suppliers. A pass is evidence that matches the combined value. [CPR-42, CPR-43, metric:$.tests.split_purchases.by_threshold.1000.headline_general_procurement.windows]  
**Evidence to inspect:** Quotes, Portal records  
**Sample:** 5 items from `split-purchases.csv`, where dominant_tag = general_procurement, threshold = 1000, largest window_total first, one item per supplier_norm, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, narratives matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/, excluding suppliers and rows already drawn in T-03.1, T-05.1, T-01.1; 62 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:134` | 2026-07-01 | Glen Cleaning Company Ltd | £779.78 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:135` | 2026-07-01 | Glen Cleaning Company Ltd | £894.59 | Capital Financing and Income Investment |
| 1 | `Over500_2026_P04_-_published.xlsx:140` | 2026-07-01 | Glen Cleaning Company Ltd | £616.69 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P04_-_published.xlsx:144` | 2026-07-03 | Glen Cleaning Company Ltd | £891.09 | Development & Housing |
| 1 | `Over500_2026_P04_-_published.xlsx:133` | 2026-07-06 | Glen Cleaning Company Ltd | £863.46 | Development & Housing |
| 1 | `Over500_2026_P04_-_published.xlsx:145` | 2026-07-06 | Glen Cleaning Company Ltd | £891.09 | Development & Housing |
| 1 | `Over500_2026_P04_-_published.xlsx:131` | 2026-07-07 | Glen Cleaning Company Ltd | £587.50 | Community Services |
| 1 | `Over500_2026_P04_-_published.xlsx:124` | 2026-07-13 | Glen Cleaning Company Ltd | £706.95 | Children's Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:138` | 2026-07-23 | Glen Cleaning Company Ltd | £779.78 | Children's Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:139` | 2026-07-23 | Glen Cleaning Company Ltd | £779.78 | Children's Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:169` | 2026-07-24 | Glen Cleaning Company Ltd | £779.78 | Finance, Property & Procurement |
| 1 | `Over500_2026_P04_-_published.xlsx:396` | 2026-07-24 | Glen Cleaning Company Ltd | £616.69 | Education (DSG Funded) & Other Education Grants |
| 1 | `Over500_2026_P04_-_published.xlsx:397` | 2026-07-24 | Glen Cleaning Company Ltd | £930.63 | Community Services |
| 1 | `Over500_2026_P04_-_published.xlsx:400` | 2026-07-24 | Glen Cleaning Company Ltd | £894.59 | Capital Financing and Income Investment |
| 1 | `Over500_2026_P04_-_published.xlsx:130` | 2026-07-28 | Glen Cleaning Company Ltd | £590.79 | Children's Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:125` | 2026-07-29 | Glen Cleaning Company Ltd | £706.95 | Children's Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:126` | 2026-07-30 | Glen Cleaning Company Ltd | £901.77 | Community Services |
| 1 | `Over500_2026_P04_-_published.xlsx:141` | 2026-07-30 | Glen Cleaning Company Ltd | £901.77 | Community Services |
| 1 | `Over500_2026_P04_-_published.xlsx:142` | 2026-07-30 | Glen Cleaning Company Ltd | £901.77 | Community Services |
| 2 | `Over500_2026_P03_-_published.xlsx:280` | 2026-06-25 | BERKSHIRE MECHANICAL SERVICES | £1,000.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:146` | 2026-07-03 | BERKSHIRE MECHANICAL SERVICES | £800.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:375` | 2026-07-03 | BERKSHIRE MECHANICAL SERVICES | £845.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:48` | 2026-07-06 | BERKSHIRE MECHANICAL SERVICES | £975.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:78` | 2026-07-06 | BERKSHIRE MECHANICAL SERVICES | £800.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:370` | 2026-07-08 | BERKSHIRE MECHANICAL SERVICES | £520.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:49` | 2026-07-08 | BERKSHIRE MECHANICAL SERVICES | £650.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:81` | 2026-07-08 | BERKSHIRE MECHANICAL SERVICES | £600.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:372` | 2026-07-09 | BERKSHIRE MECHANICAL SERVICES | £625.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:50` | 2026-07-09 | BERKSHIRE MECHANICAL SERVICES | £1,000.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:56` | 2026-07-09 | BERKSHIRE MECHANICAL SERVICES | £615.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:57` | 2026-07-09 | BERKSHIRE MECHANICAL SERVICES | £900.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:373` | 2026-07-10 | BERKSHIRE MECHANICAL SERVICES | £775.00 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:28` | 2026-05-13 | ANCHOR PIPEWORK LIMITED | £890.60 | Education & SEND |
| 3 | `Over500_2026_P02_-_published.xlsx:53` | 2026-05-14 | ANCHOR PIPEWORK LIMITED | £622.02 | Finance, Property & Procurement |
| 3 | `Over500_2026_P02_-_published.xlsx:15` | 2026-05-28 | ANCHOR PIPEWORK LIMITED | £510.50 | Adult Social Care |
| 3 | `Over500_2026_P02_-_published.xlsx:16` | 2026-05-29 | ANCHOR PIPEWORK LIMITED | £579.63 | Adult Social Care |
| 3 | `Over500_2026_P02_-_published.xlsx:24` | 2026-05-29 | ANCHOR PIPEWORK LIMITED | £651.60 | Adult Social Care |
| 3 | `Over500_2026_P02_-_published.xlsx:52` | 2026-05-29 | ANCHOR PIPEWORK LIMITED | £633.55 | Environment |
| 3 | `Over500_2026_P02_-_published.xlsx:56` | 2026-05-29 | ANCHOR PIPEWORK LIMITED | £883.98 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:56` | 2026-06-02 | ANCHOR PIPEWORK LIMITED | £752.60 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:48` | 2026-06-09 | ANCHOR PIPEWORK LIMITED | £903.68 | Community Services |
| 3 | `Over500_2026_P03_-_published.xlsx:57` | 2026-06-10 | ANCHOR PIPEWORK LIMITED | £546.25 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:640` | 2026-07-02 | Stripeweb | £544.83 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:643` | 2026-07-03 | Stripeweb | £646.03 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:562` | 2026-07-08 | Stripeweb | £711.59 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:1018` | 2026-07-09 | Stripeweb | £616.52 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:1019` | 2026-07-13 | Stripeweb | £541.15 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:1020` | 2026-07-13 | Stripeweb | £578.92 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:563` | 2026-07-17 | Stripeweb | £506.59 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:644` | 2026-07-19 | Stripeweb | £575.59 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:646` | 2026-07-24 | Stripeweb | £643.09 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:564` | 2026-07-30 | Stripeweb | £636.19 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:647` | 2026-07-31 | Stripeweb | £506.22 | Finance, Property & Procurement |
| 5 | `Over500_2026_P04_-_published.xlsx:149` | 2026-07-13 | CONNICK TREE CARE | £797.76 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:215` | 2026-07-13 | CONNICK TREE CARE | £715.85 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:216` | 2026-07-13 | CONNICK TREE CARE | £578.24 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:151` | 2026-07-14 | CONNICK TREE CARE | £641.69 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:209` | 2026-07-16 | CONNICK TREE CARE | £501.13 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:211` | 2026-07-23 | CONNICK TREE CARE | £865.20 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:409` | 2026-07-24 | CONNICK TREE CARE | £713.50 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:410` | 2026-07-28 | CONNICK TREE CARE | £535.60 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:152` | 2026-07-31 | CONNICK TREE CARE | £535.60 | Environment |

**T-01.3. Test.** For each sampled window at the upper threshold obtain the tender or quotation record and the contract notice, and confirm the route the Rules require for the combined value (CPR-45); record call-offs under a written contract or Purchasing Scheme as a pass route. [CPR-45, CPR-08, metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows]  
**Evidence to inspect:** Tender record, Portal and notice references, written contract  
**Sample:** 3 items from `split-purchases.csv`, where dominant_tag = general_procurement, threshold = 500000, largest window_total first, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, narratives matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/; 99 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:727` | 2026-05-11 | VolkerHighways Ltd | £3,196.62 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:696` | 2026-05-12 | VolkerHighways Ltd | £2,566.36 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:700` | 2026-05-12 | VolkerHighways Ltd | £85,125.00 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:701` | 2026-05-12 | VolkerHighways Ltd | £17,896.87 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:710` | 2026-05-12 | VolkerHighways Ltd | £119,381.40 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:714` | 2026-05-12 | VolkerHighways Ltd | £1,550.00 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:720` | 2026-05-12 | VolkerHighways Ltd | £32,864.67 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:724` | 2026-05-12 | VolkerHighways Ltd | £7,828.20 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:692` | 2026-05-13 | VolkerHighways Ltd | £185,970.32 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:702` | 2026-05-13 | VolkerHighways Ltd | £195,844.36 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:703` | 2026-05-13 | VolkerHighways Ltd | £12,297.34 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2173` | 2026-05-19 | VolkerHighways Ltd | £28,217.54 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2176` | 2026-05-19 | VolkerHighways Ltd | £54,241.36 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2179` | 2026-05-19 | VolkerHighways Ltd | £17,882.35 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2184` | 2026-05-19 | VolkerHighways Ltd | £101,925.86 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2193` | 2026-05-19 | VolkerHighways Ltd | £1,668.58 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2170` | 2026-05-20 | VolkerHighways Ltd | £16,304.62 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2185` | 2026-05-20 | VolkerHighways Ltd | £19,420.72 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:704` | 2026-05-20 | VolkerHighways Ltd | £43,509.85 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:705` | 2026-05-20 | VolkerHighways Ltd | £157,038.29 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:728` | 2026-05-20 | VolkerHighways Ltd | £10,169.81 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:731` | 2026-05-20 | VolkerHighways Ltd | £2,585.44 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2172` | 2026-05-22 | VolkerHighways Ltd | £2,070.26 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:729` | 2026-05-22 | VolkerHighways Ltd | £46,320.84 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:730` | 2026-05-22 | VolkerHighways Ltd | £1,679.16 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:734` | 2026-05-22 | VolkerHighways Ltd | £5,199.81 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2180` | 2026-05-26 | VolkerHighways Ltd | £7,015.34 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2182` | 2026-05-26 | VolkerHighways Ltd | £4,046.54 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:697` | 2026-05-26 | VolkerHighways Ltd | £1,711.48 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:711` | 2026-05-26 | VolkerHighways Ltd | £200,305.25 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:712` | 2026-05-26 | VolkerHighways Ltd | £83,960.48 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:715` | 2026-05-26 | VolkerHighways Ltd | £5,225.72 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:716` | 2026-05-26 | VolkerHighways Ltd | £850.00 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:721` | 2026-05-26 | VolkerHighways Ltd | £10,122.39 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:725` | 2026-05-26 | VolkerHighways Ltd | £28,989.53 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:726` | 2026-05-26 | VolkerHighways Ltd | £2,610.11 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:693` | 2026-05-27 | VolkerHighways Ltd | £5,997.50 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:694` | 2026-05-27 | VolkerHighways Ltd | £8,175.00 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:698` | 2026-05-27 | VolkerHighways Ltd | £34,813.14 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:699` | 2026-05-27 | VolkerHighways Ltd | £1,793.45 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:706` | 2026-05-27 | VolkerHighways Ltd | £149,153.26 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:722` | 2026-05-27 | VolkerHighways Ltd | £54,099.60 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:707` | 2026-05-28 | VolkerHighways Ltd | £58,615.47 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:2117` | 2026-06-08 | VolkerHighways Ltd | £3,393.12 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:2133` | 2026-06-08 | VolkerHighways Ltd | £18,761.89 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:2402` | 2026-06-08 | VolkerHighways Ltd | £15,899.60 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:683` | 2026-06-08 | VolkerHighways Ltd | £23,591.22 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:699` | 2026-06-08 | VolkerHighways Ltd | £329,988.88 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:700` | 2026-06-08 | VolkerHighways Ltd | £95,421.19 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:702` | 2026-06-08 | VolkerHighways Ltd | £4,205.33 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:703` | 2026-06-08 | VolkerHighways Ltd | £46,778.61 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:728` | 2026-06-08 | VolkerHighways Ltd | £11,515.39 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:729` | 2026-06-08 | VolkerHighways Ltd | £299,416.56 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:701` | 2026-06-09 | VolkerHighways Ltd | £307,338.45 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:684` | 2026-06-22 | VolkerHighways Ltd | £366,872.38 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:727` | 2026-06-24 | VolkerHighways Ltd | £1,151.28 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1291` | 2026-07-06 | VolkerHighways Ltd | £118,015.06 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3192` | 2026-07-06 | VolkerHighways Ltd | £7,341.73 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:792` | 2026-07-07 | VolkerHighways Ltd | £1,024.51 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1289` | 2026-07-13 | VolkerHighways Ltd | £651.56 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3184` | 2026-07-13 | VolkerHighways Ltd | £17,882.35 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3210` | 2026-07-13 | VolkerHighways Ltd | £54,241.36 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3786` | 2026-07-13 | VolkerHighways Ltd | £1,500.00 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:602` | 2026-07-13 | VolkerHighways Ltd | £4,081.14 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:621` | 2026-07-13 | VolkerHighways Ltd | £13,855.87 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:736` | 2026-07-13 | VolkerHighways Ltd | £577.53 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:791` | 2026-07-13 | VolkerHighways Ltd | £1,675.31 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:799` | 2026-07-13 | VolkerHighways Ltd | £800.00 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1295` | 2026-07-14 | VolkerHighways Ltd | £11,615.51 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1310` | 2026-07-14 | VolkerHighways Ltd | £6,704.19 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3186` | 2026-07-14 | VolkerHighways Ltd | £1,432.22 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3303` | 2026-07-14 | VolkerHighways Ltd | £3,323.18 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:794` | 2026-07-14 | VolkerHighways Ltd | £76,834.61 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:795` | 2026-07-14 | VolkerHighways Ltd | £161,847.24 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:798` | 2026-07-14 | VolkerHighways Ltd | £77,034.27 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1292` | 2026-07-15 | VolkerHighways Ltd | £56,244.83 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1293` | 2026-07-15 | VolkerHighways Ltd | £2,500.00 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3187` | 2026-07-15 | VolkerHighways Ltd | £1,606.50 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3211` | 2026-07-15 | VolkerHighways Ltd | £14,141.01 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3304` | 2026-07-15 | VolkerHighways Ltd | £12,585.51 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3308` | 2026-07-15 | VolkerHighways Ltd | £101,925.86 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3787` | 2026-07-15 | VolkerHighways Ltd | £1,000.00 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:619` | 2026-07-15 | VolkerHighways Ltd | £195,182.14 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:620` | 2026-07-15 | VolkerHighways Ltd | £69,616.13 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:739` | 2026-07-15 | VolkerHighways Ltd | £10,165.33 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:819` | 2026-07-15 | VolkerHighways Ltd | £12,778.97 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:821` | 2026-07-15 | VolkerHighways Ltd | £11,256.01 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:822` | 2026-07-15 | VolkerHighways Ltd | £14,660.85 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:1296` | 2026-07-16 | VolkerHighways Ltd | £4,797.35 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3185` | 2026-07-16 | VolkerHighways Ltd | £17,882.35 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3302` | 2026-07-16 | VolkerHighways Ltd | £54,241.36 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3309` | 2026-07-17 | VolkerHighways Ltd | £3,337.15 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:618` | 2026-07-17 | VolkerHighways Ltd | £101,925.86 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:742` | 2026-07-17 | VolkerHighways Ltd | £7,732.30 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:777` | 2026-07-17 | VolkerHighways Ltd | £2,391.13 | Environment |
| 3 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 3 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 3 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 3 | `Over500_2026_P02_-_published.xlsx:654` | 2026-05-27 | SoftwareONE UK Ltd | £1,759.34 | Transformation, Customer & ICT |


## R-06: Same supplier, same amount paid more than once within a short period [12 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether repeat payments of an identical amount were each supported by a separate purchase.

**C-06.1. Expected control.** Written evidence of each purchase is held and supports each payment. [CPR-23] Owner: Service Director.

**T-06.1. Test.** Trace each sampled group to its invoices and orders and confirm each payment was for a separate supply. A pass is separate supporting documents for each payment. [CPR-23, metric:$.tests.duplicates.tiers.different_time.by_dominant_tag.general_procurement.groups]  
**Evidence to inspect:** Invoices, orders, remittance advice  
**Sample:** 10 items from `duplicates.csv`, where dominant_tag = general_procurement, tier = different_time, largest gbp_beyond_first first, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, narratives matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/; 29 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:3308` | 2026-07-15 | VolkerHighways Ltd | £101,925.86 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:618` | 2026-07-17 | VolkerHighways Ltd | £101,925.86 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3210` | 2026-07-13 | VolkerHighways Ltd | £54,241.36 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3302` | 2026-07-16 | VolkerHighways Ltd | £54,241.36 | Environment |
| 3 | `Over500_2026_P02_-_published.xlsx:2160` | 2026-05-12 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:2161` | 2026-05-13 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 4 | `Over500_2026_P04_-_published.xlsx:3184` | 2026-07-13 | VolkerHighways Ltd | £17,882.35 | Environment |
| 4 | `Over500_2026_P04_-_published.xlsx:3185` | 2026-07-16 | VolkerHighways Ltd | £17,882.35 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:598` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:734` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:789` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:1288` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 6 | `Over500_2026_P04_-_published.xlsx:259` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:264` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:474` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:8` | 2026-05-13 | Pavillion Publishing and Media Ltd | £9,084.60 | Adult Social Care |
| 7 | `Over500_2026_P02_-_published.xlsx:643` | 2026-05-14 | Pavillion Publishing and Media Ltd | £9,084.60 | Executive Director People - Children's Services |
| 8 | `Over500_2026_P02_-_published.xlsx:412` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:416` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:418` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:369` | 2026-05-12 | BROADWAY CARS | £3,640.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:372` | 2026-05-12 | BROADWAY CARS | £3,640.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:395` | 2026-05-13 | BROADWAY CARS | £3,640.00 | Education & SEND |
| 10 | `Over500_2026_P02_-_published.xlsx:187` | 2026-05-11 | CONNICK TREE CARE | £1,009.40 | Environment |
| 10 | `Over500_2026_P02_-_published.xlsx:188` | 2026-05-14 | CONNICK TREE CARE | £1,009.40 | Environment |
| 10 | `Over500_2026_P02_-_published.xlsx:191` | 2026-05-21 | CONNICK TREE CARE | £1,009.40 | Environment |
| 10 | `Over500_2026_P02_-_published.xlsx:197` | 2026-05-28 | CONNICK TREE CARE | £1,009.40 | Environment |
| 10 | `Over500_2026_P03_-_published.xlsx:144` | 2026-06-04 | CONNICK TREE CARE | £1,009.40 | Environment |
| 10 | `Over500_2026_P03_-_published.xlsx:141` | 2026-06-10 | CONNICK TREE CARE | £1,009.40 | Environment |

**T-06.2. Test.** Trace each sampled placement group to the placement agreement, invoices and remittance and confirm each payment was for a separate period or service. Placements are exempt from competition under CPR-53, not from the evidence rule. [CPR-23, CPR-53, metric:$.tests.duplicates.tiers.different_time.by_dominant_tag.care_or_education_placement.groups]  
**Evidence to inspect:** Placement agreement, invoices, remittance advice  
**Sample:** 10 items from `duplicates.csv`, where dominant_tag = care_or_education_placement, tier = different_time, largest gbp_beyond_first first, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/; 84 transactions

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
| 2 | `Over500_2026_P03_-_published.xlsx:2310` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2191` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2192` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2193` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2314` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:3108` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2171` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2172` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2196` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2198` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2319` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2320` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:3116` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2242` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2243` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2247` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2249` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2252` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2253` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2255` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2257` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2260` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P02_-_published.xlsx:2263` | 2026-05-21 | Phoenix Child Care Limited -The Grange School | £21,988.16 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:2157` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:2158` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:3102` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:2159` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:3103` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:2306` | 2026-06-03 | Sukhbir Singh and Harvinder Singh T/A Calcot Services for Children (CSFC) | £18,768.75 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P02_-_published.xlsx:2246` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P02_-_published.xlsx:2248` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P02_-_published.xlsx:2251` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 6 | `Over500_2026_P02_-_published.xlsx:2266` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 6 | `Over500_2026_P02_-_published.xlsx:2267` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 6 | `Over500_2026_P02_-_published.xlsx:2269` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 7 | `Over500_2026_P04_-_published.xlsx:3064` | 2026-07-16 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 7 | `Over500_2026_P04_-_published.xlsx:3091` | 2026-07-22 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 7 | `Over500_2026_P04_-_published.xlsx:3084` | 2026-07-24 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 7 | `Over500_2026_P04_-_published.xlsx:3087` | 2026-07-31 | Paradigm Care Services Ltd. | £17,000.00 | Children's Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:2008` | 2026-06-16 | Care Services To You | £23,989.77 | Children's Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:1931` | 2026-06-16 | Care Services To You | £23,989.77 | Children's Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:3044` | 2026-06-22 | Care Services To You | £23,989.77 | Children's Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:3750` | 2026-07-17 | Care Services To You | £23,989.77 | Children's Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:3092` | 2026-07-23 | Care Services To You | £23,989.77 | Children's Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:3161` | 2026-07-23 | Care Services To You | £23,989.77 | Children's Social Care |
| 10 | `Over500_2026_P02_-_published.xlsx:2245` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £23,210.00 | Education (DSG Funded) & Other Education Grants |
| 10 | `Over500_2026_P02_-_published.xlsx:2258` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £23,210.00 | Education (DSG Funded) & Other Education Grants |
| 10 | `Over500_2026_P02_-_published.xlsx:2262` | 2026-05-21 | Phoenix Child Care Limited -The Grange School | £23,210.00 | Education (DSG Funded) & Other Education Grants |


## R-02: Payments clustered just below the quotation threshold [9 (High; Medium - High (Amber))]

**Audit objective.** Conclude whether payments just below the quotation threshold had the lower-band quote evidence and were not part of a larger requirement.

**C-02.1. Expected control.** Purchases below the quotation threshold are supported by the quote the Rules require and are not kept below it by splitting. [CPR-42, CPR-08] Owner: Service Director.

**T-02.1. Test.** For each sampled payment obtain the quote and order and confirm whether it belongs to a larger requirement that reaches the threshold (CPR-43). [CPR-42, CPR-43, metric:$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement.count]  
**Evidence to inspect:** Quote, order, related orders to the supplier  
**Sample:** 9 items from `threshold-clustering.csv`, where tag = general_procurement, threshold = 25000, largest Net amount first, excluding supplier_norm matching /\b(COUNCIL|CNCL|NHS|POLICE|FIRE|WALLET|PREPAID|PAYPOINT)\b/, Narrative matching /Contribution|External audit|Allowances|Direct Payment|Insurance Premiums/, (only 9 available); 9 transactions

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


## R-07: Waivers, exceptions and award approvals not evidenced [6 (Moderate; Moderate)]

**Audit objective.** Conclude whether exceptions, waivers and awards were approved in writing by the officers the Rules name.

**C-07.1. Expected control.** Waivers and exceptions are granted only by the officers named in the Rules and recorded in writing. [CPR-14, CPR-15, CPR-16, CPR-19] Owner: S151 Officer and Monitoring Officer.

**T-07.1. Test.** Obtain the exception and waiver register and test a sample of entries for the approver and written record the Rules require. [CPR-14, CPR-19, metric:$.contracts.active_in_window]  
**Evidence to inspect:** Exception register, approval records  
**Sample:** Register and decision records are documents; no transaction in the spend data identifies a waiver.

**C-07.2. Expected control.** Awards are made by the officer the Rules name for the contract value. [CPR-38, CPR-39] Owner: Service Director.

**T-07.2. Test.** Take the ten active notices in the notice export with the largest Awarded Value, obtain the award decision record for each and confirm the approver matches the value band for the award. [CPR-38, CPR-39, metric:$.contracts.active_in_window]  
**Evidence to inspect:** Award decision records, delegation record  
**Sample:** Award decisions are documents; the ten largest active notices by Awarded Value are selected from the notice export in the step.


## Prepared-by-client (PBC) request list

Derived from the test steps above. Each item names the tests that need it.

| # | Risk | Item requested | For tests |
|---|---|---|---|
| 1 | R-03 | Contract file or exception record for each sampled supplier | T-03.1 |
| 2 | R-03 | Quotation or tender evidence and notice references | T-03.1 |
| 3 | R-03 | Provider choice record for each sampled placement supplier | T-03.2 |
| 4 | R-05 | Contract and variation approvals for each sampled supplier | T-05.1 |
| 5 | R-05 | Payment ledger for the contract term | T-05.1 |
| 6 | R-04 | Extension approval or replacement contract for each sampled supplier | T-04.1 |
| 7 | R-01 | Purchase orders and quotations for the sampled windows | T-01.1 |
| 8 | R-01 | Written contract or Purchasing Scheme terms where call-offs were made | T-01.1 |
| 9 | R-01 | Quotes for each sampled window | T-01.2 |
| 10 | R-01 | Tender or quotation record and notice for each sampled window | T-01.3 |
| 11 | R-06 | Invoices and orders for each sampled payment group | T-06.1 |
| 12 | R-06 | Placement agreement and invoices for each sampled payment group | T-06.2 |
| 13 | R-02 | Quote and order for each sampled payment | T-02.1 |
| 14 | R-07 | Exception and waiver register | T-07.1 |
| 15 | R-07 | Award decision records for contracts in the notice export | T-07.2 |
