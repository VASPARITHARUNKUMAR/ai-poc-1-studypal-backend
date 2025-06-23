from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from enum import Enum

from groq_service import ask_groq
from ollama_service import ask_ollama

class ModelName(str, Enum):
    groq = "groq"
    ollama = "ollama"

class ChatRequest(BaseModel):
    query: str
    model: ModelName

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(req: ChatRequest):
    loop = asyncio.get_running_loop()
    try:
        if req.model == ModelName.groq:
            response = await loop.run_in_executor(None, ask_groq, req.query)
        elif req.model == ModelName.ollama:
            response = await loop.run_in_executor(None, ask_ollama, req.query)
        else:
            raise HTTPException(status_code=400, detail="Invalid model selected")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling model: {str(e)}")
    return {"response": response}
