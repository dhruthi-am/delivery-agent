from fastapi import APIRouter

from app.schemas.call_schema import CallRequest
from app.agents.delivery_agent import handle_delivery_call
from app.services.customer_summary import end_delivery_call

from fastapi import Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

router = APIRouter()


@router.get("/")
def root():
    return {
        "status": "Running",
        "message": "Customer Delivery Agent Backend is running successfully!"
    }


@router.post("/simulate-call")
def simulate_call(request: CallRequest):

    # Temporary conversation ID
    # Later this will come from Twilio's Call SID
    conversation_id = "demo"

    # Let the delivery agent handle the complete workflow
    result = handle_delivery_call(
        conversation_id=conversation_id,
        message=request.message
    )

    # Return the result
    return {
        "received_message": request.message,
        **result
    }

@router.post("/end-call")
def end_call():

    result = end_delivery_call(
        conversation_id="demo"
    )

    return result

@router.post("/voice")
async def voice(request: Request):

    response = VoiceResponse()

    gather = Gather(
    input="speech",
    action="/process-speech",
    method="POST",
    speech_timeout="auto",
    language="en-IN"
)
    gather.say(
    "Hello. This is the AI Delivery Assistant. Please tell me the customer name or how I can assist with the delivery today."
)

    response.append(gather)

    return Response(
        content=str(response),
        media_type="application/xml"
    )

@router.post("/process-speech")
async def process_speech(request: Request):

    try:
        form = await request.form()

        print("=" * 50)
        print("FORM DATA")
        print(dict(form))
        print("=" * 50)

        speech = form.get("SpeechResult")

        if not speech:
            speech = "No response received."

        call_sid = form.get("CallSid")

        print("Speech:", speech)
        print("Call SID:", call_sid)
        print("=" * 50)

        # Process conversation
        result = handle_delivery_call(
            conversation_id=call_sid,
            message=speech
        )

        print(result)

        response = VoiceResponse()

        gather = Gather(
            input="speech",
            action="/process-speech",
            method="POST",
            speech_timeout="auto"
        )

        gather.say(result["ai_reply"])

        response.append(gather)

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    except Exception as e:

        print("=" * 50)
        print("PROCESS SPEECH ERROR")
        import traceback
        traceback.print_exc()
        print("=" * 50)

        response = VoiceResponse()

        gather = Gather(
            input="speech",
            action="/process-speech",
            method="POST",
            speech_timeout="auto"
        )

        gather.say(
            "I'm sorry. Our AI service is temporarily unavailable. Please repeat your last message in a few seconds."
        )

        response.append(gather)

        return Response(
            content=str(response),
            media_type="application/xml"
        )

@router.post("/call-status")
async def call_status(request: Request):

    form = await request.form()

    status = form.get("CallStatus")
    call_sid = form.get("CallSid")

    print("=" * 50)
    print("CALL STATUS")
    print("Status:", status)
    print("Call SID:", call_sid)
    print("=" * 50)

    if status == "completed":
        end_delivery_call(
            conversation_id=call_sid
        )

    return {"success": True}