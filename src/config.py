import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-author-agent")
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'author_agent.db'}")
SELAR_API_URL = os.getenv("SELAR_API_URL", "")
SELAR_API_KEY = os.getenv("SELAR_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "daniel")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "author123")

APP_TITLE = "Daniel Kwesi Ansah | Amazon + Selar Growth Engine"
AMAZON_PROFILE_URL = "https://amazon.com/author/danielkwesiansah"
SELAR_STORE_URL = "https://selar.com/m/danielkwesiansah"
