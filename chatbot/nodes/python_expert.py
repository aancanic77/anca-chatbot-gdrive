from chatbot.schema import ChatState

def node_python_expert(state: ChatState) -> ChatState:
    state["messages"].append({
        "role": "assistant",
        "content": "Întrebarea ta este despre Python. Hai să vedem ce eroare ai și cum o rezolvăm."
    })
    return state
