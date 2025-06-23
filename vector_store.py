from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
chroma = Chroma(persist_directory="db", embedding_function=embedding)


def save_to_vector_store(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(documents)
    chroma.add_documents(splits)
    chroma.persist()


def query_rag(query):
    retriever = chroma.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)
    return "\n".join([d.page_content for d in docs])
