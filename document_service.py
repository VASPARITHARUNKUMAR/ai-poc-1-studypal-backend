import os
import uuid
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from backend.services.vector_service import store_in_vector_db

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_upload(file, semester, subject):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    ext = file.filename.split(".")[-1].lower()
    if ext == "pdf":
        loader = PyPDFLoader(file_path)
    elif ext == "docx":
        loader = Docx2txtLoader(file_path)
    elif ext == "txt":
        loader = TextLoader(file_path)
    else:
        return {"status": "Unsupported format"}

    documents = loader.load()
    store_in_vector_db(documents, semester, subject)
    return {"status": "Uploaded successfully"}