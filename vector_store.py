import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load embedding model
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Chroma store placeholder
chroma_store = None

def save_to_vector_store(documents: List[Document]) -> None:
    """
    Save raw documents directly to the Chroma vector store without any chunking.

    Args:
        documents (List[Document]): List of LangChain Document objects.
    """
    global chroma_store
    try:
        logger.info("Saving raw documents to vector store...")
        chroma_store = Chroma.from_documents(documents, embedding)
        logger.info(f"Saved {len(documents)} documents to Chroma vector store.")
    except Exception as e:
        logger.error(f"Error saving documents: {e}", exc_info=True)
        raise

def query_rag(query: str, top_k: int = 3) -> str:
    """
    Retrieve top_k relevant documents for the given query.

    Args:
        query (str): Natural language query.
        top_k (int): Number of top results to retrieve.

    Returns:
        str: Concatenated content of top-k documents.
    """
    global chroma_store
    if chroma_store is None:
        logger.error("Chroma vector store is not initialized.")
        return "Vector store not initialized."

    try:
        logger.info(f"Querying vector store with: '{query}'")
        retriever = chroma_store.as_retriever(search_kwargs={"k": top_k})
        docs = retriever.get_relevant_documents(query)
        logger.info(f"Retrieved {len(docs)} documents.")
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        logger.error(f"Failed to retrieve documents: {e}", exc_info=True)
        return "Error during query."
