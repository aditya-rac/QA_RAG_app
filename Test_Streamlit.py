import os
import sys
import tempfile
import streamlit as st

# Import the modular components
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model
from exception import customexception


def save_uploaded_file(uploaded_file):
    """
    Save the uploaded file to a temporary directory and return the file path.
    """
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path, temp_dir


def main():
    st.set_page_config(page_title="QA with Documents", layout="centered")
    st.title("QA with Documents (Debug Test)")

    uploaded_file = st.file_uploader("Upload your document (PDF, TXT, DOCX, JSON)", type=["pdf", "txt", "docx", "json"])

    if uploaded_file:
        st.success("File uploaded successfully!")
        st.write(f"Uploaded file name: **{uploaded_file.name}**")

        try:
            with st.spinner("Processing file..."):
                # Save the uploaded file
                file_path, temp_dir = save_uploaded_file(uploaded_file)

                # Load the data using load_data from data_ingestion.py
                st.info("Loading document data...")
                documents = load_data(temp_dir)
                st.write(f"**Loaded {len(documents)} document(s).**")

                # Load the model using load_model from model_api.py
                st.info("Loading Gemini-Pro model...")
                model = load_model()

                # Generate embeddings using download_gemini_embedding
                st.info("Generating embeddings and initializing query engine...")
                query_engine = download_gemini_embedding(model, documents)

                st.success("Document processed successfully! Ready for queries.")

                # User input for querying the document
                query = st.text_input("Enter your question:")
                if st.button("Submit Query"):
                    with st.spinner("Processing your query..."):
                        response = query_engine.query(query)
                        if "|" in response.response:
                            # Render table-like content as Markdown
                            st.markdown(response.response, unsafe_allow_html=True)
                        else:
                            # Render plain text responses
                            st.write("Response:", response.response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write("Check the logs for more details.")


if __name__ == "__main__":
    main()
