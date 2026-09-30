import json
from pathlib import Path
from typing import Any, Dict, List

from src.config import BASE_DIR, JSON_PRODUCTS_PATH


class MarketingAgent:
    def __init__(self, product_source: str | None = None):
        self.product_source = product_source or str(JSON_PRODUCTS_PATH)

    def load_catalog(self) -> List[Dict[str, Any]]:
        try:
            with open(self.product_source, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data.get("products", [])
        except FileNotFoundError:
            return []

    def generate_campaigns(self) -> List[Dict[str, Any]]:
        products = self.load_catalog()
        campaigns = []
        for product in products:
            campaigns.append(
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "channel": product["channel"],
                    "goal": product["goal"],
                    "ad_headline": self.make_headline(product),
                    "ad_copy": self.make_ad_copy(product),
                    "cta": self.make_cta(product),
                    "budget_recommendation": self.budget_for(product),
                    "target_audience": product["audience"],
                }
            )
        return campaigns

    def make_headline(self, product: Dict[str, Any]) -> str:
        return f"{product['name']} for {product['audience']}"

    def make_ad_copy(self, product: Dict[str, Any]) -> str:
        return (
            f"Discover {product['name']} and unlock practical strategies for growth. "
            f"{product['tagline']} Made for {product['audience']}."
        )

    def make_cta(self, product: Dict[str, Any]) -> str:
        return f"Get {product['name']} today"

    def budget_for(self, product: Dict[str, Any]) -> float:
        map_budget = {
            "lead_generation": 120,
            "sales_growth": 180,
            "upsell": 220,
            "conversion": 95,
        }
        return map_budget.get(product["goal"], 100)

    def summary(self) -> Dict[str, Any]:
        products = self.load_catalog()
        total_value = sum(float(product["price"]) for product in products)
        return {
            "total_products": len(products),
            "average_price": round(total_value / len(products), 2) if products else 0,
            "best_selling_channel": "Amazon",
            "campaign_count": len(self.generate_campaigns()),
        }
