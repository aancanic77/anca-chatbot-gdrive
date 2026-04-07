import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from groq import Groq
from chatbot.graph import run_chat
load_dotenv()
app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message","").strip()
    messages=[{"role":"user","content":user_message}]
    result=run_chat(messages,client)
    return jsonify({"messages":result})
if __name__=="__main__":
    app.run(debug=True)
