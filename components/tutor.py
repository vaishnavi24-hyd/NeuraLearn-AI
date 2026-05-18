import streamlit as st

def render():
    st.markdown("<h2 class='neon-text-purple'>Interactive AI Tutor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Ask complex questions and receive simplified, visual explanations.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mock Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to your Neural Workspace. How can I assist your learning today?"}
        ]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Enter your query here..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"[System Alert: AI Backend Disconnected in Phase 1] Received query: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(f"<span style='color: var(--neon-purple);'>{response}</span>", unsafe_allow_html=True)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Pre-defined prompts
    st.markdown("### Suggested Neural Prompts")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Explain Quantum Entanglement visually")
        st.button("Break down the Krebs Cycle step-by-step")
    with col2:
        st.button("Summarize the uploaded History notes")
        st.button("Generate a practice problem for Calculus")
