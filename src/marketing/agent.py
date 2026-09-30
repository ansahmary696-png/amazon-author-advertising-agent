import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "author_agent.db"
JSON_PRODUCTS_PATH = BASE_DIR / "data" / "products.json"


def connect_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            price REAL,
            currency TEXT,
            channel TEXT,
            category TEXT,
            tagline TEXT,
            audience TEXT,
            cover TEXT,
            inventory INTEGER,
            rating REAL,
            goal TEXT,
            active INTEGER DEFAULT 1,
            source TEXT DEFAULT 'seed'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            channel TEXT,
            objective TEXT,
            keywords TEXT,
            creative TEXT,
            budget REAL,
            status TEXT DEFAULT 'draft'
        )
        """
    )
    conn.commit()
    conn.close()

    # seed data if empty
    if not list_products():
        seed_products()


def seed_products() -> None:
    if not JSON_PRODUCTS_PATH.exists():
        return
    with JSON_PRODUCTS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    conn = connect_db()
    for product in data.get("products", []):
        conn.execute(
            """
            INSERT OR REPLACE INTO products (
                id, name, type, price, currency, channel, category, tagline,
                audience, cover, inventory, rating, goal, active, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product["id"],
                product["name"],
                product["type"],
                float(product["price"]),
                product["currency"],
                product["channel"],
                product["category"],
                product["tagline"],
                product["audience"],
                product["cover"],
                int(product["inventory"]),
                float(product.get("rating", 0)),
                product["goal"],
                1,
                "seed",
            ),
        )
    conn.commit()
    conn.close()


def list_products() -> List[Dict[str, Any]]:
    conn = connect_db()
    rows = conn.execute("SELECT * FROM products WHERE active = 1 ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_product(product: Dict[str, Any]) -> Dict[str, Any]:
    conn = connect_db()
    conn.execute(
        """
        INSERT OR REPLACE INTO products (
            id, name, type, price, currency, channel, category, tagline,
            audience, cover, inventory, rating, goal, active, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product.get("id") or f"prod-{len(list_products()) + 1}",
            product.get("name"),
            product.get("type", "product"),
            float(product.get("price", 0)),
            product.get("currency", "USD"),
            product.get("channel", "Selar"),
            product.get("category", "general"),
            product.get("tagline", ""),
            product.get("audience", "general audience"),
            product.get("cover", ""),
            int(product.get("inventory", 0)),
            float(product.get("rating", 0)),
            product.get("goal", "conversion"),
            1,
            "manual",
        ),
    )
    conn.commit()
    conn.close()
    return product


def list_campaigns() -> List[Dict[str, Any]]:
    conn = connect_db()
    rows = conn.execute("SELECT * FROM campaigns ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_campaign(campaign: Dict[str, Any]) -> Dict[str, Any]:
    conn = connect_db()
    conn.execute(
        """
        INSERT INTO campaigns (name, channel, objective, keywords, creative, budget, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            campaign.get("name"),
            campaign.get("channel", "Amazon"),
            campaign.get("objective", "growth"),
            ", ".join(campaign.get("keywords", [])),
            campaign.get("creative", ""),
            float(campaign.get("budget", 0)),
            campaign.get("status", "draft"),
        ),
    )
    conn.commit()
    conn.close()
    return campaign
