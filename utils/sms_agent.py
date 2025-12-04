import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv()

ADWINGS_URL = os.getenv("ADWINGS_SMS_URL")
CLIENT_ID = os.getenv("ADWINGS_CLIENT_ID")
CLIENT_PASSWORD = os.getenv("ADWINGS_CLIENT_PASSWORD")
SENDER_ID = os.getenv("ADWINGS_SENDER_ID")
WELCOME_SMS_TEXT = os.getenv("WELCOME_SMS_TEXT", "")

WELCOME_TEMPLATE_ID = os.getenv("ADWINGS_WELCOME_TEMPLATE_ID")
DLT_ENTITY_ID = os.getenv("ADWINGS_DLT_ENTITY_ID")


def send_welcome_sms(mobile: str, firstname: str) -> str:
    """
    Send SMS via AdWings with DLT template ID mapped correctly.
    """

    # Replace '*' placeholder with user's name
    message = WELCOME_SMS_TEXT.replace("*", firstname)

    payload = {
        "apiver": "1.0",
        "sms": {
            "ver": "2.0",
            "dlr": {"url": ""},
            "messages": [
                {
                    "udh": "0",
                    "coding": 1,
                    "text": message,  # mapped message
                    "property": 0,
                    "id": "1",

                    "dlt": {
                        "tmid": WELCOME_TEMPLATE_ID,   # DLT Template ID
                        "entityid": DLT_ENTITY_ID,     # DLT Entity ID
                        "sid": SENDER_ID               # Sender ID: RMCODE
                    },

                    "addresses": [
                        {
                            "from": SENDER_ID,
                            "to": "91" + mobile,
                            "seq": "1",
                            "tag": ""
                        }
                    ]
                }
            ]
        }
    }

    credentials = f"{CLIENT_ID}:{CLIENT_PASSWORD}".encode("ascii")
    auth = base64.b64encode(credentials).decode("ascii")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth}",
    }

    response = requests.post(
        ADWINGS_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    print("\nSMS REQUEST JSON:", json.dumps(payload, indent=2))
    print("SMS RESPONSE:", response.status_code, response.text)

    return response.text
