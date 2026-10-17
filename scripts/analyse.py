"""analyse.py - risk-indicator tests over spend-clean.csv (and notices-clean.csv if present).

Writes outputs/analytics.json and CSVs in outputs/analytics-full/.
All thresholds are read from outputs/rules.json; none are typed here.
Outputs describe indicators to investigate, not findings of wrongdoing.
"""
import difflib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, "outputs", "analytics-full")
OUTJ = os.path.join(ROOT, "outputs", "analytics.json")
TAGS = ["general_procurement", "care_or_education_placement", "grant", "agency_staff", "premises_non_procurement"]
WINDOW_DAYS = 30      # split-purchase window: anchor date + 29 days (30 calendar days inclusive)
DUP_DAYS = 7          # duplicate window: consecutive equal payments within 7 calendar days
CLUSTER_BELOW = 0.9   # band fractions (method parameters, not thresholds)
CLUSTER_ABOVE = 1.1
BASE_LO, BASE_HI = 0.5, 1.5
RATIO_MIN = 0.85
OVERSPEND_RATIO = 1.25

CAVEAT = ("contracts.csv holds published *notices*, not a contract register. It holds awards published on Contracts "
          "Finder in roughly the last five years. A contract awarded earlier (e.g. long-running waste or highways "
          "contracts), one advertised only on Find a Tender, a framework call-off recorded under another buyer, or an "
          "exempt placement will have no notice here. \"No notice found\" is therefore an indicator to check against "
          "the council's contract register, never evidence of off-contract spend.")
GENERIC = set("""AND OF THE SERVICES SERVICE GROUP CARE COMPANY HOMES HOME HOUSE UNIVERSITY COUNCIL TRUST SOLUTIONS
CONSULTANCY CONSULTING ASSOCIATES PARTNERSHIP NETWORK CENTRE CENTER TRAVEL CARS COACHES TAXIS CONSTRUCTION HEALTHCARE
HEALTH SCHOOL SCHOOLS EDUCATION SUPPORT LIVING CHILDREN CHILDRENS SEN BERKSHIRE WEST SOUTH NORTH EAST READING NEWBURY
THATCHAM HUNGERFORD SOUTHERN SYSTEMS SOFTWARE HOUSING SECURITY CLEANING FOSTERING COMMUNITY BUSINESS MANAGEMENT
FACILITIES SUPPLIES CATERING TRANSPORT ENGINEERING HIRE PROPERTY PROPERTIES VALLEY""".split())


def stop(msg):
    print("STOP: " + msg, file=sys.stderr)
    sys.exit(1)


def r2(x):
    return round(float(x), 2)


# ------------------------------------------------------------------ thresholds
def derive_thresholds(rules):
    use = [r for r in rules["rules"] if r.get("type") in ("threshold", "approver", "anti-avoidance")]
    vals = {}
    for r in use:
        for side in ("low", "high"):
            v = r.get(f"threshold_{side}")
            if v is None:
                continue
            e = vals.setdefault(int(v), {"rule_ids": [], "low_incl": [], "high_incl": [], "trigger_actions": [], "rules": []})
            e["rule_ids"].append(r["rule_id"])
            inc = r.get(f"threshold_{side}_inclusive")
            (e["low_incl"] if side == "low" else e["high_incl"]).append((r["rule_id"], inc))
            if side == "low":
                e["trigger_actions"].append((r["rule_id"], r.get("required_action") or ""))
    out = []
    for v in sorted(vals):
        e = vals[v]
        notes = []
        lows = {i for _, i in e["low_incl"] if i is not None}
        highs = {i for _, i in e["high_incl"] if i is not None}
        if lows:
            inclusive = True if lows == {True} else (False if lows == {False} else True)
            if len(lows) > 1:
                notes.append("rules disagree on whether the trigger is 'at or above' or 'above'; treated as at-or-above")
        else:
            # value only appears as an upper bound: 'less than T' means T itself triggers the next band
            inclusive = (False in highs) or not highs
        # boundary gap check: trigger 'above T' and some band 'less than T' -> T itself in no band
        if lows == {False} and False in highs:
            notes.append("boundary gap: some rules say 'less than' and others 'above' this value, so a value exactly equal falls in neither band")
        comp = [rid for rid, a in e["trigger_actions"] if re.search(r"quot|tender", a, re.I)]
        publ = [rid for rid, a in e["trigger_actions"]
                if re.search(r"Portal|CDP|advert", a, re.I) and not re.search(r"no advertising", a, re.I)]
        out.append({"value": v, "inclusive": inclusive,
                    "trigger": ">= value" if inclusive else "> value",
                    "competition_triggering": bool(comp), "competition_rule_ids": comp,
                    "publication_rule_ids": publ,
                    "rule_ids": sorted(set(e["rule_ids"])), "notes": notes,
                    "basis": "compared with spend Net amount (ex-VAT), i.e. App B ex-VAT values"})
    return out


