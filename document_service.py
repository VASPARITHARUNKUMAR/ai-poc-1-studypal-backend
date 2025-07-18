import os
import logging
from fastapi import UploadFile
from langchain_community.document_loaders import (
    TextLoader, Docx2txtLoader, UnstructuredExcelLoader,
    UnstructuredPowerPointLoader, UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader,
    UnstructuredFileLoader, UnstructuredImageLoader, CSVLoader,
)
from langchain_community.document_loaders import PDFMinerLoader
from vector_store import save_to_vector_store

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".pptx", ".xlsx", ".csv", ".md", ".txt",
    ".jpg", ".jpeg", ".png"
}

logger = logging.getLogger(__name__)

def ingest_document(file: UploadFile, semester: str, subject: str):
    logger.info(f"Starting ingest_document for file: {file.filename}")
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"File type not supported: {ext}")
        return {"status": "❌ File type not supported", "extension": ext}

    folder = f"uploads/{semester}/{subject}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.filename)

    contents = file.file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        logger.warning(f"File too large: {file_size_mb:.2f} MB")
        return {"status": f"❌ File too large. Limit is {MAX_FILE_SIZE_MB} MB", "size_mb": f"{file_size_mb:.2f} MB"}

    with open(path, "wb") as f:
        f.write(contents)

    # Ensure file is closed no matter what
    try:
        if ext == ".pdf":
            docs = PDFMinerLoader(path).load()
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
        logger.info(f"Loaded {len(docs)} documents from file")
    except Exception as e:
        logger.error(f"Failed to process document: {e}", exc_info=True)
        return {"status": "❌ Failed to process document", "error": str(e)}
    finally:
        file.file.close()

    try:
        save_to_vector_store(docs)
        logger.info("Saved embeddings to vector store")
    except Exception as e:
        logger.error(f"Failed to save embeddings: {e}", exc_info=True)
        return {"status": "❌ Failed to save embeddings", "error": str(e)}

    return {"status": "✅ Document uploaded and processed.", "file": file.filename, "size": f"{file_size_mb:.2f} MB"}
