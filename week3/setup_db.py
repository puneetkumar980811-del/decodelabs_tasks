"""
Load the cleaned e-commerce dataset into a SQLite database.

Usage:
    python setup_db.py [input.xlsx] [output.db]

Default input : C:\\Users\\laptop\\Documents\\Downloads\\Dataset for Data Analytics - Cleaned.xlsx
Default output: sql_data_analysis/orders.db  (table: orders)
"""

import sys
import sqlite3
import pandas as pd
from pathlib import Path

INPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\laptop\Documents\Downloads\Dataset for Data Analytics - Cleaned.xlsx"
)
OUTPUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "orders.db"

df = pd.read_excel(INPUT, sheet_name=0)

# Normalize the Date column to ISO text (YYYY-MM-DD) so SQLite sorts it correctly.
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

conn = sqlite3.connect(OUTPUT)
df.to_sql("orders", conn, if_exists="replace", index=False)

with conn:
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_product ON orders(Product)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(OrderStatus)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(Date)"
    )

n = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
conn.close()

print(f"Loaded {n} rows x {df.shape[1]} columns -> {OUTPUT}")
