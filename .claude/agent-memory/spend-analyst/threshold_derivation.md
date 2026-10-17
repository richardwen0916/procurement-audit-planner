---
name: threshold-derivation
description: How thresholds/competition/publication flags are derived from rules.json and the high-value threshold choice
metadata:
  type: feedback
---

Derive inclusivity from the trigger side (threshold_low); if a value only appears as an upper bound "less than T",
T triggers (inclusive). Flag a boundary gap when rules say both "above T" and "less than T".
Competition-triggering = trigger-side required_action matches `quot|tender`; this makes the App B row A
(one quote, no advertising) value the lowest competition threshold.
For high_value_suppliers/off_contract I used the lowest competition threshold whose rule requires Portal/CDP
publication, and reported the lowest-competition tier as counts only.
**Why:** the agent spec says "lowest competition-triggering threshold" but also "publication threshold"; CLAUDE.md
says the tender/publication threshold. Taking the literal reading would class nearly every supplier.
**How to apply:** keep this choice, state it in the report, and ask the lead/auditor to confirm it (2026-10-15).
Values cited only by required-action rules (transparency duties) are listed under thresholds_not_tested.
