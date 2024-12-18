import os
import sys
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file.docs import DocxReader
from llama_index.readers.json import JSONReader
from exception import customexception
from logger import logging

def load_data(data_dir):
    """
    Load documents from a specified directory. Supports PDF, TXT, DOCX, and JSON formats.

    Parameters:
    - data_dir (str): The path to the directory containing documents.

    Returns:
    - A list of loaded Document objects.
    """
    try:
        logging.info("Data loading started...")
        logging.info("Supported file formats: PDF, TXT, DOCX, JSON.")

        # Resolve the absolute path for the given directory
        data_path = os.path.abspath(data_dir)

        if not os.path.exists(data_path):
            logging.error(f"The specified directory '{data_path}' does not exist.")
            raise FileNotFoundError(f"The directory '{data_path}' does not exist.")

        documents = []

        # Process TXT and PDF files using SimpleDirectoryReader
        txt_pdf_files = [file for file in os.listdir(data_path) if file.endswith((".txt", ".pdf"))]
        if txt_pdf_files:
            logging.info("Using SimpleDirectoryReader for TXT and PDF files...")
            loader = SimpleDirectoryReader(input_dir=data_path, required_exts=[".txt", ".pdf"])
            documents.extend(loader.load_data())

        # Process DOCX files using DocxReader
        docx_reader = DocxReader()
        for file in os.listdir(data_path):
            if file.endswith(".docx"):
                file_path = os.path.join(data_path, file)
                logging.info(f"Using DocxReader to load DOCX file: {file_path}")
                documents.extend(docx_reader.load_data(file_path))

        # Process JSON files using JSONReader
        json_reader = JSONReader()
        for file in os.listdir(data_path):
            if file.endswith(".json"):
                file_path = os.path.join(data_path, file)
                logging.info(f"Using JSONReader to load JSON file: {file_path}")
                documents.extend(json_reader.load_data(input_file=file_path, extra_info={}))

        if not documents:
            logging.error("No valid documents found in the specified directory.")
            raise ValueError("No valid documents to load.")

        logging.info(f"Data loading completed successfully. {len(documents)} document(s) loaded.")
        return documents

    except Exception as e:
        logging.error("An exception occurred during data loading.", exc_info=True)
        raise customexception(e, sys)
