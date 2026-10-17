---
name: risk-assessment
description: Rate procurement risks for the West Berkshire audit plan on the council's own likelihood × impact method. The agent writes judgments with citations to outputs/risk-ratings.json; build_register.py resolves every citation and figure, computes scores and bands from history.json, and renders outputs/risk-register.md and the auditor's decision template outputs/auditor-comments.md. Loaded by the risk-assessor agent.
---

# risk-assessment

Turn `rules.json`, `analytics.json` and `history.json` into a rated risk
register that a human auditor approves, amends or rejects.

**Division of labour.** You (the agent) judge: which risks exist, which rubric
row each meets, which impact dimension applies, and why. The builder
(`build_register.py`) does everything mechanical: it resolves citations, fills
every figure from analytics.json, multiplies, looks up the matrix label and
band, applies the repeat-finding uplift, checks your rubric choice against the
data, and renders the files. You never type a number that comes from data, and
you never compute a score.

Governing principles (CLAUDE.md): Python computes every number; everything
traceable; indicators, not accusations; context discipline; missing or
malformed input means stop and report.

## Files

| | Path | Who writes it |
| --- | --- | --- |
| In | `outputs/rules.json` | `/extract-rules` |
| In | `outputs/analytics.json` | spend-analyst |
| In | `outputs/history.json` | findings-analyst |
| **Your output** | `outputs/risk-ratings.json` | you |
| Out | `outputs/risk-register.md` | builder |
| Out | `outputs/auditor-comments.md` | builder (auditor fills in Decision and Comment) |
| Out | `outputs/risk-register.json` | builder: machine-readable state (scores, figures, applied decisions). Used for revision diffs and by QA. Never edit it |

Run the builder with:

```bash
.venv/bin/python .claude/skills/risk-assessment/build_register.py
```

Exit codes: `0` clean; `2` built, but one or more risks were dropped (fix and
re-run); `1` failed, nothing written (read the `FAIL` lines).

## Step 1: Read the inputs (aggregates only)

- `rules.json`: rule IDs, clauses, conditions, `notes`.
- `analytics.json`: read the structure and headline counts. **Never** load an
  `analytics-full/` CSV into context; cite the summary paths instead. Note
  `skipped` and `population.limitations`: a skipped test is not a zero.
- `history.json`: `audits` (AUD-*), `risk_themes` (RT-*), `agreed_actions`,
  `discrepancies` (DSC-*), `gaps`, `scoring_method`.

If `scoring_method.usable` is false, the builder falls back to a 1–5 Very
low…Very high scale and says so in the header; you rate the same way.

## Step 2: Choose the risks

One risk per theme where a rule, a metric or a history item gives evidence.
Typical themes, each with the analytics path that measures it (paths checked
against analytics.json of 2026-10-15; confirm they still exist):

| Theme | Rules | Count metric (general procurement) |
| --- | --- | --- |
| Requirements split below a threshold | CPR-12, CPR-53–55 | `$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows` |
| Payments clustered just below a threshold | CPR-53–55 | `$.tests.threshold_clustering.by_threshold.25000.below_band_by_tag.general_procurement.count` |
| High-value suppliers with no contract notice found | CPR-34, CPR-54–57 | `$.tests.off_contract.headline_unmatched_general_procurement.suppliers` |
| Spend after every matched notice ended (extension approval) | CPR-61 | `$.tests.expired_notice_spend.by_dominant_tag.general_procurement` |
| Spend above the award's annual rate (variation approval) | CPR-62 | `$.tests.spend_vs_award.flagged_ratio_ge_threshold` |
| Same supplier, same amount within 7 days | CPR-31 | `$.tests.duplicates.tiers.different_time.by_dominant_tag.general_procurement.groups` |
| Waivers/exceptions, award approvals, contract records | CPR-19–26, CPR-49–52 | none (council records only): rubric L2 |

Use general-procurement counts where analytics splits by tag: care and
education placements are exempt from competition (CPR-63, App C row F) and
grants follow a different route. Mention the placement figures as context, not
as the count. Where a test was skipped (e.g. the statutory-threshold tiers),
say so in the evidence; do not rate the skipped tier.

## Step 3: Likelihood: the rubric

The council's likelihood scale (history.json `scoring_method.likelihood_scale`)
is the probability the risk occurs within 12 months. For audit planning, "the
risk occurs" means **the control the rule requires does not operate for at
least one transaction in the next 12 months**. Rate at the strategy's
**actual** level: current controls, as evidenced by the data.

