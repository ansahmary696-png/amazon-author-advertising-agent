# Amazon Author Advertising Agent

A production-ready growth engine for an author brand and digital sales ecosystem.

## Features
- Landing page and CTA funnel
- Marketing dashboard
- Admin CMS
- AI-generated ad copy
- Amazon Ads integration hooks
- Selar API sync hooks
- Stripe checkout support
- Email and SMS messaging support
- SQLite data storage
- Docker and Render ready

## Stack
- Python
- Flask
- SQLite
- Stripe
- OpenAI-compatible API
- HTML/CSS/JavaScript

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Admin login
- Username: daniel
- Password: author123

## Routes
- `/` — home page
- `/dashboard` — analytics dashboard
- `/admin` — protected admin area
- `/login` — admin login
- `/api/overview`
- `/api/products`
- `/api/campaigns`
- `/api/ai-copy`
- `/api/admin/product`
- `/api/admin/campaign`
- `/api/sync-selar`
- `/api/create-checkout-session`

## Deployment

Docker:

```bash
docker build -t daniel-author-agent .
docker run -p 5000:5000 daniel-author-agent
```

Render:
- Use the included `render.yaml`.

## Notes
Set real credential values in `.env` before production deployment.