def below_mask(a, t):
    lo = CLUSTER_BELOW * t["value"]
    return (a >= lo) & ((a < t["value"]) if t["inclusive"] else (a <= t["value"]))


def above_mask(a, t):
    hi = CLUSTER_ABOVE * t["value"]
    return ((a >= t["value"]) if t["inclusive"] else (a > t["value"])) & (a < hi)


def meets(x, t):
    return x >= t["value"] if t["inclusive"] else x > t["value"]


def under(x, t):
    return x < t["value"] if t["inclusive"] else x <= t["value"]


# ------------------------------------------------------------------ matching
def dtoks(name):
    return frozenset(t for t in name.split() if t not in GENERIC and len(t) >= 3)


def build_matcher(spend_names, notice_names):
    spend_tok_count = Counter(t for n in spend_names for t in dtoks(n))
    notice_tok_count = Counter(t for n in notice_names for t in dtoks(n))
    notice_list = sorted(set(notice_names))
    notice_set = set(notice_list)
    ntoks = {n: dtoks(n) for n in notice_list}

    def match_supplier(name):
        if not name:
            return "none", "", None, ""
        if name in notice_set:
            return "exact", name, 1.0, "exact"
        best, best_r = "", 0.0
        for n in notice_list:
            r = difflib.SequenceMatcher(None, name, n).ratio()
            if r > best_r:
                best, best_r = n, r
        if best_r >= RATIO_MIN:
            return "near_ratio", best, round(best_r, 3), f"SequenceMatcher ratio >= {RATIO_MIN}"
        st = dtoks(name)
        for n in notice_list:
            nt = ntoks[n]
            if not st or not nt:
                continue
            small, large = (st, nt) if len(st) <= len(nt) else (nt, st)
            if not small <= large:
                continue
            if len(small) >= 2:
                return "near_contain", n, round(difflib.SequenceMatcher(None, name, n).ratio(), 3), \
                    f"distinctive subset >=2 tokens {sorted(small)}"
            tok = next(iter(small))
            if spend_tok_count[tok] == 1 and notice_tok_count[tok] == 1:
                return "near_contain", n, round(difflib.SequenceMatcher(None, name, n).ratio(), 3), \
                    f"single distinctive token '{tok}' unique on both sides"
        return "none", "", None, ""
    return match_supplier


# ------------------------------------------------------------------ helpers
def sup_display(df):
    return df.groupby("supplier_norm")["supplier_original"].agg(lambda s: s.value_counts().index[0])


def topn(df, cols, n=20):
    recs = df[cols].head(n).to_dict(orient="records")
    for r in recs:
        for k, v in list(r.items()):
            if isinstance(v, float):
                r[k] = round(v, 2)
            elif isinstance(v, (pd.Timestamp,)):
                r[k] = str(v.date())
    return recs


def tag_split(df, amount_col="Net amount", tag_col="tag"):
    g = df.groupby(tag_col)[amount_col].agg(["count", "sum"])
    return {t: {"count": int(g.loc[t, "count"]) if t in g.index else 0,
                "gbp": r2(g.loc[t, "sum"]) if t in g.index else 0.0} for t in TAGS}


# ------------------------------------------------------------------ tests
def test_clustering(d, thresholds):
    out = {"description": "single payments in the band just below each threshold, compared with the band just above "
                          "and a wider baseline band", "parameters": {"below_band": f"{CLUSTER_BELOW}*T to T",
                          "above_band": f"T to {CLUSTER_ABOVE}*T", "baseline_band": f"{BASE_LO}*T to {BASE_HI}*T",
                          "inclusivity": "if trigger is '>= T' the below band excludes T; if '> T' it includes T"},
           "by_threshold": {}}
    full = []
    a = d["Net amount"]
    for t in thresholds:
        T = t["value"]
        b = d[below_mask(a, t)].sort_values("Net amount", ascending=False)
        ab = d[above_mask(a, t)]
        base = d[(a >= BASE_LO * T) & (a < BASE_HI * T)]
        conc = b.groupby("supplier_norm").agg(n=("row_id", "count"), gbp=("Net amount", "sum")) \
            .sort_values(["n", "gbp"], ascending=False).head(20)
        disp = sup_display(d)
        notes = list(t["notes"])
        if BASE_LO * T <= d["Net amount"].min():
            notes.append("baseline band starts at or below the £500 publication floor, so its lower part is not observable")
        blk = {"threshold": T, "trigger": t["trigger"], "rule_ids": t["rule_ids"],
               "below_band": {"count": int(len(b)), "gbp": r2(b["Net amount"].sum()),
                              "range": [CLUSTER_BELOW * T, T], "includes_T": not t["inclusive"]},
               "above_band_comparator": {"count": int(len(ab)), "gbp": r2(ab["Net amount"].sum())},
               "baseline_band": {"count": int(len(base)), "gbp": r2(base["Net amount"].sum())},
               "below_band_by_tag": tag_split(b),
               "supplier_concentration_top20": [{"supplier": disp[s], "supplier_norm": s, "n": int(r.n), "gbp": r2(r.gbp)}
                                                for s, r in conc.iterrows()],
               "top20": topn(b, ["row_id", "supplier_original", "Net amount", "pay_date", "Service", "Narrative", "tag"]),
               "notes": notes}
        out["by_threshold"][str(T)] = blk
        bb = b.copy()
        bb["threshold"] = T
        full.append(bb)
    pd.concat(full).to_csv(os.path.join(FULL, "threshold-clustering.csv"), index=False)
    out["full_list"] = "outputs/analytics-full/threshold-clustering.csv"
    return out


