"""
Run every SQL query in queries.sql against orders.db and save the results.

Usage:
    python run_queries.py [db_path]

Outputs:
    - query_results.md   (formatted results for every query)
    - console output     (same content)
"""

import sys
import re
import sqlite3
from pathlib import Path

DB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "orders.db"
QUERIES = Path(__file__).parent / "queries.sql"
OUT = Path(__file__).parent / "query_results.md"

text = QUERIES.read_text(encoding="utf-8").replace("\r\n", "\n")

# Each query section looks like:
#   -- --------------------------------------------------------------------
#   -- Q<n>. Title
#   -- --------------------------------------------------------------------
#   SELECT ...
# The regex captures the title line and the SQL body that follows it, up to
# the next query's separator block (or the end of the file).
QUERY_RE = re.compile(
    r"--\s*(Q\d+\.[^\n]*(?:\n--[^\n]*)*)\n--\s*-+\n(.*?)(?=\n--\s*-+\n--\s*Q\d+|\Z)",
    re.DOTALL,
)

conn = sqlite3.connect(DB)
out = []
out.append("# SQL Query Results")
out.append("")
out.append(f"**Database:** {DB.name}  |  **Queries:** `{QUERIES.name}`")
out.append("")

matches = list(QUERY_RE.finditer(text))
for m in matches:
    title = re.sub(r"\n--\s*", " ", m.group(1).strip())
    body = "\n".join(
        line for line in m.group(2).splitlines()
        if not line.strip().startswith("--")
    ).strip().rstrip(";")

    out.append(f"## {title}")
    out.append("")
    try:
        cur = conn.execute(body)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
    except Exception as e:
        out.append(f"**ERROR:** {e}")
        out.append("")
        print(f"!! {title} -> ERROR: {e}")
        continue

    if not rows:
        out.append("_(no rows returned)_")
        out.append("")
        print(f"- {title} (0 rows)")
        continue

    out.append("| " + " | ".join(cols) + " |")
    out.append("|" + "|".join(["---"] * len(cols)) + "|")
    def fmt(v):
        if isinstance(v, float):
            return f"{v:,.2f}"
        return str(v)

    for r in rows:
        out.append("| " + " | ".join(fmt(v) for v in r) + " |")
    out.append("")
    print(f"- {title} ({len(rows)} rows)")

conn.close()

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"\nResults saved: {OUT}")
