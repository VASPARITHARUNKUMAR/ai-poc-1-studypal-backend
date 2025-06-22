import os
import uuid
from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from .vector_service import store_in_vector_db

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def get_extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return os.path.splitext(filename)[1].lower()

async def process_upload(file, semester, subject):
    original_filename = file.filename
    print(f"Received file: {original_filename}")  # 🔍 Debug

    ext = get_extension(original_filename)
    print(f"File extension: {ext}")  # 🔍 Debug

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {ext}")

    # Save file
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}_{original_filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Choose appropriate loader
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise HTTPException(status_code=400, detail=f"Unexpected error for extension: {ext}")

    # Load and store
    documents = loader.load()
    store_in_vector_db(documents, semester, subject)

    return {"status": "Uploaded successfully"}
async def process_upload(file, semester, subject):
    print(f"[DEBUG] Raw filename: {file.filename}")
    print(f"[DEBUG] Content type: {file.content_type}")

    if not file.filename:
        return {"status": "Filename missing from uploaded file!"}

    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1].lower()
    print(f"[DEBUG] Extracted extension: {ext}")

    if ext not in [".pdf", ".docx", ".txt"]:
        return {"status": f"Unsupported format: {ext}"}

    # Save the file
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f_out:
        f_out.write(await file.read())

    # Pick loader
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        return {"status": f"Unexpected error with format: {ext}"}

    documents = loader.load()
    store_in_vector_db(documents, semester, subject)
    return {"status": "Uploaded successfully"}
