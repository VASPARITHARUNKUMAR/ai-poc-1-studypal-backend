from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from some_llm_factory import get_llm

async def answer_query(question, semester, subject, model_name):
    vectordb = Chroma(collection_name="studypal")
    llm = get_llm(model_name)
    chain = RetrievalQA(llm=llm, retriever=vectordb.as_retriever())
    return chain.run(question)
