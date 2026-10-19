---
name: builder-pitfalls
description: build_register.py syntax traps - list indices in citation tags, typed-figure regex hits on risk IDs and day counts, where AUD no-uplift reasons go, how to log revision overrides
metadata:
  type: feedback
---

Builder syntax traps found on 2026-10-16 (first draft run):

1. **No `[n]` list index inside a `[metric:…]` tag.** CITE_RE stops at the first `]`, so `[metric:$.population.limitations[4]]` does not resolve and the risk is DROPPED. List items work inside placeholders: `{{$.skipped[0].reason|raw}}`. For a citation, cite a nearby dict path instead.
   **Why:** a dropped risk means exit 2. **How to apply:** use tags only for dict-only paths; use `{{…|raw}}` for list items.

2. **The typed-figure regex catches any number of two or more digits.** That includes "R-03" (it reads as `03`) and "30 days". Refer to other risks by description, not ID, and put window lengths in placeholders, e.g. `{{$.tests.split_purchases.parameters.window_days}}`.

3. **Citing an adverse audit without an uplift gives a WARN** that stays even with a reason. Put the "theme differs" reason in `likelihood.justification` (the skill asks for it there), not in evidence. Report the WARN as deliberate.

4. **Top-level `excluded` in risk-ratings.json is ignored by the builder.** Excluded themes appear only in the report to the lead, not in the register.

5. **Revision overrides (2026-10-16, rev 1):** for a score override, change only `likelihood.score` (leave `rubric` as the row the data meets) and log `override: true`; the builder then shows "Rubric Lx" beside the overridden score. When quoting the auditor's comment in a justification, drop its typed figures and restate them as `{{…}}` placeholders, or the typed-figure check warns. Log the justification edit as its own change entry. Do NOT add a risk-level `"auditor_override": true` key (as the agent prompt suggests): the builder treats it as an unlogged change and FAILs with "unrequested change: … auditor_override" (seen 2026-10-17). `override: true` in the revision change entry is what marks the override; a `likelihood.auditor_override` key was tolerated.

6. **Quoting a £ figure from an auditor comment (2026-10-16, rev 1):** `|gbp` renders pence ("£N.00"), so the quote no longer matches the comment. Write `£{{path|int}}` instead to reproduce the auditor's wording. Get the threshold value from a parameter path such as `$.tests.split_purchases.by_threshold.<t>.threshold`.
   **Why:** a successful build re-stamps auditor-comments.md to the new revision, so any later edit, even a cosmetic one, FAILs with "set revision.number to N+1". **How to apply:** get the wording right before the first successful revision build. If you find a flaw afterwards, revert to the built text (the rebuild is idempotent, same build hash) and report the flaw rather than starting an unrequested revision.

7. **history.json schema drift crashes the builder before any risk is checked (2026-10-17).** `Method.__init__` expects `scoring_method.likelihood_scale` and `impact_scale` as *lists* of `{score, label, …}`, `combination.cells` as a list of 25 `{likelihood, impact, label, score_printed}`, and `corporate_register_threshold` keyed by reading (`table_4`, `figure_4`, each with `section` and `score_at_or_above`). A findings-analyst output with `{entries: […]}` scales, `matrix_rows` instead of `cells`, or a single flat CRR object gives a TypeError traceback (exit 1, nothing written).
   **Why:** the inputs and builder are read-only for this agent, so the run must stop. **How to apply:** if the builder dies in `Method`, compare these four keys first, then stop and report the mismatch so findings-analyst can be re-run. Do not reshape history.json yourself. Draft risk-ratings.json first anyway; it can be rebuilt once history.json is fixed.

8. **The skill's theme table rule IDs can be stale (2026-10-17).** The IDs in the SKILL.md theme table did not match the current rules.json numbering (e.g. extension, variation, placement-exemption and written-evidence rules sat on different CPR numbers). **Why:** a wrong ID still resolves if the number exists, so the builder won't catch a mis-cited rule. **How to apply:** map each theme to rules by reading `condition`/`required_action` in the current rules.json, never by the table's numbers.

9. **Placeholders for the spend-data publication floor (2026-10-17).** No dict path holds it; it sits in a list (`thresholds_not_tested`), so use a `{{…[n].value|int}}` placeholder after checking the index, and don't borrow a nearby threshold path (one draft did, and stated the wrong floor).

10. **`scoring_method.evaluation_levels` must be a list of `{level, …}` (2026-10-19).** history.json had it as a dict keyed `gross`/`actual`/…, so build_register.py line ~873 died with `AttributeError: 'str' object has no attribute 'get'` (exit 1, nothing written). Same class as item 7. **How to apply:** after drafting ratings, if the builder dies in `main` or `Method`, check the shape of every `scoring_method` key against what the builder iterates, then stop and report for findings-analyst to re-run. Do not edit history.json or the builder. Keep the drafted risk-ratings.json; it rebuilds once the input is fixed.

11. **Dates in justification text trip the typed-figure WARN (2026-10-19, rev 1).** Writing "comment of 2026-10-19" in a justification gave three WARNs (2026, 10, 19). **How to apply:** write "the auditor's comment" with no date. Also, auditor comments can contain pasted table-border debris (│ characters); quote only the meaningful part and don't try to fix the comments file.
