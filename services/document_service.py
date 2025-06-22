import os
import uuid
from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from .vector_service import store_in_vector_db

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def get_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

async def process_upload(file, semester, subject):
    original_filename = file.filename
    ext = get_extension(original_filename)

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {ext}")

    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}_{original_filename}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load based on extension
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file format.")

        documents = loader.load()
        store_in_vector_db(documents, semester, subject)

        return {"status": "Uploaded successfully", "filename": saved_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
