import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "author_agent.db"
JSON_PRODUCTS_PATH = BASE_DIR / "data" / "products.json"

APP_TITLE = "Daniel Kwesi Ansah | Amazon + Selar Growth Engine"
AMAZON_PROFILE_URL = "https://amazon.com/author/danielkwesiansah"
SELAR_STORE_URL = "https://selar.com/m/danielkwesiansah"

SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "daniel")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "author123")

AMAZON_CLIENT_ID = os.getenv("AMAZON_CLIENT_ID", "")
AMAZON_CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET", "")
AMAZON_REFRESH_TOKEN = os.getenv("AMAZON_REFRESH_TOKEN", "")
AMAZON_PROFILE_ID = os.getenv("AMAZON_PROFILE_ID", "")
AMAZON_REGION = os.getenv("AMAZON_REGION", "us-east-1")

SELAR_API_URL = os.getenv("SELAR_API_URL", "")
SELAR_API_KEY = os.getenv("SELAR_API_KEY", "")
SELAR_WEBHOOK_SECRET = os.getenv("SELAR_WEBHOOK_SECRET", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")


def connect_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect_db()

    conn.execute("""
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
    """)

    conn.execute("""
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
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'admin'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            source TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    if not list_products():
        seed_products()

    if not get_user_by_username(ADMIN_USERNAME):
        create_user(ADMIN_USERNAME, ADMIN_PASSWORD, "admin")


def get_user_by_username(username: str) -> Dict[str, Any] | None:
    conn = connect_db()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(username: str, password: str, role: str = "admin") -> Dict[str, Any]:
    conn = connect_db()
    conn.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role),
    )
    conn.commit()
    conn.close()
    return {"username": username, "role": role}


def seed_products() -> None:
    if not JSON_PRODUCTS_PATH.exists():
        return

    with JSON_PRODUCTS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    conn = connect_db()
    for product in data.get("products", []):
        conn.execute("""
            INSERT OR REPLACE INTO products (
                id, name, type, price, currency, channel, category, tagline,
                audience, cover, inventory, rating, goal, active, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        ))
    conn.commit()
    conn.close()


def list_products() -> List[Dict[str, Any]]:
    conn = connect_db()
    rows = conn.execute("SELECT * FROM products WHERE active = 1 ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_product(product: Dict[str, Any]) -> Dict[str, Any]:
    conn = connect_db()
    conn.execute("""
        INSERT OR REPLACE INTO products (
            id, name, type, price, currency, channel, category, tagline,
            audience, cover, inventory, rating, goal, active, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product.get("id") or f"prod-{int(__import__('time').time())}",
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
    ))
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
    conn.execute("""
        INSERT INTO campaigns (name, channel, objective, keywords, creative, budget, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        campaign.get("name"),
        campaign.get("channel", "Amazon"),
        campaign.get("objective", "growth"),
        ", ".join(campaign.get("keywords", [])),
        campaign.get("creative", ""),
        float(campaign.get("budget", 0)),
        campaign.get("status", "draft"),
    ))
    conn.commit()
    conn.close()
    return campaign
