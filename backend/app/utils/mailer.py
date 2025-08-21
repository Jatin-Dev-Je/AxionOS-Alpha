import smtplib
from email.message import EmailMessage
from typing import Optional

from ..config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM


def send_email(to: str, subject: str, html: str, text: Optional[str] = None) -> None:
	if not SMTP_HOST or not SMTP_PORT:
		raise RuntimeError("SMTP not configured. Set SMTP_HOST and SMTP_PORT in .env")

	msg = EmailMessage()
	msg["From"] = EMAIL_FROM
	msg["To"] = to
	msg["Subject"] = subject
	if text:
		msg.set_content(text)
	msg.add_alternative(html, subtype="html")

	with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
		server.ehlo()
		try:
			server.starttls()
		except Exception:
			# If server doesn't support STARTTLS, continue plaintext (dev/local)
			pass
		if SMTP_USER and SMTP_PASSWORD:
			server.login(SMTP_USER, SMTP_PASSWORD)
		server.send_message(msg)
