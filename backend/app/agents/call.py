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
    url="https://prankster-freezing-boundless.ngrok-free.dev/voice"
)

print("Calling...")
print(call.sid)