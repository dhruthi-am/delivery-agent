import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_response(conversation):

    customer = conversation["customer"]
    platform = conversation["platform"]
    intent = conversation["intent"]
    status = conversation["status"]
    summary = conversation["summary"]
    messages = conversation["messages"]
    order = conversation.get("order")

    # ----------------------------------
    # Build Order Details
    # ----------------------------------

    if order:

        order_details = f"""

Customer: {order["customer"]}
Platform: {order["platform"]}
Payment: {order["payment"]}
Instruction: {order["instruction"]}
"""

    else:

        order_details = """
No verified order was found.
"""

    # ----------------------------------
    # Build Conversation History
    # ----------------------------------

    conversation_history = ""

    if summary:

        conversation_history += (
            "Previous Summary:\n"
            f"{summary}\n\n"
        )

    conversation_history += "Recent Conversation:\n\n"

    for message in messages:

        conversation_history += (
            f'{message["role"].capitalize()}: '
            f'{message["content"]}\n'
        )

    # ----------------------------------
    # Load Prompt Template
    # ----------------------------------

    with open(
        "app/prompts/delivery_prompt.txt",
        "r",
        encoding="utf-8"
    ) as file:

        template = file.read()

    prompt = template.format(
        customer=customer,
        platform=platform,
        intent=intent,
        status=status,
        summary=summary or "No previous conversation summary.",
        order_details=order_details,
        conversation_history=conversation_history
)

    # ----------------------------------
    # Gemini Response
    # ----------------------------------

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()