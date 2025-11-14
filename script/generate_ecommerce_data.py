from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path
import random


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(filename: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    file_path = DATA_DIR / filename
    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_users() -> list[dict[str, object]]:
    base_date = datetime(2024, 1, 1)
    names = [
        "Ava Patel",
        "Noah Smith",
        "Liam Chen",
        "Emma Lopez",
        "Mia Davis",
        "Elijah Lee",
        "Isabella Brown",
        "Sophia Wilson",
        "James Garcia",
        "Lucas Nguyen",
        "Amelia Clark",
        "Harper Miller",
        "Ethan Hernandez",
        "Oliver Johnson",
        "Charlotte Martinez",
    ]
    tiers = ["Bronze", "Silver", "Gold"]
    users = []
    for idx in range(15):
        name = names[idx]
        user_id = f"U{idx+1:03d}"
        email = name.lower().replace(" ", ".") + "@shopperhub.com"
        join_date = (base_date + timedelta(days=idx * 3)).date().isoformat()
        tier = tiers[idx % len(tiers)]
        users.append(
            {
                "user_id": user_id,
                "name": name,
                "email": email,
                "join_date": join_date,
                "loyalty_tier": tier,
            }
        )
    return users


def generate_products() -> list[dict[str, object]]:
    categories = [
        ("Smartwatch", "Wearables", 149.99),
        ("Noise Cancelling Headphones", "Audio", 199.5),
        ("4K Monitor", "Displays", 329.0),
        ("Mechanical Keyboard", "Peripherals", 119.0),
        ("Gaming Mouse", "Peripherals", 59.0),
        ("Wireless Charger", "Accessories", 39.99),
        ("Portable SSD", "Storage", 109.5),
        ("Bluetooth Speaker", "Audio", 89.0),
        ("Fitness Tracker", "Wearables", 99.0),
        ("Smart Home Hub", "Smart Home", 129.0),
        ("Action Camera", "Cameras", 249.0),
        ("Drone Mini", "Cameras", 399.0),
        ("E-reader", "Tablets", 139.0),
        ("USB-C Hub", "Accessories", 49.5),
        ("Noise Sensor", "Smart Home", 79.0),
    ]
    products = []
    for idx, (name, category, price) in enumerate(categories, start=1):
        products.append(
            {
                "product_id": f"P{idx:03d}",
                "name": name,
                "category": category,
                "price": f"{price:.2f}",
                "in_stock": 50 + idx * 3,
            }
        )
    return products


def generate_orders(users: list[dict[str, object]], products: list[dict[str, object]]):
    rng = random.Random(42)
    base_date = datetime(2024, 2, 1)
    statuses = ["Processing", "Shipped", "Delivered"]
    price_lookup = {p["product_id"]: float(p["price"]) for p in products}
    orders = []
    for idx in range(15):
        user = users[idx]
        product = products[idx]
        quantity = rng.randint(1, 4)
        order_date = (base_date + timedelta(days=idx)).date().isoformat()
        status = statuses[idx % len(statuses)]
        orders.append(
            {
                "order_id": f"O{idx+1:03d}",
                "user_id": user["user_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "order_date": order_date,
                "status": status,
                "order_total": f"{quantity * price_lookup[product['product_id']]:.2f}",
            }
        )
    return orders


def generate_reviews(orders: list[dict[str, object]]):
    rng = random.Random(7)
    comments = [
        "Great value for the price.",
        "Fast shipping and solid quality.",
        "Met my expectations.",
        "Would definitely recommend.",
        "Packaging could be better, product works fine.",
    ]
    base_date = datetime(2024, 3, 1)
    reviews = []
    for idx, order in enumerate(orders):
        reviews.append(
            {
                "review_id": f"R{idx+1:03d}",
                "order_id": order["order_id"],
                "rating": rng.randint(3, 5),
                "comment": comments[idx % len(comments)],
                "review_date": (base_date + timedelta(days=idx)).date().isoformat(),
            }
        )
    return reviews


def generate_payments(orders: list[dict[str, object]]):
    methods = ["Credit Card", "PayPal", "Gift Card"]
    statuses = ["Completed", "Completed", "Pending"]
    payments = []
    for idx, order in enumerate(orders):
        payments.append(
            {
                "payment_id": f"PM{idx+1:03d}",
                "order_id": order["order_id"],
                "amount": order["order_total"],
                "method": methods[idx % len(methods)],
                "payment_status": statuses[idx % len(statuses)],
            }
        )
    return payments


def main():
    users = generate_users()
    products = generate_products()
    orders = generate_orders(users, products)
    reviews = generate_reviews(orders)
    payments = generate_payments(orders)

    write_csv(
        "users.csv",
        ["user_id", "name", "email", "join_date", "loyalty_tier"],
        users,
    )
    write_csv(
        "products.csv",
        ["product_id", "name", "category", "price", "in_stock"],
        products,
    )
    write_csv(
        "orders.csv",
        [
            "order_id",
            "user_id",
            "product_id",
            "quantity",
            "order_date",
            "status",
            "order_total",
        ],
        orders,
    )
    write_csv(
        "reviews.csv",
        ["review_id", "order_id", "rating", "comment", "review_date"],
        reviews,
    )
    write_csv(
        "payments.csv",
        ["payment_id", "order_id", "amount", "method", "payment_status"],
        payments,
    )
    print(f"Generated CSV files in {DATA_DIR}")


if __name__ == "__main__":
    main()