def test_splits(d, thresholds):
    comp = [t for t in thresholds if t["competition_triggering"]]
    out = {"description": "same normalised supplier, 2 or more payments each under the threshold within a 30-calendar-day "
                          "window whose combined total reaches the threshold",
           "parameters": {"window_days": WINDOW_DAYS, "window_definition": "anchor payment date to anchor + 29 days inclusive (calendar dates)",
                          "dedupe": "per supplier per threshold, overlapping windows (sharing a payment) reduced to the highest total",
                          "thresholds": [t["value"] for t in comp]},
           "rule_ids": sorted({"CPR-12"} | {r for t in comp for r in t["competition_rule_ids"]}),
           "caveat": "payments of £500 or less are not published, so these counts are lower bounds; periodic care fees legitimately recur",
           "by_threshold": {}}
    all_rows = []
    for t in comp:
        T = t["value"]
        cand = d[under(d["Net amount"], t)].sort_values(["supplier_norm", "pay_date", "row_id"])
        wins = []
        for sup, g in cand.groupby("supplier_norm", sort=False):
            if len(g) < 2:
                continue
            dates = g["pay_date"].values
            amts = g["Net amount"].values
            ids = g["row_id"].values
            qual = []
            for i in range(len(g)):
                end = dates[i] + pd.Timedelta(days=WINDOW_DAYS - 1).to_timedelta64()
                j = i
                while j + 1 < len(g) and dates[j + 1] <= end:
                    j += 1
                if j > i:
                    tot = float(amts[i:j + 1].sum())
                    if meets(round(tot, 2), t):
                        qual.append((round(tot, 2), i, j))
            qual.sort(key=lambda x: (-x[0], x[1]))
            used = set()
            for tot, i, j in qual:
                rng = set(range(i, j + 1))
                if rng & used:
                    continue
                used |= rng
                sub = g.iloc[i:j + 1]
                tg = sub.groupby("tag")["Net amount"].sum().sort_values(ascending=False)
                wins.append({"threshold": T, "supplier": sub["supplier_original"].value_counts().index[0],
                             "supplier_norm": sup, "window_start": str(pd.Timestamp(dates[i]).date()),
                             "window_end_last_payment": str(pd.Timestamp(dates[j]).date()),
                             "n_payments": int(j - i + 1), "window_total": tot,
                             "distinct_amounts": int(sub["Net amount"].nunique()),
                             "max_payment": r2(sub["Net amount"].max()),
                             "services": "; ".join(sorted(sub["Service"].unique())),
                             "narratives": "; ".join(sorted(sub["Narrative"].unique())),
                             "dominant_tag": tg.index[0], "mixed_tags": bool(len(tg) > 1),
                             "row_ids": " ".join(ids[i:j + 1])})
        w = pd.DataFrame(wins)
        if w.empty:
            out["by_threshold"][str(T)] = {"windows": 0, "suppliers": 0, "gbp": 0.0}
            continue
        w = w.sort_values("window_total", ascending=False)
        all_rows.append(w)
        by_tag = {tg: {"windows": int((w.dominant_tag == tg).sum()), "suppliers": int(w.loc[w.dominant_tag == tg, "supplier_norm"].nunique()),
                       "gbp": r2(w.loc[w.dominant_tag == tg, "window_total"].sum())} for tg in TAGS}
        cols = ["supplier", "window_start", "window_end_last_payment", "n_payments", "window_total", "distinct_amounts",
                "services", "dominant_tag", "row_ids"]
        out["by_threshold"][str(T)] = {
            "threshold": T, "trigger": t["trigger"], "rule_ids": t["competition_rule_ids"],
            "windows": int(len(w)), "suppliers": int(w["supplier_norm"].nunique()), "gbp": r2(w["window_total"].sum()),
            "by_dominant_tag": by_tag,
            "headline_general_procurement": by_tag["general_procurement"],
            "placement_separately": by_tag["care_or_education_placement"],
            "top20_general_procurement": topn(w[w.dominant_tag == "general_procurement"], cols),
            "top20_care_or_education_placement": topn(w[w.dominant_tag == "care_or_education_placement"], cols),
            "top20_all": topn(w, cols)}
    if all_rows:
        pd.concat(all_rows).to_csv(os.path.join(FULL, "split-purchases.csv"), index=False)
    out["full_list"] = "outputs/analytics-full/split-purchases.csv"
    return out


