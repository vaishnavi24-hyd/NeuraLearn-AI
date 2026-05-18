import streamlit as st
import time
from services.embedding_service import generate_embeddings, get_embedding_dimension

def render():
    st.markdown("<h2 class='neon-text-purple'>Neural Vector Embeddings</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Transform semantic chunks into high-dimensional vector representations using MiniLM.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Check if we have chunks ready
    if 'chunks' not in st.session_state or not st.session_state.chunks:
        st.warning("No data chunks found. Please process PDFs in the 'Data Chunking' module first.")
        return
        
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = []
    if 'embedding_time' not in st.session_state:
        st.session_state.embedding_time = 0.0

    # Controls
    st.markdown("<div class='btn-purple'>", unsafe_allow_html=True)
    if st.button("Initialize Vector Generation", use_container_width=True):
        start_time = time.time()
        
        # UI Loading sequence
        progress_text = "Loading transformer weights into memory..."
        progress_bar = st.progress(0, text=progress_text)
        time.sleep(0.5) # Simulated initialization
        
        progress_bar.progress(30, text="Encoding chunks into vector space...")
        
        # Execute embeddings
        generated_embeddings = generate_embeddings(st.session_state.chunks)
        
        progress_bar.progress(100, text="Neural encoding complete.")
        time.sleep(0.5)
        progress_bar.empty()
        
        end_time = time.time()
        
        st.session_state.embeddings = generated_embeddings
        st.session_state.embedding_time = round(end_time - start_time, 2)
        st.success("Vector generation successfully finalized.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dashboard Stats
    if st.session_state.embeddings:
        total_embeddings = len(st.session_state.embeddings)
        total_chunks = len(st.session_state.chunks)
        coverage = round((total_embeddings / total_chunks) * 100, 1) if total_chunks > 0 else 0
        dim = get_embedding_dimension()
        
        st.markdown("### Vector Topography")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center; padding: 15px;">
                    <div class="card-value neon-text-cyan">{total_embeddings}</div>
                    <div class="card-text">Total Vectors</div>
                </div>
            ''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center; padding: 15px;">
                    <div class="card-value">{dim}</div>
                    <div class="card-text">Dimensions</div>
                </div>
            ''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center; padding: 15px;">
                    <div class="card-value neon-text-purple">{coverage}%</div>
                    <div class="card-text">Chunk Coverage</div>
                </div>
            ''', unsafe_allow_html=True)
        with c4:
            st.markdown(f'''
                <div class="cyber-card" style="text-align: center; padding: 15px;">
                    <div class="card-value">{st.session_state.embedding_time}s</div>
                    <div class="card-text">Processing Time</div>
                </div>
            ''', unsafe_allow_html=True)
            
        # Preview Section
        st.markdown("### Embedding Matrix Preview (First 10)")
        
        for emb in st.session_state.embeddings[:10]:
            # Format a truncated preview of the array
            vector = emb['embedding']
            vector_preview = ", ".join([f"{v:.4f}" for v in vector[:5]])
            
            st.markdown(f'''
                <div class="cyber-card" style="margin-bottom: 15px;">
                    <div style="color: var(--neon-cyan); font-family: 'Orbitron', sans-serif; font-size: 1.1rem; margin-bottom: 8px;">
                        Vector ID: {emb['chunk_id'][:8]}...
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;">
                        Source: {emb['filename']} | Page: {emb['page_number']}
                    </div>
                    <div class="text-preview-container" style="max-height: 150px; font-size: 0.8rem;">
<span style="color: var(--neon-purple);">[Text Content]</span>
{emb['text'][:200]}...

<span style="color: var(--neon-purple);">[Vector Coordinates]</span>
[{vector_preview}, ... ({dim} dimensions)]
                    </div>
                </div>
            ''', unsafe_allow_html=True)
