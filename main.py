from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from groq_service import ask_groq
from ollama_service import ask_ollama
from document_service import ingest_document
from vector_store import query_rag
import logging
from utils import log_event

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic model for chat request
class ChatRequest(BaseModel):
    query: str
    model: str  # 'groq' or 'ollama'


# Optionally, model for upload metadata validation
class UploadMetadata(BaseModel):
    semester: constr(strip_whitespace=True, min_length=1, max_length=10)
    subject: constr(strip_whitespace=True, min_length=1, max_length=50)


app = FastAPI(title="StudyPal Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production for security
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/upload", tags=["Documents"], summary="Upload study materials")
async def upload(
        file: UploadFile = File(...),
        semester: str = Form(...),
        subject: str = Form(...)
):
    # Validate semester and subject using UploadMetadata
    try:
        meta = UploadMetadata(semester=semester, subject=subject)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid semester or subject: {e}")

    logger.info(f"Received upload request: {file.filename}, semester: {meta.semester}, subject: {meta.subject}")

    # Reset file pointer before ingestion
    file.file.seek(0)

    result = ingest_document(file, meta.semester, meta.subject)
    log_event(f"Upload - {file.filename} for {meta.semester}/{meta.subject}")

    if "❌" in result.get("status", ""):
        raise HTTPException(status_code=400, detail=result.get("status"))

    return result


@app.post("/chat", tags=["Chat"], summary="Ask a question to the model")
async def chat(req: ChatRequest):
    logger.info(f"Received chat query for model '{req.model}': {req.query}")
    log_event(f"Chat query - Model: {req.model} - Query: {req.query}")

    if req.model not in ["groq", "ollama"]:
        logger.warning(f"Invalid model requested: {req.model}")
        raise HTTPException(status_code=400, detail="Invalid model specified. Choose 'groq' or 'ollama'.")

    # Query without chunk-based RAG
    context = query_rag(req.query)

    try:
        if req.model == "groq":
            response = ask_groq(req.query, context)
        else:
            response = ask_ollama(req.query, context)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error generating model response: {e}")
        raise HTTPException(status_code=500, detail="Error generating response from model.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