def supplier_table(d, factor):
    g = d.groupby("supplier_norm")
    st = pd.DataFrame({"total_gbp": g["Net amount"].sum(), "n_payments": g["row_id"].count()})
    st["annualised_estimate"] = st["total_gbp"] * factor
    st["supplier"] = sup_display(d)
    bt = d.groupby(["supplier_norm", "tag"])["Net amount"].sum().reset_index().sort_values(["supplier_norm", "Net amount"], ascending=[True, False])
    st["dominant_tag"] = bt.groupby("supplier_norm")["tag"].first()
    st["n_tags"] = bt.groupby("supplier_norm")["tag"].nunique()
    st["spans_tags"] = st["n_tags"] > 1
    top_nar = d.groupby(["supplier_norm", "Narrative"])["Net amount"].sum().reset_index().sort_values("Net amount", ascending=False)
    st["main_narrative"] = top_nar.groupby("supplier_norm")["Narrative"].first()
    top_svc = d.groupby(["supplier_norm", "Service"])["Net amount"].sum().reset_index().sort_values("Net amount", ascending=False)
    st["main_service"] = top_svc.groupby("supplier_norm")["Service"].first()
    st["n_services"] = d.groupby("supplier_norm")["Service"].nunique()
    st["row_ids"] = g["row_id"].agg(lambda s: " ".join(s))
    st["row_ids_first10"] = g["row_id"].agg(lambda s: " ".join(list(s)[:10]))
    return st.reset_index()


def test_high_value(st, pub_t, low_comp_t, stat_value):
    out = {"description": "suppliers whose annualised estimate reaches the publication/competition threshold; population "
                          "for which contract evidence is requested during fieldwork (Phase 3 PBC list)",
           "parameters": {"threshold": pub_t["value"], "trigger": pub_t["trigger"],
                          "threshold_choice": ("lowest competition-triggering threshold whose rule requires Portal/CDP "
                                               "publication (rule_ids " + ", ".join(pub_t["publication_rule_ids"]) + "); "
                                               "the lower competition threshold (" + str(low_comp_t["value"]) + ", rule_ids "
                                               + ", ".join(low_comp_t["competition_rule_ids"]) + ") requires one quote with "
                                               "no advertising, so suppliers there would never appear on Contracts Finder"),
                          "measure": "annualised estimate = 3-period total x (12 / months_covered)"},
           "rule_ids": sorted(set(pub_t["rule_ids"])), "tiers": {}}
    hv = st[meets(st["annualised_estimate"], pub_t)].sort_values("annualised_estimate", ascending=False).copy()
    by_tag = {}
    for tg in TAGS:
        s = hv[hv.dominant_tag == tg]
        by_tag[tg] = {"suppliers": int(len(s)), "gbp_in_window": r2(s.total_gbp.sum()),
                      "annualised_estimate_gbp": r2(s.annualised_estimate.sum()), "spanning_several_tags": int(s.spans_tags.sum())}
    cols = ["supplier", "annualised_estimate", "total_gbp", "n_payments", "main_narrative", "main_service", "n_services",
            "spans_tags", "row_ids_first10"]
    out["tiers"]["publication_threshold"] = {
        "threshold": pub_t["value"], "suppliers": int(len(hv)), "gbp_in_window": r2(hv.total_gbp.sum()),
        "annualised_estimate_gbp": r2(hv.annualised_estimate.sum()), "by_dominant_tag": by_tag,
        "headline_general_procurement": by_tag["general_procurement"],
        "top20_general_procurement": topn(hv[hv.dominant_tag == "general_procurement"], cols),
        "top20_care_or_education_placement": topn(hv[hv.dominant_tag == "care_or_education_placement"], cols),
        "top20_grant": topn(hv[hv.dominant_tag == "grant"], cols),
        "top20_agency_staff": topn(hv[hv.dominant_tag == "agency_staff"], cols),
        "top20_premises_non_procurement": topn(hv[hv.dominant_tag == "premises_non_procurement"], cols)}
    lc = st[meets(st["annualised_estimate"], low_comp_t)]
    out["tiers"]["lowest_competition_threshold_counts_only"] = {
        "threshold": low_comp_t["value"], "rule_ids": low_comp_t["competition_rule_ids"],
        "suppliers": int(len(lc)), "annualised_estimate_gbp": r2(lc.annualised_estimate.sum()),
        "note": "counts only; not used for contract-evidence requests (no publication required at this level)"}
    skipped = []
    if stat_value is None:
        out["tiers"]["statutory"] = {"skipped": True, "reason": "STATUTORY_THRESHOLD_GOODS_SERVICES is null"}
        skipped.append({"test": "high_value_suppliers", "tier": "statutory", "reason": "STATUTORY_THRESHOLD_GOODS_SERVICES is null"})
    hv.drop(columns=["row_ids_first10"]).to_csv(os.path.join(FULL, "high-value-suppliers.csv"), index=False)
    out["full_list"] = "outputs/analytics-full/high-value-suppliers.csv"
    return out, hv, skipped


