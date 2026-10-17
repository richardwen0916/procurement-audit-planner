# Procurement Audit Planner (West Berkshire Council)

An agentic system built with Claude Code to plan an internal audit of procurement
for West Berkshire Council from public data. It:

1. turns the council's purchasing rulebook into testable rules,
2. analyses the full spend population against those rules,
3. reads past audit history,
4. rates the risks on the council's own scale, and
5. produces a cross-checked audit planning pack for a human auditor to approve.

**Live app:** https://procurement-audit-planner.fly.dev is an independent web harness
(FastAPI + Claude Agent SDK, hosted on Fly.io). It runs the whole workflow from the browser:
extract rules, the two analysts, the risk assessor, the auditor gate, the agent team and
sign-off. Anyone can view the outputs; starting a run needs a passcode. The code is in
[`harness/`](harness/), [`Dockerfile`](Dockerfile) and [`fly.toml`](fly.toml).

The full system specification is in [`CLAUDE.md`](CLAUDE.md). This README covers:

- the skills and agents,
- how they work together,
- confirmation that every step of the build guide is complete.

Two design principles run through everything:

- **The LLM reads and judges; Python computes every number.** Every quote, figure and
  sampled transaction is re-checked by a script before sign-off.
- **The outputs are risk indicators to investigate, not findings.** Nothing in this repo
  alleges wrongdoing by the council, any department or any supplier.

---

## Skills (`.claude/skills/`)

| Skill | Who uses it | What it does | Script |
|---|---|---|---|
| **`extract-rules`** | The human runs it with `/extract-rules` | Turns `data/contract-rules.pdf` (Contract Procedure Rules, Part 8) into `outputs/rules.json`: one entry per testable rule, with clause, thresholds as GBP integers, required action, approver and a verbatim quote. The anti-splitting rule is tagged `anti-avoidance`, and clauses that can't be tested go in an `excluded` list with a reason. | `verify_quotes.py` checks every quote word for word against the PDF |
| **`risk-assessment`** | Loaded by the `risk-assessor` agent | The rating method. Risks are scored likelihood 1–5 × impact 1–5 on the council's own scale, taken from its Risk Management Strategy 2024–27. The agent writes cited judgments to `outputs/risk-ratings.json`. The builder resolves every citation, computes scores and bands, and renders `risk-register.md` and the auditor's decision template `auditor-comments.md`. A judgment with no citation (rule, metric or history item) is rejected, and a repeat finding raises likelihood by one point. | `build_register.py`, with fixture tests in `tests/` |
| **`audit-program`** | Loaded by the `planner` teammate | Turns the auditor-approved risks into the planning pack: risk → expected control → test step → targeted sample, plus the PBC (request) list. The planner writes its judgments to `outputs/audit-plan.json`. The builder checks the auditor gate, draws the samples from the full flagged lists, and renders the memo, the risk-control matrix, the audit program and `pack-figures.json`. | `build_pack.py` (`--gate` checks that the auditor has decided every risk) |

## Agents (`.claude/agents/`)

### Sub-agents (Phase 1–2)

| Agent | Inputs → outputs | Role |
|---|---|---|
| **`spend-analyst`** | `rules.json`, `data/spend/*.xlsx`, `data/contracts.csv` → `outputs/analytics.json`, `outputs/analytics-full/` | Writes and runs Python under `scripts/` (`clean.py`, `analyse.py`, `selfcheck.py`), then cleans and analyses the data (details below). Never does arithmetic itself. |
| **`findings-analyst`** | `data/committee/*.pdf` → `outputs/history.json` | Extracts past audit coverage and assurance opinions, agreed actions, risk themes and the council's risk-scoring method. Every item is sourced to a document and page, and `scripts/verify_history.py` checks each quote on its stated page. It reads and sources only; it never scores risks. |
| **`risk-assessor`** | `rules.json` + `analytics.json` + `history.json` → `risk-register.md`, `auditor-comments.md` | Follows the `risk-assessment` skill and stops at the auditor's approval gate. After a rejection it re-runs with the auditor's decisions and produces the next revision of the register. |

The `spend-analyst`'s analysis in detail:

- **Cleaning:** it cleans three monthly spend workbooks, finding the header row in each and normalising supplier names.
- **Contract notices:** it parses the raw Contracts Finder export, unpacking the supplier strings and parsing every date with an explicit format.
- **Tests:** it runs threshold clustering, split purchases, off-contract spend, duplicate payments, spend after a notice expired, and spend against the award value. Every threshold comes from `rules.json`.

### Agent team (Phase 3)

