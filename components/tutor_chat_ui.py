import streamlit as st
from services.rag_service import generate_rag_response

def render():
    st.markdown("<h2 class='neon-text-purple'>AI Knowledge Tutor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Ask complex questions grounded securely in your uploaded knowledge base.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Welcome to the Neural Workspace. How can I assist your learning today?", "citations": []}
        ]

    # Container for chat history
    chat_container = st.container(height=500)
    
    with chat_container:
        for message in st.session_state.chat_messages:
            # Custom styling for user vs assistant
            is_user = message["role"] == "user"
            
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Render citations if they exist for assistant messages
                if not is_user and message.get("citations"):
                    with st.expander("🔍 View Neural Citations"):
                        for i, citation in enumerate(message["citations"]):
                            similarity = max(0, 1.0 - citation.get('distance', 1.0))
                            st.markdown(f'''
                                <div class="cyber-card" style="margin-bottom: 10px; padding: 10px; border-left: 3px solid var(--neon-cyan);">
                                    <div style="font-size: 0.8rem; color: var(--neon-cyan); margin-bottom: 5px;">
                                        [Match {i+1}] Sim: {round(similarity * 100, 1)}% | Source: {citation['metadata'].get('filename')} | Page: {citation['metadata'].get('page_number')}
                                    </div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted); font-family: monospace;">
                                        {citation['document'][:300]}...
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)

    # Input handling
    if prompt := st.chat_input("Query the knowledge core..."):
        
        # Append and display user message immediately
        st.session_state.chat_messages.append({"role": "user", "content": prompt, "citations": []})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Assistant thinking state
            with st.chat_message("assistant"):
                with st.spinner("Consulting Vector Database & Engaging LLM..."):
                    # Execute RAG Pipeline
                    response_data = generate_rag_response(prompt)
                    
                    answer = response_data.get("answer", "Error generating response.")
                    citations = response_data.get("citations", [])
                    
                # Display final answer
                st.markdown(answer)
                
                # Display citations
                if citations:
                    with st.expander("🔍 View Neural Citations"):
                        for i, citation in enumerate(citations):
                            similarity = max(0, 1.0 - citation.get('distance', 1.0))
                            st.markdown(f'''
                                <div class="cyber-card" style="margin-bottom: 10px; padding: 10px; border-left: 3px solid var(--neon-cyan);">
                                    <div style="font-size: 0.8rem; color: var(--neon-cyan); margin-bottom: 5px;">
                                        [Match {i+1}] Sim: {round(similarity * 100, 1)}% | Source: {citation['metadata'].get('filename')} | Page: {citation['metadata'].get('page_number')}
                                    </div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted); font-family: monospace;">
                                        {citation['document'][:300]}...
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                            
        # Save assistant message to state
        st.session_state.chat_messages.append({
            "role": "assistant", 
            "content": answer,
            "citations": citations
        })
