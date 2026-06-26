import os
import smtplib
from email.message import EmailMessage

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    raise ValueError("Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.")

msg = EmailMessage()
msg["Subject"] = "Purchase2Pay Pipeline Completed"
msg["From"] = GMAIL_USER
msg["To"] = "admin@omgananayaka.in"

msg.set_content("""
Purchase2Pay Pipeline Completed Successfully.

✓ Kafka
✓ Spark Streaming
✓ DuckDB
✓ Soda Quality Checks
""")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    smtp.send_message(msg)

print("Mail sent successfully.")