These three run as teammates, enabled by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in
`.claude/settings.json`. They coordinate by messaging each other directly; the lead
session doesn't relay between them.

| Teammate | Owns | Role |
|---|---|---|
| **`planner`** | `audit-plan.json` → `planning-memo.md`, `risk-control-matrix.md`, `audit-program.md`, `samples/`, `pack-figures.json` | Runs the gate, writes the plan, runs `build_pack.py` until the build is clean, and announces `PACK READY v<n>`. It revises the plan in answer to challenges and QA failures, but leaves rating and scope points for the auditor. |
| **`challenger`** | `challenges.md` | Reads the plan against the evidence (`analytics.json`, `history.json`, `rules.json`) and challenges weak spots: samples, pass rules, missing rules, ratings, scope. It runs at most two rounds and ends each challenge as resolved, declined (with the reason accepted) or *for the auditor*. |
| **`qa-reviewer`** | `review.md` | Runs `scripts/checks/run_checks.py` on every version the planner announces and sends failures straight to the planner. Sign-off stays blocked until all four checks pass. |

The QA checks in `scripts/checks/`:

- **`check_quotes.py`:** every rule quote and register excerpt is in the source PDF.
- **`check_numbers.py`:** every figure in the pack matches the analytics outputs.
- **`check_trace.py`:** every rule traces to a risk, a control and a test, or has a not-tested reason. Every approved risk is planned, and no challenge is left open or uncited.
- **`check_samples.py`:** every sampled transaction exists in the spend data.

Each agent keeps how-to lessons (never evidence) in `.claude/agent-memory/<agent>/`.

---

## How they work together

```
                 [data/contract-rules.pdf]
                            |
         (1) /extract-rules  ← skill, invoked by the human
                            |
                       rules.json
                            |
        +-------------------+--------------------+
        |                                        |
 (2) spend-analyst  ← sub-agent           findings-analyst ← sub-agent
     spend xlsx + contracts.csv              committee PDFs
     writes + runs Python (scripts/)         reads and sources
        |                                        |
   analytics.json (+ analytics-full/)        history.json
        +-------------------+--------------------+
                            |
 (3) risk-assessor ← sub-agent, using the risk-assessment skill
                            |
              risk-register.md + auditor-comments.md
                            |
 (4) HUMAN GATE: the auditor approves / amends / rejects each risk
     → the risk-assessor re-runs and produces the next revision
                            |
 (5) AGENT TEAM (after build_pack.py --gate passes)
       planner ──PACK READY v<n>──► challenger, qa-reviewer
       challenger ──challenges (≤2 rounds)──► planner ──rebuild──► …
       qa-reviewer ──check failures──► planner
       all three ──DONE──► lead, who shuts the team down
                            |
 (6) HUMAN GATE: the auditor reads review.md + challenges.md and signs off
```

To run it:

1. Set up the environment: `python -m venv .venv && .venv/bin/pip install -r requirements.txt`.
   The verifiers also need `pdftotext` (poppler).
2. In Claude Code, run the steps in order:
   1. `/extract-rules`
   2. "Run the spend-analyst" and "Run the findings-analyst"
   3. "Run the risk-assessor"
   4. Fill in `outputs/auditor-comments.md` and re-run the risk-assessor.
   5. "Run the agent team", which follows the lead procedure in `CLAUDE.md`.
   6. Sign the block at the end of `outputs/review.md`.

To re-check the signed-off pack: `.venv/bin/python scripts/checks/run_checks.py`.

---

## Confirmation: build guide completed

