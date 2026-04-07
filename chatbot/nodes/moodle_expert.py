from chatbot.schema import ChatState

def node_moodle_expert(state: ChatState) -> ChatState:
    state["messages"].append({
        "role": "assistant",
        "content": "Întrebarea ta este despre Moodle. Vrei să configurăm un quiz, un forum sau o lecție?"
    })
    return state
