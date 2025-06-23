import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from vector_store import save_to_vector_store


def ingest_document(file, semester, subject):
    folder = f"uploads/{semester}/{subject}"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.filename)

    # read the upload file correctly
    contents = file.file.read()
    with open(path, "wb") as f:
        f.write(contents)
    file.file.close()

    # Load documents based on file type
    if path.endswith(".pdf"):
        docs = PyPDFLoader(path).load()
    elif path.endswith(".docx"):
        docs = Docx2txtLoader(path).load()
    else:
        docs = TextLoader(path).load()

    save_to_vector_store(docs)
    return {"status": "✅ Document uploaded and processed."}
