"""
Data Analysis Pipeline — Cleaned e-commerce dataset
====================================================
Computes:
  1. Basic statistics (count / mean / median / std / min / max / quartiles)
  2. Trends over time (monthly orders & revenue, monthly avg basket)
  3. Outlier detection (IQR method on numeric columns)
  4. Distributions (products, payment methods, statuses, referral sources)
  5. Charts (PNG) + a Markdown summary report

Usage:
  python analyze_dataset.py [input.xlsx] [output_folder]
"""

import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Console-safe UTF-8 output (avoids cp1252 crashes / mojibake on Windows)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:  # very old Python without reconfigure
    pass

# ---------------------------------------------------------------- paths
INPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\laptop\Documents\Downloads\Dataset for Data Analytics - Cleaned.xlsx"
)
OUT_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else INPUT.parent / "analysis_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(INPUT, sheet_name=0)
N_COLS_ORIG = df.shape[1]
df["Date"] = pd.to_datetime(df["Date"])
df["YearMonth"] = df["Date"].dt.to_period("M")

sns.set_theme(style="whitegrid", palette="muted")
report = []
def log(msg=""):
    print(msg)
    report.append(msg)


def iqr_outliers(series):
    """Return (mask, lower_bound, upper_bound) for IQR-based outliers."""
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return (series < lo) | (series > hi), lo, hi

NUMERIC = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]
CATEGORICAL = ["Product", "PaymentMethod", "OrderStatus", "ReferralSource", "CouponCode"]

log("# Data Analysis Report")
log(f"\n**Dataset:** {INPUT.name} — {df.shape[0]} orders, {N_COLS_ORIG} columns")
log(f"**Period:** {df['Date'].min().date()} → {df['Date'].max().date()}")

# ===================================================== 1. basic statistics
log("\n## 1. Basic Statistics")
log("\n| Column | Count | Mean | Median | Std Dev | Min | Max |")
log("|---|---|---|---|---|---|---|")
for c in NUMERIC:
    s = df[c]
    log(f"| {c} | {s.count()} | {s.mean():,.2f} | {s.median():,.2f} | "
        f"{s.std():,.2f} | {s.min():,.2f} | {s.max():,.2f} |")

log("\n**Categorical counts (top 3 per column):**")
for c in CATEGORICAL:
    top = df[c].value_counts().head(3)
    log(f"- **{c}:** " + ", ".join(f"{k} ({v})" for k, v in top.items()))

# ===================================================== 2. trends
log("\n## 2. Trends Over Time")
monthly = (df.groupby("YearMonth")
             .agg(orders=("OrderID", "count"),
                  revenue=("TotalPrice", "sum"),
                  avg_basket=("TotalPrice", "mean"))
             .reset_index())
monthly["YearMonth"] = monthly["YearMonth"].astype(str)
log("\n**Monthly orders & revenue:**")
log("| Month | Orders | Revenue | Avg Basket |")
log("|---|---|---|---|")
for _, r in monthly.iterrows():
    log(f"| {r['YearMonth']} | {r['orders']} | ${r['revenue']:,.0f} | ${r['avg_basket']:,.2f} |")

# YoY comparison (2023 vs 2024, note 2025 is partial: Jan-Jun)
yearly = (df.groupby(df["Date"].dt.year)
            .agg(orders=("OrderID", "count"),
                 revenue=("TotalPrice", "sum"))
            .reset_index().rename(columns={"Date": "Year"}))
log("\n**Yearly summary (2025 is partial — Jan to Jun only):**")
for _, r in yearly.iterrows():
    log(f"- {int(r['Year'])}: {r['orders']} orders, ${r['revenue']:,.0f} revenue")

# Seasonality: month-of-year average orders — computed on FULL years only
# (2023 & 2024) so the partial 2025 data does not skew months Jan-Jun.
full_years = df[df["Date"].dt.year.isin([2023, 2024])]
# Normalize by days per month -> average orders per day, so months with
# fewer days (Feb) are not under-counted.
days_per_month = pd.Series({1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31})
orders_per_month = full_years.groupby(full_years["Date"].dt.month)["OrderID"].count()
season = orders_per_month / days_per_month
season = season / season.max() * 100
log("\n**Seasonal index (avg orders/day vs peak month; full years 2023-2024 only):**")
for m in range(1, 13):
    if m in season.index:
        log(f"- Month {m:02d}: {season[m]:.0f}%")

# ===================================================== 3. outliers (IQR)
log("\n## 3. Outlier Detection (IQR method)")
outlier_by_col = {}
for c in NUMERIC:
    mask, lo, hi = iqr_outliers(df[c])
    n = int(mask.sum())
    flag = "!" if n else "ok"
    log(f"- **{c}:** {flag} {n} outliers (bounds [{lo:.2f}, {hi:.2f}])")
    if n:
        outlier_by_col[c] = df.loc[mask, "OrderID"].astype(str).tolist()
if outlier_by_col:
    log("\n**Outlier order IDs:**")
    for c, ids in outlier_by_col.items():
        shown = ", ".join(ids[:15])
        log(f"- {c}: {shown}{' ...' if len(ids) > 15 else ''}")
    log("\n_Note: flagged outliers may be legitimate high-value orders rather than"
        " data errors — see Key Observations._")

# ===================================================== 4. distributions
log("\n## 4. Distributions")
log("\n**Order status:**")
for k, v in df["OrderStatus"].value_counts().items():
    log(f"- {k}: {v} ({v/len(df)*100:.1f}%)")
