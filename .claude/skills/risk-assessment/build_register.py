#!/usr/bin/env python3
"""Build the risk register from the risk-assessor's judgments.

Usage: build_register.py [--root DIR]

Reads   <root>/outputs/risk-ratings.json   (the agent's judgments)
        <root>/outputs/analytics.json      (figures and metric citations)
        <root>/outputs/history.json        (scoring method, AUD-/RT-/DSC- items)
        <root>/outputs/rules.json          (CPR- rule IDs)
        <root>/outputs/auditor-comments.md (auditor decisions, if any)
        <root>/outputs/risk-register.json  (state of the previous build, if any)
Writes  <root>/outputs/risk-register.md
        <root>/outputs/auditor-comments.md
        <root>/outputs/risk-register.json

The builder resolves every citation tag and {{$.path}} placeholder, computes
score = likelihood x impact, the matrix label and band from history.json,
checks each rubric choice against the data, and drops any risk that fails.
After the auditor gate it checks a revision against the auditor's decisions.

Exit 0 clean; 2 built but risks dropped; 1 failed (nothing written).
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

# ---- Likelihood rubric cut-offs (see SKILL.md, Step 3) ----------------------
L3_MAX = 9    # 1..L3_MAX instances -> L3 Likely
L4_MIN = 10   # L4_MIN or more instances -> L4 Almost certain
RUBRIC_SCORE = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}

DECISIONS = {"approve": "Approve", "amend": "Amend", "reject": "Reject"}
STATUSES = {"proposed", "rejected"}
DIMENSIONS = {"financial", "personal", "assets", "reputation", "compliance"}
ADVERSE_RE = re.compile(r"limited|weak|no assurance|minimal|unsatisfactory", re.I)
DIFF_FIELDS = [
    "title", "risk", "rule_ids", "status",
    "likelihood.rubric", "likelihood.score", "likelihood.count_metric",
    "likelihood.justification", "likelihood.uplift",
    "impact.score", "impact.dimension", "impact.basis_metric", "impact.justification",
    "evidence", "proposed_focus",
]
FALLBACK_LABELS = {1: "Very low", 2: "Low", 3: "Medium", 4: "High", 5: "Very high"}

CITE_RE = re.compile(r"\[(rule|metric|history):([^\]]+)\]")
PH_RE = re.compile(r"\{\{\s*(\$[^}|]*?)\s*(?:\|\s*(\w+)\s*)?\}\}")
PATH_TOKEN_RE = re.compile(r"\.([^.\[\]]+)|\[(\d+)\]")
MONEY_KEY_RE = re.compile(r"gbp|total|annualised|awarded_value|award_annual_rate", re.I)
TYPED_FIGURE_RE = re.compile(
    r"£\s*\d[\d,]*(?:\.\d+)?(?:\s?(?:bn|billion|million|m|k)\b)?|\d[\d,]*(?:\.\d+)?\s*%|\b\d+\.\d+\b"
    r"|\b\d{2,}(?:,\d{3})*\b")
ACCUSATORY_RE = re.compile(
    r"\b(fraud\w*|corrupt\w*|wrongdoing|misconduct|illegal\w*|unlawful\w*|deliberate\w*|"
    r"theft|stole\w*|abuse\w*)\b", re.I)
DECISION_HEADER_RE = re.compile(r"<!--\s*register:\s*rev\s+(\d+)\s*·\s*build\s+([0-9a-f]+)\s*-->")


class Fail(Exception):
    """A whole-build failure: nothing is written."""


_MISSING = object()


# ---- Path resolution and formatting -----------------------------------------
def resolve(doc, path: str):
    """Resolve '$.a.b.25000[0].c' in doc; return _MISSING if any step fails."""
    path = path.strip()
    if not path.startswith("$"):
        return _MISSING
    rest, node, pos = path[1:], doc, 0
    while pos < len(rest):
        m = PATH_TOKEN_RE.match(rest, pos)
        if not m:
            return _MISSING
        key, idx = m.group(1), m.group(2)
        if key is not None:
            if isinstance(node, dict) and key in node:
                node = node[key]
            else:
                return _MISSING
        else:
            i = int(idx)
            if isinstance(node, list) and 0 <= i < len(node):
                node = node[i]
            else:
                return _MISSING
        pos = m.end()
    return node


def last_key(path: str) -> str:
    keys = [m.group(1) for m in PATH_TOKEN_RE.finditer(path.strip()[1:]) if m.group(1)]
    return keys[-1] if keys else ""


def fmt_value(value, path: str, fmt: str | None) -> str:
    if fmt == "raw" or isinstance(value, (str, bool)):
        return str(value)
    if not isinstance(value, (int, float)):
        raise ValueError("not a scalar figure")
    if fmt is None:
        fmt = "gbp" if MONEY_KEY_RE.search(last_key(path)) else ("int" if isinstance(value, int) else "num")
    if fmt == "gbp":
        return f"£{value:,.2f}"
    if fmt == "int":
        if isinstance(value, float) and not value.is_integer():
            raise ValueError("|int on a non-integer value")
        return f"{int(value):,}"
    if fmt == "num":
        return f"{value:,}"
    raise ValueError(f"unknown format '|{fmt}'")


def is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def get(d: dict, dotted: str):
    node = d
    for k in dotted.split("."):
        node = node.get(k) if isinstance(node, dict) else None
    return node


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


# ---- Inputs ------------------------------------------------------------------
def load_json(path: Path, what: str):
    if not path.exists():
        raise Fail(f"{what} missing: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise Fail(f"{what} is not valid JSON ({path}): {e}")


def index_history(history: dict) -> dict:
    """Map every item id in history.json to (top-level collection, item)."""
    out = {}

    def walk(node, top):
        if isinstance(node, dict):
            if isinstance(node.get("id"), str):
                out[node["id"]] = (top, node)
            for v in node.values():
                walk(v, top)
        elif isinstance(node, list):
            for v in node:
                walk(v, top)

    for key, val in history.items():
        walk(val, key)
    return out


class Method:
    """The council's scoring method from history.json, or the fallback."""

    def __init__(self, history: dict):
        sm = history.get("scoring_method") or {}
        self.usable = bool(sm.get("usable"))
        self.source = sm.get("source_document")
        self.reason = sm.get("reason")
        self.notes: list[str] = []          # resolutions applied, for the header
        self.likelihood, self.impact = {}, {}
        self.cells, self.bands = {}, []
        self.crr_used, self.crr_other = None, []
        if not self.usable:
            self.likelihood = {s: {"label": l} for s, l in FALLBACK_LABELS.items()}
            self.impact = {s: {"label": l} for s, l in FALLBACK_LABELS.items()}
            return
        for e in sm.get("likelihood_scale", []):
            self.likelihood[e["score"]] = e
        for e in sm.get("impact_scale", []):
            self.impact[e["score"]] = e
        if sorted(self.likelihood) != [1, 2, 3, 4, 5] or sorted(self.impact) != [1, 2, 3, 4, 5]:
            raise Fail("history.json scoring_method: likelihood_scale and impact_scale must each define scores 1-5")
        for c in (sm.get("combination") or {}).get("cells", []):
            self.cells[(c["likelihood"], c["impact"])] = c
        if len(self.cells) != 25:
            raise Fail(f"history.json scoring_method.combination.cells has {len(self.cells)} cells, expected 25")
        for (l, i), c in self.cells.items():
            if c.get("score_printed") != l * i:
                raise Fail(f"matrix cell L{l} x I{i} prints {c.get('score_printed')}, not {l * i}; "
                           "the method is not a plain product, so the builder cannot score")
        self.bands = sm.get("bands", [])
        for (l, i), c in sorted(self.cells.items()):
            if self.band(l * i) is None:
                raise Fail(f"score {l * i} (L{l} x I{i}) falls in no band of scoring_method.bands")

        # Conflict: band names in Figure 1 vs Table 4.
        pairs = sorted({(c["label"], self.band(l * i)["level"]) for (l, i), c in self.cells.items()
                        if c["label"] != self.band(l * i)["level"]})
        if pairs:
            self.notes.append(
                "Band names differ between the matrix (Figure 1) and the band table (Table 4): "
                + "; ".join(f"Figure 1 '{a}' = Table 4 '{b}'" for a, b in pairs)
                + ". The register shows both: *Matrix* is the Figure 1 label, *Band* the Table 4 level.")
        for b in self.bands:
            if not b.get("rag"):
                self.notes.append(f"Table 4 prints no RAG colour name for '{b['level']}'; shown as 'not printed'.")

        # Conflict: Corporate Risk Register threshold.
        crr = sm.get("corporate_register_threshold") or {}
        found = {k: v for k, v in crr.items() if isinstance(v, dict) and is_int(v.get("score_at_or_above"))}
        if found:
            key = "table_4" if "table_4" in found else max(found, key=lambda k: found[k]["score_at_or_above"])
            self.crr_used = (key, found[key])
            self.crr_other = [(k, v) for k, v in found.items() if k != key
                              and v["score_at_or_above"] != found[key]["score_at_or_above"]]
            if self.crr_other:
                self.notes.append(
                    f"Corporate Risk Register threshold conflicts: used **{found[key]['section']}** "
                    f"(score {found[key]['score_at_or_above']} or above), because that table defines the bands "
                    "and their escalation. Not used: "
                    + "; ".join(f"{v['section']} (score {v['score_at_or_above']} or above)" for _, v in self.crr_other)
                    + ". Risks that qualify only under the unused reading are marked †.")

        # Conflict: £ endpoints shared between adjacent impact bands.
        shared = [(lo, hi) for lo, hi in zip(self._fin_bands(), self._fin_bands()[1:])
                  if lo["gbp_high"] is not None and lo["gbp_high"] == hi["gbp_low"]]
        if shared:
            self.notes.append(
                "Impact £ bands share endpoints ("
                + ", ".join(f"£{lo['gbp_high']:,}" for lo, _ in shared)
                + "). Convention used: a value equal to a shared endpoint goes to the higher band, unless "
                "the higher band is printed as strictly greater ('>'), when it stays in the lower band.")

    def _fin_bands(self):
        return [self.impact[s] for s in sorted(self.impact) if "gbp_low" in self.impact[s]]

    def band(self, score: int):
        for b in self.bands:
            lo = b.get("score_low") if b.get("score_low") is not None else 0
            hi = b.get("score_high") if b.get("score_high") is not None else 10 ** 9
            if lo <= score <= hi:
                return b
        return None

    def financial_score(self, value: float):
        best = None
        for s in sorted(self.impact):
            e = self.impact[s]
            lo = e.get("gbp_low")
            strict = str(e.get("financial", "")).lstrip().startswith(">")
            if lo is None or value > lo or (value == lo and not strict):
                best = s
        return best


