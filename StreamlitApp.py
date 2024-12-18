import os
import tempfile
import streamlit as st
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

# Streamlit UI
st.title("Ask Your Question")

uploaded_file = st.file_uploader("Upload your document (PDF, TXT, DOCX, JSON)", type=["pdf", "txt", "docx", "json"])

if uploaded_file:
    st.info(f"Document '{uploaded_file.name}' successfully uploaded!")

    try:
        with st.spinner("Loading data from the document..."):
            # Save the uploaded file
            file_path, temp_dir = save_uploaded_file(uploaded_file)

            # Use load_data from data_ingestion.py to process documents
            documents = load_data(temp_dir)

            # Load the model and create embeddings
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