I followed the build guide ([procurement-audit-planner.vercel.app](https://procurement-audit-planner.vercel.app/))
from Setup through Lesson 4 (Agent teams), and the steps below are complete. On
2026-10-16 every deliverable was checked against this repo, and every verifier was re-run.

### Setup

| Step | Deliverable | Status |
|---|---|---|
| 1.1 | Project folder, Claude Code running | ✅ |
| 1.2 | `CLAUDE.md` with the full specification | ✅ |
| 1.3 | `data/`: rules PDF, 3 spend workbooks (P02–P04), `contracts.csv`, 4 committee papers | ✅ |
| 1.4 | `.venv` with pandas and openpyxl, `requirements.txt` | ✅ |
| 1.5 | `.claude/skills`, `.claude/agents`, `scripts/`, `outputs/` | ✅ |

### Lesson 1: Skills

| Step | Deliverable | Status |
|---|---|---|
| 2.1 | `extract-rules` skill: `SKILL.md` + `verify_quotes.py` | ✅ |
| 2.2 | `outputs/rules.json`: 64 testable rules and 48 excluded clauses. Verifier: `ALL CHECKS PASSED (64 rules, 48 excluded, 0 warning(s))` | ✅ re-run |

### Lesson 2: Sub-agents

| Step | Deliverable | Status |
|---|---|---|
| 3.1 | `.claude/agents/spend-analyst.md` | ✅ |
| 3.2 | `outputs/analytics.json` (7 tests), `outputs/analytics-full/` (13 files), `scripts/clean.py`, `scripts/analyse.py`, `scripts/selfcheck.py`. Self-check: `8/8 passed` | ✅ re-run |
| 3.3 | `.claude/agents/findings-analyst.md`, `scripts/verify_history.py` | ✅ |
| 3.4 | `outputs/history.json`: 20 audits, 14 risk themes, the council's scoring method. Verifier: `ALL CHECKS PASSED` | ✅ re-run |
| 3.5 | `risk-assessment` skill: `SKILL.md`, `build_register.py`, fixture tests. Tests: `6 passed, 0 failed` | ✅ re-run |
| 3.6 | `.claude/agents/risk-assessor.md`; `CLAUDE.md` flow names it in step (3) | ✅ |
| 3.7 | `outputs/risk-register.md`, `outputs/auditor-comments.md`, `outputs/risk-ratings.json` | ✅ |

### Lesson 3: The human gate

| Step | Deliverable | Status |
|---|---|---|
| 4.1 | Decision template reviewed alongside the register | ✅ |
| 4.2 | Decisions recorded by Richard Wen on 2026-10-16: 8 approved, 1 amended (R-08 likelihood 2 → 3), 0 rejected | ✅ |
| 4.3 | `risk-register.md` rebuilt as **revision 1**, with the R-08 change marked as an auditor override | ✅ |

### Lesson 4: Agent teams

| Step | Deliverable | Status |
|---|---|---|
| 5.1 | Gate closed: `build_pack.py --gate` reports register revision 1, 9 decisions, **9 risks approved and in scope (R-01–R-09)**, none out of scope | ✅ |
| 5.2 | `.claude/settings.json` sets `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. A smoke test confirmed the three teammates start and message each other. | ✅ |
| 5.3 | `audit-program` skill: `SKILL.md` + `build_pack.py` | ✅ |
| 5.4 | `.claude/agents/planner.md`, with its message protocol | ✅ |
| 5.5 | `.claude/agents/challenger.md`, which owns `outputs/challenges.md` | ✅ |
| 5.6 | `.claude/agents/qa-reviewer.md`, plus `scripts/checks/`: `run_checks.py`, `check_quotes.py`, `check_numbers.py`, `check_trace.py`, `check_samples.py` | ✅ |
| 5.7 | Team run complete, with the results in the run summary below | ✅ re-run |
| 5.8 | Sign-off block in `outputs/review.md` completed: Richard Wen, 2026-10-16, **sign off** | ✅ |

The step 5.7 team run in figures:

- **Pack versions:** three, v1 to v3.
- **Challenges:** 12, of which 7 were resolved, 1 declined and 4 marked for the auditor (#3, #5, #9, #12). None is open.
- **Pack contents:** `planning-memo.md`, `risk-control-matrix.md`, `audit-program.md`, and 14 per-test sample files in `outputs/samples/` holding 385 sampled transactions.
- **QA verdict:** `review.md` reads **READY FOR SIGN-OFF**, with all 4 checks passing:
  - quotes: 64 rules
  - numbers: 403 figures
  - trace: 35 rules cited, 29 with a not-tested reason
  - samples: 385 transactions

The guide's own worked example closes the gate at register revision 2, with 10 decisions
(8 approved, 1 amended, 1 rejected). This run's register had 9 risks, and the auditor
rejected none. The gate therefore closed at revision 1, with all 9 risks in scope. The
outcome the guide requires for step 5.3, 9 approved risks in scope, is the same.

---

## Repository layout

```
CLAUDE.md                 system specification (read by Claude Code every session)
README.md                 this file
requirements.txt          pandas, openpyxl
.claude/
  settings.json           enables agent teams
  skills/                 extract-rules, risk-assessment, audit-program
  agents/                 spend-analyst, findings-analyst, risk-assessor,
                          planner, challenger, qa-reviewer
  agent-memory/           per-agent how-to lessons
data/                     public council inputs (read-only)
scripts/                  clean.py, analyse.py, selfcheck.py, verify_history.py
  checks/                 QA scripts run by the qa-reviewer
outputs/                  rules, analytics, history, register, signed-off pack
```

All the data is public:

- West Berkshire Council: Contract Procedure Rules, "Expenditure over £500", Governance
  Committee papers
- UK Government: Contracts Finder
