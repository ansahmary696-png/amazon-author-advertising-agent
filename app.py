from typing import Dict, List


def build_campaign_templates() -> List[Dict]:
    return [
        {
            "name": "Amazon Author Launch",
            "channel": "Amazon",
            "objective": "Increase discovery and book sales",
            "keywords": ["personal growth book", "business mindset", "author bestseller"],
            "creative": "Highlight transformation, credibility, and reader outcomes.",
            "budget": 250,
        },
        {
            "name": "Selar Offer Boost",
            "channel": "Selar",
            "objective": "Increase checkout conversions",
            "keywords": ["digital growth guide", "author resource", "self-improvement toolkit"],
            "creative": "Promote value, practical takeaways, and instant access.",
            "budget": 180,
        },
        {
            "name": "Retargeting Edge",
            "channel": "Cross-channel",
            "objective": "Recover abandoned interest",
            "keywords": ["book launch", "author strategy", "online earnings"],
            "creative": "Use urgency, value proof, and limited-time discounts.",
            "budget": 140,
        },
    ]
