import streamlit as st
from pypdf import PdfWriter, PdfReader
from io import BytesIO
from streamlit_sortables import sort_items

# Page Configuration
st.set_page_config(
    page_title="PDF Fusion Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cleaned-up CSS (Backgrounds are now handled by config.toml)
st.markdown("""
<style>
    .css-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #1E1E1E;
        border: 1px solid #303030;
        margin-bottom: 20px;
    }
    .css-card h3 { 
        margin-top: 0; 
        font-size: 1.2rem; 
        font-weight: 600; 
        color: #FAFAFA; 
    }
    [data-testid="stMetricValue"] { 
        font-size: 1.8rem !important; 
        color: #FF4B4B !important; 
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def get_pdf_stats(pdf_files):
    total_pages = 0
    total_size_mb = 0
    stats_map = {} 

    for pdf in pdf_files:
        try:
            pdf.seek(0)
            reader = PdfReader(pdf)
            pages = len(reader.pages)
            size_mb = pdf.size / (1024 * 1024)
            
            stats_map[pdf.name] = {
                "pages": pages,
                "size": f"{size_mb:.2f} MB"
            }
            total_pages += pages
            total_size_mb += size_mb
        except Exception:
            stats_map[pdf.name] = {"pages": "Error", "size": "N/A"}
            
    return stats_map, total_pages, total_size_mb

def merge_pdfs(ordered_files, password=None):
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

# Sidebar Controls
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

# Main Interface
st.title("📄 PDF Fusion Pro")
st.caption("Enterprise-grade document merging and security dashboard.")
st.markdown("---")

uploaded_pdfs = st.file_uploader(
    "Drag & drop your PDFs here to begin processing", 
    type="pdf", 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Logic Execution
if uploaded_pdfs:
    stats_map, total_pages, total_size = get_pdf_stats(uploaded_pdfs)
    num_files = len(uploaded_pdfs)
    file_map = {f.name: f for f in uploaded_pdfs}

    # Metrics Display
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Documents Queued", f"{num_files}", delta="Ready")
    m2.metric("Total Pages", f"{total_pages}")
    m3.metric("Total Size", f"{total_size:.2f} MB")
    m4.metric("Security", "Protected" if add_password else "Standard", delta="Secure" if add_password else None, delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # Two-Column Layout
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<div class="css-card"><h3>🗂️ Reorder Files (Drag & Drop)</h3>', unsafe_allow_html=True)
        st.info("💡 Tip: Drag the items below to change the merge order.")
        
        original_items = []
        for f in uploaded_pdfs:
            meta = stats_map.get(f.name, {})
            label = f"{f.name} :: {meta.get('pages')} Pgs | {meta.get('size')}"
            original_items.append(label)

        sorted_items = sort_items(original_items, direction="vertical")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="css-card"><h3>🚀 Actions & Status</h3>', unsafe_allow_html=True)
        
        ordered_files_list = []
        try:
            for item_str in sorted_items:
                fname = item_str.split(" :: ")[0]
                if fname in file_map:
                    ordered_files_list.append(file_map[fname])
            can_merge = True
        except Exception:
            can_merge = False

        st.markdown(f"**Target:** `{output_name}`")
        
        # Validation Logic
        if add_password and not user_password:
             st.warning("⚠️ Please set a password.")
             can_merge = False
        elif num_files == 1 and not add_password:
             st.info("ℹ️ Upload 2+ files to merge, or enable password protection to lock this single file.")
             can_merge = False

        # Action Button
        if can_merge:
            action_text = "Lock PDF 🔒" if num_files == 1 else "Begin Merge Sequence ⚡"
            
            if st.button(action_text):
                with st.spinner("Processing..."):
                    final_pdf = merge_pdfs(ordered_files_list, user_password)
                    st.success("✅ Complete!")
                    st.download_button(
                        label="📥 Download PDF",
                        data=final_pdf,
                        file_name=output_name,
                        mime="application/pdf",
                    )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 To get started, upload your PDF documents above.")