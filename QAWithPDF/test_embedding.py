import sys
import os
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model


try:
    # Load model
    print("Loading model...")
    model = load_model()
    print("Model loaded successfully.")

    # Load documents from the specified directory
    data_directory = "path_to_your_data_directory"  # Update this path accordingly
    print(f"Loading documents from directory: {data_directory}")
    documents = load_data(data_directory)
    print(f"{len(documents)} documents loaded successfully.")

    # Test embedding functionality
    print("Testing embedding functionality...")
    query_engine = download_gemini_embedding(model, documents)
    print("Embedding index created successfully.")

    # Query the engine with a sample question
    user_question = "Your sample question here"  # Update this question accordingly
    print(f"Querying: {user_question}")
    response = query_engine.query(user_question)
    print("Query response:", response.response)

except Exception as e:
    print("Error occurred:", e)
