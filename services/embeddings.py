from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from some_model import get_embedding_model

def generate_embeddings(file_path):
    loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, overlap=50)
    chunks = splitter.split_documents(docs)
    embed_model = get_embedding_model()
    vectordb = Chroma.from_documents(chunks, embed_model, collection_name="studypal")
    return {"chunks": len(chunks)}
