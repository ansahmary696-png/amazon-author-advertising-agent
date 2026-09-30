# amazon-author-advertising-agent

A super advertising agent and sales promotion system for:
- Amazon Author: https://amazon.com/author/danielkwesiansah
- Selar Store: https://selar.com/m/danielkwesiansah

This project combines a marketing landing page, product catalog insights, campaign generation, dashboard analytics, and automation scripts to help grow sales and visibility across Amazon and Selar.

## Features

- Landing page for the author brand and store
- Author/store dashboard with performance overview
- Product catalog with pricing and offers
- Marketing campaign templates for Amazon and Selar
- Automation scripts for campaign monitoring and reporting
- AI-style ad copy generation for books and digital products
- Metrics summary for impressions, CTR, conversions, and ROAS

## Project structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── products.json
├── scripts/
│   ├── run_agent.py
│   └── monitor.py
├── src/
│   └── marketing/
│       ├── __init__.py
│       ├── __init__.py
│       ├── agent.py
│       └── campaign_templates.py
├── templates/
│   ├── index.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
└── .gitignore
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:
- http://localhost:5000/
- http://localhost:5000/dashboard

## Example automation

```bash
python scripts/run_agent.py
```

## Notes

This project is designed as a starter marketing automation system for an author brand. You can connect it to your real Amazon Ads API, Selar product data, or a CMS later.

## License

MIT
