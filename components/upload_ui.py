import streamlit as st
import time
from services.pdf_service import save_pdf, extract_pdf_data

def render():
    st.markdown("<h2 class='neon-text-cyan'>Data Ingestion Module</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Upload PDF materials into the knowledge core. Extracted text will be primed for neural processing.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize session state for uploaded documents
    if 'uploaded_docs' not in st.session_state:
        st.session_state.uploaded_docs = []

    # Upload section
    uploaded_files = st.file_uploader(
        "Initialize File Transfer (PDF only)", 
        accept_multiple_files=True, 
        type=['pdf']
    )
    
    if st.button("Process Uploads"):
        if uploaded_files:
            # Process new files
            with st.spinner("Executing neural extraction pipeline..."):
                for uploaded_file in uploaded_files:
                    # Check if already processed to avoid duplicates in session state
                    if not any(doc['filename'] == uploaded_file.name for doc in st.session_state.uploaded_docs):
                        # Save file to disk
                        file_path = save_pdf(uploaded_file)
                        
                        # Extract data
                        extracted_data = extract_pdf_data(file_path)
                        st.session_state.uploaded_docs.append(extracted_data)
                        
                        # Artificial delay for animated loading effect
                        time.sleep(0.5) 
            
            st.success(f"Successfully processed {len(uploaded_files)} file(s).")
        else:
            st.warning("Please upload files before processing.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Display Uploaded Documents as Glowing Cards
    if st.session_state.uploaded_docs:
        st.markdown("### Processed Knowledge Nodes")
        
        for doc in st.session_state.uploaded_docs:
            st.markdown(f'''
                <div class="cyber-card" style="border-color: var(--neon-cyan);">
                    <div class="card-title">{doc['filename']}</div>
                    <div class="card-text" style="margin-bottom: 15px;">
                        <span style="color: var(--neon-purple);">Pages:</span> {doc['page_count']} &nbsp;|&nbsp; 
                        <span style="color: var(--neon-purple);">Ingested:</span> {doc['upload_timestamp']}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            with st.expander(f"View Extracted Text Preview - {doc['filename']}"):
                st.markdown(f'''
                    <div class="text-preview-container">
{doc['text'][:5000]} {"... [Text Truncated for Preview]" if len(doc['text']) > 5000 else ""}
                    </div>
                ''', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    else:
        # Premium Onboarding Empty State
        st.markdown('''
            <div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
                <div class="empty-state-icon">📂</div>
                <h3 style="color: var(--text-main);">Knowledge Core Offline</h3>
                <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
                    Upload your first PDF document to initialize the neural pathways. The system will automatically chunk, embed, and index your data for high-speed semantic retrieval.
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('''
                <div class="cyber-card" style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">📄</div>
                    <div class="card-title">Supported Formats</div>
                    <p class="card-text">
                        PDF Documents (.pdf)<br>
                        Max file size: 200MB
                    </p>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown('''
                <div class="cyber-card" style="text-align: center; border-color: var(--neon-purple);">
                    <div style="font-size: 2rem; margin-bottom: 10px;">⚡</div>
                    <div class="card-title">Processing Capacity</div>
                    <p class="card-text">
                        Concurrent parsing enabled<br>
                        High-fidelity OCR extraction
                    </p>
                </div>
            ''', unsafe_allow_html=True)
