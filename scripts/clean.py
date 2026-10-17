"""clean.py - load, validate, exclude and tag spend; parse Contracts Finder notices.

Outputs (outputs/analytics-full/): spend-clean.csv, spend-excluded.csv,
notices-clean.csv, cleaning-log.json. Data under data/ is read-only.
Stops (non-zero exit) on missing columns, unparseable dates/amounts, nulls,
or negative amounts.
"""
import glob
import json
import os
import re
import sys
from datetime import datetime

import openpyxl
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs", "analytics-full")
SHEET = "Data to publish"
EXPECTED = ["Service", "Expenditure category", "Narrative", "Date", "Net amount", "Supplier name"]

# ---------------------------------------------------------------- normalisation
STOP_TOKENS = {"LTD", "LIMITED", "PLC", "LLP", "LLC", "INC", "CIC", "CIO", "UK", "THE"}


def normalise_supplier(name):
    if name is None or (isinstance(name, float) and pd.isna(name)):
        return ""
    s = str(name).upper()
    s = s.replace("&", " AND ")
    s = re.sub(r"\([^)]*\)", " ", s)          # bracketed qualifiers e.g. (CHAPS ONLY)
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\bT\s*/\s*AS?\b.*$", " ", s)    # T/A ... suffix
    s = re.sub(r"\bTRADING\s+AS\b.*$", " ", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    toks = [t for t in s.split() if t not in STOP_TOKENS]
    return " ".join(toks)


# ---------------------------------------------------------------- regexes (logged)
RX = {
    "redacted_supplier": r"^\s*REDACTED\s*$",
    "pension_statutory_narrative": r"LGPS|PENSION|SUPERANNUATION",
    "inter_authority_supplier": r"\b(COUNCIL|BOROUGH|COUNTY|CNCL|NHS|POLICE|FIRE AUTHORITY|FIRE AND RESCUE|HMRC|HM REVENUE|DEPARTMENT FOR|MINISTRY OF)\b",
    "inter_authority_narrative": r"JOINT ARRANGEMENTS",
    "inter_authority_not_if_narrative": r"^\s*PRIVATE CONTRACTORS\s*$",
    "tag_placement_service": r"^(ADULT SOCIAL CARE|CHILDREN'S SOCIAL CARE|EDUCATION)",
    "tag_placement_narrative": r"^\s*(PRIVATE CONTRACTORS|OTHER AGENCIES|VOLUNTARY ASSOCIATIONS)\s*$",
    "tag_grant": r"GRANT",
    "tag_agency_staff": r"AGENCY",
    "tag_premises_non_procurement": r"RENT|RATES|WATER RATES|LEASE",
}
EXCLUSION_REASONS = {
    "redacted_supplier": "Supplier shown as 'Redacted' aggregates many payees (often individuals); cannot be used in supplier-level tests.",
    "pension_statutory": "Pension/LGPS/superannuation contributions are statutory, not procurement.",
    "inter_authority": "Payments to other public bodies (councils, NHS, police, fire, HMRC, government departments) or joint arrangements are not competitive procurement (Private Contractors narrative kept).",
}


def stop(msg):
    print("STOP: " + msg, file=sys.stderr)
    sys.exit(1)


def parse_text_date(v):
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%m/%d/%y %H:%M", "%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(v.strip(), fmt)
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------- spend
def load_spend():
    files = sorted(glob.glob(os.path.join(DATA, "spend", "*.xlsx"))) + sorted(glob.glob(os.path.join(DATA, "spend", "*.csv")))
    if not files:
        stop("no spend files in data/spend/")
    frames, file_log = [], []
    for f in files:
        base = os.path.basename(f)
        if f.endswith(".csv"):
            stop(f"{base}: CSV spend input not handled by this version; add a loader rather than guess")
        raw = pd.read_excel(f, sheet_name=SHEET, header=None)
        hits = raw.index[raw[0].astype(str).str.strip() == "Service"].tolist()
        if not hits:
            stop(f"{base}: no row whose first cell is 'Service'")
        h = hits[0]
        df = pd.read_excel(f, sheet_name=SHEET, header=h)
        cols = [str(c).strip() for c in df.columns]
        if cols != EXPECTED:
            stop(f"{base}: columns {cols} != expected {EXPECTED}")
        df.columns = cols
        # sheet row: header at raw index h -> sheet row h+1; data index i -> sheet row h+2+i
        df["sheet_row"] = df.index + h + 2
        df = df.dropna(how="all", subset=EXPECTED)
        # verify row_ids against the workbook itself (openpyxl, 1-based rows)
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        ws = wb[SHEET]
        amt_by_row = {}
        for r_idx, row in enumerate(ws.iter_rows(min_col=5, max_col=5, values_only=True), start=1):
            amt_by_row[r_idx] = row[0]
        wb.close()
        bad = 0
        for sr, amt in zip(df["sheet_row"], df["Net amount"]):
            v = amt_by_row.get(sr)
            try:
                if v is None or abs(float(v) - float(amt)) > 0.001:
                    bad += 1
            except (TypeError, ValueError):
                bad += 1
        if bad:
            stop(f"{base}: {bad} rows whose computed sheet row does not match the workbook amount")
        df["source_file"] = base
        df["row_id"] = base + ":" + df["sheet_row"].astype(str)
        file_log.append({"file": base, "sheet": SHEET, "header_sheet_row": int(h + 1), "rows": int(len(df))})
        frames.append(df)
    d = pd.concat(frames, ignore_index=True)

    # nulls
    for c in ["Date", "Net amount", "Supplier name"]:
        n = int(d[c].isna().sum()) + int((d[c].astype(str).str.strip() == "").sum())
        if n:
            stop(f"{n} null/blank values in '{c}'")
    # dates
    def to_dt(v):
        if isinstance(v, (pd.Timestamp, datetime)):
            return pd.Timestamp(v)
        if isinstance(v, str):
            p = parse_text_date(v)
            return pd.Timestamp(p) if p else None
        return None
    d["Date"] = d["Date"].map(to_dt)
    if d["Date"].isna().any():
        stop(f"{int(d['Date'].isna().sum())} dates failed to parse (explicit M/D/Y formats only)")
    amt = pd.to_numeric(d["Net amount"], errors="coerce")
    if amt.isna().any():
        stop(f"{int(amt.isna().sum())} amounts failed to parse")
    d["Net amount"] = amt.round(2)
    neg = d[d["Net amount"] < 0]
    if len(neg):
        stop(f"{len(neg)} negative amounts, e.g. {neg['row_id'].head(5).tolist()}")
    d["pay_date"] = d["Date"].dt.normalize()
    d["Date_ts"] = d["Date"].dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]
    cat_blank = d["Expenditure category"].isna() | (d["Expenditure category"].astype(str).str.strip() == "")
    d["Expenditure category"] = d["Expenditure category"].where(~cat_blank, "Uncategorised")
    d["supplier_original"] = d["Supplier name"].astype(str)
    d["supplier_norm"] = d["Supplier name"].map(normalise_supplier)
    for c in ["Service", "Narrative", "Supplier name"]:
        d[c] = d[c].astype(str).str.strip()
    return d, file_log, int(cat_blank.sum()), float(d.loc[cat_blank, "Net amount"].sum())


