import logging
from typing import List
from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup embedding and vectorstore
embedding_model = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
chroma_store = Chroma(persist_directory="db", embedding_function=embedding_model)

def save_to_vector_store(documents):
    try:
        print("Saving documents directly to vector store without chunking...")
        chroma_store = Chroma.from_documents(documents, embedding)
        # chroma_store.persist()  # ❌ REMOVE or COMMENT this line
    except Exception as e:
        print(f"Failed to save documents to vector store: {e}")
        raise
def query_rag(query: str, top_k: int = 3) -> str:
    """
    Retrieves relevant documents from vector store using the query.

    Args:
        query (str): The query string.
        top_k (int): Number of top documents to retrieve.

    Returns:
        str: Concatenated contents of relevant documents.
    """
    try:
        logger.info(f"Querying vector store with query: '{query}'")
        retriever = chroma_store.as_retriever(search_kwargs={"k": top_k})

        # Correct way to call retriever per latest LangChain version
        docs = retriever.invoke(query)  # or docs = retriever(query)

        logger.info(f"Retrieved {len(docs)} documents.")
        return "\n".join(doc.page_content for doc in docs)

    except Exception as e:
        logger.error(f"Vector store query failed: {e}", exc_info=True)
        return "An error occurred during retrieval."