log("\n**Payment method:**")
for k, v in df["PaymentMethod"].value_counts().items():
    log(f"- {k}: {v} ({v/len(df)*100:.1f}%)")
log("\n**Product mix (% of orders):**")
for k, v in df["Product"].value_counts().items():
    log(f"- {k}: {v/len(df)*100:.1f}%")
log("\n**Referral source:**")
for k, v in df["ReferralSource"].value_counts().items():
    log(f"- {k}: {v} ({v/len(df)*100:.1f}%)")

# Top products by revenue
prod_rev = df.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False)
log("\n**Revenue by product:**")
for k, v in prod_rev.items():
    log(f"- {k}: ${v:,.0f} ({v/prod_rev.sum()*100:.1f}% of revenue)")

# Coupon usage effect (all orders retained a coupon after cleaning, so we
# compare FREESHIP vs SAVE10 vs WINTER15 baskets instead)
log("\n**Coupon impact on average basket:**")
avg_by_coupon = df.groupby("CouponCode")["TotalPrice"].agg(["mean", "count"])
for code, row in avg_by_coupon.iterrows():
    log(f"- {code}: ${row['mean']:,.2f} avg basket (n={int(row['count'])})")

# ===================================================== 5. charts
log("\n## Charts Generated")
def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    log(f"- `{name}` saved")

# 5a. Monthly revenue + orders trend
fig, ax1 = plt.subplots(figsize=(11, 5))
x = monthly["YearMonth"]
ax1.bar(x, monthly["revenue"], color="#4C72B0", alpha=0.85, label="Revenue")
ax1.set_ylabel("Revenue ($)", color="#4C72B0")
ax1.tick_params(axis="x", rotation=60)
ax2 = ax1.twinx()
ax2.plot(x, monthly["orders"], color="#C44E52", marker="o", label="Orders")
ax2.set_ylabel("Orders", color="#C44E52")
ax1.set_title("Monthly Revenue and Order Volume")
fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.92))
save(fig, "1_monthly_trend.png")

# 5b. Revenue by product
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.barplot(x=prod_rev.index, y=prod_rev.values, hue=prod_rev.index,
            ax=ax, palette="viridis", legend=False)
ax.set_title("Revenue by Product")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis="x", rotation=30)
save(fig, "2_revenue_by_product.png")

# 5c. Price distributions by product
fig, ax = plt.subplots(figsize=(10, 4.5))
sns.boxplot(data=df, x="Product", y="UnitPrice", ax=ax)
ax.set_title("Unit Price Distribution by Product")
ax.tick_params(axis="x", rotation=30)
save(fig, "3_price_distribution.png")

# 5d. Order status pie
fig, ax = plt.subplots(figsize=(6.5, 6.5))
df["OrderStatus"].value_counts().plot.pie(
    ax=ax, autopct="%1.1f%%", startangle=90,
    colors=sns.color_palette("Set2"), textprops={"fontsize": 10})
ax.set_ylabel("")
ax.set_title("Order Status Breakdown")
save(fig, "4_order_status.png")

# 5e. Quantity distribution
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["Quantity"], discrete=True, ax=ax, color="#55A868")
ax.set_title("Order Quantity Distribution")
save(fig, "5_quantity_distribution.png")

# 5f. Avg basket trend
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(x, monthly["avg_basket"], color="#8172B2", marker="s")
ax.set_title("Average Basket Size Over Time")
ax.tick_params(axis="x", rotation=60)
ax.set_ylabel("Avg Basket ($)")
save(fig, "6_avg_basket_trend.png")

# ===================================================== 6. key observations
log("\n## 5. Key Observations")
observations = []
total_rev = df["TotalPrice"].sum()
avg_basket = df["TotalPrice"].mean()
top_month = monthly.loc[monthly["revenue"].idxmax()]
best_product = prod_rev.idxmax()
status_share = df["OrderStatus"].value_counts(normalize=True)
if "Cancelled" in status_share.index and status_share["Cancelled"] > 0.1:
    observations.append(f"⚠️ **Cancellation risk:** "
                        f"{status_share['Cancelled']*100:.1f}% of orders are cancelled "
                        f"— worth investigating (payment failures? stock issues?).")
observations.append(f"📈 **Revenue trend:** strongest month was {top_month['YearMonth']} "
                    f"(${top_month['revenue']:,.0f}); "
                    f"average basket is ${avg_basket:,.2f}.")
observations.append(f"🏆 **Best product:** {best_product} generates the most revenue "
                    f"({prod_rev[best_product]/total_rev*100:.1f}% of total).")
high_returns = status_share.get("Returned", 0)
observations.append(f"↩️ **Returns:** {high_returns*100:.1f}% of orders are returned.")
if outlier_by_col.get("TotalPrice"):
    observations.append(
        f"💰 **High-value orders:** {len(outlier_by_col['TotalPrice'])} orders exceed "
        f"the IQR upper bound (${max(df['TotalPrice']):,.2f} max) — these are large"
        f" baskets, not data errors (max possible = $699.93 x 5 units).")
for o in observations:
    log(f"- {o}")

# ---------------------------------------------------------------- save report
md_path = OUT_DIR / "analysis_report.md"
md_path.write_text("\n".join(report), encoding="utf-8")
print(f"\nReport saved: {md_path}")
print(f"Charts saved: {OUT_DIR}")
