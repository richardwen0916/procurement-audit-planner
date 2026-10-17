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

5. **Revision overrides (2026-10-16, rev 1):** for a score override, change only `likelihood.score` (leave `rubric` as the row the data meets) and log `override: true`; the builder then shows "Rubric Lx" beside the overridden score. When quoting the auditor's comment in a justification, drop its typed figures and restate them as `{{…}}` placeholders, or the typed-figure check warns. Log the justification edit as its own change entry.

6. **Quoting a £ figure from an auditor comment (2026-10-16, rev 1):** `|gbp` renders pence ("£N.00"), so the quote no longer matches the comment. Write `£{{path|int}}` instead to reproduce the auditor's wording. Get the threshold value from a parameter path such as `$.tests.split_purchases.by_threshold.<t>.threshold`.
   **Why:** a successful build re-stamps auditor-comments.md to the new revision, so any later edit, even a cosmetic one, FAILs with "set revision.number to N+1". **How to apply:** get the wording right before the first successful revision build. If you find a flaw afterwards, revert to the built text (the rebuild is idempotent, same build hash) and report the flaw rather than starting an unrequested revision.
