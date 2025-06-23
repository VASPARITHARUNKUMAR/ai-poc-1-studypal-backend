from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq_service import ask_groq
from ollama_service import ask_ollama

class ChatRequest(BaseModel):
    query: str
    model: str  # "groq" or "ollama"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(req: ChatRequest):
    if req.model == "groq":
        return {"response": ask_groq(req.query)}
    elif req.model == "ollama":
        return {"response": ask_ollama(req.query)}
    else:
        return {"response": f"❌ Invalid model selected: {req.model}"}
