import sys
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import StorageContext, load_index_from_storage
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model
from exception import customexception
from logger import logging

def download_gemini_embedding(model, documents):
    """
    Downloads and initializes a Gemini Embedding model for vector embeddings.

    Parameters:
    - model: The language model to be used for embeddings.
    - documents: A list of Document objects to process into embeddings.

    Returns:
    - A query engine initialized with the created vector store index.
    """
    try:
        logging.info("Initializing Gemini Embedding model...")
        gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")
        Settings.llm = model
        Settings.embed_model = gemini_embed_model
        Settings.chunk_size = 800
        Settings.chunk_overlap = 20

        logging.info("Processing documents into embeddings...")

        # Create the index from the documents
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist()

        logging.info("Embedding index created successfully.")
        query_engine = index.as_query_engine()
        return query_engine

    except Exception as e:
        logging.error("An error occurred during the embedding process.", exc_info=True)
        raise customexception(e, sys)
