from flask_mail import Message
from app.extensions import mail
from flask import current_app
import random
import string
from datetime import datetime, timedelta, timezone


def generate_otp(length=6) -> str:
    """Generate a random numerical OTP"""
    return ''.join(random.choices(string.digits, k=length))


def get_otp_expiry(minutes=10) -> datetime:
    """Get the expiry time for an OTP"""
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


def send_otp_email(recipient_email: str, otp_code: str):
    """Send an OTP code via Brevo SMTP relay using Flask-Mail."""
    subject = "BloodLink — Your Verification Code"
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 520px; margin: 0 auto;
                padding: 30px; border: 1px solid #e5e7eb; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 24px;">
            <h2 style="color: #dc2626; font-size: 28px; margin: 0;">&#129657; BloodLink</h2>
            <p style="color: #6b7280; margin-top: 6px;">Blood Donor & Emergency Network</p>
        </div>
        <h3 style="text-align: center; color: #111827;">Email Verification</h3>
        <p style="color: #374151;">Use the code below to verify your email address.
           It expires in <strong>10 minutes</strong>.</p>
        <div style="background: #fef2f2; border: 2px dashed #dc2626; border-radius: 10px;
                    padding: 24px; text-align: center; margin: 24px 0;">
            <p style="margin: 0; color: #6b7280; font-size: 13px; letter-spacing: 1px;">
                YOUR ONE-TIME PASSWORD
            </p>
            <h1 style="color: #dc2626; font-size: 48px; letter-spacing: 12px;
                       margin: 10px 0 0 0; font-weight: 900;">{otp_code}</h1>
        </div>
        <p style="color: #9ca3af; font-size: 13px;">
            If you did not create a BloodLink account, please ignore this email.
        </p>
    </div>
    """

    try:
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            html=html_body
        )
        mail.send(msg)
        current_app.logger.info(f"[EMAIL] OTP sent successfully to {recipient_email}")
    except Exception as e:
        # Email failed — log fallback OTP to console so user can still verify
        current_app.logger.warning("")
        current_app.logger.warning("=" * 55)
        current_app.logger.warning("           ⚠  FALLBACK OTP (EMAIL FAILED)  ⚠         ")
        current_app.logger.warning(f"  Recipient : {recipient_email}")
        current_app.logger.warning(f"  OTP Code  : {otp_code}")
        current_app.logger.warning(f"  Error     : {str(e)}")
        current_app.logger.warning("=" * 55)
        current_app.logger.warning("")
        # Do NOT raise — registration still succeeds, OTP is in logs
