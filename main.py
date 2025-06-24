import certifi
import os
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq_service import ask_groq
from ollama_service import ask_ollama
from document_service import ingest_document
from vector_store import query_rag
import os
os.environ["CURL_CA_BUNDLE"] = ""

class ChatRequest(BaseModel):
    query: str
    model: str  # groq or ollama

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/upload")
async def upload(file: UploadFile = File(...), semester: str = Form(...), subject: str = Form(...)):
    return ingest_document(file, semester, subject)

@app.post("/chat")
async def chat(req: ChatRequest):
    if req.model in ["groq", "ollama"]:
        context = query_rag(req.query)
        if req.model == "groq":
            return {"response": ask_groq(req.query, context)}
        else:
            return {"response": ask_ollama(req.query, context)}
    return {"response": "Invalid model"}
