# test_chat.py
import requests

url = "http://localhost:8000/chat"
session_id = None

print("💬 Educational Tutor Chatbot (type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting chatbot.")
        break

    payload = {"message": user_input}
    if session_id:
        payload["session_id"] = session_id

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        session_id = data["session_id"]
        print("Tutor:", data["response"])
    else:
        print("❌ Error:", response.status_code, response.text)
