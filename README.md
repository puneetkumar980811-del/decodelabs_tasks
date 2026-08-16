# Decode Labs — Data Analytics Tasks

A 3-week data analytics project built around a single e-commerce orders dataset
(`Dataset for Data Analytics.xlsx`). Each week adds a new skill: cleaning the
data, analyzing it with Python, and querying it with SQL.

**Dataset:** 891 orders, 14 columns (Date, OrderID, CustomerID, Product,
Quantity, UnitPrice, TotalPrice, ItemsInCart, ShippingAddress, PaymentMethod,
OrderStatus, TrackingNumber, CouponCode, ReferralSource)
**Period:** 2023-01-01 → 2025-06-30

## Project Structure

```
.
├── week1/   Data cleaning (pandas)
├── week2/   Data analysis & visualization (pandas, matplotlib, seaborn)
└── week3/   SQL analysis (SQLite)
```

## Week 1 — Data Cleaning (`week1/`)

Cleans the raw dataset into a consistent, analysis-ready form.

| File | Purpose |
|---|---|
| `clean_dataset.py` | Cleaning pipeline (see below) |
| `Dataset for Data Analytics.xlsx` | Raw input dataset |
| `Dataset for Data Analytics - Cleaned.xlsx` | Cleaned output |

**What `clean_dataset.py` does:**
1. **Missing values** — drops rows with missing data (e.g. rows without a coupon code)
2. **Duplicates** — removes exact duplicate rows and duplicate OrderIDs
3. **Format corrections**
   - Dates converted to datetime (`YYYY-MM-DD`)
   - Prices rounded to 2 decimals
   - Text stripped/normalized, product names title-cased
   - `TotalPrice` recomputed as `Quantity × UnitPrice` where inconsistent
   - OrderID / CustomerID / TrackingNumber validated against expected formats
4. **Final validation** — reports remaining missing values, duplicates, and total rows removed

**Run it:**
```bash
python clean_dataset.py "Dataset for Data Analytics.xlsx" "Dataset for Data Analytics - Cleaned.xlsx"
```

## Week 2 — Data Analysis (`week2/`)

Analyzes the cleaned dataset and produces charts plus a Markdown report.

| File | Purpose |
|---|---|
| `analyze_dataset.py` | Analysis pipeline (see below) |
| `analysis_output/` | 6 charts (PNG) + `analysis_report.md` |

**What `analyze_dataset.py` does:**
1. **Basic statistics** — count / mean / median / std / min / max for numeric columns
2. **Trends over time** — monthly orders & revenue, average basket, yearly summary, seasonal index
3. **Outlier detection** — IQR method on numeric columns
4. **Distributions** — order status, payment method, product mix, referral source, coupon impact
5. **Charts** — monthly trend, revenue by product, price distribution, order status, quantity distribution, avg basket trend
6. **Key observations** — automatic insights (cancellation rate, top product, high-value orders)

**Run it:**
```bash
python analyze_dataset.py "Dataset for Data Analytics - Cleaned.xlsx" analysis_output
```

### Highlights from the analysis
- 💰 Total revenue: **$942,361** across 891 orders (avg basket **$1,057.64**)
- 🏆 Best product: **Printer** — 16.4% of total revenue
- ⚠️ 21.5% of orders are cancelled, 19.2% returned
- 📈 Strongest month: 2023-10 ($49,379 revenue)

## Week 3 — SQL Analysis (`week3/`)

Loads the cleaned dataset into SQLite and answers business questions with SQL.

| File | Purpose |
|---|---|
| `setup_db.py` | Loads the cleaned Excel file into SQLite (`orders.db`, table `orders`) |
| `queries.sql` | 14 queries — SELECT, WHERE, GROUP BY, HAVING, ORDER BY, aggregates |
| `run_queries.py` | Executes the queries against the database |
| `query_results.md` | Results of all 14 queries |
| `orders.db` | SQLite database (891 rows) |

**What the queries demonstrate:**
- Basic `SELECT` + `LIMIT` (Q1)
- Filtering with `WHERE` and `IN` (Q2, Q3, Q10)
- Sorting with `ORDER BY` (Q4)
- Aggregation with `GROUP BY` — `COUNT`, `SUM`, `AVG` (Q5–Q7, Q12)
- `HAVING` to filter grouped results (Q8)
- Date extraction with `strftime` (Q9)
- Coupon performance and cancellation analysis (Q11, Q13, Q14)

**Run it:**
```bash
python setup_db.py "Dataset for Data Analytics - Cleaned.xlsx" orders.db
python run_queries.py
```

### Sample findings
- Credit Card orders have the highest average basket ($1,162.50)
- Instagram is the top referral source (198 orders, $212,628 revenue)
- Laptop has the most cancelled orders (30 of 127)