# ---- Per-risk validation -----------------------------------------------------
class Ctx:
    def __init__(self, analytics, history, rules, method):
        self.analytics, self.history, self.method = analytics, history, method
        self.hist = index_history(history)
        self.rules = {r["rule_id"]: r for r in rules.get("rules", [])}
        self.agreed_action_ids = {a.get("id") for a in history.get("agreed_actions", []) if isinstance(a, dict)}


def prose_fields(risk: dict):
    lk, im = risk.get("likelihood") or {}, risk.get("impact") or {}
    yield "risk", risk.get("risk")
    yield "likelihood.justification", lk.get("justification")
    if isinstance(lk.get("uplift"), dict):
        yield "likelihood.uplift.justification", lk["uplift"].get("justification")
    yield "impact.justification", im.get("justification")
    for n, e in enumerate(risk.get("evidence") or []):
        yield f"evidence[{n}]", e
    yield "proposed_focus", risk.get("proposed_focus")


def check_text(text: str, ctx: Ctx, errors: list, where: str):
    """Return (n_resolved_citations, metric_paths, placeholder_paths)."""
    n_ok, metrics, phs = 0, [], []
    for kind, ref in CITE_RE.findall(text):
        ref = ref.strip()
        if kind == "rule":
            ok = ref in ctx.rules
        elif kind == "history":
            ok = ref in ctx.hist
        else:
            ok = resolve(ctx.analytics, ref) not in (_MISSING, None)
            metrics.append(ref)
        if ok:
            n_ok += 1
        else:
            errors.append(f"{where}: citation [{kind}:{ref}] does not resolve")
    for path, fmt in PH_RE.findall(text):
        phs.append(path)
        v = resolve(ctx.analytics, path)
        if v is _MISSING or v is None:
            errors.append(f"{where}: placeholder {{{{{path}}}}} does not resolve in analytics.json")
            continue
        try:
            fmt_value(v, path, fmt or None)
        except ValueError as e:
            errors.append(f"{where}: placeholder {{{{{path}}}}}: {e}")
    if "{{" in PH_RE.sub("", text) or "}}" in PH_RE.sub("", text):
        errors.append(f"{where}: malformed placeholder (expected {{{{$.path}}}} or {{{{$.path|fmt}}}})")
    return n_ok, metrics, phs


