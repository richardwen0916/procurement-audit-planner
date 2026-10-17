"""selfcheck.py - re-derive one flagged item per test from spend-clean.csv / notices-clean.csv
independently of analyse.py, and confirm one row_id against the source workbook."""
import json
import os

import openpyxl
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, "outputs", "analytics-full")
a = json.load(open(os.path.join(ROOT, "outputs", "analytics.json")))
d = pd.read_csv(os.path.join(FULL, "spend-clean.csv"), dtype={"row_id": str})
d["pay_date"] = pd.to_datetime(d["pay_date"], format="%Y-%m-%d")
n = pd.read_csv(os.path.join(FULL, "notices-clean.csv"), dtype={"notice_id": str})
n["contract_end"] = pd.to_datetime(n["contract_end"], format="%Y-%m-%d")
n["contract_start"] = pd.to_datetime(n["contract_start"], format="%Y-%m-%d")
T = a["tests"]
months = a["population"]["months_covered"]
ws_start = pd.Timestamp(a["population"]["date_min"])
results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def norm_of(supplier_display):
    return d.loc[d.supplier_original == supplier_display, "supplier_norm"].iloc[0]


# 1 threshold clustering: top row at 25000, and the band count re-derived
tc = T["threshold_clustering"]["by_threshold"]["25000"]
r0 = tc["top20"][0]
row = d[d.row_id == r0["row_id"]].iloc[0]
cnt = int(((d["Net amount"] >= 22500) & (d["Net amount"] < 25000)).sum())
check("threshold_clustering 25000", 22500 <= row["Net amount"] < 25000 and cnt == tc["below_band"]["count"],
      f"row_id {r0['row_id']} amount {row['Net amount']}; band count {cnt} vs json {tc['below_band']['count']}")
# the same row in the workbook itself
f, sr = r0["row_id"].rsplit(":", 1)
wb = openpyxl.load_workbook(os.path.join(ROOT, "data", "spend", f), read_only=True, data_only=True)
cell = [c for c in wb["Data to publish"].iter_rows(min_row=int(sr), max_row=int(sr), values_only=True)][0]
wb.close()
check("workbook row", abs(float(cell[4]) - row["Net amount"]) < 0.005 and str(cell[5]).strip() == row["Supplier name"],
      f"{f} sheet row {sr}: amount {cell[4]}, supplier matches")

# 2 split purchases: top general_procurement window at 25000
w = T["split_purchases"]["by_threshold"]["25000"]["top20_general_procurement"][0]
ids = w["row_ids"].split()
s = d[d.row_id.isin(ids)]
sn = s.supplier_norm.iloc[0]
win = d[(d.supplier_norm == sn) & (d.pay_date >= pd.Timestamp(w["window_start"])) &
        (d.pay_date <= pd.Timestamp(w["window_start"]) + pd.Timedelta(days=29)) & (d["Net amount"] < 25000)]
check("split_purchases 25000", set(win.row_id) == set(ids) and round(win["Net amount"].sum(), 2) == w["window_total"]
      and (s["Net amount"] < 25000).all(),
      f"window from {w['window_start']}, {len(win)} payments re-summed {round(win['Net amount'].sum(), 2)} vs json {w['window_total']}; row_ids {' '.join(ids[:4])}")

# 3 high value suppliers: top general_procurement supplier
h = T["high_value_suppliers"]["tiers"]["publication_threshold"]["top20_general_procurement"][0]
first_id = h["row_ids_first10"].split()[0]
sn = d.loc[d.row_id == first_id, "supplier_norm"].iloc[0]
tot = d.loc[d.supplier_norm == sn, "Net amount"].sum()
check("high_value_suppliers", round(tot * 12 / months, 2) == h["annualised_estimate"],
      f"supplier total {round(tot, 2)} x 12/{months} = {round(tot * 12 / months, 2)} vs json {h['annualised_estimate']}; first row_id {first_id}")

# 4 duplicates: top different_time group
g = T["duplicates"]["tiers"]["different_time"]["top20"][0]
ids = g["row_ids"].split()
sn = d.loc[d.row_id == ids[0], "supplier_norm"].iloc[0]
grp = d[(d.supplier_norm == sn) & (d["Net amount"] == g["amount"]) &
        (d.pay_date >= pd.Timestamp(g["first_date"])) & (d.pay_date <= pd.Timestamp(g["last_date"]))]
dts = sorted(grp.pay_date)
gaps_ok = all((b - a_).days <= 7 for a_, b in zip(dts, dts[1:]))
check("duplicates different_time", set(grp.row_id) == set(ids) and gaps_ok and grp.Date_ts.nunique() > 1,
      f"{len(grp)} rows of {g['amount']} between {g['first_date']} and {g['last_date']}; row_ids {' '.join(ids)}")

# 5 off_contract: top unmatched general_procurement supplier
o = T["off_contract"]["top20_unmatched_general_procurement"][0]
first_id = o["row_ids_first10"].split()[0]
sn = d.loc[d.row_id == first_id, "supplier_norm"].iloc[0]
tot = d.loc[d.supplier_norm == sn, "Net amount"].sum()
active = n[n.contract_end.isna() | (n.contract_end >= ws_start)]
check("off_contract", sn not in set(active.supplier_norm) and round(tot * 12 / months, 2) == o["annualised_estimate"],
      f"no exact active-notice name; annualised {round(tot * 12 / months, 2)} vs json {o['annualised_estimate']}; first row_id {first_id}")

# 6 expired notice spend: top supplier
e = T["expired_notice_spend"]["top20"][0]
first_id = e["row_ids_first10"].split()[0]
sn = d.loc[d.row_id == first_id, "supplier_norm"].iloc[0]
nn = n[n.supplier_norm == sn]
check("expired_notice_spend", len(nn) > 0 and (nn.contract_end < ws_start).all()
      and round(d.loc[d.supplier_norm == sn, "Net amount"].sum(), 2) == e["total_gbp"],
      f"notices {e['notice_ids']} all end <= {nn.contract_end.max().date()} < {ws_start.date()}; total re-summed matches; first row_id {first_id}")

# 7 spend vs award: top ratio
v = T["spend_vs_award"]["top20"][0]
first_id = v["row_ids_first10"].split()[0]
sn = d.loc[d.row_id == first_id, "supplier_norm"].iloc[0]
note = n[n.notice_id == v["notice_id"]].iloc[0]
yrs = (note.contract_end - note.contract_start).days / 365.25
ratio = d.loc[d.supplier_norm == sn, "Net amount"].sum() * 12 / months / (note.awarded_value / yrs)
check("spend_vs_award", round(ratio, 2) == v["ratio"] and note.supplier_norm == sn and note.suppliers_on_notice == 1,
      f"notice {v['notice_id']} ratio re-derived {round(ratio, 4)} vs json {round(v['ratio'], 4)}; first row_id {first_id}")

print(f"selfcheck: {sum(results)}/{len(results)} passed")
