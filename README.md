# PDF Merger Web App

This is a simple PDF merger web application built using **Streamlit** and **PyPDF2**. The app allows users to upload multiple PDF files and merge them into one document, which can then be downloaded.

## Features

- Upload multiple PDF files.
- Merge the PDFs into a single file.
- Download the merged PDF.

## Requirements

- Python 3.x
- Streamlit
- PyPDF2

## Installation

1. **Clone the repository** or download the code files.

2. **Install the required dependencies**:

   ```bash
   pip install streamlit pypdf2
   ```

## How to Run

1. **Run the app locally** using Streamlit:

   ```bash
   streamlit run pdf_merger.py
   ```

2. **Open your browser** and go to `http://localhost:8501`.

3. **Upload PDFs** to merge and download the merged result.

## Usage

1. Upload two or more PDF files.
2. Click the "Merge PDFs" button.
3. After the PDFs are merged, click the "Download Merged PDF" button to save the merged file.

## File Structure

```
pdf_merger_app/
├── venv      # virtual environment
├── pdf_merger.py      # main Python script for running the streamlit app
├── requirement.txt     # all the requirement for this file to run properly
└── README.md             
```

## Example Output

You can expect a merged PDF file named `merged_output.pdf` after merging the uploaded PDFs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

