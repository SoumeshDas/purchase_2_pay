import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

REPORT_FILE = "/jobs/output/quality_report.json"

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

TO_EMAIL = os.getenv("TO_EMAIL", "admin@omgananayaka.in")

if not Path(REPORT_FILE).exists():
    raise FileNotFoundError(f"{REPORT_FILE} not found")

with open(REPORT_FILE) as f:
    report = json.load(f)

status = report.get("status", "UNKNOWN")
subject = f"[{status}] Purchase2Pay Pipeline Report"

html = f"""
<html>
<body style="font-family:Arial">
<h2>Purchase2Pay Pipeline Report</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th align="left">Pipeline</th><td>{report['pipeline']}</td></tr>
<tr><th align="left">Status</th><td><b>{status}</b></td></tr>
<tr><th align="left">Execution</th><td>{report['execution_time']}</td></tr>
<tr><th align="left">Duration</th><td>{report['duration_seconds']} sec</td></tr>
<tr><th align="left">Total Checks</th><td>{report['total_checks']}</td></tr>
<tr><th align="left">Passed</th><td>{report['passed']}</td></tr>
<tr><th align="left">Failed</th><td>{report['failed']}</td></tr>
<tr><th align="left">Warnings</th><td>{report['warnings']}</td></tr>
</table>

<h3>Quality Checks</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Check</th><th>Status</th><th>Actual</th></tr>
"""

for c in report.get("checks", []):
    color = "#ccffcc" if c["status"] == "PASSED" else "#ffcccc"
    html += (
        f"<tr bgcolor='{color}'>"
        f"<td>{c['name']}</td>"
        f"<td>{c['status']}</td>"
        f"<td>{c.get('actual', '')}</td>"
        "</tr>"
    )

html += "</table></body></html>"

msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = GMAIL_USER
msg["To"] = TO_EMAIL
msg.set_content("HTML capable mail client required.")
msg.add_alternative(html, subtype="html")

log = report.get("log_file")
if log and Path(log).exists():
    with open(log, "rb") as f:
        msg.add_attachment(
            f.read(), maintype="text", subtype="plain", filename=Path(log).name
        )

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    smtp.send_message(msg)

print("Email sent successfully.")
