import os
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

    # Create a sample DOCX file (Requires python-docx)
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a sample DOCX file.")
    doc.save(os.path.join(test_dir, "sample.docx"))

    # Create a sample PDF file (Requires PyPDF2)
    from PyPDF2 import PdfWriter
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=200, height=200)
    with open(os.path.join(test_dir, "sample.pdf"), "wb") as f:
        pdf_writer.write(f)

    # Create a sample JSON file
    json_content = {
        "title": "Sample JSON",
        "content": "This is a sample JSON file.",
        "data": {"key": "value", "number": 42}
    }
    import json
    with open(os.path.join(test_dir, "sample.json"), "w") as f:
        json.dump(json_content, f, indent=4)

    return test_dir


def test_load_data():
    """
    Tests the load_data function for DOCX, TXT, PDF, and JSON file types.
    """
    # Setup test directory
    test_dir = setup_test_directory()
    print(f"Testing load_data with directory: {test_dir}")

    try:
        # Call the load_data function
        documents = load_data(test_dir)

        # Check if documents are loaded
        print(f"Loaded {len(documents)} document(s).")
        for doc in documents:
            print(f"Doc ID: {doc.get_doc_id()}")  # Access document ID
            print(f"Text: {doc.get_text()}")  # Access document text

        # Assertions for each file type
        # Check for TXT file content
        assert any("This is a sample text file." in doc.get_text() for doc in documents), "TXT file not loaded."

        # Check for DOCX file content
        assert any("This is a sample DOCX file." in doc.get_text() for doc in documents), "DOCX file not loaded."

        # Check for PDF (allow blank text but ensure it's loaded)
        assert any(doc.get_text() == "" for doc in documents), "PDF file not loaded."

        # Check for JSON file content
        assert any("This is a sample JSON file." in doc.get_text() for doc in documents), "JSON file not loaded."

        print("All tests passed successfully!")

    except Exception as e:
        print(f"Test failed with error: {e}")

    finally:
        # Cleanup test directory
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"Test directory '{test_dir}' cleaned up.")


if __name__ == "__main__":
    test_load_data()
