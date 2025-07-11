import os
from fastapi import UploadFile
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredExcelLoader,
    UnstructuredPowerPointLoader, UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader,
    UnstructuredFileLoader, UnstructuredImageLoader, CSVLoader
)
from vector_store import save_to_vector_store

# Set max upload size (in MB)
MAX_FILE_SIZE_MB = 10

# Supported file extensions
ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".pptx", ".xlsx", ".csv", ".md", ".txt",
    ".jpg", ".jpeg", ".png"
}

def ingest_document(file: UploadFile, semester: str, subject: str):
    ext = os.path.splitext(file.filename)[1].lower()

    # Check file extension
    if ext not in ALLOWED_EXTENSIONS:
        return {"status": "❌ File type not supported", "extension": ext}

    # Create folder path
    folder = f"uploads/{semester}/{subject}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.filename)

    # Read and validate file size
    contents = file.file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return {"status": f"❌ File too large. Limit is {MAX_FILE_SIZE_MB} MB", "size_mb": f"{file_size_mb:.2f} MB"}

    # Save file
    with open(path, "wb") as f:
        f.write(contents)
    file.file.close()

    # Load document based on file extension
    try:
        if ext == ".pdf":
            docs = PyPDFLoader(path).load()
        elif ext == ".docx":
            docs = Docx2txtLoader(path).load()
        elif ext == ".doc":
            docs = UnstructuredWordDocumentLoader(path).load()
        elif ext == ".pptx":
            docs = UnstructuredPowerPointLoader(path).load()
        elif ext == ".xlsx":
            docs = UnstructuredExcelLoader(path).load()
        elif ext == ".csv":
            docs = CSVLoader(file_path=path).load()
        elif ext == ".md":
            docs = UnstructuredMarkdownLoader(path).load()
        elif ext in [".jpg", ".jpeg", ".png"]:
            docs = UnstructuredImageLoader(path).load()
        elif ext == ".txt":
            docs = TextLoader(path).load()
        else:
            docs = UnstructuredFileLoader(path).load()
    except Exception as e:
        return {"status": "❌ Failed to process document", "error": str(e)}

    # Save embeddings to vector store
    save_to_vector_store(docs)
    return {"status": "✅ Document uploaded and processed.", "file": file.filename, "size": f"{file_size_mb:.2f} MB"}
