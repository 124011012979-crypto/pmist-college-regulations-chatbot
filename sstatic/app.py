import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()  # reads the .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR)

API_KEY = os.getenv("API_KEY", "")
API_URL = os.getenv("API_URL", "https://api.groq.com/openai/v1/chat/completions")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

SYSTEM = (
    "You are the PMIST B.Tech Regulations R-2024 assistant. "
    "Answer ONLY using the CONTEXT given. Mention clause numbers like (R7.3) when present. "
    "Reply in the same style as the student's question (English, Tamil, or Tanglish). "
    "Keep it short and clear, use simple points if needed. "
    "If the context does not contain the answer, say it is not in the regulations I have "
    "and suggest asking the HoD or Dean (Academic Courses). Never invent rules or numbers."
)


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()[:500]
    context = (data.get("context") or "")[:6000]
    if not question:
        return jsonify(error="empty question"), 400
    if not API_KEY or API_KEY.startswith("paste_"):
        print("ERROR: put your real key in the .env file (API_KEY=...)")
        return jsonify(error="api key missing"), 500
    try:
        r = requests.post(
            API_URL,
            headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "temperature": 0.2,
                "max_tokens": 500,
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": "CONTEXT:\n" + context + "\n\nQUESTION: " + question},
                ],
            },
            timeout=30,
        )
        if r.status_code != 200:
            print("AI error", r.status_code, r.text[:300])
            return jsonify(error="ai failed"), 502
        return jsonify(answer=r.json()["choices"][0]["message"]["content"].strip())
    except Exception as e:
        print("AI error:", e)
        return jsonify(error="ai failed"), 502


if __name__ == "__main__":
    app.run(debug=True)
