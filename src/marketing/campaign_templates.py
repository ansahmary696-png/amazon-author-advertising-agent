import json
from pathlib import Path
from typing import Dict, List


class MarketingAgent:
    """Generate smart marketing campaigns and recommendations."""

    def __init__(self, catalog_path: str = "data/products.json"):
        self.catalog_path = Path(catalog_path)

    def load_catalog(self) -> List[Dict]:
        with self.catalog_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("products", [])

    def generate_campaigns(self) -> List[Dict]:
        products = self.load_catalog()
        campaigns = []

        for product in products:
            campaign = {
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
            campaigns.append(campaign)

        return campaigns

    def make_headline(self, product: Dict) -> str:
        return f"{product['name']} for {product['audience']}"

    def make_ad_copy(self, product: Dict) -> str:
        return (
            f"Discover {product['name']} and unlock practical strategies for growth. "
            f"{product['tagline']} Built for {product['audience']}."
        )

    def make_cta(self, product: Dict) -> str:
        return f"Get {product['name']} today"

    def budget_for(self, product: Dict) -> float:
        budget_map = {
            "lead_generation": 120,
            "sales_growth": 180,
            "upsell": 220,
            "conversion": 95,
        }
        return budget_map.get(product["goal"], 100)

    def summary(self) -> Dict:
        products = self.load_catalog()
        total_value = sum(product["price"] for product in products)
        return {
            "total_products": len(products),
            "average_price": round(total_value / len(products), 2),
            "best_selling_channel": "Amazon",
            "campaign_count": len(self.generate_campaigns()),
        }
