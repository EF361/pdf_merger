# PDF Merger  

![Python version](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Streamlit](https://img.shields.io/badge/Streamlit-%E2%9A%A1%EF%B8%8F-red)  
![PyPDF](https://img.shields.io/badge/Library-PyPDF-informational)  
![License](https://img.shields.io/badge/License-MIT-green)  
![Repository Size](https://img.shields.io/github/repo-size/EF361/pdf_merger)  

## Executive Summary  
**PDF Merger** is a lightweight, browser-based utility powered by Python and Streamlit for merging, splitting, and manipulating PDF files. It simplifies PDF processing with a user-friendly interface, while ensuring secure handling of files through temporary storage and strict cleanup rules.  

## Key Features  
- **Merge PDFs:** Combine multiple PDF files into a single document with custom page order.  
- **Split PDFs:** Extract specific pages or ranges into separate files.  
- **Page Reordering:** Rearrange pages or remove unwanted ones before creating the output file.  
- **Encrypted and Corrupted PDFs:** Built-in handling for encrypted files (with password input) and graceful error reporting for malformed PDFs.  
- **Temporary File Lifecycle:** Uses secure, temporary file storage that guarantees cleanup after each session or operation.  
- **Extensive File Validations:** Supports large files, mixed page sizes, and rotated documents, with upload size and processing-time limits to ensure smooth performance.  
- **Actionable Errors:** Provides user-friendly error messages for various scenarios like maximum file size exceeded, unsupported formats, or empty uploads.  
- **Test Coverage:** Tested for edge cases, including encrypted, corrupted, large-sized, and empty PDFs to ensure robust functionality.  

## Architecture & Workflow  

```mermaid
flowchart TD  
    A[User Uploads PDFs] -->|Streamlit Upload Form| B[Streamlit Backend]  
    B -->|Temporary Storage| C[File Validation]  
    C -->|Ensure Encryption/Corruption Check| D[Define Operations (Merge/Split/Order)]  
    D -->|PyPDF Processing| E[[Temporary Output File]]  
    E -->|Present Download Link| F[User Downloads File]  
    E -->|Session or Operation Ends| G[Temporary File Cleanup]  
```  

Each uploaded file is processed through Streamlit's backend, stored as a temporary file, and validated for encryption, size, or corruption. After completing the operation (e.g., merging, splitting), the temporary storage is cleaned up to ensure no files persist beyond their session or purpose.  

## Tech Stack & Tools  
- **Programming Language:** Python 3.8+  
- **Web Framework:** Streamlit  
- **PDF Processing:** PyPDF  
- **Testing:** pytest (edge-case simulations: encrypted, corrupted, and large PDFs)  

## Quickstart / Installation  

Follow these steps to spin up the **PDF Merger** locally on your machine:  

1. **Clone the Repository**  
    ```bash  
    git clone https://github.com/EF361/pdf_merger.git  
    cd pdf_merger  
    ```  

2. **Set up Python Environment**  
    Create a virtual environment and install dependencies:  
    ```bash  
    python3 -m venv venv  
    source venv/bin/activate  # Use `venv\Scripts\activate` on Windows  
    pip install -r requirements.txt  
    ```  

3. **Run the Application**  
    Start the Streamlit server:  
    ```bash  
    streamlit run app.py  
    ```  
    Open [http://localhost:8501](http://localhost:8501) in your browser to begin using the app.  

4. **Testing**  
    Run the test suite to validate edge-case handling:  
    ```bash  
    pytest tests/  
    ```  

## Security & Limitations  
- **File Handling:** Uploaded files are temporarily stored for processing and automatically deleted after each session or at the end of the file's lifecycle. No files are permanently retained in this application.  
- **Resource Limits:**  
  - **File Size Limit:** 50 MB per file  
  - **Page Count Limit:** 1,000 pages per document  
  - **Processing Time Limit:** 60 seconds per operation  

    If these limits are exceeded, the app will provide clear feedback to the user.  

- **Feature Roadmap:**  
  Additional plans for annotation, watermarking, and batch encryption/decryption are underway. Unsupported operations are currently marked as "Planned."  

---

**Author:** Alicia Goh ([@EF361](https://github.com/EF361))  
Delivered with precision, reliability, and security in mind. If you find this project useful, please ⭐ the repository!