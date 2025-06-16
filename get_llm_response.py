#from dotenv import load_dotenv
#from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

#load_dotenv()

#llm = ChatGroq(
#   model="llama-3.1-8b-instant",
#    temperature=0,
#    max_tokens=None,
#    timeout=None,
#    max_retries=2
#)

llm=ChatOllama(
    model= "deepseek-r1:1.5b",
    temperature=0
)

def get_answer(question):
    answer= llm.invoke(question)
    answer= answer.content
    return answer
