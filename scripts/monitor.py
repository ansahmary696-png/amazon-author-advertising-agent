#!/usr/bin/env python3

from src.marketing.agent import MarketingAgent


def main():
    agent = MarketingAgent()
    campaigns = agent.generate_campaigns()
    for campaign in campaigns:
        print(f"{campaign['product_name']} | {campaign['channel']} | ${campaign['budget_recommendation']}")
        print(f"Headline: {campaign['ad_headline']}")
        print(f"CTA: {campaign['cta']}")
        print()


if __name__ == "__main__":
    main()
