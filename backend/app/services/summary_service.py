from app.services.ai_service import client


def generate_summary(conversation):

    customer = conversation["customer"]
    platform = conversation["platform"]
    status = conversation["status"]
    intent = conversation["intent"]
    instruction = conversation["instruction"]
    messages = conversation["messages"]

    # Build conversation history
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text