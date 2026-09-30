from typing import Any

import stripe

from src.config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_checkout_session(
    product_name: str,
    price: float,
    quantity: int = 1,
    success_url: str = "",
    cancel_url: str = "",
) -> str | None:
    if not STRIPE_SECRET_KEY:
        return None

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product_name},
                    "unit_amount": int(float(price) * 100),
                },
                "quantity": quantity,
            }],
            mode="payment",
            success_url=success_url or "https://example.com/success",
            cancel_url=cancel_url or "https://example.com/cancel",
        )
        return session.id
    except Exception:
        return None
