from app.memory.conversation_memory import (
    add_message,
    get_conversation,
    update_conversation
)

from app.services.message_parser import extract_details
from app.services.order_service import verify_order
from app.services.decision_service import decide_delivery_action
from app.services.ai_service import generate_response


def handle_delivery_call(
    conversation_id: str,
    message: str
):

    # ---------------------------------
    # Load conversation
    # ---------------------------------

    conversation = get_conversation(conversation_id)

    add_message(
        conversation_id,
        "executive",
        message
    )

    # Refresh
    conversation = get_conversation(conversation_id)

    # ---------------------------------
    # Parse latest message
    # ---------------------------------

    details = extract_details(message, conversation)

    # ---------------------------------
    # Update memory with NEW information
    # ---------------------------------

    if details["customer"] is not None:
        update_conversation(
            conversation_id,
            "customer",
            details["customer"]
        )

    if details["platform"] is not None:
        update_conversation(
            conversation_id,
            "platform",
            details["platform"]
        )

    update_conversation(
        conversation_id,
        "intent",
        details["intent"]
    )

    # Refresh after updating memory
    conversation = get_conversation(conversation_id)

    customer = conversation["customer"]
    platform = conversation["platform"]

    # ---------------------------------
    # Verify order only if needed
    # ---------------------------------

    if (
        conversation.get("order") is None
        and customer is not None
        and platform is not None
    ):

        order = verify_order(
            customer,
            platform
        )

        if order is not None:

            update_conversation(
                conversation_id,
                "order",
                order
            )

            update_conversation(
                conversation_id,
                "phone",
                order["phone"]
            )

            

            update_conversation(
                conversation_id,
                "payment",
                order["payment"]
            )

            update_conversation(
                conversation_id,
                "instruction",
                order["instruction"]
            )

        # Refresh
        conversation = get_conversation(conversation_id)

    # ---------------------------------
    # Read verified order from memory
    # ---------------------------------

    order = conversation.get("order")

    decision = decide_delivery_action(order)

    update_conversation(
        conversation_id,
        "status",
        decision["status"]
    )

    update_conversation(
        conversation_id,
        "instruction",
        decision["instruction"]
    )

    # Refresh
    conversation = get_conversation(conversation_id)

    # ---------------------------------
    # Generate AI reply
    # ---------------------------------

    ai_reply = generate_response(conversation)

    add_message(
        conversation_id,
        "assistant",
        ai_reply
    )

    conversation = get_conversation(conversation_id)

    return {
        "customer": conversation["customer"],
        "platform": conversation["platform"],
        "status": conversation["status"],
        "instruction": conversation["instruction"],
        "ai_reply": ai_reply,
        "conversation": conversation
    }