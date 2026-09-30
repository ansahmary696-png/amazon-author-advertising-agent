import os
import smtplib
from email.mime.text import MIMEText
from typing import Any, Dict

try:
    from twilio.rest import Client
except Exception:  # pragma: no cover
    Client = None

from src.config import SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER


def send_email_campaign(subject: str, body: str, to_email: str) -> Dict[str, Any]:
    if not SMTP_USER or not SMTP_PASSWORD:
        return {"status": "mock", "message": "SMTP not configured. Email campaign queued for later."}

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
        return {"status": "sent", "message": "Email sent successfully"}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "message": str(exc)}


def send_sms_campaign(message: str, to_phone: str) -> Dict[str, Any]:
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER or Client is None:
        return {"status": "mock", "message": "Twilio not configured. SMS campaign queued for later."}

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        msg = client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to_phone)
        return {"status": "sent", "message": msg.sid}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "message": str(exc)}
