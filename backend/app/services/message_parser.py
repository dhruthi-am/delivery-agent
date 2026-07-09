import json
from app.services.ai_service import client


def extract_details(message: str, conversation: dict):

    with open(
        "app/prompts/parse_prompt.txt",
        "r",
        encoding="utf-8"
    ) as file:
        template = file.read()

    prompt = template.format(
        message=message,
        customer=conversation.get("customer"),
        platform=conversation.get("platform"),
        intent=conversation.get("intent")
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        text = response.text.strip()

        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1]).strip()

        details = json.loads(text)

    except Exception:
        details = {
            "customer": None,
            "platform": None,
            "intent": "UNKNOWN"
        }

    return details