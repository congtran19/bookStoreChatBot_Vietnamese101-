
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import os, json, uuid
from typing import Optional
from LLM.core.chat_engine import ChatEngine

app = FastAPI(title="LLM API (integrated)")

# load config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

SERVER_API_KEY = os.environ.get("SERVER_API_KEY") or config.get("server_api_key")

HISTORY_DIR = os.path.join(BASE_DIR, "history")
os.makedirs(HISTORY_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    user: str
    session_id: Optional[str] = None
    model_id: Optional[str] = None
    prompt: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str

class SessionListResponse(BaseModel):
    user: str
    session_list : list


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(check_api_key)])
def chat(req: ChatRequest):
    

    return ChatResponse(session_id=session_id, reply=reply)

