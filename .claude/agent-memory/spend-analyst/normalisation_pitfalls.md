---
name: normalisation-pitfalls
description: Supplier-name normalisation and exclusion-regex pitfalls found in WBC spend data, and fixes applied
metadata:
  type: project
---

- Trading-as appears as `T/A`, `t/a:`, `T/AS`, `( T/A ...)` and `Trading as`. A `\bT/A\b` regex misses `T/AS`.
  **Fix:** `\bT\s*/\s*AS?\b.*$` (2026-10-15). Stripping the suffix discards the trading name, which is sometimes the
  only name on the notice side; consider proposing to the auditor a second match key on the trading name.
- The fixed inter_authority supplier regex (`COUNTY`, `BOROUGH`, ...) can catch non-public bodies whose name contains
  those words (e.g. county sports partnerships). **How to apply:** after clean.py, list inter_authority suppliers via
  value_counts and report any false positive rather than silently editing the spec regex.
- "(excl Joint Arrangements)" appears inside a narrative; the JOINT ARRANGEMENTS narrative clause would match it.
  Log rows matched by narrative only (clean.py does) and check that count.
