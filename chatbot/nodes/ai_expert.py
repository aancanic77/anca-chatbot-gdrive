from chatbot.schema import ChatState
from groq import Groq

def node_ai_expert(state: ChatState, client: Groq) -> ChatState:
    response = client.chat.completions.create(
        model="llama-3-8b-8192",
        messages=state["messages"]
    )
    state["messages"].append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    return state
