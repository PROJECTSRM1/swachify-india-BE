import os
import smtplib
import requests
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =============================
# EMAIL CORE FUNCTION (FIXED)
# =============================
def send_email(to_email: str, subject: str, body: str, html: bool = False) -> bool:
    try:
        sender_email = os.getenv("MAIL_USERNAME")
        sender_password = os.getenv("MAIL_PASSWORD")
        mail_server = os.getenv("MAIL_SERVER")
        mail_port = int(os.getenv("MAIL_PORT", 587))

        print("📧 SMTP USER:", sender_email)
        print("📧 SMTP SERVER:", mail_server)

        if not sender_email or not sender_password:
            raise Exception("SMTP credentials missing")

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        if html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("✅ EMAIL SENT TO:", to_email)
        return True

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))
        return False


# =============================
# WELCOME EMAIL
# =============================
def send_welcome_email(email: str, name: str) -> bool:
    subject = "Welcome to Swachify India 🇮🇳"
    body = f"""
Dear {name},

🎉 Welcome to Swachify India!

Your registration is successful.
You can now book services and manage everything easily.

Regards,
Swachify India Team
"""
    return send_email(email, subject, body)


# =============================
# FORGOT PASSWORD OTP
# =============================
def send_forgot_password_otp(
    email: str,
    otp: str,
    first_name: Optional[str] = None
) -> bool:
    name = first_name or "User"

    subject = "Swachify India - Password Reset OTP"
    body = f"""
Dear {name},

Your OTP to reset your Swachify India password is:
OTP: {otp}

This OTP is valid for 10 minutes.
If you did not request this, please ignore this email.

Regards,
Swachify India Team
"""
    return send_email(email, subject, body)


# =============================
# EMAIL OTP (HTML)
# =============================
def send_email_otp(email: str, otp: str) -> bool:
    subject = "Swachify India - Email Verification"
    body = f"""
<h3>Email Verification</h3>
<p>Your OTP is:</p>
<h2>{otp}</h2>
<p>Valid for 5 minutes</p>
"""
    return send_email(email, subject, body, html=True)


# =============================
# SMS FUNCTIONS (UNCHANGED)
# =============================
def send_sms(mobile: str, message: str, template_id: str) -> bool:
    try:
        payload = {
            "clientId": os.getenv("ADWINGS_CLIENT_ID"),
            "clientSecret": os.getenv("ADWINGS_CLIENT_PASSWORD"),
            "senderId": os.getenv("ADWINGS_SENDER_ID"),
            "dltEntityId": os.getenv("ADWINGS_DLT_ENTITY_ID"),
            "templateId": template_id,
            "mobileNumber": mobile,
            "message": message,
        }

        response = requests.post(
            os.getenv("ADWINGS_SMS_URL"),
            json=payload,
            timeout=10
        )

        print("📱 SMS RESPONSE:", response.text)
        return response.status_code == 200

    except Exception as e:
        print("❌ SMS ERROR:", str(e))
        return False


def send_welcome_sms(mobile: str, user_name: str) -> bool:
    text = os.getenv("WELCOME_SMS_TEXT").replace("*", user_name)
    return send_sms(
        mobile=mobile,
        message=text,
        template_id=os.getenv("ADWINGS_WELCOME_TEMPLATE_ID")
    )
