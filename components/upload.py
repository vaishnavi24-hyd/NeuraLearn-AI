import streamlit as st

def render():
    st.markdown("<h2 class='neon-text-cyan'>Data Ingestion Module</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Upload PDF materials, lecture notes, or syllabus files into the knowledge core.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    uploaded_files = st.file_uploader(
        "Initialize File Transfer", 
        accept_multiple_files=True, 
        type=['pdf', 'txt', 'docx']
    )
    
    if uploaded_files:
        st.markdown(f"<p style='color: var(--neon-cyan);'>[SYSTEM] Neural ingestion started for {len(uploaded_files)} file(s)...</p>", unsafe_allow_html=True)
        st.progress(0, text="Processing...")
        st.markdown('''
            <div class="cyber-card" style="border-color: var(--neon-cyan);">
                <div class="card-title">Processing Status</div>
                <div class="card-text">Extraction algorithms standby. RAG pipeline not yet implemented in Phase 1.</div>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            <div class="cyber-card">
                <div class="card-title">Supported Formats</div>
                <ul class="card-text">
                    <li>PDF Documents (.pdf)</li>
                    <li>Text Files (.txt)</li>
                    <li>Word Documents (.docx)</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <div class="cyber-card">
                <div class="card-title">Processing Capacity</div>
                <ul class="card-text">
                    <li>Max file size: 50MB</li>
                    <li>Concurrent parsing enabled</li>
                    <li>Semantic chunking (Pending)</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
