from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Educational Tutor Chatbot")

# In-memory chat sessions
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

# System prompt
SYSTEM_PROMPT = "You are a helpful, accurate educator tutor."

# API settings
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "deepseek/deepseek-r1-distill-llama-70b:free"

# Request model
class ChatRequest(BaseModel):
    session_id: Optional[str] = None  # ✅ Optional string — allows None
    message: str

# Response model
class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: List[Dict[str, str]]

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Educational Tutor Chatbot is running."}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    user_message = request.message

    # Start new session if needed
    if session_id not in chat_sessions:
        chat_sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Append user's message
    chat_sessions[session_id].append({"role": "user", "content": user_message})

    # Prepare request to OpenRouter
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": chat_sessions[session_id],
        "temperature": 0.7
    }

    # Call OpenRouter API
    async with httpx.AsyncClient() as client:
        response = await client.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        assistant_reply = result["choices"][0]["message"]["content"]

    # Append assistant reply to history
    chat_sessions[session_id].append({"role": "assistant", "content": assistant_reply})

    return ChatResponse(
        session_id=session_id,
        response=assistant_reply,
        history=chat_sessions[session_id]
    )