def strip_markup(text: str) -> str:
    return PH_RE.sub(" ", CITE_RE.sub(" ", text))


def validate_risk(risk: dict, ctx: Ctx, overrides: dict):
    """Return (errors, warnings, computed). overrides: {field: True} accepted off-rubric."""
    errors, warnings = [], []
    rid = risk.get("risk_id", "?")
    m = ctx.method
    if not isinstance(rid, str) or not re.fullmatch(r"R-\d{2,}", rid):
        errors.append(f"risk_id '{rid}' must look like R-01")
    for f in ("title", "risk", "proposed_focus"):
        if not isinstance(risk.get(f), str) or not risk[f].strip():
            errors.append(f"'{f}' missing or empty")
    if risk.get("status", "proposed") not in STATUSES:
        errors.append(f"status '{risk.get('status')}' not in {sorted(STATUSES)}")
    for r in risk.get("rule_ids") or []:
        if r not in ctx.rules:
            errors.append(f"rule_ids: {r} is not in rules.json")
    if not isinstance(risk.get("evidence", []), list):
        errors.append("evidence must be a list of strings")
    lk, im = risk.get("likelihood"), risk.get("impact")
    if not isinstance(lk, dict) or not isinstance(im, dict):
        errors.append("likelihood and impact must both be objects")
        return errors, warnings, None

    cites, all_refs = {}, []
    for where, text in prose_fields(risk):
        if text is None and where in ("risk", "proposed_focus"):
            continue
        if not isinstance(text, str):
            errors.append(f"{where}: must be a string")
            continue
        n_ok, metrics, phs = check_text(text, ctx, errors, where)
        cites[where] = (n_ok, metrics, phs)
        all_refs += CITE_RE.findall(text)
        for hit in TYPED_FIGURE_RE.findall(strip_markup(text)):
            warnings.append(f"{where}: typed figure '{hit.strip()}' in prose; use a {{{{$.path}}}} placeholder or a citation tag")
        for hit in ACCUSATORY_RE.findall(strip_markup(text)):
            warnings.append(f"{where}: word '{hit}' may read as an accusation; describe the indicator instead")

    for where in ("likelihood.justification", "impact.justification"):
        if where in cites and cites[where][0] == 0:
            errors.append(f"{where}: no resolvable citation ([rule:…], [metric:…] or [history:…])")

    # Likelihood rubric.
    rubric, base = lk.get("rubric"), lk.get("score")
    cm = lk.get("count_metric")
    note_l = None
    if rubric not in RUBRIC_SCORE:
        errors.append(f"likelihood.rubric '{rubric}' not in {sorted(RUBRIC_SCORE)}")
    elif not is_int(base) or not 1 <= base <= 5:
        errors.append("likelihood.score must be an integer 1-5")
    else:
        expected, problem = RUBRIC_SCORE[rubric], None
        if base != expected and not overrides.get("likelihood"):
            problem = f"likelihood.score {base} does not match rubric {rubric} (score {expected})"
        cv = resolve(ctx.analytics, cm) if isinstance(cm, str) else None
        just = cites.get("likelihood.justification", (0, [], []))
        if rubric in ("L2", "L5"):
            if cm is not None:
                problem = problem or f"rubric {rubric} takes no count_metric (set it to null)"
        elif not isinstance(cm, str):
            problem = problem or f"rubric {rubric} needs a count_metric"
        elif cv is _MISSING or not is_int(cv):
            errors.append(f"likelihood.count_metric {cm} does not resolve to an integer count")
        else:
            ok = {"L1": cv == 0, "L3": 1 <= cv <= L3_MAX, "L4": cv >= L4_MIN}[rubric]
            if not ok:
                actual = "L1" if cv == 0 else ("L3" if cv <= L3_MAX else "L4")
                problem = problem or f"count_metric is {cv}, which meets rubric {actual}, not {rubric}"
            if cm not in just[1] and cm not in just[2]:
                errors.append("likelihood.justification must show the count_metric as {{…}} or [metric:…]")
        if rubric == "L5":
            aa = [ref for kind, ref in CITE_RE.findall(lk.get("justification") or "")
                  if kind == "history" and ref.strip() in ctx.agreed_action_ids]
            if not aa:
                problem = problem or "rubric L5 needs the justification to cite an agreed action [history:…] from history.json agreed_actions"
        if problem:
            if overrides.get("likelihood"):
                note_l = problem
            else:
                errors.append(problem)

    # Repeat-finding uplift.
    up, uplift_item = lk.get("uplift"), None
    if up is not None:
        hid = up.get("history_id") if isinstance(up, dict) else None
        coll, item = ctx.hist.get(hid, (None, None))
        if coll != "audits":
            errors.append(f"likelihood.uplift.history_id '{hid}' is not an audit in history.json")
        elif not (ADVERSE_RE.search(str(item.get("opinion") or ""))
                  or ADVERSE_RE.search(str(item.get("implementation_opinion") or ""))):
            errors.append(f"likelihood.uplift cites {hid} ({item.get('opinion')}); a repeat-finding uplift needs an adverse opinion")
        else:
            uplift_item = item
        if not isinstance(up, dict) or not str(up.get("justification") or "").strip():
            errors.append("likelihood.uplift needs a justification")
    cited_adverse = sorted({ref.strip() for kind, ref in all_refs if kind == "history"
                            and ctx.hist.get(ref.strip(), (None,))[0] == "audits"
                            and (ADVERSE_RE.search(str(ctx.hist[ref.strip()][1].get("opinion") or ""))
                                 or ADVERSE_RE.search(str(ctx.hist[ref.strip()][1].get("implementation_opinion") or "")))})
    if cited_adverse and up is None:
        warnings.append(f"cites adverse audit(s) {', '.join(cited_adverse)} without a repeat-finding uplift; "
                        "say in the justification why the theme differs")

    # Impact.
    iscore, dim, basis = im.get("score"), im.get("dimension"), im.get("basis_metric")
    note_i = None
    if not is_int(iscore) or not 1 <= iscore <= 5:
        errors.append("impact.score must be an integer 1-5")
    if dim not in DIMENSIONS:
        errors.append(f"impact.dimension '{dim}' not in {sorted(DIMENSIONS)}")
    elif dim == "financial":
        bv = resolve(ctx.analytics, basis) if isinstance(basis, str) else _MISSING
        just = cites.get("impact.justification", (0, [], []))
        if not isinstance(basis, str):
            errors.append("impact.dimension 'financial' needs basis_metric (a £ figure path)")
        elif not isinstance(bv, (int, float)) or isinstance(bv, bool):
            errors.append(f"impact.basis_metric {basis} does not resolve to a number")
        else:
            if basis not in just[1] and basis not in just[2]:
                errors.append("impact.justification must show the basis_metric as {{…}} or [metric:…]")
            if m.usable and is_int(iscore):
                exp = m.financial_score(bv)
                if exp != iscore:
                    msg = f"impact.score {iscore} but basis_metric {fmt_value(bv, basis, 'gbp')} falls in Table 1 band {exp}"
                    if overrides.get("impact"):
                        note_i = msg
                    else:
                        errors.append(msg)
    elif basis is not None:
        errors.append(f"impact.basis_metric must be null for dimension '{dim}'")

    if errors or not is_int(base) or not is_int(iscore):
        return errors, warnings, None
    final_l = min(5, base + 1) if uplift_item else base
    score = final_l * iscore
    comp = {"likelihood_base": base, "likelihood": final_l, "impact": iscore, "score": score,
            "uplift": ({"history_id": up["history_id"], "opinion": uplift_item.get("opinion"),
                        "implementation_opinion": uplift_item.get("implementation_opinion"),
                        "capped": base == 5} if uplift_item else None),
            "override_notes": {k: v for k, v in (("likelihood", note_l), ("impact", note_i)) if v}}
    if m.usable:
        cell, band = m.cells[(final_l, iscore)], m.band(score)
        comp.update(matrix_label=cell["label"], band=band["level"], rag=band.get("rag"))
        if m.crr_used:
            comp["crr"] = score >= m.crr_used[1]["score_at_or_above"]
            comp["crr_other_only"] = [v["section"] for _, v in m.crr_other
                                      if score >= v["score_at_or_above"] and not comp["crr"]]
    else:
        comp.update(matrix_label=None, band=None, rag=None, crr=None, crr_other_only=[])
    return errors, warnings, comp


