import streamlit as st
from pypdf import PdfWriter, PdfReader
from io import BytesIO
import pandas as pd 

# --- 1. PAGE & THEME CONFIGURATION ---
st.set_page_config(
    page_title="PDF Fusion Pro",
    page_icon="📄",
    layout="wide",
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
    stats_data = []
    total_pages = 0
    total_size_mb = 0

    for index, pdf in enumerate(pdf_files):
        try:
            # Reset pointer to read file info
            pdf.seek(0)
            reader = PdfReader(pdf)
            pages = len(reader.pages)
            size_mb = pdf.size / (1024 * 1024)
            
            stats_data.append({
                "Order": index + 1, 
                "Filename": pdf.name,
                "Pages": pages,
                "Size (MB)": round(size_mb, 2)
            })
            total_pages += pages
            total_size_mb += size_mb
        except Exception:
            stats_data.append({
                "Order": index + 1,
                "Filename": pdf.name, 
                "Pages": 0, 
                "Size (MB)": 0.0
            })
            
    return stats_data, total_pages, total_size_mb

def merge_pdfs(ordered_files, password=None):
    """Merges PDFs and optionally encrypts them."""
    merger = PdfWriter()
    for pdf in ordered_files:
        pdf.seek(0) 
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
    st.markdown("v1.3 Pro")

# --- 5. MAIN DASHBOARD ---

# Header Section
st.title("📄 PDF Fusion Pro")
st.caption("Enterprise-grade document merging and security dashboard.")
st.markdown("---")

# File Upload Section 
uploaded_pdfs = st.file_uploader(
    "Drag & drop your PDFs here to begin processing", 
    type="pdf", 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Dashboard Content 
if uploaded_pdfs:
    # 1. Map files for easy retrieval later {filename: file_object}
    file_map = {f.name: f for f in uploaded_pdfs}

    # 2. Get file statistics
    raw_stats, total_pages, total_size = get_pdf_stats(uploaded_pdfs)
    num_files = len(uploaded_pdfs)

    # 3. Create DataFrame for Editing
    df = pd.DataFrame(raw_stats)

    # 4. Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Documents Queued", f"{num_files}", delta="Ready")
    m2.metric("Total Pages", f"{total_pages}", help="Sum of pages across all documents.")
    m3.metric("Total Size", f"{total_size:.2f} MB")
    m4.metric("Security Status", "Protected" if add_password else "Standard", delta="Secure" if add_password else None, delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True) 

    # 5. Main Content Columns
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="css-card"><h3>🗂️ Document Queue (Edit Order)</h3>', unsafe_allow_html=True)
        st.info("💡 Tip: Click the **Order** numbers below to rearrange the merge sequence.")
        
        # INTERACTIVE DATA EDITOR
        edited_df = st.data_editor(
            df,
            column_config={
                "Order": st.column_config.NumberColumn(
                    "Merge Order",
                    help="1 = First page, 2 = Second page...",
                    min_value=1,
                    step=1,
                    required=True,
                ),
                "Size (MB)": st.column_config.NumberColumn(
                    "Size (MB)",
                    format="%.2f MB"
                )
            },
            disabled=["Filename", "Pages", "Size (MB)"], 
            hide_index=True,
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="css-card"><h3>🚀 Actions & Status</h3>', unsafe_allow_html=True)
        
        # --- RE-SORTING LOGIC ---
        # 1. Sort the dataframe based on the user's "Order" input
        sorted_df = edited_df.sort_values(by="Order")
        
        # 2. Rebuild the list of file objects in the new order
        # We handle cases where filenames might be missing (safety check)
        try:
            ordered_files_list = [file_map[row['Filename']] for index, row in sorted_df.iterrows()]
            can_merge = True
        except KeyError:
            st.error("⚠️ Error mapping files. Please remove duplicates.")
            can_merge = False

        st.markdown(f"**Output Target:** `{output_name}`")
        
        # Validation Logic
        if add_password and not user_password:
             st.warning("⚠️ Please set a password in the sidebar.")
             can_merge = False
        elif num_files < 2:
             st.info("ℹ️ Please upload at least 2 files to merge.")
             can_merge = False

        if can_merge:
            if st.button("Begin Merge Sequence ⚡"):
                with st.spinner("Merging documents in specified order..."):
                    final_pdf = merge_pdfs(ordered_files_list, user_password)
                    st.success("✅ Merge Complete!")
                    
                    st.download_button(
                        label="📥 Download Final PDF",
                        data=final_pdf,
                        file_name=output_name,
                        mime="application/pdf",
                    )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 To get started, upload your PDF documents above.")