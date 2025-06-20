from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHROMA_DIR = "./vectordb"
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def store_in_vector_db(documents, semester, subject):
    texts = text_splitter.split_documents(documents)
    Chroma.from_documents(texts, embedding, persist_directory=CHROMA_DIR).persist()