def classify_exclusion(row):
    sup = row["Supplier name"].upper()
    nar = row["Narrative"].upper()
    if re.search(RX["redacted_supplier"], sup):
        return "redacted_supplier"
    if re.search(RX["pension_statutory_narrative"], nar):
        return "pension_statutory"
    if (re.search(RX["inter_authority_supplier"], sup) or re.search(RX["inter_authority_narrative"], nar)) \
            and not re.search(RX["inter_authority_not_if_narrative"], nar):
        return "inter_authority"
    return ""


def tag_row(row):
    svc = row["Service"].upper()
    nar = row["Narrative"].upper()
    if re.search(RX["tag_placement_service"], svc) and re.search(RX["tag_placement_narrative"], nar):
        return "care_or_education_placement"
    if re.search(RX["tag_grant"], nar):
        return "grant"
    if re.search(RX["tag_agency_staff"], nar):
        return "agency_staff"
    if re.search(RX["tag_premises_non_procurement"], nar):
        return "premises_non_procurement"
    return "general_procurement"


# ---------------------------------------------------------------- notices
COUNCIL_NAMES = {"WEST BERKSHIRE COUNCIL", "WEST BERKSHIRE"}
SUPPLIER_COL = "Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]"


def load_notices(window_start):
    path = os.path.join(DATA, "contracts.csv")
    log = {"contracts_present": False}
    if not os.path.exists(path):
        log["reason"] = "data/contracts.csv not found"
        return None, log
    c = pd.read_csv(path, dtype=str, keep_default_na=False)
    need = ["Notice Identifier", "Organisation Name", "Title", "Published Date", "Awarded Date", "Awarded Value",
            SUPPLIER_COL, "Contract start date", "Contract end date", "OJEU Procedure Type"]
    miss = [n for n in need if n not in c.columns]
    if miss:
        stop(f"contracts.csv missing columns {miss}")
    log["rows_in_file"] = int(len(c))
    org = c["Organisation Name"].str.strip().str.upper()
    keep = org.isin(COUNCIL_NAMES)
    log["organisation_names_kept"] = {k: int(v) for k, v in c.loc[keep, "Organisation Name"].value_counts().items()}
    log["organisation_names_dropped"] = {k: int(v) for k, v in c.loc[~keep, "Organisation Name"].value_counts().items()}
    log["rows_dropped_other_buyers"] = int((~keep).sum())
    c = c[keep].copy()
    dup = c["Notice Identifier"].duplicated()
    log["rows_dropped_duplicate_notice_id"] = int(dup.sum())
    c = c[~dup].copy()
    log["rows_for_council"] = int(len(c))
    warnings = []
    if log["rows_in_file"] == 1000:
        warnings.append("contracts.csv has exactly 1,000 rows: the Contracts Finder export cap may have truncated it")

    def dmy(s):
        s = s.strip()
        return pd.Timestamp(datetime.strptime(s, "%d/%m/%Y")) if s else pd.NaT
    for col, new in [("Contract start date", "contract_start"), ("Contract end date", "contract_end"), ("Awarded Date", "awarded_date")]:
        try:
            c[new] = c[col].map(dmy)
        except ValueError as e:
            stop(f"contracts.csv '{col}' failed %d/%m/%Y parse: {e}")
    try:
        # ISO 8601 with offset; '+01:00' and 'Z' both occur. Explicit format, normalised to UTC.
        c["published"] = c["Published Date"].map(
            lambda s: pd.Timestamp(datetime.strptime(s.strip(), "%Y-%m-%dT%H:%M:%S%z")).tz_convert("UTC").tz_localize(None) if s.strip() else pd.NaT)
    except ValueError as e:
        stop(f"contracts.csv 'Published Date' failed ISO parse: {e}")
    c["awarded_value"] = pd.to_numeric(c["Awarded Value"].str.replace(",", "").str.strip().replace("", "0"), errors="coerce")
    if c["awarded_value"].isna().any():
        stop("contracts.csv Awarded Value failed to parse")
    c["pub_year"] = c["published"].map(lambda t: t.year if pd.notna(t) else None)
    rows = []
    malformed = 0
    for _, r in c.iterrows():
        packed = r[SUPPLIER_COL].strip()
        if not packed:
            blocks = []
        else:
            blocks = packed.strip()
            if blocks.startswith("["):
                blocks = blocks[1:]
            if blocks.endswith("]"):
                blocks = blocks[:-1]
            blocks = blocks.split("][")
        n = len(blocks)
        for b in blocks:
            parts = b.split("|")
            if len(parts) < 4:
                malformed += 1
            name = parts[0].strip()
            ch = parts[3].strip() if len(parts) >= 4 and parts[2].strip().upper() == "COMPANIES_HOUSE" else ""
            rows.append({
                "notice_id": r["Notice Identifier"], "title": r["Title"], "ojeu_procedure_type": r["OJEU Procedure Type"].strip(),
                "awarded_value": float(r["awarded_value"]), "awarded_date": r["awarded_date"], "published": r["published"],
                "contract_start": r["contract_start"], "contract_end": r["contract_end"],
                "suppliers_on_notice": n, "supplier_original": name, "supplier_norm": normalise_supplier(name),
                "companies_house_no": ch,
            })
    n_df = pd.DataFrame(rows)
    if n_df.empty or len(c) < 20:
        log["contracts_present"] = False
        log["reason"] = f"fewer than 20 council notices after filtering ({len(c)})"
        return None, log
    n_df["ended_before_window"] = n_df["contract_end"].notna() & (n_df["contract_end"] < window_start)
    n_df["active_in_window"] = ~n_df["ended_before_window"]
    n_df["source"] = "contracts_finder"
    log["contracts_present"] = True
    log["notices"] = int(c["Notice Identifier"].nunique())
    log["notice_supplier_pairs"] = int(len(n_df))
    log["notices_without_supplier"] = int((c[SUPPLIER_COL].str.strip() == "").sum())
    log["malformed_supplier_blocks"] = malformed
    log["distinct_suppliers"] = int(n_df["supplier_norm"].nunique())
    log["pairs_with_companies_house_no"] = int((n_df["companies_house_no"] != "").sum())
    act = c["contract_end"].isna() | (c["contract_end"] >= window_start)
    log["active_in_window"] = int(act.sum())
    log["ended_before_window"] = int((~act).sum())
    log["active_pairs"] = int(n_df["active_in_window"].sum())
    log["ended_pairs"] = int(n_df["ended_before_window"].sum())
    log["zero_value_awards"] = int((c["awarded_value"] == 0).sum())
    log["max_suppliers_on_one_notice"] = int(n_df["suppliers_on_notice"].max())
    rpy = c["pub_year"].value_counts().sort_index()
    log["rows_per_year"] = {str(int(k)): int(v) for k, v in rpy.items()}
    log["published_range"] = [str(c["published"].min().date()), str(c["published"].max().date())]
    if len(rpy) > 2:
        med = float(rpy.median())
        cur_year = c["published"].max().year
        for y, v in rpy.items():
            # partial first/last years are expected to be thinner; flag full years under a third of the median
            if int(y) not in (rpy.index.min(), cur_year) and v < med / 3:
                warnings.append(f"publication year {int(y)} has {int(v)} notices, under a third of the median year: possible export gap")
    log["warnings"] = warnings
    return n_df, log


