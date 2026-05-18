import streamlit as st
from services.rag_service import generate_rag_response
from services.analytics_service import track_question

def render():
    st.markdown("<h2 class='neon-text-purple'>AI Knowledge Tutor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Ask complex questions grounded securely in your uploaded knowledge base.</p>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # NEURAL CONFIGURATION PANEL
    # ---------------------------------------------------------
    with st.expander("⚙️ Neural Configuration Panel", expanded=False):
        st.markdown("<h4 style='color: var(--neon-cyan);'>Adaptive Learning Controls</h4>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            level = st.selectbox(
                "Explanation Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=1
            )
        with c2:
            length = st.select_slider(
                "Response Length",
                options=["50 words", "100 words", "250 words", "500 words", "Detailed Explanation"],
                value="Detailed Explanation"
            )
        with c3:
            style = st.selectbox(
                "Teaching Style",
                ["Simple Language", "Technical", "Exam-Oriented", "Storytelling", "Bullet Points", "Step-by-Step"],
                index=0
            )
            
        c4, c5 = st.columns(2)
        with c4:
            visual_toggle = st.toggle("Enable Visual Explanations", value=False)
        with c5:
            quiz_toggle = st.toggle("Enable Quiz Generation", value=False)
            
        # Store active controls
        active_controls = {
            "level": level,
            "length": length,
            "style": style
        }

    st.markdown("---")
    
    # Contextual Badges
    badges_html = f"""
    <div style='display: flex; gap: 10px; margin-bottom: 15px;'>
        <span style='background: rgba(176, 38, 255, 0.2); border: 1px solid var(--neon-purple); color: var(--neon-purple); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;'>{level} Mode</span>
        <span style='background: rgba(0, 243, 255, 0.2); border: 1px solid var(--neon-cyan); color: var(--neon-cyan); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;'>{style}</span>
    """
    if visual_toggle:
        badges_html += "<span style='background: rgba(0, 255, 128, 0.2); border: 1px solid #00ff80; color: #00ff80; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;'>Visuals Enabled</span>"
    if quiz_toggle:
        badges_html += "<span style='background: rgba(255, 200, 0, 0.2); border: 1px solid #ffc800; color: #ffc800; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;'>Quiz Enabled</span>"
    badges_html += "</div>"
    
    st.markdown(badges_html, unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Welcome to the Neural Workspace. How can I assist your learning today?", "citations": []}
        ]
        
    # Auto-submit handler from smart buttons
    if "pending_query" in st.session_state and st.session_state.pending_query:
        prompt = st.session_state.pending_query
        st.session_state.pending_query = None
    else:
        prompt = st.chat_input("Query the knowledge core...")

    # Container for chat history
    chat_container = st.container(height=500)
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_messages):
            is_user = message["role"] == "user"
            
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Render citations if they exist for assistant messages
                if not is_user and message.get("citations"):
                    with st.expander("🔍 View Neural Citations"):
                        for j, citation in enumerate(message["citations"]):
                            similarity = max(0, 1.0 - citation.get('distance', 1.0))
                            st.markdown(f'''
                                <div class="cyber-card" style="margin-bottom: 10px; padding: 10px; border-left: 3px solid var(--neon-cyan);">
                                    <div style="font-size: 0.8rem; color: var(--neon-cyan); margin-bottom: 5px;">
                                        [Match {j+1}] Sim: {round(similarity * 100, 1)}% | Source: {citation['metadata'].get('filename')} | Page: {citation['metadata'].get('page_number')}
                                    </div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted); font-family: monospace;">
                                        {citation['document'][:300]}...
                                    </div>
                                </div>
                            ''', unsafe_allow_html=True)
                
                # Smart Tutoring Action Buttons ONLY for the most recent assistant message (excluding the greeting)
                if not is_user and i == len(st.session_state.chat_messages) - 1 and i > 0:
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    bc1, bc2, bc3, bc4 = st.columns(4)
                    
                    if bc1.button("🔁 Explain Simpler", key=f"btn_simpler_{i}"):
                        st.session_state.pending_query = f"Can you explain your previous answer about that topic much simpler, as if I'm a complete beginner?"
                        st.rerun()
                    if bc2.button("📚 More Detailed", key=f"btn_detail_{i}"):
                        st.session_state.pending_query = f"Can you expand on your previous answer and provide much more technical detail?"
                        st.rerun()
                    if bc3.button("🧠 Generate Quiz", key=f"btn_quiz_{i}"):
                        st.session_state.pending_query = f"Based on your previous answer, generate a quick 3-question multiple choice quiz to test my knowledge."
                        st.rerun()
                    if bc4.button("🗺️ Visualize Concept", key=f"btn_vis_{i}"):
                        st.session_state.pending_query = f"Can you provide a structured textual map or step-by-step breakdown of that concept?"
                        st.rerun()

    # Input handling
    if prompt:
        # Track analytics
        track_question("Tutor Chat")
        
        # Append and display user message immediately
        st.session_state.chat_messages.append({"role": "user", "content": prompt, "citations": []})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Assistant thinking state
            with st.chat_message("assistant"):
                with st.spinner(f"Consulting Vector Database & Engaging LLM ({level} Mode)..."):
                    # Execute RAG Pipeline with adaptive controls
                    response_data = generate_rag_response(prompt, controls=active_controls)
                    
                    answer = response_data.get("answer", "Error generating response.")
                    citations = response_data.get("citations", [])
                    
                # Display final answer
                st.markdown(answer)
                
                # Display citations
                if citations:
                    with st.expander("🔍 View Neural Citations"):
                        for j, citation in enumerate(citations):
                            similarity = max(0, 1.0 - citation.get('distance', 1.0))
                            st.markdown(f'''
                                <div class="cyber-card" style="margin-bottom: 10px; padding: 10px; border-left: 3px solid var(--neon-cyan);">
                                    <div style="font-size: 0.8rem; color: var(--neon-cyan); margin-bottom: 5px;">
                                        [Match {j+1}] Sim: {round(similarity * 100, 1)}% | Source: {citation['metadata'].get('filename')} | Page: {citation['metadata'].get('page_number')}
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
        st.rerun()
