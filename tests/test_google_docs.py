from groq import Groq
from chatbot.graph import run_chat
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def main():
    question = "Ce înseamnă claritate în documentul Google Drive?"
    messages = [{"role": "user", "content": question}]
    result = run_chat(messages, client)

    for msg in result:
        print(f"{msg['role']}: {msg['content']}\n")

if __name__ == "__main__":
    main()
