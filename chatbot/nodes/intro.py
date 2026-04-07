from chatbot.schema import ChatState

def node_intro(state: ChatState) -> ChatState:
    state["messages"].insert(0, {
        "role": "system",
        "content": "Ești un profesor de AI și Moodle, calm și clar."
    })
    return state
