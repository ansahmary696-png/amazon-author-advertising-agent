import os
from typing import Dict, List

from src.config import OPENAI_API_KEY


def generate_ad_copy(product_name: str, audience: str, channel: str = "Amazon") -> Dict[str, str]:
    if OPENAI_API_KEY:
        try:
            import openai

            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            text = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a direct-response marketing strategist for author branding.",
                    },
                    {
                        "role": "user",
                        "content": f"Write a short high-converting ad for {product_name} for {audience} on {channel}. Include headline, body, CTA.",
                    },
                ],
            )
            response = text.choices[0].message.content
            return {"headline": response.splitlines()[0], "body": response, "cta": "Get it now"}
        except Exception:
            pass

    headline = f"{product_name} for {audience}"
    body = (
        f"Build momentum with {product_name}. Perfect for {audience} who want clarity, practical action, and measurable growth. "
        f"Designed for modern readers and buyers on {channel}."
    )
    return {"headline": headline, "body": body, "cta": "Shop now"}


def generate_campaign_variants(product_name: str, audience: str) -> List[str]:
    return [
        f"{product_name}: built for {audience} who want action and transformation.",
        f"A smarter way to grow with {product_name}. Built for {audience}.",
        f"Discover {product_name} and unlock your next level of growth.",
    ]
