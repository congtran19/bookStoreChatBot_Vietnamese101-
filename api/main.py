from fastapi import FastAPI
from core.react_agents import ReActAgent
from core.model_factory import ModelFactory
from core.chat_engine import ChatEngine

app = FastAPI()

@app.post("/chat")
def chat_api(request: dict):
    user_input = request.get("message", "")
    reply = engine.chat(user_input)
    return {"reply": reply}