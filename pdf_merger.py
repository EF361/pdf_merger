import streamlit as st
from pypdf import PdfWriter, PdfReader
from io import BytesIO

# --- 1. PAGE & THEME CONFIGURATION ---
st.set_page_config(
    page_title="PDF Fusion Pro",
    page_icon="📄",
    layout="wide", # <--- Key change for dashboard feel
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS FOR DASHBOARD UI ---
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0E1117;
    }
    /* Card-like containers for sections */
    .css-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #1E1E1E;
        border: 1px solid #303030;
        margin-bottom: 20px;
    }
    /* Styled headers inside cards */
    .css-card h3 {
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #FAFAFA;
    }
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #FF4B4B !important;
    }
    /* Custom button */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: 600;
    }
    /* File uploader area styling */
    [data-testid="stFileUploader"] {
        padding: 20px;
        border: 2px dashed #404040;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def get_pdf_stats(pdf_files):
    """Analyzes uploaded files to get page counts and total size."""
    stats = []
    total_pages = 0
    total_size_mb = 0
    
    for pdf in pdf_files:
        try:
            # Reset pointer to read file info
            pdf.seek(0)
            reader = PdfReader(pdf)
            pages = len(reader.pages)
            size_mb = pdf.size / (1024 * 1024)
            
            stats.append({
                "name": pdf.name,
                "pages": pages,
                "size": f"{size_mb:.2f} MB"
            })
            total_pages += pages
            total_size_mb += size_mb
        except Exception:
            stats.append({"name": pdf.name, "pages": "Error", "size": "N/A"})
            
    return stats, total_pages, total_size_mb

def merge_pdfs(pdf_files, password=None):
    """Merges PDFs and optionally encrypts them."""
    merger = PdfWriter()
    for pdf in pdf_files:
        pdf.seek(0) # Ensure we read from the start
        reader = PdfReader(pdf)
        merger.append(reader)

    merged_pdf = BytesIO()
    if password:
        merger.encrypt(password)
        
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    return merged_pdf

# --- 4. SIDEBAR (SETTINGS) ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")
    
    st.subheader("Output Settings")
    output_name = st.text_input("Filename", value="Monthly_Report", help="The name of your merged file.")
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
        
    st.markdown("---")
    st.subheader("Security")
    add_password = st.toggle("Enable Password Protection")
    user_password = None
    if add_password:
        user_password = st.text_input("Enter Password", type="password", placeholder="Required to open file")
        if user_password:
            st.caption("✅ Password set")
        else:
            st.caption("⚠️ Please enter a password")

    st.markdown("---")
    st.markdown("YOUR BRAND · v1.2")

# --- 5. MAIN DASHBOARD ---

# Header Section
st.title("📄 PDF Fusion Pro")
st.caption("Enterprise-grade document merging and security dashboard.")
st.markdown("---")

# File Upload Section (Full Width)
uploaded_pdfs = st.file_uploader(
    "Drag & drop your PDFs here to begin processing", 
    type="pdf", 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Dashboard Content (Only shows if files are uploaded)
if uploaded_pdfs:
    # 1. Get file statistics
    file_stats, total_pages, total_size = get_pdf_stats(uploaded_pdfs)
    num_files = len(uploaded_pdfs)

    # 2. Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Documents Queued", f"{num_files}", delta="Ready")
    m2.metric("Total Pages", f"{total_pages}", help="Sum of pages across all documents.")
    m3.metric("Total Size", f"{total_size:.2f} MB")
    m4.metric("Security Status", "Protected" if add_password else "Standard", delta="Secure" if add_password else None, delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # 3. Main Content Columns
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="css-card"><h3>🗂️ Document Queue</h3>', unsafe_allow_html=True)
        
        # Display files in a clean table format
        st.dataframe(
            file_stats, 
            column_config={
                "name": "Document Name",
                "pages": st.column_config.NumberColumn("Pages", format="%d"),
                "size": "File Size"
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="css-card"><h3>🚀 Actions & Status</h3>', unsafe_allow_html=True)
        
        st.markdown(f"**Ready to create:** `{output_name}`")
        if add_password and not user_password:
             st.warning("⚠️ Please set a password in the sidebar.")
             can_merge = False
        elif num_files < 2:
             st.info("ℹ️ Please upload at least 2 files to merge.")
             can_merge = False
        else:
             can_merge = True

        if can_merge:
            if st.button("Begin Merge Sequence ⚡"):
                with st.spinner("Merging documents..."):
                    final_pdf = merge_pdfs(uploaded_pdfs, user_password)
                    st.success("✅ Merge Complete!")
                    
                    st.download_button(
                        label="📥 Download Final PDF",
                        data=final_pdf,
                        file_name=output_name,
                        mime="application/pdf",
                    )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty State
    st.info("👆 To get started, upload your PDF documents above.")