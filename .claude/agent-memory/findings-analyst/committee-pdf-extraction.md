---
name: committee-pdf-extraction
description: Structure quirks of the committee PDFs and quoting techniques that pass scripts/verify_history.py
metadata:
  type: project
---

How-to lessons for extracting committee papers (learned 2026-10-15). Not evidence; re-read the PDFs every run.

- **Completed-work appendices: plain text breaks table rows.** Row cells get split by directorate headings, so some title/opinion pairs are not adjacent. Read rows from the `-layout` text; quote "Title Opinion" only when it is contiguous in plain text, otherwise quote the title alone (or the contiguous fragment) and add an `extraction_note`. **Why:** verifier matches against plain pdftotext. **How to apply:** for every row, check adjacency in plain text before choosing the quote.
- **Verifier normaliser strips hyphens/dashes and bullets** (`[-•▪●⁃…]` → space, en dash → hyphen → space), so quotes spanning "15 -25", "Advisory – no", "• Score 9" verify as long as the words match. Quotes must be ≥12 chars, so short cells (e.g. "100%") need a row-level quote.
- **Strategy tables:** Table 1 (impact) and Table 3 (appetite) garble in plain text but each cell's text survives contiguously; quote cell by cell. Table 3 spans two pages, and a cell can straddle the boundary: quote the part on one page. Table 3 marks the appetite by shading, which text extraction loses, so take the set levels from the 5.10 statements.
- **Strategy page numbers:** the printed page equals the PDF page from the Appendix A cover onward; the covering-report pages print none. Appendix 1 (policy) restarts section numbering, so label it "Appendix 1, x.y".
- **Plan covering report** is the covering report only. Its appendices are listed in section 8 but not included. It prints no page numbers, so cite sections.
- **Known absent:** Corporate/Strategic Risk Register (exempt), plan Appendices A–F, and the covering reports for the completed-work appendices. No paper lists individual agreed actions.
- Building history.json from a Python script in the scratchpad (helper that makes a source/page/quote dict) worked well and passed the verifier first time.
