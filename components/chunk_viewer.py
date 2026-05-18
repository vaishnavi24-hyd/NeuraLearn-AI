import streamlit as st
import time
from services.chunking_service import process_document

def render():
    st.markdown("<h2 class='neon-text-purple'>Neural Chunking Pipeline</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Segment uploaded knowledge nodes into semantic chunks to prepare for future embedding models.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize chunk storage in session state
    if 'chunks' not in st.session_state:
        st.session_state.chunks = []
        
    # Configuration Controls
    st.markdown("### Chunking Parameters")
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.slider(
            "Chunk Size (Characters)", 
            min_value=200, max_value=4000, value=1000, step=100,
            help="Maximum number of characters per chunk."
        )
    with col2:
        chunk_overlap = st.slider(
            "Chunk Overlap (Characters)", 
            min_value=0, max_value=1000, value=200, step=50,
            help="Overlap between sequential chunks to preserve context."
        )
        
    # Process Button
    st.markdown("<div class='btn-purple'>", unsafe_allow_html=True)
    if st.button("Execute Neural Chunking", use_container_width=True):
        if 'uploaded_docs' not in st.session_state or not st.session_state.uploaded_docs:
            st.warning("No documents found. Please upload PDFs in the 'Upload Notes' module first.")
        else:
            with st.spinner("Executing recursive text splitting..."):
                all_chunks = []
                for doc in st.session_state.uploaded_docs:
                    chunks = process_document(doc, chunk_size, chunk_overlap)
                    all_chunks.extend(chunks)
                    time.sleep(0.3) # Simulated loading for animation effect
                
                st.session_state.chunks = all_chunks
            st.success(f"Successfully generated {len(all_chunks)} chunks.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dashboard Stats & Visualizations
    if st.session_state.chunks:
        chunks = st.session_state.chunks
        total_chunks = len(chunks)
        avg_len = sum(c['length'] for c in chunks) // total_chunks if total_chunks > 0 else 0
        unique_files = len(set(c['filename'] for c in chunks))
        
        st.markdown("### Chunking Statistics")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center; border-color: var(--neon-purple);">
                    <div class="card-value neon-text-purple">{total_chunks}</div>
                    <div class="card-text">Total Chunks</div>
                </div>
            ''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center;">
                    <div class="card-value">{avg_len}</div>
                    <div class="card-text">Avg. Characters/Chunk</div>
                </div>
            ''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center;">
                    <div class="card-value neon-text-cyan">{unique_files}</div>
                    <div class="card-text">Source Documents</div>
                </div>
            ''', unsafe_allow_html=True)
            
        st.markdown("### Chunk Explorer (Previewing first 20)")
        
        # Display chunk previews
        for chunk in chunks[:20]:
            st.markdown(f'''
                <div class="cyber-card" style="margin-bottom: 10px; padding: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: var(--neon-cyan); font-family: 'Orbitron', sans-serif;">Chunk #{chunk['chunk_index']}</div>
                        <div style="color: var(--text-muted); font-size: 0.8rem;">
                            Source: {chunk['filename']} | Page: {chunk['page_number']} | Length: {chunk['length']}
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            with st.expander("View Chunk Content"):
                st.markdown(f'''
                    <div class="text-preview-container" style="border-color: var(--neon-purple);">
{chunk['text']}
                    </div>
                    <div style="margin-top: 10px; color: var(--text-muted); font-size: 0.7rem; font-family: monospace;">
                        ID: {chunk['chunk_id']}
                    </div>
                ''', unsafe_allow_html=True)
