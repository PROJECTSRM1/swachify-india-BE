# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from dotenv import load_dotenv
# import os

# load_dotenv()

# conf = ConnectionConfig(
#     MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
#     MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
#     MAIL_FROM=os.getenv("MAIL_FROM"),
#     MAIL_PORT=int(os.getenv("MAIL_PORT")),
#     MAIL_SERVER=os.getenv("MAIL_SERVER"),

#     MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
#     MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",

#     USE_CREDENTIALS=True,
# )

# fast_mail = FastMail(conf)


# async def send_welcome_email(email: str, name: str) -> bool:
#     """
#     Sends a welcome email to the user.
#     Returns True on success, False on failure.
#     """


#     try:
#         subject = "Welcome to Swachify India 🇮🇳"


#         body = f"""
#         Dear {name},


#         🎉 Welcome to Swachify India!


#         Your registration is successful. Now you can explore our platform,
#         book services, post tasks, and grow with our ecosystem.


#         Regards,
#         Swachify India Team
#         """


#         message = MessageSchema(
#             subject=subject,
#             recipients=[email],  # must be a list
#             body=body,
#             subtype="plain"
#         )


#         # Attempt sending the email
#         await fast_mail.send_message(message)


#         print("📧 EMAIL SENT SUCCESSFULLY TO:", email)
#         return True


#     except Exception as error:
#         print("❌ EMAIL SENDING ERROR:", str(error))
#         return False




# async def send_forgot_password_otp(email: str, otp: str, first_name: str | None = None):
#     display_name = first_name or "User"

#     subject = "Swachify India - Password Reset OTP"

#     body = f"""
#     Dear {display_name},

#     Your OTP to reset your Swachify India password is: {otp}

#     This OTP is valid for 10 minutes. If you did not request a password reset,
#     please ignore this email.

#     Regards,
#     Swachify India Team
#     """

#     message = MessageSchema(
#         subject=subject,
#         recipients=[email],
#         body=body,
#         subtype="plain"
#     )

#     await fast_mail.send_message(message)




import os
import ssl
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Optional

import os
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=to_email,
            subject=subject,
            plain_text_content=body,
        )

        # ✅ LOCAL WINDOWS FIX
        if os.getenv("ENV") == "local":
            ssl._create_default_https_context = ssl._create_unverified_context

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)

        print("📧 Email sent to:", to_email)
        return True

    except Exception as e:
        print("❌ SendGrid Email Error:", str(e))
        return False



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


# ==================================================
# FORGOT PASSWORD OTP EMAIL
# ==================================================

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


# ==================================================
# ADWINGS SMS
# ==================================================

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




def send_email_otp(email: str, otp: str):
    message = Mail(
        from_email=os.getenv("SENDGRID_FROM_EMAIL"),
        to_emails=email,
        subject="Your OTP Code",
        html_content=f"""
        <h3>Email Verification</h3>
        <p>Your OTP is:</p>
        <h2>{otp}</h2>
        <p>Valid for 5 minutes</p>
        """
    )

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)
