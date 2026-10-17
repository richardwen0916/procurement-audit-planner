---
name: selfcheck-tips
description: Self-check comparison pitfall - analytics.json top-20 values are rounded to 2 dp
metadata:
  type: project
---

topn() in analyse.py rounds floats to 2 dp in the top-20 lists, so self-check comparisons of ratios must
round the re-derived value to 2 dp (an exact comparison failed spuriously on 2026-10-15). The CSVs in
analytics-full hold unrounded values.
