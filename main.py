from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services import document_service, chat_service
from models import DocumentUploadRequest, ChatRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), semester: str = Form(...), subject: str = Form(...)):
    return await document_service.process_upload(file, semester, subject)

@app.post("/chat")
async def chat(query: ChatRequest):
    return await chat_service.answer_question(query)
