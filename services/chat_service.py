from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI, Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
CHROMA_DIR = "./vectordb"

# Switch model provider here
USE_LOCAL = True
llm = Ollama(model="llama2") if USE_LOCAL else OpenAI()

vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

async def answer_question(query_obj):
    answer = qa.run(query_obj.query)
    return {"response": answer}