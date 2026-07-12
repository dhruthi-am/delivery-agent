from app.memory.conversation_memory import (
    get_conversation,
    update_summary,
    clear_conversation
)

from app.services.summary_service import generate_summary
from app.services.whatsapp_service import send_whatsapp_message


def end_delivery_call(conversation_id: str):

    print("=" * 50)
    print("END DELIVERY CALL")
    print("Conversation ID:", conversation_id)

    conversation = get_conversation(conversation_id)

    print("Conversation:")
    print(conversation)
    print("=" * 50)

    # No active conversation
    if not conversation["messages"]:
        return {
            "status": "No Active Conversation",
            "message": "There is no conversation to summarize."
        }

    # Generate summary
    try:
        summary = generate_summary(conversation)
        print("Generated Summary:")
        print(summary)

    except Exception as e:
        return {
            "status": "Summary Generation Failed",
            "error": str(e)
        }

    # Save summary
    update_summary(
        conversation_id,
        summary
    )

    conversation = get_conversation(conversation_id)

    phone = conversation.get("phone")

    if not phone:
        return {
            "status": "Phone Number Missing",
            "summary": conversation["summary"]
        }
    print("=" * 50)
    print("Sending WhatsApp...")
    print("Phone:", phone)
    print("Summary:", conversation["summary"])
    print("=" * 50)
    whatsapp_result = send_whatsapp_message(
        phone,
        conversation["summary"]
    )

    print("=" * 50)
    print("WHATSAPP RESULT")
    print(whatsapp_result)
    print("=" * 50)

    result = {
        "status": "Call Ended",
        "customer": conversation["customer"],
        "platform": conversation["platform"],
        "phone": phone,
        "summary": conversation["summary"],
        "whatsapp": whatsapp_result
    }

    # Clear memory only if WhatsApp was sent successfully
    if whatsapp_result["success"]:
        clear_conversation(conversation_id)

    return result