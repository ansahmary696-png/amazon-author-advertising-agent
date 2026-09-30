import os
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from src.config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    AMAZON_PROFILE_URL,
    APP_TITLE,
    SELAR_STORE_URL,
    SECRET_KEY,
)
from src.config import (
    init_db,
    list_campaigns,
    list_products,
    save_campaign,
    save_product,
)
from src.marketing.agent import MarketingAgent
from src.marketing.campaign_templates import build_campaign_templates
from src.services.ai_creatives import generate_ad_copy
from src.services.communications import send_email_campaign, send_sms_campaign
from src.services.payments import create_checkout_session
from src.services.selar_sync import sync_selar_products

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper


@app.before_request
def ensure_db_ready():
    init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("admin"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/api/overview")
def overview():
    agent = MarketingAgent()
    summary = agent.summary()
    return jsonify({
        "title": APP_TITLE,
        "amazon": AMAZON_PROFILE_URL,
        "selar": SELAR_STORE_URL,
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
            {"name": "SMS", "performance": 81, "goal": "Urgency"},
        ],
    })


@app.route("/api/products")
def products():
    return jsonify(list_products())


@app.route("/api/campaigns")
def campaigns():
    items = list_campaigns()
    if items:
        return jsonify(items)
    return jsonify(build_campaign_templates())


@app.route("/api/ai-copy", methods=["POST"])
def ai_copy():
    payload = request.get_json() or {}
    product_name = payload.get("product_name", "Book Launch")
    audience = payload.get("audience", "new readers")
    channel = payload.get("channel", "Amazon")
    creative = generate_ad_copy(product_name, audience, channel)
    return jsonify({"creative": creative})


@app.route("/api/admin/product", methods=["POST"])
@login_required
def save_admin_product():
    payload = request.get_json() or {}
    item = save_product(payload)
    return jsonify({"success": True, "product": item})


@app.route("/api/admin/campaign", methods=["POST"])
@login_required
def save_admin_campaign():
    payload = request.get_json() or {}
    item = save_campaign(payload)
    return jsonify({"success": True, "campaign": item})


@app.route("/api/sync-selar")
@login_required
def sync_selar():
    products = sync_selar_products()
    if not products:
        return jsonify({"success": False, "message": "No Selar products returned. Configure SELAR_API_URL or use mock catalog."})

    for product in products:
        save_product({
            "id": product.get("id") or f"selar-{len(products)}",
            "name": product.get("name") or "Selar Product",
            "type": product.get("type", "product"),
            "price": product.get("price", 0),
            "currency": product.get("currency", "USD"),
            "channel": "Selar",
            "category": product.get("category", "digital"),
            "tagline": product.get("tagline", "High-value product"),
            "audience": product.get("audience", "growth-focused buyers"),
            "cover": product.get("cover", ""),
            "inventory": product.get("inventory", 0),
            "rating": product.get("rating", 0),
            "goal": product.get("goal", "conversion"),
        })

    return jsonify({"success": True, "count": len(products)})


@app.route("/api/create-checkout-session", methods=["POST"])
def create_checkout():
    payload = request.get_json() or {}
    session_id = create_checkout_session(
        product_name=payload.get("product_name", "Author Growth Blueprint"),
        price=payload.get("price", 49.00),
        quantity=payload.get("quantity", 1),
        success_url=payload.get("success_url") or url_for("home", _external=True),
        cancel_url=payload.get("cancel_url") or url_for("home", _external=True),
    )
    if not session_id:
        return jsonify({"success": False, "message": "Stripe is not configured."}), 400
    return jsonify({"success": True, "checkout_session_id": session_id})


@app.route("/api/communications/email", methods=["POST"])
@login_required
def send_email():
    payload = request.get_json() or {}
    result = send_email_campaign(
        payload.get("subject", "Campaign update"),
        payload.get("body", ""),
        payload.get("to_email", "")
    )
    return jsonify(result)


@app.route("/api/communications/sms", methods=["POST"])
@login_required
def send_sms():
    payload = request.get_json() or {}
    result = send_sms_campaign(
        payload.get("message", "Check out our latest offer!"),
        payload.get("to_phone", "")
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
