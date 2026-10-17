#!/usr/bin/env python3
"""QA check: every quote exists in its source.

1. Runs the extract-rules verifier: every verbatim_quote in outputs/rules.json
   is found in data/contract-rules.pdf on its stated page.
2. Every rule source line printed in outputs/risk-register.md
   ("- CPR-xx: clause C, p.N: condition") matches that rule's clause, page
   and condition in rules.json. Zero lines found is a failure, so a format
   change cannot pass silently.
Prints PASS/FAIL lines and a summary; exit 0 when clean.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERIFIER = ROOT / ".claude/skills/extract-rules/verify_quotes.py"
RULES = ROOT / "outputs/rules.json"
PDF = ROOT / "data/contract-rules.pdf"
REGISTER = ROOT / "outputs/risk-register.md"


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()


def main():
    fails = []
    if not VERIFIER.exists():
        fails.append(f"verifier missing: {VERIFIER}")
    else:
        p = subprocess.run([sys.executable, str(VERIFIER), str(RULES), str(PDF)], capture_output=True, text=True)
        last = (p.stdout.strip().splitlines() or ["(no output)"])[-1]
        print(f"verify_quotes.py: exit {p.returncode}: {last}")
        if p.returncode != 0:
            fails.append("verify_quotes.py reported failures: " + last)
    rules = {r["rule_id"]: r for r in json.loads(RULES.read_text())["rules"]}
    # The register's Sources lists print each cited rule as "- CPR-xx: clause C, p.N: condition" (build_register.py).
    n_excerpts = 0
    if not REGISTER.exists():
        fails.append(f"register missing: {REGISTER}")
    else:
        for m in re.finditer(r"^- (CPR-\d+): clause (.+?), p\.(\d+): (.*?)\s*$", REGISTER.read_text(encoding="utf-8"), re.M):
            rid, clause, page, cond = m.groups()
            n_excerpts += 1
            r = rules.get(rid)
            if not r:
                fails.append(f"register cites unknown rule {rid}")
            elif (norm(str(r.get("clause"))), str(r.get("page")), norm(str(r.get("condition")))) != (norm(clause), page, norm(cond)):
                fails.append(f"register source line for {rid} does not match rules.json (clause, page or condition)")
        if n_excerpts == 0:
            fails.append("register has no rule source lines to check; the format may have changed")
    print(f"register rule source lines checked: {n_excerpts}")
    for f in fails:
        print("FAIL ", f)
    print(f"SUMMARY quotes: rules={len(rules)} register_excerpts={n_excerpts} failures={len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
