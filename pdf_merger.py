import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO


# function to merge the pdfs together
def merge_pdfs(pdf_files):
    merger = PdfMerger()

    for pdf in pdf_files:
        merger.append(pdf)

    # save the merged pdf into a BytesIO object
    merged_pdf = BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)

    return merged_pdf


# streamlit ui
st.title("PDF Merger")

st.write("Upload multiple PDF files to merge them into one document.")

# allow the user to upload multiple pdfs
uploaded_pdfs = st.file_uploader(
    "Choose PDF files", type="pdf", accept_multiple_files=True
)

# only show the merged button if at least 2 documents is uploaded
if uploaded_pdfs and len(uploaded_pdfs) > 1:
    if st.button("Merge PDFs"):
        # call the merged function
        merged_pdf = merge_pdfs(uploaded_pdfs)

        # display a download button after the function has been called
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf,
            file_name="merged_output.pdf",
            mime="application/pdf",
        )
else:
    st.write("Please upload at least two PDF files to merge.")
