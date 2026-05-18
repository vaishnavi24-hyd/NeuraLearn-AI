import streamlit as st
from streamlit_mermaid import st_mermaid
from services.rag_service import generate_rag_response
from services.diagram_service import generate_diagram_syntax, extract_key_points

def render():
    st.markdown("<h2 class='neon-text-cyan'>Visual Explanations</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Generate side-by-side text answers and structural process maps to accelerate comprehension.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input area
    query = st.text_input("Enter a concept, workflow, or system to visualize:", placeholder="e.g., How does the backpropagation algorithm work?")
    
    st.markdown("<div class='btn-cyan'>", unsafe_allow_html=True)
    submit = st.button("Generate Visual Explanation", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if submit:
        if not query:
            st.warning("Please enter a concept to visualize.")
            return
            
        with st.spinner("Synthesizing Text & Structural Mappings..."):
            
            # Step 1: Run standard RAG to get the answer and citations
            rag_result = generate_rag_response(query)
            answer = rag_result.get("answer", "Error generating text response.")
            citations = rag_result.get("citations", [])
            
            # Extract just the texts from citations to pass to diagram generator
            context_texts = [c["document"] for c in citations]
            
            # Step 2: Generate Diagram Syntax
            mermaid_syntax = generate_diagram_syntax(query, context_texts)
            
            # Step 3: Extract Key Points
            key_points = extract_key_points(context_texts)
            
        st.success("Visual synthesis complete.")
        
        # Display side-by-side
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### Text Synthesis")
            st.markdown(f'''
                <div class="cyber-card" style="padding: 20px; border-color: var(--neon-purple); height: 100%;">
                    <div style="font-size: 1.05rem; line-height: 1.6;">
                        {answer}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            if citations:
                with st.expander("🔍 View Neural Citations"):
                    for i, citation in enumerate(citations):
                        sim = max(0, 1.0 - citation.get('distance', 1.0))
                        st.markdown(f"**[Match {i+1}] Sim: {round(sim*100,1)}% | Source: {citation['metadata'].get('filename')}**")
                        st.caption(citation['document'][:200] + "...")
                        
        with col2:
            st.markdown("### Structural Map")
            
            if mermaid_syntax == "NO_DIAGRAM":
                st.info("The knowledge core determined that this topic does not have enough structural information to generate a reliable diagram.")
            else:
                # Render the Mermaid diagram
                st.markdown('<div class="cyber-card" style="padding: 20px; border-color: var(--neon-cyan); background-color: #1a1a2e;">', unsafe_allow_html=True)
                # We wrap st_mermaid in a try block in case the LLM syntax breaks it
                try:
                    # st_mermaid uses a white background by default, we can't easily theme the SVG inside without CSS hacks
                    # but we can try to pass a theme parameter if it supports it, or just let it render.
                    st_mermaid(mermaid_syntax, height=400)
                except Exception as e:
                    st.error("Generated Mermaid syntax contained errors. View raw syntax below.")
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("👨‍💻 View Raw Mermaid Syntax"):
                    st.code(mermaid_syntax, language="mermaid")
                    
            st.markdown("### Key Concept Extractions")
            st.markdown(f'''
                <div class="cyber-card" style="padding: 15px; border-left: 3px solid var(--neon-cyan);">
                    {key_points}
                </div>
            ''', unsafe_allow_html=True)
