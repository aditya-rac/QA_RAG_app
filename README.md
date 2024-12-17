# Information Retrieval Using LlamaIndex and Google Gemini

## Overview
This project enables **information retrieval** and **question answering** on uploaded documents (PDF, TXT, DOCX, and JSON).  
It is based on the original implementation by [Sunny Suvita](https://github.com/sunnysavita10/Information-Retrival-Using-LlamaIdex-and-Google_Gemini).

For the original implementation and detailed guide, follow Sunny Suvita's YouTube video:  
[Watch the YouTube Video](https://www.youtube.com/watch?v=hqJxgbxczOo&t=7456s&ab_channel=SunnySavita).

---

## Enhancements in This Project
1. **Updated to the Latest LlamaIndex**:
   - Replaced the deprecated `ServiceContext` with the **Settings module**.

2. **Extended File Type Support**:
   - Added support for **DOCX** files using `DocxReader`.
   - Added support for **JSON** files using `JSONReader`.

3. **Improved Streamlit App**:
   - Files are **saved temporarily** before processing for compatibility with LlamaIndex.
   - **Tabular responses** are rendered cleanly using Markdown.
   - Non-tabular responses display as plain text.

4. **Unit Testing**:
   - Added tests for:
     - **Data Ingestion** (`test_ingestion.py`) – Verifies file handling for TXT, PDF, DOCX, and JSON.
     - **Embeddings** (`test_embeddings.py`) – Ensures embedding creation and query functionality.

---


