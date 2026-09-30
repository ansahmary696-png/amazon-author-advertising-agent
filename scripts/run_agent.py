import json
from pathlib import Path

from flask import Flask, jsonify, render_template

from src.marketing.agent import MarketingAgent
from src.marketing.campaign_templates import build_campaign_templates

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/overview")
def overview():
    agent = MarketingAgent()
    summary = agent.summary()
    return jsonify({
        "hero": {
            "site_name": "Daniel Kwesi Ansah",
            "brand": "Amazon + Selar Growth Engine",
            "amazon": "https://amazon.com/author/danielkwesiansah",
            "selar": "https://selar.com/m/danielkwesiansah",
        },
        "metrics": {
            "total_products": summary["total_products"],
            "average_price": summary["average_price"],
            "campaign_count": summary["campaign_count"],
            "best_channel": summary["best_selling_channel"],
        },
        "channels": [
            {"name": "Amazon", "performance": 88, "goal": "Reach"},
            {"name": "Selar", "performance": 92, "goal": "Sales"},
            {"name": "Email", "performance": 76, "goal": "Retention"},
        ],
    })


@app.route("/api/products")
def products():
    catalog_path = Path("data/products.json")
    with catalog_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data["products"])


@app.route("/api/campaigns")
def campaigns():
    return jsonify(build_campaign_templates())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
