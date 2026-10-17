---
name: challenge-techniques
description: How to find weak samples/tests in the planner's pack quickly — which analytics.json sections to compare against which pack fields
metadata:
  type: feedback
---

Techniques that surfaced the strongest round-one challenges (how-to only, no findings):

- Compare each test's sample `where` filter with the `by_dominant_tag` split of the
  same metric. The excluded tag often holds most of the £. Exemption from competition
  (placements) does not exempt a payment from evidence or duplicate controls.
- For clustering, read below_band vs above_band_comparator per tier before accepting
  which tier the sample targets; the tier with the signal may be untested.
- Scan every sample table's Supplier column for public bodies (council, CNCL, NHS) that
  slipped the inter-authority word list, and for non-procurement narratives.
- Check `per_group_n` caps against `n_payments` in the top20 windows: a capped draw
  cannot settle "is this one requirement" or cumulative over-spend questions.
- Ratio or cumulative indicators (spend vs award) need spend-to-date evidence, not
  the largest single payments. Ask for a ledger PBC item.
- Look for tests that grade against a value the analytics marks null in `$.skipped`;
  ask for a PBC item supplying it rather than dropping the test.
- Trace each rule in the register's per-risk Sources into the control's cites; missing
  ones are cheap, concrete `control` challenges.

- Ask only for sample filters on columns the analytics-full CSV actually has (asks
  like "regular interval" or "repeat suppliers first" were declined as inexpressible).
  Phrase asks as where/exclude/order_by on named columns.
- Sizing rules come from the audit-program skill; the planner will decline larger
  samples. Spend those challenges on what is drawn, not on how many.
- The builder writes the memo Scope section; the planner controls only purpose,
  background, approach and limitations text. Ask for "a memo line", not a section.
- After a refill, re-scan the new sample rows: exclusions pull in the next payees,
  which may be non-procurement (contributions, fees, wallet top-ups).

- Cross-sample overlap is a cheap, accepted ask: the same supplier drawn in several
  tests wastes slots. Ask for "excluding suppliers already drawn in T-x"; the builder
  draws in plan order, so the planner may reorder the risks to make that work.
- Pass rules often lack a legitimate route (call-off under a term contract; one-off
  purchase below the quote tier). Ask "what would a compliant item look like?" for each test.
- QA's check_trace.py checks every challenge row's Evidence cell for a rule ID, metric path
  or history ID. "as #3" fails, so repeat the actual citations in repeated challenges.
- Read `samples/T-*.csv` (narrative column) to re-scan draws; analytics-full is off limits.

**Why:** these were found by cross-reading, not by reading the pack alone; the pack
looks internally consistent and passes builder checks.
**How to apply:** run this checklist first, then order challenges by £ moved.
Use analytics metric paths for every number; never compute sums yourself — ask the
builder to report coverage (sampled £ vs headline £) instead.
