---
name: input-format-quirks
description: Parsing quirks in contracts.csv dates/supplier field and spend workbook row numbering, with fixes
metadata:
  type: project
---

- contracts.csv `Published Date` mixes `+01:00` offsets and `Z` suffix. Python 3.10 `datetime.fromisoformat` rejects `Z`.
  **Why:** clean.py stopped on first run (2026-10-15). **How to apply:** parse with explicit `%Y-%m-%dT%H:%M:%S%z`, convert to UTC.
- Spend sheet row for a data row = pandas index + header_index + 2 (header found via header=None scan). Verified against
  openpyxl for every row in clean.py. **How to apply:** keep that assertion; it guards row_id against blank leading rows.
- Supplier column name in contracts.csv is literally `Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]`.
  Some non-council rows pack hundreds of blocks; filter to the council before inspecting block counts.
