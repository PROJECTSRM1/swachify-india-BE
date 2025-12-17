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



def send_welcome_sms(mobile: str, firstname: str) -> bool:
    """
    Send SMS via AdWings using DLT-approved template.
    Returns True if SMS is accepted/sent successfully, False otherwise.
    """


    try:
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
                        "text": message,
                        "property": 0,
                        "id": "1",


                        "dlt": {
                            "tmid": WELCOME_TEMPLATE_ID,
                            "entityid": DLT_ENTITY_ID,
                            "sid": SENDER_ID
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


        print("\n SMS REQUEST PAYLOAD:", json.dumps(payload, indent=2))
        print(" SMS RESPONSE:", response.status_code, response.text)


        if response.status_code != 200:
            print(" SMS HTTP ERROR:", response.text)
            return False


        try:
            result = response.json()

            if "status" in result and result["status"].lower() not in ["success", "submitted", "queued"]:
                print("SMS PROVIDER REPORTED FAILURE:", result)
                return False


        except Exception as json_error:
            print("SMS RESPONSE JSON PARSE ERROR:", json_error)
            return False


        print(" SMS SENT SUCCESSFULLY!")
        return True


    except Exception as e:
        print(" SMS ERROR:", str(e))
        return False