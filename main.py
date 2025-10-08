#viết api cho tôi 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.react_agents import ReActAgent
from core.model_factory import ModelFactory
from core.tool import SearchBookTool, OrderBookTool
from database.database_manager import Database_Manager
from typing import List, Dict, Any  
import uvicorn
import json
from pathlib import Path        

app = FastAPI()
db = Database_Manager()
tools = {
    "SearchBookTool": SearchBookTool(db),
    "OrderBookTool": OrderBookTool(db)
}
model = ModelFactory.create("model1")
ReActAgent = ReActAgent(model=model, tools=tools)   
class ChatRequest(BaseModel):
    message: str
class ChatResponse(BaseModel):
    reply: str
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = ReActAgent.run(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

