import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)


def send_whatsapp_message(
    phone: str,
    message: str
):

    if not phone.startswith("whatsapp:"):
        phone = f"whatsapp:{phone}"

    try:

        response = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=phone
        )

        return {
            "success": True,
            "sid": response.sid,
            "status": response.status
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
    
if __name__ == "__main__":

    result = send_whatsapp_message(
        "+919483683335",      # Replace with your own WhatsApp number
        "Hello from the AI Delivery Agent!"
    )

    print(result)