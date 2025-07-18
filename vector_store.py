import logging
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # Use langchain_huggingface per deprecation warnings

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup embedding model (updated import and usage)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Chroma vector store (empty at start)
# You can instantiate this here or inside save function if you want to reload each time.
chroma_store = None

def save_to_vector_store(documents: List) -> None:
    """
    Save documents directly to the Chroma vector store without chunking.

    Args:
        documents (List[Document]): List of LangChain Document objects.
    """
    global chroma_store
    try:
        logger.info("Saving documents directly to vector store without chunking...")
        # Create a new vector store from documents and embeddings
        chroma_store = Chroma.from_documents(documents, embedding)
        logger.info(f"Saved {len(documents)} documents to Chroma vector store.")
        # Note: No need to call persist() with this Chroma version
    except Exception as e:
        logger.error(f"Failed to save documents to vector store: {e}", exc_info=True)
        raise

def query_rag(query: str, top_k: int = 3) -> str:
    global chroma_store
    if chroma_store is None:
        logger.error("Vector store is not initialized. Please add documents first.")
        return "Vector store not initialized."

    try:
        logger.info(f"Querying vector store with query: '{query}'")
        retriever = chroma_store.as_retriever(search_kwargs={"k": top_k})
        # Use get_relevant_documents to fetch documents
        docs = retriever.get_relevant_documents(query)

        logger.info(f"Retrieved {len(docs)} documents.")
        return "\n".join(doc.page_content for doc in docs)

    except Exception as e:
        logger.error(f"Vector store query failed: {e}", exc_info=True)
        return "An error occurred during retrieval."
