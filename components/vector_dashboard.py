import streamlit as st
import time
from services.vector_store_service import store_embeddings, get_db_stats, query_database
from services.embedding_service import load_embedding_model

def render():
    st.markdown("<h2 class='neon-text-purple'>Database & Retrieval</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Manage ChromaDB persistence and execute semantic similarity searches against the knowledge core.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 1. Database Storage Management
    st.markdown("### Vector Storage")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if 'embeddings' in st.session_state and st.session_state.embeddings:
            st.info(f"You have {len(st.session_state.embeddings)} uncommitted vectors in the current session.")
            
            st.markdown("<div class='btn-purple'>", unsafe_allow_html=True)
            if st.button("Commit Session Vectors to Database"):
                with st.spinner("Writing to ChromaDB..."):
                    count = store_embeddings(st.session_state.embeddings)
                    time.sleep(0.5) # Simulate slight delay for effect
                st.success(f"Successfully committed {count} vectors to persistent storage.")
                # Optional: clear session embeddings after commit
                # st.session_state.embeddings = []
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No uncommitted vectors in session. Generate vectors in the previous step first.")
            
    with col2:
        # Show DB Stats
        stats = get_db_stats()
        status_color = "var(--neon-cyan)" if "Online" in stats["status"] else "red"
        st.markdown(f'''
            <div class="cyber-card" style="padding: 15px;">
                <h4 style="margin-top:0;">Database Health</h4>
                <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 5px;">Status: <span style="color: {status_color};">{stats['status']}</span></div>
                <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 5px;">Collection: <span style="color: var(--neon-purple);">{stats['collection']}</span></div>
                <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 5px;">Total Vectors: <span style="color: var(--neon-cyan); font-weight: bold; font-size: 1.2rem;">{stats['total_vectors']}</span></div>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 2. Semantic Retrieval Testing
    st.markdown("### Semantic Retrieval Testing")
    
    query = st.text_input("Enter a test query to search the vector database:", placeholder="e.g., What is the definition of neural networks?")
    
    num_results = st.slider("Number of results to retrieve", min_value=1, max_value=10, value=3)
    
    if st.button("Run Semantic Search", type="primary"):
        if not query:
            st.warning("Please enter a query.")
        elif stats['total_vectors'] == 0:
            st.error("The database is empty. Please commit vectors first.")
        else:
            with st.spinner("Generating query embedding and searching ChromaDB..."):
                # Embed the query
                model = load_embedding_model()
                query_vector = model.encode([query])[0].tolist()
                
                # Search the DB
                results = query_database(query_vector, n_results=num_results)
                
            st.success("Search complete.")
            
            st.markdown("#### Top Matches")
            if not results:
                st.info("No matching results found.")
            else:
                for i, res in enumerate(results):
                    # Cosine distance: lower is more similar. Convert to a pseudo-similarity score.
                    # Chroma returns distance. If metric is cosine, distance = 1 - cosine_similarity.
                    similarity_score = max(0, 1.0 - res['distance'])
                    score_percentage = round(similarity_score * 100, 1)
                    
                    st.markdown(f'''
                        <div class="cyber-card" style="margin-bottom: 15px; border-left: 4px solid var(--neon-cyan);">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <div style="color: var(--neon-purple); font-weight: bold;">Match #{i+1}</div>
                                <div style="color: var(--neon-cyan);">Similarity: {score_percentage}%</div>
                            </div>
                            <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 10px;">
                                Source: {res['metadata'].get('filename', 'Unknown')} | Page: {res['metadata'].get('page_number', 'N/A')}
                            </div>
                            <div class="text-preview-container" style="max-height: 200px;">
{res['document']}
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
