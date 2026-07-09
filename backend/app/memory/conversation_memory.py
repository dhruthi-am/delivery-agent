# Stores all active conversations in memory
conversations = {}


def get_conversation(conversation_id: str):
    """
    Returns an existing conversation.
    Creates a new one if it doesn't exist.
    """

    if conversation_id not in conversations:

        conversations[conversation_id] = {
            "customer": None,
            "platform": None,
            "phone": None,
            "payment": None,
            "status": None,
            "instruction": None,
            "intent": None,
            "summary": None,
            "order": None,
            "messages": []
        }

    return conversations[conversation_id]


def update_conversation(
    conversation_id: str,
    key: str,
    value
):
    """
    Updates a single field in the conversation.
    Example:
    customer = Dhruthi
    platform = Amazon
    """

    conversation = get_conversation(conversation_id)

    conversation[key] = value


def add_message(
    conversation_id: str,
    role: str,
    content: str
):
    """
    Stores each message exchanged during the conversation.
    """

    conversation = get_conversation(conversation_id)

    conversation["messages"].append(
        {
            "role": role,
            "content": content
        }
    )


def clear_conversation(conversation_id: str):
    """
    Removes a conversation after it has been
    summarized and saved.
    """

    if conversation_id in conversations:

        del conversations[conversation_id]

def update_summary(
    conversation_id: str,
    summary: str
):

    conversation = get_conversation(conversation_id)

    conversation["summary"] = summary

def trim_messages(
    conversation_id: str,
    keep_last: int = 6
):

    conversation = get_conversation(conversation_id)

    conversation["messages"] = conversation["messages"][-keep_last:]