Pick the **one** row the evidence meets. The builder checks your row against
the count metric, so two runs on the same evidence give the same score.

| Row | Score | Evidence that meets it | `count_metric` |
| --- | --- | --- | --- |
| L1 | 1 Rare | A full-population test for this risk ran and found **0** instances in general procurement | required; resolves to 0 |
| L2 | 2 Unlikely | **No public-data test can measure this risk** (council-records rules). Absence of evidence is not evidence of absence, so it is rated Unlikely, never Rare | must be `null` |
| L3 | 3 Likely | Test found **1–9** instances in general procurement | required; 1 ≤ value ≤ 9 |
| L4 | 4 Almost certain | Test found **10 or more** instances in general procurement | required; value ≥ 10 |
| L5 | 5 Certain | A source states the control **is not operating**: an open or overdue agreed action on the same control. Data indicators alone never reach L5 | `null`; justification must cite `[history:<agreed_actions id>]` |

Cut-offs (10; L5 needs an agreed action) are constants at the top of
`build_register.py` (`L3_MAX`, `L4_MIN`); change them there, not per risk.

The count must be an **integer count of instances** (windows, payments,
suppliers, groups), never a £ figure, and the justification must show it as a
`{{…}}` placeholder.

**Repeat-finding uplift.** If a past audit on the **same theme** had an
adverse opinion (Limited Assurance, Weak, No Assurance, or implementation
Unsatisfactory), add `"uplift": {"history_id": "AUD-nn", "justification": "…"}`.
The builder checks the opinion is adverse, adds one point (capped at 5) and
states it in the register. Do not change `score` yourself. If you cite an
adverse audit without applying the uplift, the builder warns; say in the
justification why the theme differs.

## Step 4: Impact

Choose the **one** Table 1 dimension the evidence speaks to most directly:
`financial`, `personal`, `assets`, `reputation` or `compliance`.

- **financial**: set `basis_metric` to the £ figure at stake for the risk
  (the annualised estimate or window total of the flagged general-procurement
  population). The builder maps it to the Table 1 £ bands and your `score`
  must match. Prefer this dimension whenever the analytics gives a £ figure.
- **any other dimension**: `basis_metric` is `null`. Choose the score whose
  Table 1 descriptor fits, and quote or paraphrase that descriptor in the
  justification. The builder prints the descriptor next to your score so the
  auditor can see the match. Use `compliance` for rules whose failure is a
  legal/publication breach (e.g. CDP notices, Key Decisions).

## Step 5: Write `outputs/risk-ratings.json`

```json
{
  "assessment_level": "actual",
  "risks": [
    {
      "risk_id": "R-01",
      "title": "Requirements split below the quotation threshold",
      "status": "proposed",
      "rule_ids": ["CPR-12", "CPR-54"],
      "risk": "Related payments to one supplier may together exceed a threshold that each single payment stays under, so the quotation and notice requirements of [rule:CPR-54] may not be applied ([rule:CPR-12]).",
      "likelihood": {
        "rubric": "L4",
        "score": 4,
        "count_metric": "$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows",
        "justification": "{{$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows}} supplier windows in general procurement combine to cross the threshold [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement].",
        "uplift": null
      },
      "impact": {
        "score": 5,
        "dimension": "financial",
        "basis_metric": "$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp",
        "justification": "The windows total {{$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp}} in the period [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp]."
      },
      "evidence": [
        "Placements shown separately: {{$.tests.split_purchases.by_threshold.25000.placement_separately.windows}} windows, exempt under [rule:CPR-63]."
      ],
      "proposed_focus": "Test the largest general-procurement windows for a single requirement and the quotation evidence required by [rule:CPR-54]."
    }
  ],
  "revision": null
}
```

Field rules:

- `risk_id`: `R-NN`, unique, stable across revisions (never renumber).
- `status`: `proposed`, or `rejected` only when applying an auditor Reject.
- Prose fields (`risk`, both `justification`s, `evidence[]`,
  `proposed_focus`, uplift `justification`) may contain:
  - **citations**: `[rule:CPR-NN]`, `[metric:$.path.in.analytics]`,
    `[history:AUD-NN|RT-NN|DSC-NN|…]`;
  - **figures**: `{{$.path}}`, optionally with a format, `{{$.path|gbp}}`,
    `|int`, `|num`, `|raw`. Default format follows the key name (keys with
    `gbp`, `total`, `annualised`, `awarded_value`, `award_annual_rate` are
    shown as £).
