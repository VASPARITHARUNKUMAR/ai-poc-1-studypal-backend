from langchain_openai import ChatOpenAI
import os
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="vectordb", embedding_function=embedding)

llm = ChatOpenAI(
    model="mixtral-8x7b-32768",  # or "llama3-70b-8192" etc., based on what you want
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
    temperature=0.7
)

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

async def answer_question(query: str):
    return {"response": qa_chain.run(query)}
