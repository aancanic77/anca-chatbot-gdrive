from typing import List, Dict, TypedDict

class ChatState(TypedDict):
    messages: List[Dict[str, str]]
    topic: str
    context: str
