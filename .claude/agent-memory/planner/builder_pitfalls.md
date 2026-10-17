---
name: builder-pitfalls
description: build_pack.py traps for audit-plan.json: literal-figure regex, group row_ids separator, sample-kind fit per analytics-full file
metadata:
  type: feedback
---

Pitfalls met when building the pack with build_pack.py.

- Literal-figure check (NUM_RE) fires on "£" followed by a digit and on any standalone 3+ digit number. So "payments over £500" (as in the skill's own example) fails, and "S.151" fails (the dot makes "151" a word). Write "S151 Officer", "the publication floor", and use {{$.path}} placeholders for thresholds and ratios. Clause refs like 6.16 or CPR-54 are fine.
  **Why:** the builder rejects the whole memo line otherwise.
  **How to apply:** before building, scan prose (memo, objective, control, step, evidence) for £digits and 3+ digit numbers.
- `groups` samples: the builder splits `row_ids` on `;` or `,`, but analytics-full group files (split-purchases.csv, duplicates.csv) have been written space-separated. Then every id "is not found in spend-clean.csv" and the test yields no transactions. Neither file is the planner's: report PLANNER BLOCKED, do not switch to a `suppliers` recipe (it would pull the wrong payments).
  **How to apply:** if a groups test fails this way, check the separator with `head -2 file | od -c` first.
- Sample kinds that fit each file: threshold-clustering.csv = rows (filter threshold + tag); split-purchases.csv = groups (threshold + dominant_tag, distinct_by supplier_norm, per_group_n to cap large windows); duplicates.csv = groups (tier + dominant_tag); off-contract.csv = suppliers (match_class none/exact/near_ratio/near_contain + dominant_tag); expired-notice-spend.csv, spend-vs-award.csv (where_min ratio), high-value-suppliers.csv = suppliers.
- The spend-analyst's inter-authority exclusion misses public bodies with abbreviated names (e.g. CNCL). The challenger expects supplier-level and rows samples in general procurement to carry `where_not_match` on supplier_norm with a council/NHS/police/fire pattern (include CNCL), and a memo limitation saying the word list errs in both directions.
- The challenger also rejects non-procurement payees in quote or waiver samples: add a narrative `where_not_match` (main_narrative in supplier files, Narrative in rows files) for Contribution|External audit|Allowances|Direct Payment, and WALLET|PREPAID|PAYPOINT in the supplier pattern; add Insurance Premiums to the narrative pattern (claim settlements). split-purchases.csv's narrative column is `narratives` (plural) and needs the same exclusion. Check the narrative value counts of the draw population first.
- Memo Scope section is builder-rendered; scope notes from the auditor (e.g. a tag left for a separate review) go in memo.purpose.
- The challenger rejects capped `per_group_n` on split windows and on spend-vs-award: deciding "one requirement" or "cumulative spend vs award" needs every payment, so use per_group_n 0 there.
- Builder walks risks in plan order, so a test named in `exclude_drawn_in` must sit earlier in the plan. The challenger expects T-01.1 (splits) to skip suppliers drawn in T-03.1/T-08.1: list R-03 and R-08 before R-01 and say why in memo.approach.
- Challenger expectations seen on a first pass: split-test pass route for call-offs under a written contract/Purchasing Scheme (cite CPR-60); expired-notice sample filtered to at_or_above_publication_threshold = True (never question suppliers below it); CPR-42 (bond) tested in the over-500k award test, not left untested; placement near-threshold rows (threshold-clustering, tag placement) sampled for R-09 as a second test.
- Rating/scope-typed challenges that ask only for a memo line: still reply `for the auditor` and leave the plan unchanged (agent-file rule); the challenger may re-raise it in round two.

Related: [[audit-program-wording]]