# ---- Auditor comments --------------------------------------------------------
def split_row(line: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip().replace("\\|", "|") for c in cells]


def read_comments(path: Path):
    """Return (header (rev, build) or None, {risk_id: {'decision','comment','title'}}, errors)."""
    if not path.exists():
        return None, {}, []
    text = path.read_text(encoding="utf-8")
    hm = DECISION_HEADER_RE.search(text)
    header = (int(hm.group(1)), hm.group(2)) if hm else None
    out, errors = {}, []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 6 or not re.fullmatch(r"R-\d{2,}", cells[0]):
            continue
        dec_raw, comment = cells[4], cells[5]
        dec = DECISIONS.get(dec_raw.lower()) if dec_raw else None
        if dec_raw and not dec:
            errors.append(f"auditor-comments.md {cells[0]}: decision '{dec_raw}' is not Approve, Amend or Reject")
        if dec == "Amend" and not comment:
            errors.append(f"auditor-comments.md {cells[0]}: Amend needs a comment saying what to change")
        out[cells[0]] = {"decision": dec, "comment": comment, "title": cells[1]}
    return header, out, errors


def esc(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def write_comments(path: Path, revision: int, build: str, risks: list, computed: dict, prior: dict):
    lines = [
        "# Auditor decisions on the risk register",
        "",
        f"<!-- register: rev {revision} · build {build} -->",
        "",
        f"Register: `outputs/risk-register.md`, revision {revision} (build `{build}`).",
        "",
        "For each risk write one **Decision**: `Approve` (in scope as rated), `Amend` (say what to "
        "change in **Comment**) or `Reject` (take it out of audit scope; say why). Do not use the `|` "
        "character in a comment. Leave the other columns as they are; they are rewritten on each build "
        "and your decisions are kept.",
        "",
        "| Risk | Title | L × I = Score | Band | Decision | Comment |",
        "|---|---|---|---|---|---|",
    ]
    seen = set()
    for r in risks:
        rid = r["risk_id"]
        c = computed.get(rid)
        if not c:
            continue          # dropped by the builder: the agent fixes it; the auditor does not decide it
        seen.add(rid)
        sc = f"{c['likelihood']} × {c['impact']} = {c['score']}"
        band = c.get("band") or ""
        if r.get("status") == "rejected":
            band = f"{band} (rejected)"
        p = prior.get(rid, {})
        lines.append(f"| {rid} | {esc(r.get('title', ''))} | {sc} | {esc(band)} | "
                     f"{esc(p.get('decision') or '')} | {esc(p.get('comment') or '')} |")
    orphans = {k: v for k, v in prior.items() if k not in seen and (v.get("decision") or v.get("comment"))}
    if orphans:
        lines += ["", "## Decisions on risks no longer in the register", "",
                  "Kept so nothing you wrote is lost.", "",
                  "| Risk | Title | L × I = Score | Band | Decision | Comment |", "|---|---|---|---|---|---|"]
        for rid, v in sorted(orphans.items()):
            lines.append(f"| {rid} | {esc(v.get('title', ''))} | | | {esc(v.get('decision') or '')} | {esc(v.get('comment') or '')} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---- Revision checks ---------------------------------------------------------
def field_value(risk: dict, field: str):
    if risk is None:
        return _MISSING
    if field == "status":
        return risk.get("status", "proposed")
    return get(risk, field) if "." in field else risk.get(field)


def diff_risks(old: list, new: list):
    old_by, new_by = {r["risk_id"]: r for r in old}, {r["risk_id"]: r for r in new}
    diffs = []
    for rid in sorted(set(old_by) | set(new_by)):
        if rid not in old_by:
            diffs.append((rid, "added", None, None))
        elif rid not in new_by:
            diffs.append((rid, "removed", None, None))
        else:
            for f in DIFF_FIELDS:
                a, b = field_value(old_by[rid], f), field_value(new_by[rid], f)
                if canonical(a) != canonical(b):
                    diffs.append((rid, f, a, b))
            extra = (set(old_by[rid]) | set(new_by[rid])) - {f.split(".")[0] for f in DIFF_FIELDS} - {"risk_id"}
            for k in sorted(extra):
                if canonical(old_by[rid].get(k)) != canonical(new_by[rid].get(k)):
                    diffs.append((rid, k, old_by[rid].get(k), new_by[rid].get(k)))
    return diffs


def check_revision(rev: dict, state: dict, risks: list, decisions: dict, header):
    """Validate a revision against the previous build. Return (change rows, new override fields)."""
    errs = []
    if header is None or header[1] != state["build"]:
        raise Fail("auditor-comments.md was written for a different build "
                   f"({'none' if header is None else 'rev %d build %s' % header}) than the last register "
                   f"(rev {state['revision']} build {state['build']}); the auditor must decide on the current register")
    applied = state.get("decisions_applied", {})
    new_dec = {rid: d for rid, d in decisions.items()
               if d.get("decision") and {"decision": d["decision"], "comment": d["comment"]} != applied.get(rid)}
    diffs = diff_risks(state["ratings_risks"], risks)
    diff_keys = {(rid, f) for rid, f, _, _ in diffs}
    changes = rev.get("changes")
    if not isinstance(changes, list):
        raise Fail("revision.changes must be a list (use [] when every decision is Approve)")
    logged, new_overrides = set(), {}
    for n, ch in enumerate(changes):
        rid, f = ch.get("risk_id"), ch.get("field")
        ref = ch.get("decision_ref") or rid
        if f not in DIFF_FIELDS + ["added", "removed"]:
            errs.append(f"revision.changes[{n}]: field '{f}' is not a known field")
            continue
        d = new_dec.get(ref)
        if not d:
            errs.append(f"revision.changes[{n}] ({rid} {f}): decision_ref {ref} has no new auditor decision")
        elif d["decision"] == "Approve":
            errs.append(f"revision.changes[{n}] ({rid} {f}): {ref} was Approved; nothing on it may change")
        elif d["decision"] == "Reject" and (f != "status" or rid != ref):
            errs.append(f"revision.changes[{n}] ({rid} {f}): a Reject on {ref} only authorises its status")
        if (rid, f) not in diff_keys:
            errs.append(f"revision.changes[{n}]: logs a change to {rid} {f} that was not made")
        logged.add((rid, f))
        if ch.get("override"):
            if f.startswith("likelihood."):
                new_overrides.setdefault(rid, {})["likelihood"] = True
            elif f.startswith("impact."):
                new_overrides.setdefault(rid, {})["impact"] = True
    for rid, f, a, b in diffs:
        if (rid, f) not in logged:
            errs.append(f"unrequested change: {rid} {f} differs from revision {state['revision']} "
                        "and is not logged in revision.changes against an Amend/Reject decision")
    cur = {r["risk_id"]: r for r in risks}
    for rid, d in sorted(new_dec.items()):
        if d["decision"] == "Amend" and not any((c.get("decision_ref") or c.get("risk_id")) == rid for c in changes):
            errs.append(f"decision not applied: {rid} Amend ('{d['comment']}') has no logged change")
        if d["decision"] == "Reject" and (rid not in cur or cur[rid].get("status") != "rejected"):
            errs.append(f"decision not applied: {rid} Reject but its status is not 'rejected'")
        if rid not in cur and not any(c.get("field") == "removed" and c.get("risk_id") == rid for c in changes):
            errs.append(f"auditor decision on {rid}, which is not in the ratings")
    if errs:
        raise Fail("revision check failed:\n  " + "\n  ".join(errs))
    rows = []
    for rid, f, a, b in diffs:
        ch = next(c for c in changes if (c.get("risk_id"), c.get("field")) == (rid, f))
        ref = ch.get("decision_ref") or rid
        rows.append({"risk_id": rid, "field": f, "from": a, "to": b, "decision_ref": ref,
                     "decision": new_dec[ref]["decision"], "comment": new_dec[ref]["comment"],
                     "override": bool(ch.get("override")) or new_dec[ref]["decision"] == "Reject",
                     "note": ch.get("note")})
    approved_unchanged = sorted(rid for rid, d in new_dec.items() if d["decision"] == "Approve")
    return rows, new_overrides, approved_unchanged, new_dec


# ---- Rendering ---------------------------------------------------------------
class Renderer:
    def __init__(self, ctx: Ctx):
        self.ctx = ctx

    def text(self, s: str, metrics: list, figures: list, rid: str) -> str:
        def ph(m):
            path, fmt = m.group(1), m.group(2)
            v = resolve(self.ctx.analytics, path)
            out = fmt_value(v, path, fmt)
            figures.append({"risk_id": rid, "path": path, "value": v, "shown": out})
            return out

        def cite(m):
            kind, ref = m.group(1), m.group(2).strip()
            if kind == "metric":
                if ref not in metrics:
                    metrics.append(ref)
                return f"[M{metrics.index(ref) + 1}]"
            return ref
        return CITE_RE.sub(cite, PH_RE.sub(ph, s))

    def history_line(self, hid: str) -> str:
        coll, it = self.ctx.hist[hid]
        if coll == "audits":
            op = it.get("opinion") or "no opinion"
            if it.get("implementation_opinion"):
                op += f"; implementation {it['implementation_opinion']}"
            return f"{hid}: {it.get('audit_title')} ({it.get('kind', '').replace('_', ' ')}), {op}, period to {it.get('period_end')} [{it.get('source')} p.{it.get('pdf_page')}]"
        label = it.get("theme") or it.get("issue") or it.get("title") or it.get("item") or ""
        return f"{hid}: {label} [{it.get('source')} p.{it.get('pdf_page')}]"


def short(v) -> str:
    if v is _MISSING or v is None:
        return "–"
    if isinstance(v, (str, int, float)) and len(str(v)) <= 40:
        return str(v)
    return "text revised" if isinstance(v, str) else "revised"


def render_register(out: Path, ctx: Ctx, ratings: dict, risks: list, computed: dict, dropped: list,
                    warnings_by: dict, revision: int, build: str, rev_rows: list, approved_unchanged: list,
                    decisions: dict, rev_summary, prev_state, overrides: dict, figures: list):
    m, R = ctx.method, Renderer(ctx)
    a_gen = ctx.analytics.get("generated_at")
    h_gen = ctx.history.get("generated_at")
    L = []
    title = "Procurement risk register (West Berkshire Council)"
    L += [f"# {title}", ""]
    status = "Draft for auditor review" if revision == 0 else f"Revision {revision}"
    L += [f"**{status}** · build `{build}` · built {dt.datetime.now().isoformat(timespec='seconds')}",
          f"Inputs: analytics.json ({a_gen}), history.json ({h_gen}), rules.json, risk-ratings.json.", ""]

    if revision > 0:
        L += [f"## Revision {revision}: changes since revision {revision - 1}", ""]
        if rev_summary:
            L += [str(rev_summary), ""]
        if prev_state and prev_state.get("inputs", {}).get("analytics_generated_at") != a_gen:
            L += [f"Note: analytics.json was regenerated since revision {revision - 1} "
                  f"({prev_state.get('inputs', {}).get('analytics_generated_at')} → {a_gen}); figures may differ "
                  "even where the ratings did not change.", ""]
        if rev_rows:
            L += ["| Risk | Field | From | To | Auditor decision | Auditor comment | Override |",
                  "|---|---|---|---|---|---|---|"]
            for r in rev_rows:
                L.append(f"| {r['risk_id']} | {r['field']} | {esc(short(r['from']))} | {esc(short(r['to']))} | "
                         f"{r['decision']} ({r['decision_ref']}) | {esc(r['comment'])} | "
                         f"{'**Auditor override**' if r['override'] else ''} |")
            L.append("")
        if approved_unchanged:
            L += [f"Approved without change: {', '.join(approved_unchanged)}.", ""]
        if not rev_rows and not approved_unchanged:
            L += ["No changes.", ""]

    L += ["## Method", ""]
    if m.usable:
        lv = next((e for e in ctx.history.get("scoring_method", {}).get("evaluation_levels", [])
                   if e.get("level") == ratings.get("assessment_level")), None)
        L += [f"Scored on the council's own method: likelihood 1–5 × impact 1–5 from the {m.source} "
              "(Table 2 likelihood, Table 1 impact, Figure 1 matrix, Table 4 bands). "
              "Score = likelihood × impact, which every printed cell of Figure 1 equals.",
              f"Assessment level: **{ratings.get('assessment_level')}**"
              + (f" ({lv['definition']})." if lv else "."), ""]
    else:
        L += ["**Fallback scale.** history.json reports no usable council scoring method"
              + (f" ({m.reason})" if m.reason else "")
              + ", so likelihood and impact use 1–5 Very low … Very high and the score is their product. "
              "No council bands apply.", ""]
    L += ["Likelihood rubric (applied by the risk-assessor, checked by the builder against the cited count):",
          "",
          "| Row | Score | Evidence |", "|---|---|---|",
          "| L1 | 1 | full-population test found 0 instances in general procurement |",
          "| L2 | 2 | no public-data test can measure the risk (rated Unlikely, never Rare) |",
          f"| L3 | 3 | test found 1–{L3_MAX} instances |",
          f"| L4 | 4 | test found {L4_MIN} or more instances |",
          "| L5 | 5 | an open agreed action states the control is not operating |", "",
          "A repeat finding (a past audit on the same theme with an adverse opinion) raises likelihood by one point, "
          "capped at 5, and is stated on the risk.", "",
          "These are **risk indicators to investigate**, not findings of non-compliance or wrongdoing by the council, "
          "any service or any supplier.", ""]
    if m.usable:
        L += ["### Scoring-method conflicts", ""]
        if m.notes:
            L += ["How the builder resolved conflicts in the method (one reading used, the other marked):", ""]
            L += [f"- {n}" for n in m.notes] + [""]
        dsc = [d for d in ctx.history.get("discrepancies", []) if d.get("source") == m.source]
        if dsc:
            L += ["Discrepancies recorded in history.json for this document. Scores and labels are read only from "
                  "Table 1, Table 2, Figure 1 and Table 4, so any discrepancy not resolved above does not change a score:", ""]
            L += [f"- {d['id']} ({d.get('section')}): {d.get('issue')}" for d in dsc] + [""]

    in_scope = [r for r in risks if r["risk_id"] in computed]
    order = sorted(in_scope, key=lambda r: (-computed[r["risk_id"]]["score"], r["risk_id"]))
    L += ["## Summary", "",
          "| Risk | Title | L | I | Score | Matrix (Fig. 1) | Band (Table 4) | Corporate register | Status |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in order:
        c = computed[r["risk_id"]]
        crr = "yes" if c.get("crr") else ("† " + "; ".join(c["crr_other_only"]) if c.get("crr_other_only") else "no")
        if c.get("crr") is None:
            crr = "n/a"
        st = "Rejected by auditor (out of scope)" if r.get("status") == "rejected" else (
            "Approved" if decisions.get(r["risk_id"], {}).get("decision") in ("Approve", "Amend") and revision > 0
            else "Proposed")
        L.append(f"| {r['risk_id']} | {esc(r['title'])} | {c['likelihood']} | {c['impact']} | **{c['score']}** | "
                 f"{c.get('matrix_label') or 'n/a'} | {c.get('band') or 'n/a'} ({c.get('rag') or 'not printed'}) | {crr} | {st} |")
    if m.crr_other and any(computed[r["risk_id"]].get("crr_other_only") for r in in_scope):
        L += ["", "† Qualifies for the Corporate Risk Register only under the reading not used (see Scoring-method conflicts)."]
    L.append("")

    for r in order:
        rid, c = r["risk_id"], computed[r["risk_id"]]
        metrics, rules_cited, hist_cited = [], [], []
        for _, t in prose_fields(r):
            for kind, ref in CITE_RE.findall(t or ""):
                ref = ref.strip()
                if kind == "rule" and ref not in rules_cited:
                    rules_cited.append(ref)
                if kind == "history" and ref not in hist_cited:
                    hist_cited.append(ref)
        for x in r.get("rule_ids") or []:
            if x not in rules_cited:
                rules_cited.append(x)
        if c.get("uplift") and c["uplift"]["history_id"] not in hist_cited:
            hist_cited.append(c["uplift"]["history_id"])
        T = lambda s: R.text(s, metrics, figures, rid)
        lk, im = r["likelihood"], r["impact"]
        lab_l = m.likelihood[c["likelihood"]].get("label")
        lab_i = m.impact[c["impact"]].get("label")
        L += [f"## {rid}: {r['title']}", ""]
        if r.get("status") == "rejected":
            L += [f"> **Rejected by the auditor; out of audit scope.** Comment: {decisions.get(rid, {}).get('comment') or '–'}", ""]
        L += [f"**Risk.** {T(r['risk'])}", ""]
        lline = f"**Likelihood: {c['likelihood']} ({lab_l}).** Rubric {lk['rubric']}. {T(lk['justification'])}"
        if c.get("uplift"):
            u = c["uplift"]
            lline += (f" **Repeat finding: likelihood raised by one point** from {c['likelihood_base']} "
                      f"to {c['likelihood']}{' (already at the cap of 5)' if u['capped'] else ''}, because "
                      f"{u['history_id']} had an adverse opinion ({u['opinion']}"
                      f"{'; implementation ' + u['implementation_opinion'] if u.get('implementation_opinion') else ''}). "
                      f"{T(lk['uplift']['justification'])}")
        if c["override_notes"].get("likelihood"):
            lline += f" **Auditor override:** {c['override_notes']['likelihood']}."
        L += [lline, ""]
        iline = f"**Impact: {c['impact']} ({lab_i}), {im['dimension']}.** {T(im['justification'])}"
        if m.usable and im["dimension"] != "financial":
            desc = m.impact[c["impact"]].get(im["dimension"])
            if desc:
                iline += f" *Table 1 {im['dimension']} descriptor for {c['impact']}: \"{desc}\".*"
        if c["override_notes"].get("impact"):
            iline += f" **Auditor override:** {c['override_notes']['impact']}."
        L += [iline, ""]
        score_line = f"**Score: {c['likelihood']} × {c['impact']} = {c['score']}**"
        if m.usable:
            score_line += f" · Matrix: {c['matrix_label']} · Band: {c['band']} ({c.get('rag') or 'not printed'})"
            band = m.band(c["score"])
            score_line += f" · Escalation: {band.get('escalation')} · Response: {band.get('response')}"
        L += [score_line, ""]
        if r.get("evidence"):
            L += ["**Evidence.**", ""] + [f"- {T(e)}" for e in r["evidence"]] + [""]
        L += [f"**Proposed focus.** {T(r['proposed_focus'])}", ""]
        L += ["**Sources.**", ""]
        for x in rules_cited:
            rr = ctx.rules[x]
            L.append(f"- {x}: clause {rr.get('clause')}, p.{rr.get('page')}: {rr.get('condition')}")
        for x in hist_cited:
            L.append(f"- {R.history_line(x)}")
        for n, p in enumerate(metrics, 1):
            v = resolve(ctx.analytics, p)
            shown = canonical(v) if isinstance(v, (dict, list)) else fmt_value(v, p, None)
            if len(shown) > 160:
                shown = shown[:157] + "…"
            L.append(f"- M{n}: `{p}` = {shown}")
        if warnings_by.get(rid):
            L += ["", f"*Builder warnings: {len(warnings_by[rid])} (see build output).*"]
        L.append("")

    if dropped:
        L += ["## Not included: failed the builder's checks", "",
              "These risks were written by the risk-assessor but are **not** part of the register because a "
              "justification lacked a resolvable citation or a check failed. They need fixing and a rebuild.", ""]
        for d in dropped:
            L.append(f"- **{d['risk_id']}** {esc(d.get('title') or '')}: " + "; ".join(d["errors"]))
        L.append("")

    L += ["## Auditor decisions", ""]
    rated = [r for r in risks if r["risk_id"] in computed]
    decided = [r["risk_id"] for r in rated if decisions.get(r["risk_id"], {}).get("decision")]
    L += [f"Record one decision per risk in `outputs/auditor-comments.md`: **Approve**, **Amend** (with a comment) "
          f"or **Reject** (out of scope). Decided: {len(decided)} of {len(rated)}.", ""]
    if dropped:
        L += ["Risks under *Not included* are not for decision until the risk-assessor fixes them.", ""]
    L += ["| Risk | Decision | Comment |", "|---|---|---|"]
    for r in rated:
        d = decisions.get(r["risk_id"], {})
        L.append(f"| {r['risk_id']} | {d.get('decision') or '*pending*'} | {esc(d.get('comment') or '')} |")
    L.append("")
    if revision == 0:
        L += ["Once every risk has a decision, the risk-assessor is re-run to produce revision 1, which applies them.", ""]
    out.write_text("\n".join(L), encoding="utf-8")


# ---- Main --------------------------------------------------------------------
def main(root: Path) -> int:
    o = root / "outputs"
    ratings = load_json(o / "risk-ratings.json", "risk-ratings.json")
    analytics = load_json(o / "analytics.json", "analytics.json")
    history = load_json(o / "history.json", "history.json")
    rules = load_json(o / "rules.json", "rules.json")
    state_path = o / "risk-register.json"
    prev = load_json(state_path, "risk-register.json") if state_path.exists() else None

    if not isinstance(ratings.get("risks"), list) or not ratings["risks"]:
        raise Fail("risk-ratings.json needs a non-empty 'risks' list")
    risks = ratings["risks"]
    ids = [r.get("risk_id") for r in risks]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise Fail(f"duplicate risk_id(s): {', '.join(map(str, dup))}")
    method = Method(history)
    levels = {e.get("level") for e in (history.get("scoring_method") or {}).get("evaluation_levels", [])}
    if method.usable and levels and ratings.get("assessment_level") not in levels:
        raise Fail(f"assessment_level '{ratings.get('assessment_level')}' not one of {sorted(levels)} (history.json evaluation_levels)")
    ctx = Ctx(analytics, history, rules, method)

    header, decisions, dec_errors = read_comments(o / "auditor-comments.md")
    if dec_errors:
        raise Fail("auditor-comments.md:\n  " + "\n  ".join(dec_errors))
    rev = ratings.get("revision")
    prev_rev = prev["revision"] if prev else 0
    applied = (prev or {}).get("decisions_applied", {})
    new_decisions = {k: v for k, v in decisions.items() if v.get("decision")
                     and {"decision": v["decision"], "comment": v["comment"]} != applied.get(k)}

    # Decide the mode.
    rev_rows, approved_unchanged, new_overrides, rev_number = [], [], {}, 0
    if rev is None:
        if new_decisions:
            raise Fail("auditor-comments.md holds decisions ("
                       + ", ".join(f"{k} {v['decision']}" for k, v in sorted(new_decisions.items()))
                       + ") but risk-ratings.json has no 'revision' block; apply them and add "
                       f"\"revision\": {{\"number\": {prev_rev + 1}, \"changes\": [...]}}")
        if prev and prev_rev > 0:
            raise Fail(f"the register is at revision {prev_rev}; risk-ratings.json must keep its revision block")
    else:
        if not isinstance(rev, dict) or not is_int(rev.get("number")):
            raise Fail("revision must be an object with an integer 'number'")
        rev_number = rev["number"]
        if prev is None:
            raise Fail("a revision needs the previous build's outputs/risk-register.json; none found")
        if rev_number == prev_rev and prev_rev > 0:
            if diff_risks(prev["ratings_risks"], risks) or new_decisions:
                raise Fail(f"changes or new auditor decisions since revision {prev_rev}: "
                           f"set revision.number to {prev_rev + 1}")
            rev_rows = prev.get("revision_rows", [])
            approved_unchanged = prev.get("approved_unchanged", [])
        elif rev_number == prev_rev + 1:
            rev_rows, new_overrides, approved_unchanged, _ = check_revision(rev, prev, risks, decisions, header)
        else:
            raise Fail(f"revision.number is {rev_number}; expected {prev_rev + 1} (previous build is revision {prev_rev})")

    # Overrides carried from earlier revisions stay while the field is unchanged.
    overrides = {}
    for rid, f in ((prev or {}).get("overrides") or {}).items():
        overrides[rid] = dict(f)
    for row in rev_rows if rev_number > prev_rev else []:
        part = row["field"].split(".")[0]
        if part in ("likelihood", "impact") and rid_in(overrides, row["risk_id"], part) and not row["override"]:
            overrides[row["risk_id"]].pop(part, None)
    for rid, f in new_overrides.items():
        overrides.setdefault(rid, {}).update(f)

    computed, dropped, warnings_by = {}, [], {}
    for r in risks:
        errs, warns, comp = validate_risk(r, ctx, overrides.get(r.get("risk_id"), {}))
        warnings_by[r.get("risk_id")] = warns
        if errs:
            dropped.append({"risk_id": r.get("risk_id"), "title": r.get("title"), "errors": errs})
        else:
            computed[r["risk_id"]] = comp
    if rev_number > 0 and dropped:
        raise Fail("a revision may not drop risks; fix them:\n  "
                   + "\n  ".join(f"{d['risk_id']}: {'; '.join(d['errors'])}" for d in dropped))

    build = hashlib.sha256(canonical(risks).encode()).hexdigest()[:12]
    figures = []
    render_register(o / "risk-register.md", ctx, ratings, risks, computed, dropped, warnings_by,
                    rev_number, build, rev_rows, approved_unchanged, decisions,
                    (rev or {}).get("summary"), prev, overrides, figures)
    write_comments(o / "auditor-comments.md", rev_number, build, risks, computed, decisions)
    applied_now = {k: {"decision": v["decision"], "comment": v["comment"]}
                   for k, v in decisions.items() if v.get("decision")} if rev_number > 0 else {}
    state = {
        "revision": rev_number,
        "build": build,
        "built_at": dt.datetime.now().isoformat(timespec="seconds"),
        "inputs": {"analytics_generated_at": analytics.get("generated_at"),
                   "history_generated_at": history.get("generated_at")},
        "scoring_method": "council" if method.usable else "fallback",
        "assessment_level": ratings.get("assessment_level"),
        "risks": [{"risk_id": r["risk_id"], "title": r["title"], "status": r.get("status", "proposed"),
                   "rule_ids": r.get("rule_ids", []), **computed[r["risk_id"]]}
                  for r in risks if r["risk_id"] in computed],
        "dropped": dropped,
        "figures": figures,
        "ratings_risks": copy.deepcopy(risks),
        "decisions_applied": applied_now,
        "overrides": {k: v for k, v in overrides.items() if v},
        "revision_rows": rev_rows,
        "approved_unchanged": approved_unchanged,
        "undecided": [r["risk_id"] for r in risks
                      if r["risk_id"] in computed and not decisions.get(r["risk_id"], {}).get("decision")],
    }
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")

    for rid, ws in warnings_by.items():
        for w in ws:
            print(f"WARN  {rid}: {w}")
    for d in dropped:
        print(f"DROPPED {d['risk_id']}: " + "; ".join(d["errors"]))
    for row in rev_rows:
        print(f"REVISION {row['risk_id']} {row['field']}: {row['decision']}"
              + (" (auditor override)" if row["override"] else ""))
    if rev_number > 0 and state["undecided"]:
        print(f"WARN  undecided: {', '.join(state['undecided'])}")
    n_w = sum(len(w) for w in warnings_by.values())
    label = "draft" if rev_number == 0 else f"revision {rev_number}"
    print(f"\nBUILT {label} (build {build}): {len(computed)} risks rated, {len(dropped)} dropped, {n_w} warning(s)")
    return 2 if dropped else 0


def rid_in(d: dict, rid: str, part: str) -> bool:
    return part in d.get(rid, {})


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3],
                    help="project root holding outputs/ (default: this repo)")
    args = ap.parse_args()
    try:
        sys.exit(main(args.root))
    except Fail as e:
        print(f"FAIL  {e}")
        sys.exit(1)
