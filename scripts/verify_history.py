#!/usr/bin/env python3
"""Verify outputs/history.json against the committee PDFs.

Usage: verify_history.py HISTORY_JSON COMMITTEE_DIR

Checks: JSON shape; every item (anywhere in the tree) that has a `source`
also has an integer `pdf_page`; the source file exists; every `quote` is
found on the stated page after normalisation (whitespace collapsed, bullet
glyphs and page footers ignored, quote/dash glyphs unified).
Exit 0 with ALL CHECKS PASSED when clean.  Needs `pdftotext` on PATH.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

TOP = ("generated_at", "source_documents", "gaps", "audits", "opinion_basis", "agreed_actions",
       "planned_audits", "audit_approach", "risk_themes", "scoring_method", "discrepancies")
GLYPHS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                        "–": "-", "\u2014": "-", " ": " "})
BULLET_RE = re.compile(r"[-•▪●⁃…]")


def normalise(t: str) -> str:
    t = t.translate(GLYPHS)
    t = BULLET_RE.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()


def pages(pdf: Path) -> list[str]:
    if not shutil.which("pdftotext"):
        sys.exit("ERROR: pdftotext not on PATH")
    out = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    ps = out.split("\f")
    if ps and not ps[-1].strip():
        ps.pop()
    return [normalise(p) for p in ps]


def walk(node, path="$"):
    """Yield (path, dict) for every dict in the tree."""
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")


def scoring_shape(sm: dict) -> list[str]:
    """The layout build_register.py reads; a usable method in any other shape crashes it."""
    errs = []
    is_int = lambda v: isinstance(v, int) and not isinstance(v, bool)  # noqa: E731
    for key in ("likelihood_scale", "impact_scale"):
        scale = sm.get(key)
        if not isinstance(scale, list):
            errs.append(f"scoring_method.{key} must be a LIST of five {{score, label, ...}} entries "
                        f"(found {type(scale).__name__}); do not wrap it in an object")
            continue
        if sorted(e.get("score") for e in scale if isinstance(e, dict) and is_int(e.get("score"))) != [1, 2, 3, 4, 5] \
                or not all(isinstance(e, dict) and e.get("label") for e in scale):
            errs.append(f"scoring_method.{key} needs entries with integer score 1-5 and a label")
    for e in sm.get("impact_scale") or []:
        if isinstance(e, dict) and not ("gbp_low" in e and "gbp_high" in e):
            errs.append(f"scoring_method.impact_scale score {e.get('score')}: needs gbp_low and gbp_high keys (null if not printed)")
    cells = (sm.get("combination") or {}).get("cells") if isinstance(sm.get("combination"), dict) else None
    if not isinstance(cells, list) or len(cells) != 25 or not all(
            isinstance(c, dict) and is_int(c.get("likelihood")) and is_int(c.get("impact"))
            and is_int(c.get("score_printed")) and c.get("label") for c in cells):
        errs.append("scoring_method.combination.cells must be a list of 25 {likelihood, impact, score_printed, label} "
                    "entries, one per matrix cell")
    bands = sm.get("bands")
    if not isinstance(bands, list) or not bands or not all(
            isinstance(b, dict) and b.get("level") and "rag" in b
            and all(k in b and (b[k] is None or is_int(b[k])) for k in ("score_low", "score_high"))
            and (is_int(b["score_low"]) or is_int(b["score_high"]))
            for b in bands):
        errs.append("scoring_method.bands must be a list of {level, rag, score_low, score_high, ...} entries "
                    "(integer scores; null only for an open-ended end)")
    levels = sm.get("evaluation_levels")
    if not isinstance(levels, list) or not levels or not all(
            isinstance(e, dict) and e.get("level") and e.get("definition") for e in levels):
        errs.append("scoring_method.evaluation_levels must be a LIST of {level, definition, ...} entries "
                    f"(found {type(levels).__name__}), e.g. [{{\"level\": \"gross\", ...}}]; not an object keyed by level")
    crr = sm.get("corporate_register_threshold")
    named = {k: v for k, v in crr.items() if isinstance(v, dict) and is_int(v.get("score_at_or_above"))} \
        if isinstance(crr, dict) else {}
    if not named or not all(v.get("section") for v in named.values()):
        errs.append("scoring_method.corporate_register_threshold must map each statement of the threshold to "
                    "{section, score_at_or_above, quote, ...}, e.g. {\"table_4\": {...}, \"figure_4\": {...}}")
    return errs


def main(hist: str, cdir: str) -> int:
    errors, warnings = [], []
    try:
        doc = json.loads(Path(hist).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read {hist}: {e}")
        return 1
    for k in TOP:
        if k not in doc:
            errors.append(f"top-level key missing: {k}")
    cache: dict[str, list[str]] = {}
    n_items = n_quotes = 0
    for path, d in walk(doc):
        src = d.get("source")
        if src is None:
            if "quote" in d:
                errors.append(f"{path}: has a quote but no source")
            continue
        n_items += 1
        f = Path(cdir) / src
        if not f.exists():
            errors.append(f"{path}: source file not found: {src}")
            continue
        page = d.get("pdf_page")
        if not isinstance(page, int) or isinstance(page, bool):
            errors.append(f"{path}: pdf_page missing or not an integer")
            continue
        if src not in cache:
            cache[src] = pages(f)
        ps = cache[src]
        if not 1 <= page <= len(ps):
            errors.append(f"{path}: pdf_page {page} out of range 1..{len(ps)} for {src}")
            continue
        q = d.get("quote")
        if q is None:
            continue
        n_quotes += 1
        nq = normalise(str(q))
        if len(nq) < 12:
            errors.append(f"{path}: quote too short ({len(nq)} chars)")
        elif nq in ps[page - 1]:
            pass
        else:
            hits = [i + 1 for i, p in enumerate(ps) if nq in p]
            if hits:
                errors.append(f"{path}: quote is on page(s) {hits}, not pdf_page {page}: {q[:60]!r}…")
            elif nq in " ".join(ps):
                errors.append(f"{path}: quote straddles a page boundary: {q[:60]!r}…")
            else:
                errors.append(f"{path}: quote NOT FOUND in {src}: {q[:60]!r}…")
    sm = doc.get("scoring_method", {})
    if isinstance(sm, dict) and "usable" not in sm:
        errors.append("scoring_method.usable missing")
    elif isinstance(sm, dict) and sm.get("usable"):
        errors += scoring_shape(sm)
    print(f"history.json: {n_items} sourced items, {n_quotes} quotes, {len(cache)} documents")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("FAIL ", e)
    if errors:
        print(f"\n{len(errors)} failure(s)")
        return 1
    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
