from typing import Dict, List

from src.config import OPENAI_API_KEY


def generate_ad_copy(product_name: str, audience: str, channel: str = "Amazon") -> Dict[str, str]:
    if OPENAI_API_KEY:
        try:
            import openai
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a direct-response marketing strategist for author branding.",
                    },
                    {
                        "role": "user",
                        "content": f"Write a short high-converting ad for {product_name} for {audience} on {channel}. Include headline, body, and CTA.",
                    },
                ],
            )
            text = response.choices[0].message.content
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            headline = lines[0] if lines else f"{product_name} for {audience}"
            return {"headline": headline, "body": text, "cta": "Get it now"}
        except Exception:
            pass

    headline = f"{product_name} for {audience}"
    body = (
        f"Build momentum with {product_name}. Perfect for {audience} who want clarity, practical action, "
        f"and measurable growth. Designed for modern readers and buyers on {channel}."
    )
    return {"headline": headline, "body": body, "cta": "Shop now"}


def generate_campaign_variants(product_name: str, audience: str) -> List[str]:
    return [
        f"{product_name}: built for {audience} who want action and transformation.",
        f"A smarter way to grow with {product_name}. Built for {audience}.",
        f"Discover {product_name} and unlock your next level of growth.",
    ]
