import os
from typing import Any, Dict, List

import requests

from src.config import AMAZON_CLIENT_ID, AMAZON_CLIENT_SECRET, AMAZON_PROFILE_ID, AMAZON_REFRESH_TOKEN, AMAZON_REGION


class AmazonAdsClient:
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        profile_id: str | None = None,
        region: str | None = None,
    ):
        self.client_id = client_id or AMAZON_CLIENT_ID
        self.client_secret = client_secret or AMAZON_CLIENT_SECRET
        self.refresh_token = refresh_token or AMAZON_REFRESH_TOKEN
        self.profile_id = profile_id or AMAZON_PROFILE_ID
        self.region = region or AMAZON_REGION
        self.token_url = "https://api.amazon.com/auth/o2/token"
        self.base_url = "https://advertising-api.amazon.com"

    def get_access_token(self) -> str:
        if not self.client_id or not self.client_secret or not self.refresh_token:
            return ""

        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        try:
            response = requests.post(self.token_url, data=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            return data.get("access_token", "")
        except Exception:
            return ""

    def headers(self) -> Dict[str, str]:
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Amazon-Advertising-API-ClientId": self.profile_id,
            "Amazon-Advertising-API-Scope": "campaigns",
        }

    def get_campaigns(self) -> List[Dict[str, Any]]:
        if not self.profile_id or not self.get_access_token():
            return []

        try:
            response = requests.get(f"{self.base_url}/v2/campaigns", headers=self.headers(), timeout=20)
            response.raise_for_status()
            payload = response.json()
            return payload if isinstance(payload, list) else payload.get("campaigns", [])
        except Exception:
            return []

    def get_report(self, campaign_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
        if not self.profile_id or not self.get_access_token():
            return {}

        try:
            response = requests.post(
                f"{self.base_url}/v2/reports",
                headers=self.headers(),
                json={"campaignId": campaign_id, "startDate": start_date, "endDate": end_date},
                timeout=20,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {}

    def update_bid(self, keyword_id: str, campaign_id: str, bid: float) -> bool:
        if not self.profile_id or not self.get_access_token():
            return False

        try:
            response = requests.put(
                f"{self.base_url}/v2/keywords/{keyword_id}",
                headers=self.headers(),
                json={"campaignId": campaign_id, "bid": bid},
                timeout=20,
            )
            response.raise_for_status()
            return True
        except Exception:
            return False
