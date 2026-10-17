#!/usr/bin/env python3
"""Tests for build_register.py on the fixture in tests/fixture/.

Run: .venv/bin/python .claude/skills/risk-assessment/tests/test_build_register.py
Each case copies the fixture to a temporary directory, so nothing in outputs/ is touched.
"""
import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILDER = HERE.parent / "build_register.py"
FIXTURE = HERE / "fixture"
RESULTS = []


def run(root: Path):
    p = subprocess.run([sys.executable, str(BUILDER), "--root", str(root)], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def fresh() -> Path:
    d = Path(tempfile.mkdtemp(prefix="riskreg-"))
    shutil.copytree(FIXTURE, d, dirs_exist_ok=True)
    return d


def ratings(root: Path) -> dict:
    return json.loads((root / "outputs/risk-ratings.json").read_text())


def save(root: Path, obj: dict):
    (root / "outputs/risk-ratings.json").write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def good_only(root: Path) -> dict:
    """Fixture with R-02 replaced by a valid risk (needed for the revision cases)."""
    r = ratings(root)
    r["risks"][1] = {
        "risk_id": "R-02",
        "title": "Spend above the award value without an approved variation",
        "status": "proposed",
        "rule_ids": ["CPR-62"],
        "risk": "Annualised spend with some suppliers is above the annual rate of their published award, which may indicate a variation without the approval [rule:CPR-62] requires.",
        "likelihood": {"rubric": "L3", "score": 3,
                       "count_metric": "$.tests.spend_vs_award.flagged_ratio_ge_threshold",
                       "justification": "{{$.tests.spend_vs_award.flagged_ratio_ge_threshold}} of {{$.tests.spend_vs_award.eligible_suppliers}} eligible suppliers reach the flag ratio [metric:$.tests.spend_vs_award.parameters.ratio_flag].",
                       "uplift": None},
        "impact": {"score": 3, "dimension": "compliance", "basis_metric": None,
                   "justification": "A variation outside [rule:CPR-62] gives a reasonable possibility of challenge."},
        "evidence": [],
        "proposed_focus": "Request the variation approvals for the flagged notices under [rule:CPR-62].",
    }
    save(root, r)
    return r


def set_decisions(root: Path, decisions: dict):
    p = root / "outputs/auditor-comments.md"
    lines = []
    for line in p.read_text().splitlines():
        m = re.match(r"\| (R-\d+) \|", line)
        if m and m.group(1) in decisions:
            cells = line.strip().strip("|").split("|")
            dec, com = decisions[m.group(1)]
            cells[4], cells[5] = f" {dec} ", f" {com} "
            line = "|" + "|".join(cells) + "|"
        lines.append(line)
    p.write_text("\n".join(lines) + "\n")


def case(name):
    def deco(fn):
        try:
            fn()
            RESULTS.append((name, True, ""))
        except AssertionError as e:
            RESULTS.append((name, False, str(e)))
        return fn
    return deco


def expect(cond, msg):
    if not cond:
        raise AssertionError(msg)


# ---- The requested fixture: one good risk, one broken risk -----------------
@case("fixture: good risk rated, broken risk dropped with reasons")
def _():
    root = fresh()
    code, out = run(root)
    expect(code == 2, f"exit {code}, want 2 (built with drops)\n{out}")
    reg = (root / "outputs/risk-register.md").read_text()
    state = json.loads((root / "outputs/risk-register.json").read_text())
    r1 = next(r for r in state["risks"] if r["risk_id"] == "R-01")
    expect((r1["likelihood_base"], r1["likelihood"], r1["impact"], r1["score"]) == (4, 5, 5, 25),
           f"R-01 L/I/score {r1}")
    expect(r1["band"] == "Extreme" and r1["matrix_label"] == "Extreme" and r1["crr"] is True, f"R-01 band {r1}")
    expect([d["risk_id"] for d in state["dropped"]] == ["R-02"], f"dropped {state['dropped']}")
    errs = " ".join(state["dropped"][0]["errors"])
    for needle in ("does not resolve", "impact.justification: no resolvable citation",
                   "count_metric is 8, which meets rubric L3, not L4",
                   "impact.justification must show the basis_metric"):
        expect(needle in errs, f"R-02 errors lack '{needle}': {errs}")
    expect("WARN  R-02: impact.justification: typed figure '£2.9m'" in out, f"typed-figure warning missing\n{out}")
    for needle in ("£3,442,571.49", "64 supplier windows", "178 windows",
                   "likelihood raised by one point** from 4 to 5", "AUD-90",
                   "## Not included", "R-02", "Corporate Risk Register threshold conflicts",
                   "Figure 1 'High' = Table 4 'Medium - High'", "DSC-05", "Impact £ bands share endpoints"):
        expect(needle in reg, f"register lacks '{needle}'")
    rated = reg.split("## Not included")[0]
    expect("{{" not in rated and "[metric:" not in rated and "[rule:" not in rated, "unresolved markup in rated risks")
    expect(reg.rstrip().split("## ")[-1].startswith("Auditor decisions"), "register must end with Auditor decisions")
    com = (root / "outputs/auditor-comments.md").read_text()
    expect(re.search(r"\| R-01 \| .* \| 5 × 5 = 25 \| Extreme \|  \|  \|", com), f"R-01 template row\n{com}")
    expect("| R-02 |" not in com, "a dropped risk must not get a decision row")
    expect("Decided: 0 of 1." in reg, "decision count must cover rated risks only")
    shutil.rmtree(root)


@case("uplift citing a non-adverse audit drops the risk")
def _():
    root = fresh()
    r = ratings(root)
    r["risks"][0]["likelihood"]["uplift"]["history_id"] = "AUD-01"   # Reasonable Assurance
    save(root, r)
    code, out = run(root)
    expect(code == 2 and "AUD-01 (Reasonable Assurance); a repeat-finding uplift needs an adverse opinion" in out, out)
    shutil.rmtree(root)


@case("financial impact must match the Table 1 £ band")
def _():
    root = fresh()
    r = good_only(root)
    r["risks"][0]["impact"]["score"] = 4
    save(root, r)
    code, out = run(root)
    expect(code == 2 and "falls in Table 1 band 5" in out, out)
    shutil.rmtree(root)


@case("fallback scale when history has no usable method")
def _():
    root = fresh()
    good_only(root)
    h = json.loads((root / "outputs/history.json").read_text())
    h["scoring_method"] = {"usable": False, "reason": "fixture: no method"}
    (root / "outputs/history.json").write_text(json.dumps(h))
    code, out = run(root)
    reg = (root / "outputs/risk-register.md").read_text()
    expect(code == 0 and "**Fallback scale.**" in reg and "Very high" in reg, out)
    shutil.rmtree(root)


# ---- Revisions after the gate ----------------------------------------------
@case("revision: decisions enforced, unrequested change rejected, override marked, decisions kept")
def _():
    root = fresh()
    r = good_only(root)
    code, out = run(root)
    expect(code == 0, f"clean draft expected\n{out}")
    set_decisions(root, {"R-01": ("Approve", "Agreed."), "R-02": ("Amend", "Raise impact to 4 given the sums involved.")})

    code, out = run(root)
    expect(code == 1 and "no 'revision' block" in out, f"missing revision block must fail\n{out}")

    r["revision"] = {"number": 1, "summary": "Applied auditor decisions.", "changes": []}
    save(root, r)
    code, out = run(root)
    expect(code == 1 and "decision not applied: R-02 Amend" in out, f"unapplied Amend must fail\n{out}")

    r["risks"][1]["impact"]["score"] = 4
    r["risks"][1]["impact"]["justification"] += " The auditor raised it to Major."
    r["risks"][0]["proposed_focus"] += " Also review the supplier master file."
    r["revision"]["changes"] = [
        {"risk_id": "R-02", "field": "impact.score", "decision_ref": "R-02", "override": True, "note": "Auditor raised impact."},
        {"risk_id": "R-02", "field": "impact.justification", "decision_ref": "R-02"},
    ]
    save(root, r)
    code, out = run(root)
    expect(code == 1 and "unrequested change: R-01 proposed_focus" in out, f"unrequested change must fail\n{out}")
    expect("Raise impact to 4" in (root / "outputs/auditor-comments.md").read_text(),
           "a failed build must leave the auditor's decisions in place")

    r["risks"][0]["proposed_focus"] = r["risks"][0]["proposed_focus"].replace(" Also review the supplier master file.", "")
    r["revision"]["changes"].append({"risk_id": "R-02", "field": "evidence", "decision_ref": "R-02"})
    save(root, r)
    code, out = run(root)
    expect(code == 1 and "logs a change to R-02 evidence that was not made" in out, f"phantom change must fail\n{out}")

    r["revision"]["changes"].pop()
    save(root, r)
    code, out = run(root)
    expect(code == 0, f"valid revision expected\n{out}")
    reg = (root / "outputs/risk-register.md").read_text()
    for needle in ("**Revision 1**", "## Revision 1: changes since revision 0", "| R-02 | impact.score | 3 | 4 |",
                   "**Auditor override**", "Approved without change: R-01."):
        expect(needle in reg, f"revision register lacks '{needle}'")
    com = (root / "outputs/auditor-comments.md").read_text()
    expect("<!-- register: rev 1" in com and "| Approve | Agreed. |" in com and "Raise impact to 4" in com,
           f"decisions must survive the rewrite\n{com}")
    state = json.loads((root / "outputs/risk-register.json").read_text())
    expect(state["revision"] == 1 and state["undecided"] == [], f"state {state['revision']} {state['undecided']}")

    code, out = run(root)
    expect(code == 0 and "BUILT revision 1" in out, f"idempotent rebuild of revision 1\n{out}")

    set_decisions(root, {"R-02": ("Reject", "Out of scope this year.")})
    r["revision"] = {"number": 2, "changes": [{"risk_id": "R-02", "field": "status", "decision_ref": "R-02"}]}
    r["risks"][1]["status"] = "rejected"
    save(root, r)
    code, out = run(root)
    reg = (root / "outputs/risk-register.md").read_text()
    expect(code == 0 and "Rejected by the auditor; out of audit scope" in reg and "| R-02 | status | proposed | rejected |" in reg,
           f"reject in revision 2\n{out}")
    shutil.rmtree(root)


@case("revision against a stale auditor file fails")
def _():
    root = fresh()
    r = good_only(root)
    run(root)
    set_decisions(root, {"R-01": ("Approve", ""), "R-02": ("Approve", "")})
    p = root / "outputs/auditor-comments.md"
    p.write_text(re.sub(r"build [0-9a-f]+", "build 000000000000", p.read_text()))
    r["revision"] = {"number": 1, "changes": []}
    save(root, r)
    code, out = run(root)
    expect(code == 1 and "different build" in out, out)
    shutil.rmtree(root)


if __name__ == "__main__":
    for name, ok, msg in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"\n      {msg}"))
    failed = sum(not ok for _, ok, _ in RESULTS)
    print(f"\n{len(RESULTS) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
