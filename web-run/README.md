# Web run (hosted harness, Sonnet), 2026-10-19

A complete run of the workflow on the live app,
https://procurement-audit-planner.fly.dev, using `claude-sonnet-5-5`. It started from
empty outputs and went through every stage to the auditor's sign-off. The files here
were copied from the server's volume after sign-off, so the evidence does not depend on
the server staying up.

The signed-off pack from the local Claude Code run is in [`../outputs/`](../outputs/).
This folder is a second, independent run of the same system from the browser.

## What is here

- `outputs/` holds every output of the run, in the same layout as `../outputs/`:
  - rules, analytics, history and the risk register;
  - the auditor's decisions;
  - the pack: `planning-memo.md`, `risk-control-matrix.md`, `audit-program.md` and `samples/`;
  - `challenges.md` and `review.md`.
- `runs/` holds the harness's log of every stage run: each tool call, agent message and
  cost. It includes the earlier runs listed below.

## Result

| Stage | Outcome |
|---|---|
| Extract rules | 54 testable rules, 56 excluded clauses; quote verifier passed |
| Spend + findings analysts | `analytics.json` (7 tests), 13 full lists; `history.json` (20 audits, 9 risk themes, the council's scoring method) |
| Risk assessor | 7 risks rated on the council's likelihood × impact method |
| Auditor gate | Richard Wen: 6 approved, 1 amended (R-02 likelihood 4 → 3, as the payments just below £25k do not outnumber those just above), 0 rejected. Register revision 1 |
| Agent team | Pack v1 → v3. QA failed v1 on one memo figure; the planner fixed it in v2. The challenger raised 12 challenges over two rounds: 11 resolved, and 1 for the auditor (#4: Personal Budgets, a Limited Assurance audit, sits in no risk). 12 tests, 534 sampled transactions |
| QA | `review.md`: **READY FOR SIGN-OFF (4/4 checks pass)**: quotes, numbers (544 figures), trace, samples (534 transactions) |
| Sign-off | Signed off by the auditor in `outputs/review.md` |

The four QA checks were re-run locally on this folder's outputs with
`scripts/checks/run_checks.py`. They gave the same verdict: 4/4 pass.

## Run log

| Log | Started (UTC) | Stage | Status | Cost |
|---|---|---|---|---|
| `20261017-210201-52f4.json` | 2026-10-17 21:02 | extract-rules | ok | $1.23 |
| `20261017-210755-a4cd.json` | 2026-10-17 21:07 | analysts | ok | $1.98 |
| `20261017-211308-42ba.json` | 2026-10-17 21:13 | risk-assessor | ok | $1.16 |
| `20261017-211934-4f44.json` | 2026-10-17 21:19 | findings-analyst | ok | $1.38 |
| `20261017-212454-5613.json` | 2026-10-17 21:24 | risk-assessor | ok | $1.05 |
| `20261017-212816-df92.json` | 2026-10-17 21:28 | revise-register | ok | $0.34 |
| `20261017-213036-31e4.json` | 2026-10-17 21:30 | team | stopped | $3.53 |
| `20261019-053905-de39.json` | 2026-10-19 05:39 | extract-rules | ok | $0.37 |
| `20261019-054415-8759.json` | 2026-10-19 05:44 | analysts | ok | $0.84 |
| `20261019-055108-2f0e.json` | 2026-10-19 05:51 | risk-assessor | failed | $0.27 |
| `20261019-055931-6470.json` | 2026-10-19 05:59 | findings-analyst | ok | $0.09 |
| `20261019-060105-2088.json` | 2026-10-19 06:01 | risk-assessor | ok | $0.18 |
| `20261019-060151-3c49.json` | 2026-10-19 06:01 | revise-register | ok | $0.07 |
| `20261019-063049-d825.json` | 2026-10-19 06:30 | revise-register | ok | $0.12 |
| `20261019-063424-824c.json` | 2026-10-19 06:34 | team | ok | $1.07 |

The 2026-10-17 runs used Opus. That team run stopped when the API credit ran out; its
outputs were later replaced. The 2026-10-19 runs used Sonnet and produced this folder.

Two problems found during the run were fixed and redeployed:

- The 05:51 risk-assessor run failed because the findings-analyst wrote
  `scoring_method.evaluation_levels` as an object, not a list. The risk-assessor
  stopped and reported it rather than editing an input it does not own.
  `verify_history.py` now fails that shape at the analyst stage (commit `24dabae`).
- The sign-off form wrote its date into the QA report's `Date:` line rather than the
  sign-off block (commit `d44a73e`).
