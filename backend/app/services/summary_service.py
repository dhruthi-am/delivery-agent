from app.services.ai_service import client


def generate_summary(conversation):

    customer = conversation["customer"]
    platform = conversation["platform"]
    status = conversation["status"]
    intent = conversation["intent"]
    instruction = conversation["instruction"]
    messages = conversation["messages"]

    conversation_text = ""

    for message in messages:
        conversation_text += (
            f'{message["role"].capitalize()}: '
            f'{message["content"]}\n'
        )

    prompt = f"""
You are an AI Delivery Assistant.

Generate a WhatsApp message for the customer after the delivery call has ended.

Delivery Details

Customer: {customer}
Platform: {platform}
Verification Status: {status}
Final Delivery Instruction: {instruction}
Final Delivery Intent: {intent}

Conversation

{conversation_text}

Requirements

- Address the customer politely.
- Mention whether the order was successfully delivered or if further action is needed.
- Mention the verified delivery instruction only if it was actually followed.
- If the delivery could not be completed, clearly explain why.
- Mention pending actions only if they exist.
- Do not invent any information.
- Do not repeat the conversation.
- Do not mention internal AI decisions.
- Keep the message under 100 words.
- Generate only the WhatsApp message.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("=" * 50)
        print("SUMMARY GENERATION FAILED")
        print(e)
        print("Using fallback summary.")
        print("=" * 50)

        # Fallback summary
        if status == "Verified":

            if instruction:
                return (
                    f"Hi {customer},\n\n"
                    f"Your {platform} order has been verified.\n"
                    f"Delivery instruction: {instruction}"
                )

            return (
                f"Hi {customer},\n\n"
                f"Your {platform} order has been verified."
            )

        return (
            f"Hi {customer},\n\n"
            f"We could not complete verification for your {platform} order. "
            f"Please contact the delivery executive if further assistance is required."
        )