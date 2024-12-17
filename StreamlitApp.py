import os
import tempfile
import streamlit as st
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file.docs import DocxReader
from llama_index.readers.json import JSONReader
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

def process_document(file_path, temp_dir):
    """
    Process the uploaded file based on its extension.
    """
    if file_path.endswith(".docx"):
        # Use DocxReader for DOCX files
        st.info("Using DocxReader to process DOCX file...")
        docx_reader = DocxReader()
        return docx_reader.load_data(file_path)

    elif file_path.endswith(".json"):
        # Use JSONReader for JSON files
        st.info("Using JSONReader to process JSON file...")
        json_reader = JSONReader()
        return json_reader.load_data(input_file=file_path, extra_info={})

    else:
        # Use SimpleDirectoryReader for TXT and PDF
        st.info("Using SimpleDirectoryReader for PDF/TXT files...")
        loader = SimpleDirectoryReader(input_dir=temp_dir, required_exts=[".txt", ".pdf"])
        return loader.load_data()

# Streamlit UI
st.title("Ask Your Question")

uploaded_file = st.file_uploader("Upload your document (PDF, TXT, DOCX, JSON)", type=["pdf", "txt", "docx", "json"])

if uploaded_file:
    st.info(f"Document '{uploaded_file.name}' successfully uploaded!")

    try:
        with st.spinner("Loading data from the document..."):
            # Save the uploaded file
            file_path, temp_dir = save_uploaded_file(uploaded_file)

            # Process the document based on its type
            documents = process_document(file_path, temp_dir)

            # Load model and create embeddings
            model = load_model()
            query_engine = download_gemini_embedding(model, documents)

            st.success("Document processed successfully! Enter your question below.")

            # User input for querying
            query = st.text_input("Enter your question:")
            if st.button("Submit & Process"):
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
