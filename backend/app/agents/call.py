from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

call = client.calls.create(
    to="+919483683335",   # Your verified mobile
    from_=os.getenv("TWILIO_PHONE_NUMBER"),

    # TwiML webhook
    url="https://prankster-freezing-boundless.ngrok-free.dev/voice",

    # Status callback webhook
    status_callback="https://prankster-freezing-boundless.ngrok-free.dev/call-status",
    status_callback_method="POST",

    # Trigger callback when the call completes
    status_callback_event=["completed"]
)

print("Calling...")
print("Call SID:", call.sid)