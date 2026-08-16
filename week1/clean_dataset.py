"""
Data Cleaning Pipeline — Dataset for Data Analytics.xlsx
=========================================================
Cleans an e-commerce orders dataset by:
  1. Handling missing values (drops rows missing CouponCode — user choice)
  2. Removing duplicate rows
  3. Correcting data formats (prices → 2 decimals, dates → datetime,
     text → stripped & consistently cased, IDs → validated)

Outputs:
  - 'Dataset for Data Analytics - Cleaned.xlsx'   (cleaned data)
  - 'Data Quality Report - Before & After.txt'    (audit summary)

Usage:
  python clean_dataset.py [input.xlsx] [output.xlsx]
"""

import sys
import pandas as pd
from pathlib import Path

INPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\laptop\Documents\Downloads\Dataset for Data Analytics.xlsx"
)
OUTPUT = Path(sys.argv[2]) if len(sys.argv) > 2 else INPUT.with_name(
    "Dataset for Data Analytics - Cleaned.xlsx"
)
REPORT = OUTPUT.with_name("Data Quality Report - Before & After.txt")

# ---------------------------------------------------------------- helpers
def round2(s):
    """Round floats to 2 decimal places."""
    return s.round(2).where(s != 0, 0.0)  # also normalizes any -0.0 to 0.0

# ---------------------------------------------------------------- load raw
raw = pd.read_excel(INPUT, sheet_name=0)
report_lines = []
def log(msg=""):
    print(msg)
    report_lines.append(msg)

log("=" * 70)
log("DATA CLEANING REPORT")
log(f"Source file : {INPUT.name}")
log(f"Input shape : {raw.shape[0]} rows x {raw.shape[1]} columns")
log("=" * 70)

# ------------------------------------------------------- 1. missing values
log("\n[1] MISSING VALUES (before)")
log("-" * 40)
missing = raw.isna().sum()
missing = missing[missing > 0]
for col, n in missing.items():
    log(f"    {col:<18} {n:>5} missing  ({n/len(raw)*100:.2f}%)")

# Drop rows with missing values in ANY column (user chose to drop the
# 309 rows without a coupon code; other columns were complete).
dropped_missing = raw[raw.isna().any(axis=1)]
df = raw.dropna().copy()
log(f"    Rows dropped due to missing values : {len(dropped_missing)}")
log(f"    (reason column(s): {list(dropped_missing.columns[dropped_missing.isna().any()])})")

# ------------------------------------------------------- 2. duplicates
log("\n[2] DUPLICATES")
log("-" * 40)
full_dups = raw.duplicated().sum()
id_dups = raw.duplicated(subset=["OrderID"]).sum()
log(f"    Exact duplicate rows found  : {full_dups}")
log(f"    Duplicate OrderIDs found    : {id_dups}")
# NOTE: actual de-duplication happens AFTER format normalization (step 3),
# so rows that become identical once text is cleaned are also removed.

# ------------------------------------------------------- 3. data formats
log("\n[3] FORMAT CORRECTIONS")
log("-" * 40)

# 3a. Dates -> datetime, normalized to YYYY-MM-DD
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.normalize()
log(f"    Date            : converted to datetime (YYYY-MM-DD), range "
    f"{df['Date'].min().date()} -> {df['Date'].max().date()}")

# 3b. Prices -> 2 decimal places (fixes floating-point noise like 2853.1000000000004)
n_unprice = (df["UnitPrice"].astype(float) != df["UnitPrice"].astype(float).round(2)).sum()
n_total = (df["TotalPrice"].astype(float) != df["TotalPrice"].astype(float).round(2)).sum()
df["UnitPrice"] = round2(df["UnitPrice"].astype(float))
df["TotalPrice"] = round2(df["TotalPrice"].astype(float))
log(f"    UnitPrice       : rounded to 2 decimals ({n_unprice} values corrected)")
log(f"    TotalPrice      : rounded to 2 decimals ({n_total} values corrected)")

# 3c. Whole-number columns -> int
df["Quantity"] = df["Quantity"].astype(int)
df["ItemsInCart"] = df["ItemsInCart"].astype(int)

# 3d. Text columns -> strip whitespace, fix casing, collapse inner spaces
text_cols = ["OrderID", "CustomerID", "Product", "ShippingAddress",
             "PaymentMethod", "OrderStatus", "TrackingNumber",
             "CouponCode", "ReferralSource"]
for c in text_cols:
    df[c] = df[c].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
# Product names -> Title Case ("laptop" -> "Laptop"); keep the rest as-is
df["Product"] = df["Product"].str.title()
log(f"    Text columns    : whitespace stripped, inner spaces collapsed, "
    f"Product title-cased")

# 3e. Deduplicate AFTER normalization (catches whitespace/case variants)
before_dedup = len(df)
df = (df.drop_duplicates()
        .drop_duplicates(subset=["OrderID"])
        .reset_index(drop=True))
log(f"    Duplicates removed        : {before_dedup - len(df)}"
    f" (exact + duplicate OrderIDs, after normalization)")

# 3f. Consistency check: TotalPrice == Quantity * UnitPrice
calc = (df["Quantity"] * df["UnitPrice"]).round(2)
mismatch = (df["TotalPrice"] - calc).abs() > 0.005
if mismatch.any():
    df.loc[mismatch, "TotalPrice"] = calc[mismatch]
    log(f"    TotalPrice      : {mismatch.sum()} rows re-computed from Quantity x UnitPrice")
else:
    log(f"    TotalPrice      : consistent with Quantity x UnitPrice (0 mismatches)")

# 3g. Drop any rows that became invalid after coercion (e.g. bad dates)
invalid = df["Date"].isna()
if invalid.any():
    df = df[~invalid].reset_index(drop=True)
    log(f"    Invalid dates   : {invalid.sum()} rows removed")

# 3h. Validate ID formats (OrderID / CustomerID / TrackingNumber)
import re
id_checks = {"OrderID": r"^ORD\d{6}$", "CustomerID": r"^C\d{5}$",
             "TrackingNumber": r"^TRK\d{8}$"}
for col, pat in id_checks.items():
    bad = ~df[col].astype(str).str.match(pat)
    if bad.any():
        log(f"    {col:<14} : {bad.sum()} malformed values -> removed")
        df = df[~bad].reset_index(drop=True)
    else:
        log(f"    {col:<14} : all {len(df)} values match expected format")

# ------------------------------------------------------- 4. final validation
log("\n[4] FINAL VALIDATION")
log("-" * 40)
log(f"    Output shape        : {df.shape[0]} rows x {df.shape[1]} columns")
log(f"    Missing values left : {int(df.isna().sum().sum())}")
log(f"    Duplicates left     : {int(df.duplicated().sum())}")
log(f"    Duplicate OrderIDs  : {int(df.duplicated(subset=['OrderID']).sum())}")
log(f"    Rows removed total  : {len(raw) - len(df)} "
    f"({(len(raw) - len(df)) / len(raw) * 100:.1f}%)")

# ------------------------------------------------------- 5. save outputs
df.to_excel(OUTPUT, index=False, sheet_name="CleanData")
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

log("\n" + "=" * 70)
log(f"SAVED: {OUTPUT}")
log(f"REPORT: {REPORT}")
log("=" * 70)
