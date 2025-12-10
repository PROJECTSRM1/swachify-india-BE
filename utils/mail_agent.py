from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),

    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",

    USE_CREDENTIALS=True,
)

fast_mail = FastMail(conf)


async def send_welcome_email(email: str, name: str) -> bool:
    """
    Sends a welcome email to the user.
    Returns True on success, False on failure.
    """


    try:
        subject = "Welcome to Swachify India 🇮🇳"


        body = f"""
        Dear {name},


        🎉 Welcome to Swachify India!


        Your registration is successful. Now you can explore our platform,
        book services, post tasks, and grow with our ecosystem.


        Regards,
        Swachify India Team
        """


        message = MessageSchema(
            subject=subject,
            recipients=[email],  # must be a list
            body=body,
            subtype="plain"
        )


        # Attempt sending the email
        await fast_mail.send_message(message)


        print("📧 EMAIL SENT SUCCESSFULLY TO:", email)
        return True


    except Exception as error:
        print("❌ EMAIL SENDING ERROR:", str(error))
        return False




async def send_forgot_password_otp(email: str, otp: str, first_name: str | None = None):
    display_name = first_name or "User"

    subject = "Swachify India - Password Reset OTP"

    body = f"""
    Dear {display_name},

    Your OTP to reset your Swachify India password is: {otp}

    This OTP is valid for 10 minutes. If you did not request a password reset,
    please ignore this email.

    Regards,
    Swachify India Team
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="plain"
    )

    await fast_mail.send_message(message)

