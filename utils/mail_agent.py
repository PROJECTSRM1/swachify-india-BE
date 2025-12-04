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


async def send_welcome_email(email: str, name: str):
    subject = "Welcome to Swachify India 🇮🇳"

    body = f"""
    Dear {name},

    🎉 Welcome to Swachify India!

    Your registration is successful. Now you can explore our platform,
    post services, request cleaning, and grow with our ecosystem.

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
