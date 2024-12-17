import sys
import os
import tempfile
import streamlit as st

# Add your custom imports incrementally
# from QAWithPDF.data_ingestion import load_data
# from QAWithPDF.embedding import download_gemini_embedding
# from QAWithPDF.model_api import load_model


def main():
    st.set_page_config(page_title="QA with Documents", layout="centered")
    st.title("QA with Documents (Debug Test)")

    uploaded_file = st.file_uploader("Upload your document (PDF format)", type=["pdf"])

    if uploaded_file:
        st.write("File uploaded successfully.")
        st.write(f"Uploaded file name: {uploaded_file.name}")

if __name__ == "__main__":
    main()
