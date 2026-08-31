import smtplib
from email.message import EmailMessage

from app.core.config import settings


class EmailService:

    @staticmethod
    def send_otp_email(to_email: str, otp: str) -> None:
        subject = "Your password reset code"

        expire_minutes = settings.OTP_WINDOW_SECONDS // 60

        body = (
            f"Your OTP for resetting your password is: {otp}\n"
            f"This code expires in {expire_minutes} minutes.\n"
            "If you did not request this, you can ignore this email."
        )

        if (
            settings.SMTP_HOST
            and settings.SMTP_USER
            and settings.SMTP_PASSWORD
            and settings.SMTP_FROM
        ):
            EmailService._send_via_smtp(to_email, subject, body)
        else:
            print(f"[OTP EMAIL] to={to_email} otp={otp}")

    @staticmethod
    def _send_via_smtp(to_email: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings.SMTP_FROM
        message["To"] = to_email
        message.set_content(body)

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
