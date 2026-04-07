from typing import List, Dict
from groq import Groq

from .schema import ChatState
from .nodes.check_topic import node_check_topic
from .nodes.google_drive_expert import node_google_drive_expert
from .nodes.ai_expert import node_ai_expert
from .nodes.moodle_expert import node_moodle_expert
from .nodes.python_expert import node_python_expert
from .nodes.fallback import node_fallback
from .nodes.intro import node_intro

def run_chat(messages: List[Dict[str, str]], client: Groq) -> List[Dict[str, str]]:
    state: ChatState = {
        "messages": messages.copy(),
        "topic": "other",
        "context": ""
    }

    state = node_check_topic(state)

    if state["topic"] == "google_drive":
        state = node_google_drive_expert(state)

    if state["topic"] == "ai":
        state = node_ai_expert(state, client)
    elif state["topic"] == "moodle":
        state = node_moodle_expert(state)
    elif state["topic"] == "python":
        state = node_python_expert(state)
    elif state["topic"] == "google_drive":
        state = node_ai_expert(state, client)
    else:
        state = node_fallback(state)

    return state["messages"]
