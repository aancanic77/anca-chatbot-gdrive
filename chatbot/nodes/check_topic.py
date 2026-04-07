from chatbot.schema import ChatState

def node_check_topic(state: ChatState) -> ChatState:
    last = state["messages"][-1]["content"].lower()

    if any(k in last for k in ["ai", "model", "llm", "langgraph"]):
        state["topic"] = "ai"
    elif any(k in last for k in ["moodle", "quiz", "lesson", "forum"]):
        state["topic"] = "moodle"
    elif any(k in last for k in ["python", "eroare", "script"]):
        state["topic"] = "python"
    elif any(k in last for k in ["google drive", "document", "claritate"]):
        state["topic"] = "google_drive"
    else:
        state["topic"] = "other"

    return state
