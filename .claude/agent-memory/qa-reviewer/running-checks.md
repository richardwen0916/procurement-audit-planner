---
name: running-checks
description: How run_checks.py behaves (output format, exit code, expected trace failures before the challenge rounds close)
metadata:
  type: reference
---

- Run from the repo root: `.venv/bin/python scripts/checks/run_checks.py` (no flags needed). It runs all four checks and prints one `SUMMARY <check>: ...` line per check, then a ready-made markdown table and a `VERDICT:` line. Exit code 0 = all pass, 1 = BLOCKED. Copy the table into review.md verbatim.
- The quotes check calls verify_quotes.py internally and prints its own one-line result. Quote that line in review.md as well.
- check_trace.py reads outputs/challenges.md. Before the challenger writes it, trace fails with `challenges.md missing`. While the rounds are running, it fails with `challenges still open: #...`. Both are expected-pending, not planner failures. Write review.md only after CHALLENGER DONE and PLANNER DONE.
- outputs/challenges.md and outputs/review.md can be left over from an earlier session, so trace can PASS on v1 against old challenges. Compare challenges.md's mtime with the pack files (`ls -lT outputs/`) and treat an early trace PASS as provisional. Before writing review.md, look at it and replace the old one completely.
- The challenger can fix challenges.md without a pack rebuild (no new PACK READY). Re-run the checks when they say so; the pack version stays the same.
- In relayed sessions (no team messaging tools), put the protocol messages at the end of the handback report for the lead to send.
