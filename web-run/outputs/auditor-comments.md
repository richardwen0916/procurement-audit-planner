# Auditor decisions on the risk register

<!-- register: rev 1 · build 1c50332c723c -->

Register: `outputs/risk-register.md`, revision 1 (build `1c50332c723c`).

For each risk write one **Decision**: `Approve` (in scope as rated), `Amend` (say what to change in **Comment**) or `Reject` (take it out of audit scope; say why). Do not use the `|` character in a comment. Leave the other columns as they are; they are rewritten on each build and your decisions are kept.

| Risk | Title | L × I = Score | Band | Decision | Comment |
|---|---|---|---|---|---|
| R-01 | Requirements split below the quotation and notice threshold | 4 × 5 = 20 | Extreme | Approve |  |
| R-02 | Payments clustered just below the quotation threshold | 3 × 3 = 9 | Medium - High | Amend | Lower likelihood to 3. 10 payments sit just below £25k against 52 just above (46 vs 52 across all spend), so the data shows no clustering below the threshold. │ │ (12)                        │          │  Keep in scope as a targeted test of the 10 payments. |
| R-03 | High-value suppliers with no contract notice found | 4 × 5 = 20 | Extreme | Approve |  |
| R-04 | Spend continuing after matched contract notices ended | 3 × 4 = 12 | Medium - High | Approve |  |
| R-05 | Spend running above the annual rate of the award | 3 × 5 = 15 | Extreme | Approve |  |
| R-06 | Same supplier, same amount paid more than once within a short period | 4 × 3 = 12 | Medium - High | Approve |  |
| R-07 | Waivers, exceptions and award approvals not evidenced | 2 × 3 = 6 | Moderate | Approve |  |