- Paths start at `$`, use `.key` for object keys (numeric keys too:
  `.by_threshold.25000`) and `[n]` for list items.
- **Hard rule:** each `likelihood.justification` and `impact.justification`
  must contain at least one resolvable citation tag. A risk with none, or
  with any citation or placeholder that does not resolve, or whose rubric row,
  financial band or uplift does not check out, is **dropped** from the
  register and listed under "Not included" with the reason.
- **No typed figures.** Any figure from the data goes in a placeholder. The
  builder warns on £ amounts, percentages, decimals and numbers of two or more
  digits typed in prose. Clause numbers belong in `[rule:…]` tags.
- **Indicator language.** Describe patterns to investigate. The builder warns
  on words such as fraud, corrupt, misconduct, unlawful, deliberate. A warning
  is not an error, but each one needs a reason to stay.

## Step 6: Build, fix, report

Run the builder until it exits `0`. Fix each `DROPPED` and `FAIL` by fixing
the rating, never by loosening a citation. Review every `WARN`.

Report to the lead: the risks in score order (ID, title, L × I = score, band),
any dropped risks and why, the scoring-method conflicts the header lists, and
that the auditor's next step is to fill in `outputs/auditor-comments.md`.

## Scoring-method conflicts

history.json records conflicts inside the Risk Management Strategy. The
builder never resolves one silently. It uses one reading, marks the other in
the register, and lists both in the header:

- **Corporate Risk Register threshold** (Figure 4 says score 9 or above,
  Table 4 says 15–25): the builder uses **Table 4** (it defines the bands and
  their escalation, and agrees with 6.3, which escalates Extreme risks). Risks
  scoring 9–14 are marked † "would qualify under Figure 4".
- **Band names** (Figure 1 "High" vs Table 4 "Medium - High"): the register
  shows both, Matrix (Figure 1) and Band (Table 4).
- **Shared £ endpoints between impact bands**: a value equal to a shared
  endpoint goes to the higher band, except where the higher band is printed
  as strictly greater (">£2m"), in which case it stays in the lower band.
- **Other discrepancies** (e.g. the prose "Medium (2)" vs Table 1 "3"): the
  builder reads labels and scores only from Table 1, Table 2, Figure 1 and
  Table 4, and lists every scoring discrepancy in the header.

## Revisions after the auditor gate

The auditor writes one decision per risk in `outputs/auditor-comments.md`:
**Approve**, **Amend** (the comment says what to change) or **Reject**
(take the risk out of audit scope). Then you are re-run:

1. Read the decisions. For each **Amend**, change only what the comment asks.
   For each **Reject**, set `"status": "rejected"`. Change nothing on
   Approved risks.
2. Add a `revision` block:

```json
"revision": {
  "number": 1,
  "summary": "Applied auditor decisions of 2026-10-20.",
  "changes": [
    {"risk_id": "R-02", "field": "impact.score", "decision_ref": "R-02",
     "override": true, "note": "Auditor raised impact; rubric band is 3."},
    {"risk_id": "R-04", "field": "status", "decision_ref": "R-04", "note": "Rejected by auditor."}
  ]
}
```

- `number` = previous revision + 1 (the first revision after the draft is 1).
- One entry per changed field. Fields: `title`, `risk`, `rule_ids`,
  `status`, `likelihood.rubric`, `likelihood.score`, `likelihood.count_metric`,
  `likelihood.justification`, `likelihood.uplift`, `impact.score`,
  `impact.dimension`, `impact.basis_metric`, `impact.justification`,
  `evidence`, `proposed_focus`; or `added` for a new risk the auditor asked
  for (then `decision_ref` names the Amend row that asked for it).
- `override: true` when the auditor's instruction takes a score away from
  what the rubric or £ band gives. The builder then accepts the score, marks
  "Auditor override" and shows what the rubric gives.
- All decisions Approve: still add `{"number": 1, "changes": []}`.

The builder compares your ratings with the version the auditor saw and
**fails** if: a decision was not applied (Amend with no change, Reject without
`status: rejected`), anything changed that no Amend/Reject asked for, a logged
change was not made, or the auditor's file belongs to a different build.
It writes a revision header naming every change, with the auditor's comment
beside it.
