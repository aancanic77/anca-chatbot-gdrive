from chatbot.schema import ChatState

def node_fallback(state: ChatState) -> ChatState:
    state["messages"].append({
        "role": "assistant",
        "content": "Nu sunt sigur că am înțeles întrebarea. O poți reformula?"
    })
    return state
