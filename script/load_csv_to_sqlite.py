from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = ROOT_DIR / "ecom.db"

TABLE_CONFIG = [
    {
        "name": "users",
        "csv": "users.csv",
        "columns": ["user_id", "name", "email", "join_date", "loyalty_tier"],
        "schema": """
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                join_date TEXT NOT NULL,
                loyalty_tier TEXT NOT NULL
            )
        """,
    },
    {
        "name": "products",
        "csv": "products.csv",
        "columns": ["product_id", "name", "category", "price", "in_stock"],
        "schema": """
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                in_stock INTEGER NOT NULL
            )
        """,
    },
    {
        "name": "orders",
        "csv": "orders.csv",
        "columns": [
            "order_id",
            "user_id",
            "product_id",
            "quantity",
            "order_date",
            "status",
            "order_total",
        ],
        "schema": """
            CREATE TABLE orders (
                order_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL,
                order_total REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """,
    },
    {
        "name": "reviews",
        "csv": "reviews.csv",
        "columns": ["review_id", "order_id", "rating", "comment", "review_date"],
        "schema": """
            CREATE TABLE reviews (
                review_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL,
                review_date TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """,
    },
    {
        "name": "payments",
        "csv": "payments.csv",
        "columns": ["payment_id", "order_id", "amount", "method", "payment_status"],
        "schema": """
            CREATE TABLE payments (
                payment_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                amount REAL NOT NULL,
                method TEXT NOT NULL,
                payment_status TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """,
    },
]

FIELD_CONVERTERS = {
    "price": float,
    "in_stock": int,
    "quantity": int,
    "order_total": float,
    "rating": int,
    "amount": float,
}


def load_csv(filename: str) -> list[dict[str, object]]:
    file_path = DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {file_path}")
    with file_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            processed = {}
            for key, value in row.items():
                converter = FIELD_CONVERTERS.get(key)
                processed[key] = converter(value) if converter else value
            rows.append(processed)
        return rows


def reset_tables(conn: sqlite3.Connection):
    conn.execute("PRAGMA foreign_keys = OFF;")
    cursor = conn.cursor()
    for table_name in reversed([cfg["name"] for cfg in TABLE_CONFIG]):
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor.executescript(";\n".join(cfg["schema"].strip() for cfg in TABLE_CONFIG))
    conn.commit()


def insert_rows(conn: sqlite3.Connection, table: str, columns: list[str], rows: list[dict[str, object]]):
    placeholders = ", ".join(["?"] * len(columns))
    column_list = ", ".join(columns)
    sql = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"
    data = [[row[col] for col in columns] for row in rows]
    conn.executemany(sql, data)
    conn.commit()


def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    with sqlite3.connect(DB_PATH) as conn:
        reset_tables(conn)

        for config in TABLE_CONFIG:
            rows = load_csv(config["csv"])
            insert_rows(conn, config["name"], config["columns"], rows)
            print(f"Inserted {len(rows)} rows into {config['name']}.")

    print(f"SQLite database populated at {DB_PATH}")


if __name__ == "__main__":
    main()