def test_duplicates(d):
    rows = []
    gid = 0
    for (sup, amt), g in d.groupby(["supplier_norm", "Net amount"]):
        if len(g) < 2:
            continue
        g = g.sort_values(["pay_date", "Date_ts", "row_id"])
        dates = list(g["pay_date"])
        cluster = [0]
        for k in range(1, len(g)):
            cluster.append(cluster[-1] + (1 if (dates[k] - dates[k - 1]).days > DUP_DAYS else 0))
        g = g.assign(_c=cluster)
        for _, c in g.groupby("_c"):
            if len(c) < 2:
                continue
            gid += 1
            tier = "same_timestamp" if c["Date_ts"].nunique() == 1 else "different_time"
            tg = c.groupby("tag")["Net amount"].sum().sort_values(ascending=False)
            rows.append({"group_id": gid, "tier": tier, "supplier": c["supplier_original"].iloc[0], "supplier_norm": sup,
                         "amount": r2(amt), "n_rows": int(len(c)), "gbp_beyond_first": r2(amt * (len(c) - 1)),
                         "first_date": str(c["pay_date"].min().date()), "last_date": str(c["pay_date"].max().date()),
                         "distinct_timestamps": int(c["Date_ts"].nunique()),
                         "services": "; ".join(sorted(c["Service"].unique())),
                         "narratives": "; ".join(sorted(c["Narrative"].unique())),
                         "dominant_tag": tg.index[0], "row_ids": " ".join(c["row_id"])})
    g = pd.DataFrame(rows)
    out = {"description": "same normalised supplier, same amount to the penny, calendar dates within 7 days "
                          "(consecutive payments linked if 7 days or less apart)",
           "parameters": {"days": DUP_DAYS, "tiers": {"same_timestamp": "all rows share one payment-run timestamp (typical of a batch of equal invoices)",
                                                       "different_time": "rows on 2 or more different timestamps (higher signal)"}},
           "rule_ids": [], "caveat": "payments of £500 or less are not published, so counts are lower bounds", "tiers": {}}
    cols = ["supplier", "amount", "n_rows", "gbp_beyond_first", "first_date", "last_date", "services", "dominant_tag", "row_ids"]
    for tier in ["same_timestamp", "different_time"]:
        s = g[g.tier == tier].sort_values("amount", ascending=False) if not g.empty else g
        out["tiers"][tier] = {"groups": int(len(s)), "rows": int(s.n_rows.sum()) if len(s) else 0,
                              "gbp_beyond_first": r2(s.gbp_beyond_first.sum()) if len(s) else 0.0,
                              "by_dominant_tag": {tg: {"groups": int((s.dominant_tag == tg).sum()),
                                                       "gbp_beyond_first": r2(s.loc[s.dominant_tag == tg, "gbp_beyond_first"].sum())} for tg in TAGS} if len(s) else {},
                              "top20": topn(s, cols) if len(s) else []}
    if not g.empty:
        g.to_csv(os.path.join(FULL, "duplicates.csv"), index=False)
    out["full_list"] = "outputs/analytics-full/duplicates.csv"
    return out