def main():
    rules_path = os.path.join(ROOT, "outputs", "rules.json")
    if not os.path.exists(rules_path):
        stop("outputs/rules.json missing")
    os.makedirs(OUT, exist_ok=True)
    d, file_log, uncat_rows, uncat_gbp = load_spend()
    rows_raw = int(len(d))
    d["exclusion"] = d.apply(classify_exclusion, axis=1)
    excl = d[d["exclusion"] != ""].copy()
    clean = d[d["exclusion"] == ""].copy()
    # how many inter_authority rows were caught only by the narrative clause (transparency)
    ia = excl[excl["exclusion"] == "inter_authority"]
    ia_narr_only = int((~ia["Supplier name"].str.upper().str.contains(RX["inter_authority_supplier"].replace("\\b(", "\\b(?:"), regex=True)).sum())
    clean["tag"] = clean.apply(tag_row, axis=1)
    cols = ["row_id", "source_file", "sheet_row", "Service", "Expenditure category", "Narrative", "Date_ts", "pay_date",
            "Net amount", "Supplier name", "supplier_original", "supplier_norm"]
    clean[cols + ["tag"]].to_csv(os.path.join(OUT, "spend-clean.csv"), index=False)
    excl[cols + ["exclusion"]].to_csv(os.path.join(OUT, "spend-excluded.csv"), index=False)

    window_start = d["pay_date"].min()
    window_end = d["pay_date"].max()
    notices, nlog = load_notices(window_start)
    if notices is not None:
        notices.to_csv(os.path.join(OUT, "notices-clean.csv"), index=False)
    elif os.path.exists(os.path.join(OUT, "notices-clean.csv")):
        os.remove(os.path.join(OUT, "notices-clean.csv"))

    register_path = os.path.join(DATA, "contract-register.csv")
    register_present = os.path.exists(register_path)
    if register_present:
        stop("data/contract-register.csv present: column mapping must be inspected and added before running (not guessed)")

    exc_summary = {}
    for k in ["redacted_supplier", "pension_statutory", "inter_authority"]:
        sub = excl[excl["exclusion"] == k]
        exc_summary[k] = {"rows": int(len(sub)), "gbp": round(float(sub["Net amount"].sum()), 2), "reason": EXCLUSION_REASONS[k]}
    exc_summary["inter_authority"]["rows_matched_by_narrative_only"] = ia_narr_only
    tags = {}
    for t in ["general_procurement", "care_or_education_placement", "grant", "agency_staff", "premises_non_procurement"]:
        sub = clean[clean["tag"] == t]
        tags[t] = {"rows": int(len(sub)), "gbp": round(float(sub["Net amount"].sum()), 2), "suppliers": int(sub["supplier_norm"].nunique())}
    months = int(d["pay_date"].dt.to_period("M").nunique())
    log = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "files": file_log,
        "rows_raw": rows_raw,
        "rows_after_exclusions": int(len(clean)),
        "gbp_raw": round(float(d["Net amount"].sum()), 2),
        "gbp_after_exclusions": round(float(clean["Net amount"].sum()), 2),
        "date_min": str(window_start.date()), "date_max": str(window_end.date()),
        "months_covered": months,
        "distinct_payment_timestamps": int(d["Date_ts"].nunique()),
        "uncategorised_expenditure_category": {"rows": uncat_rows, "gbp": round(uncat_gbp, 2),
                                                "note": "blank Expenditure category labelled 'Uncategorised'; kept"},
        "negative_amounts": 0,
        "excluded": exc_summary,
        "tags": tags,
        "tagging_order": ["care_or_education_placement", "grant", "agency_staff", "premises_non_procurement", "general_procurement"],
        "regexes": RX,
        "normalise_supplier": {"stop_tokens": sorted(STOP_TOKENS),
                               "steps": "upper; & -> AND; drop (...) and [...]; drop T/A or T/AS... and TRADING AS... suffix; keep A-Z0-9 space; drop stop tokens; collapse"},
        "contracts": nlog,
        "register_present": register_present,
    }
    with open(os.path.join(OUT, "cleaning-log.json"), "w") as fh:
        json.dump(log, fh, indent=2, default=str)
    print(f"clean.py: rows_raw={rows_raw} rows_after_exclusions={len(clean)} window={window_start.date()}..{window_end.date()} "
          f"months={months} contracts_present={nlog.get('contracts_present')} register_present={register_present}")


if __name__ == "__main__":
    main()
