import os
from unittest.mock import patch
from QAWithPDF.data_ingestion import load_data

def setup_test_directory():
    """
    Sets up a test directory with sample files including TXT, PDF, DOCX, and JSON.
    """
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)

    # Create a sample TXT file
    with open(os.path.join(test_dir, "sample.txt"), "w") as f:
        f.write("This is a sample text file.")

    # Create a duplicate TXT file
    with open(os.path.join(test_dir, "duplicate.txt"), "w") as f:
        f.write("This is a duplicate text file.")

    # Create a sample DOCX file
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a sample DOCX file.")
    doc.save(os.path.join(test_dir, "sample.docx"))

    # Create a sample PDF file
    from PyPDF2 import PdfWriter
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=200, height=200)
    with open(os.path.join(test_dir, "sample.pdf"), "wb") as f:
        pdf_writer.write(f)

    # Create a sample JSON file
    import json
    json_content = {"title": "Sample JSON", "content": "This is a sample JSON file."}
    with open(os.path.join(test_dir, "sample.json"), "w") as f:
        json.dump(json_content, f, indent=4)

    return test_dir

def test_load_data():
    """
    Tests load_data by ensuring each file type is processed by the correct reader.
    """
    test_dir = setup_test_directory()
    print(f"Testing load_data with directory: {test_dir}")

    try:
        with patch("QAWithPDF.data_ingestion.SimpleDirectoryReader.load_data") as mock_txt_pdf_reader, \
             patch("QAWithPDF.data_ingestion.DocxReader.load_data") as mock_docx_reader, \
             patch("QAWithPDF.data_ingestion.JSONReader.load_data") as mock_json_reader:

            # Configure return values for mocks
            mock_txt_pdf_reader.return_value = ["Mock TXT/PDF Document"]
            mock_docx_reader.return_value = ["Mock DOCX Document"]
            mock_json_reader.return_value = ["Mock JSON Document"]

            # Call load_data
            documents = load_data(test_dir)

            # Assertions to verify which reader handled the files
            assert mock_txt_pdf_reader.called, "SimpleDirectoryReader not triggered for TXT/PDF files."
            assert mock_docx_reader.called, "DocxReader not triggered for DOCX files."
            assert mock_json_reader.called, "JSONReader not triggered for JSON files."

            # Output detailed confirmation
            print("Test Results:")
            print(f"TXT/PDF Reader triggered: {mock_txt_pdf_reader.called}")
            print(f"DOCX Reader triggered: {mock_docx_reader.called}")
            print(f"JSON Reader triggered: {mock_json_reader.called}")
            print(f"Total documents loaded: {len(documents)}")

    except Exception as e:
        print(f"Test failed with error: {e}")

    finally:
        # Clean up the test directory
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"Test directory '{test_dir}' cleaned up.")


if __name__ == "__main__":
    test_load_data()
