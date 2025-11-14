from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "ecom.db"
OUTPUT_PATH = ROOT_DIR / "output" / "order_summary.csv"


QUERY = """
SELECT
    u.name AS user_name,
    pr.name AS product_name,
    o.order_date,
    r.rating AS review_rating,
    pay.payment_status
FROM orders o
JOIN users u ON u.user_id = o.user_id
JOIN products pr ON pr.product_id = o.product_id
LEFT JOIN reviews r ON r.order_id = o.order_id
LEFT JOIN payments pay ON pay.order_id = o.order_id
ORDER BY o.order_date, o.order_id;
"""


def fetch_order_summary() -> list[tuple]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)
        rows = cursor.fetchall()
    return rows


def write_summary(rows: list[tuple]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    headers = ["user_name", "product_name", "order_date", "review_rating", "payment_status"]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    rows = fetch_order_summary()
    write_summary(rows)
    print(f"Wrote {len(rows)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