# ------------------------------------------------------------------ main
def main():
    rp = os.path.join(ROOT, "outputs", "rules.json")
    if not os.path.exists(rp):
        stop("outputs/rules.json missing")
    rules = json.load(open(rp))
    log_p = os.path.join(FULL, "cleaning-log.json")
    if not os.path.exists(log_p):
        stop("run scripts/clean.py first")
    clog = json.load(open(log_p))
    d = pd.read_csv(os.path.join(FULL, "spend-clean.csv"), dtype={"row_id": str, "Date_ts": str})
    d["pay_date"] = pd.to_datetime(d["pay_date"], format="%Y-%m-%d")
    d["supplier_norm"] = d["supplier_norm"].fillna("")
    months = clog["months_covered"]
    factor = 12 / months
    window_start = pd.Timestamp(clog["date_min"])
    params = rules.get("parameters", {})
    stat = params.get("STATUTORY_THRESHOLD_GOODS_SERVICES", {}).get("value")

    thresholds = derive_thresholds(rules)
    comp = [t for t in thresholds if t["competition_triggering"]]
    if not comp:
        stop("no competition-triggering thresholds derivable from rules.json")
    pubs = [t for t in comp if t["publication_rule_ids"]]
    if not pubs:
        stop("no publication threshold derivable from rules.json")
    pub_t, low_comp_t = pubs[0], comp[0]

    skipped = []
    for k, v in params.items():
        if v.get("value") is None:
            skipped.append({"test": "threshold_clustering, split_purchases", "tier": k,
                            "reason": f"{k} is null (auditor has not supplied it); no statutory-threshold band tested"})

    tests = {}
    tests["threshold_clustering"] = test_clustering(d, thresholds)
    tests["split_purchases"] = test_splits(d, thresholds)
    st = supplier_table(d, factor)
    tests["high_value_suppliers"], hv, sk = test_high_value(st, pub_t, low_comp_t, stat)
    skipped += sk
    tests["duplicates"] = test_duplicates(d)

    cpres = bool(clog["contracts"].get("contracts_present"))
    rpres = bool(clog.get("register_present"))
    matching = {}
    if cpres:
        n = pd.read_csv(os.path.join(FULL, "notices-clean.csv"), dtype={"notice_id": str})
        for c in ["contract_start", "contract_end"]:
            n[c] = pd.to_datetime(n[c], format="%Y-%m-%d")
        n["supplier_norm"] = n["supplier_norm"].fillna("")
        active = n[n.active_in_window]
        ended = n[n.ended_before_window]
        spend_names = sorted(st["supplier_norm"].unique())
        m_active = build_matcher(spend_names, active["supplier_norm"].unique())
        res = [m_active(s) for s in spend_names]
        sm = pd.DataFrame(res, columns=["match_class", "candidate_norm", "ratio", "rule_fired"])
        sm.insert(0, "supplier_norm", spend_names)
        sm = sm.merge(st[["supplier_norm", "supplier", "total_gbp", "annualised_estimate", "dominant_tag"]], on="supplier_norm")
        nid = active.groupby("supplier_norm")["notice_id"].agg(lambda s: " ".join(sorted(set(s))))
        sm["candidate_notice_ids"] = sm["candidate_norm"].map(nid).fillna("")
        sm.to_csv(os.path.join(FULL, "supplier-match.csv"), index=False)
        near = sm[sm.match_class.isin(["near_ratio", "near_contain"])].sort_values("annualised_estimate", ascending=False)
        near.to_csv(os.path.join(FULL, "near-matches.csv"), index=False)
        vc = sm.match_class.value_counts()
        matching = {k: int(vc.get(k, 0)) for k in ["exact", "near_ratio", "near_contain", "none"]}
        matching.update({"basis": "every non-excluded spend supplier vs active notice suppliers (normalised names)",
                         "companies_house_matching": "not possible: spend data carries no company number",
                         "near_matches_file": "outputs/analytics-full/near-matches.csv",
                         "match_file": "outputs/analytics-full/supplier-match.csv",
                         "note": "near matches are candidates for the auditor to confirm and are never counted as matches"})

        # off_contract
        hvm = hv.merge(sm[["supplier_norm", "match_class", "candidate_norm", "ratio", "rule_fired", "candidate_notice_ids"]], on="supplier_norm", how="left")
        hvm.drop(columns=["row_ids_first10"]).to_csv(os.path.join(FULL, "off-contract.csv"), index=False)
        per_class = {k: {"suppliers": int((hvm.match_class == k).sum()), "gbp_in_window": r2(hvm.loc[hvm.match_class == k, "total_gbp"].sum()),
                         "annualised_estimate_gbp": r2(hvm.loc[hvm.match_class == k, "annualised_estimate"].sum())}
                     for k in ["exact", "near_ratio", "near_contain", "none"]}
        un = hvm[hvm.match_class == "none"]
        un_tag = {tg: {"suppliers": int((un.dominant_tag == tg).sum()), "annualised_estimate_gbp": r2(un.loc[un.dominant_tag == tg, "annualised_estimate"].sum())} for tg in TAGS}
        cols = ["supplier", "annualised_estimate", "total_gbp", "n_payments", "main_narrative", "main_service", "row_ids_first10"]
        tests["off_contract"] = {
            "description": "high-value suppliers (annualised estimate at or above the publication threshold) with no "
                           "exact supplier-name match to an active Contracts Finder notice",
            "parameters": {"threshold": pub_t["value"], "population": "high_value_suppliers publication tier",
                           "active_notice_rule": "contract end date on or after spend window start, or blank"},
            "rule_ids": sorted(set(pub_t["publication_rule_ids"] + ["CPR-63"])),
            "rule_notes": "CPR-63 (App C row F) exempts individually chosen care/education placements from competition, so the placement group is expected to have few notices",
            "contracts_present": cpres, "register_present": rpres, "caveat": CAVEAT,
            "scope_note": "Only suppliers at or above the publication threshold are classed; Contracts Finder does not carry smaller awards, so results must never be used to question smaller suppliers.",
            "per_match_class": per_class, "unmatched_by_dominant_tag": un_tag,
            "headline_unmatched_general_procurement": un_tag["general_procurement"],
            "top20_unmatched_general_procurement": topn(un[un.dominant_tag == "general_procurement"], cols),
            "full_list": "outputs/analytics-full/off-contract.csv"}

        # expired_notice_spend
        ended_names = set(ended.supplier_norm) - {""}
        active_names = set(active.supplier_norm) - {""}
        exp = st[st.supplier_norm.isin(ended_names) & ~st.supplier_norm.isin(active_names)].copy()
        eg = ended.groupby("supplier_norm").agg(latest_end=("contract_end", "max"),
                                               notice_ids=("notice_id", lambda s: " ".join(sorted(set(s)))))
        exp = exp.merge(eg, left_on="supplier_norm", right_index=True)
        exp["at_or_above_publication_threshold"] = meets(exp["annualised_estimate"], pub_t)
        exp = exp.sort_values("annualised_estimate", ascending=False)
        exp.drop(columns=["row_ids_first10"]).to_csv(os.path.join(FULL, "expired-notice-spend.csv"), index=False)
        ea = exp[exp.at_or_above_publication_threshold]
        tests["expired_notice_spend"] = {
            "description": "suppliers paid in the spend window whose every exact-matched notice ended before the window started",
            "parameters": {"match": "exact normalised name", "window_start": str(window_start.date())},
            "rule_ids": ["CPR-61"], "rule_note": "CPR-61 (App C row D) requires S151 Officer approval of an extension",
            "caveat": CAVEAT + " A newer contract, an approved extension or a framework call-off may exist with no notice in this file.",
            "suppliers": int(len(exp)), "gbp_in_window": r2(exp.total_gbp.sum()),
            "annualised_estimate_gbp": r2(exp.annualised_estimate.sum()),
            "at_or_above_publication_threshold": {"suppliers": int(len(ea)), "annualised_estimate_gbp": r2(ea.annualised_estimate.sum())},
            "by_dominant_tag": {tg: int((exp.dominant_tag == tg).sum()) for tg in TAGS},
            "top20": topn(exp.assign(latest_end=exp.latest_end.dt.date.astype(str)),
                          ["supplier", "annualised_estimate", "total_gbp", "n_payments", "latest_end", "notice_ids", "dominant_tag", "row_ids_first10"]),
            "full_list": "outputs/analytics-full/expired-notice-spend.csv"}

        # spend_vs_award
        act_by_sup = active[active.supplier_norm != ""].groupby("supplier_norm")["notice_id"].nunique()
        cand = active[(active.suppliers_on_notice == 1) & (active.awarded_value > 0)]
        cand = cand[cand.supplier_norm.map(act_by_sup) == 1]
        cand = cand[cand.supplier_norm.isin(set(st.supplier_norm))].copy()
        no_dates = cand[cand.contract_start.isna() | cand.contract_end.isna()]
        cand = cand.drop(no_dates.index)
        cand["contract_years"] = (cand.contract_end - cand.contract_start).dt.days / 365.25
        bad_years = cand[cand.contract_years <= 0]
        cand = cand[cand.contract_years > 0]
        cand["award_annual_rate"] = cand.awarded_value / cand.contract_years
        sv = cand.merge(st, on="supplier_norm", suffixes=("_notice", ""))
        sv["ratio"] = sv.annualised_estimate / sv.award_annual_rate
        sv = sv.sort_values("ratio", ascending=False)
        sv.drop(columns=["row_ids_first10"]).to_csv(os.path.join(FULL, "spend-vs-award.csv"), index=False)
        fl = sv[sv.ratio >= OVERSPEND_RATIO]
        tests["spend_vs_award"] = {
            "description": "annualised estimate compared with the award's annual rate for suppliers on exactly one live, "
                           "single-supplier notice with Awarded Value > 0",
            "parameters": {"ratio_flag": OVERSPEND_RATIO, "award_annual_rate": "Awarded Value / contract years (end - start days / 365.25)",
                           "ratio": "annualised estimate / award_annual_rate",
                           "eligibility": "exact name match; supplier on exactly one active notice; that notice single-supplier with Awarded Value > 0 and both dates present"},
            "rule_ids": ["CPR-62"], "rule_note": "CPR-62 (App C row E) sets approvals for variations",
            "caveat": "Award values may be estimates or maxima, contract periods may include optional extensions, and spend may relate to other arrangements; a high ratio is an indicator to check, not evidence of over-spend.",
            "eligible_suppliers": int(len(sv)), "excluded_missing_dates": int(len(no_dates)), "excluded_nonpositive_term": int(len(bad_years)),
            "flagged_ratio_ge_threshold": int(len(fl)), "flagged_annualised_estimate_gbp": r2(fl.annualised_estimate.sum()),
            "top20": topn(sv, ["supplier", "notice_id", "title", "awarded_value", "contract_years", "award_annual_rate",
                               "annualised_estimate", "ratio", "row_ids_first10"]),
            "full_list": "outputs/analytics-full/spend-vs-award.csv"}
    else:
        for t in ["off_contract"]:
            tests[t] = {"skipped": True, "reason": "no contracts.csv or contract register in data/"}
            skipped.append({"test": t, "reason": "no contracts.csv or contract register in data/"})
        for t in ["expired_notice_spend", "spend_vs_award"]:
            tests[t] = {"skipped": True, "reason": "contracts.csv absent"}
            skipped.append({"test": t, "reason": "contracts.csv absent"})
    if not rpres:
        skipped.append({"test": "off_contract", "tier": "register", "reason": "data/contract-register.csv absent: matching uses Contracts Finder notices only"})

    cc = clog["contracts"]
    contracts = {"contracts_present": cpres, "register_present": rpres,
                 "rows_in_file": cc.get("rows_in_file", 0), "rows_for_council": cc.get("rows_for_council", 0),
                 "rows_dropped_other_buyers": cc.get("rows_dropped_other_buyers", 0),
                 "rows_dropped_duplicate_notice_id": cc.get("rows_dropped_duplicate_notice_id", 0),
                 "organisation_names_kept": cc.get("organisation_names_kept", {}),
                 "notice_supplier_pairs": cc.get("notice_supplier_pairs", 0), "distinct_suppliers": cc.get("distinct_suppliers", 0),
                 "active_in_window": cc.get("active_in_window", 0), "ended_before_window": cc.get("ended_before_window", 0),
                 "zero_value_awards": cc.get("zero_value_awards", 0), "rows_per_year": cc.get("rows_per_year", {}),
                 "published_range": cc.get("published_range", ["", ""]), "warnings": cc.get("warnings", []), "caveat": CAVEAT}
    pop = {"files": [f["file"] for f in clog["files"]], "file_detail": clog["files"],
           "rows_raw": clog["rows_raw"], "rows_after_exclusions": clog["rows_after_exclusions"],
           "gbp_raw": clog["gbp_raw"], "date_min": clog["date_min"], "date_max": clog["date_max"],
           "months_covered": months, "annualisation_factor": factor, "total_gbp": clog["gbp_after_exclusions"],
           "excluded": clog["excluded"], "tags": clog["tags"],
           "uncategorised_expenditure_category": clog["uncategorised_expenditure_category"],
           "vat_basis": "Spend 'Net amount' is ex-VAT; thresholds compared as App B ex-VAT values (rules.json notes a VAT conflict with clause 6.15).",
           "limitations": ["population is expenditure over £500 only; split-purchase and duplicate results are lower bounds",
                           "Date is a payment-run timestamp, not an invoice date; calendar dates used for windows",
                           "'Redacted' supplier rows excluded from all supplier-level tests",
                           "annualised estimate = window total x 12 / months_covered; seasonal or one-off spend distorts it",
                           "inter_authority supplier regex is a fixed word list; it can catch non-public bodies whose name contains e.g. COUNTY (see spend-excluded.csv)"]}
    thr_out = [{k: t[k] for k in ["value", "inclusive", "trigger", "competition_triggering", "rule_ids", "competition_rule_ids", "publication_rule_ids", "notes", "basis"]} for t in thresholds]
    other_nums = sorted({(int(r[s]), r["rule_id"]) for r in rules["rules"] if r.get("type") not in ("threshold", "approver", "anti-avoidance")
                         for s in ("threshold_low", "threshold_high") if r.get(s) is not None})
    out = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "scripts": ["scripts/clean.py", "scripts/analyse.py"],
           "population": pop, "thresholds": thr_out,
           "thresholds_not_tested": [{"value": v, "rule_id": rid, "reason": "cited only by a required-action rule (transparency/publication duty), not a threshold/approver/anti-avoidance rule"} for v, rid in other_nums],
           "skipped": skipped, "contracts": contracts, "matching": matching, "tests": tests}
    with open(OUTJ, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"analyse.py: wrote {OUTJ}; thresholds={[t['value'] for t in thresholds]} competition={[t['value'] for t in comp]} "
          f"publication={pub_t['value']} matching={ {k: matching.get(k) for k in ['exact','near_ratio','near_contain','none']} }")


if __name__ == "__main__":
    main()
