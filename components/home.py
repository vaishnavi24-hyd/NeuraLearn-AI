import streamlit as st
import streamlit.components.v1 as components

def render():
    # ---------------------------------------------------------
    # HERO SECTION
    # ---------------------------------------------------------
    st.markdown('''
        <div class="hero-gradient">
            <h1 class="neon-text-cyan pulse-glow" style="font-size: 4rem; margin-bottom: 0;">NeuroLearn AI</h1>
            <h3 style="color: var(--text-main); font-weight: 300; margin-top: 10px;">Advanced Educational Intelligence Core</h3>
            <p style="color: var(--text-muted); font-size: 1.2rem; max-width: 800px; margin: 20px auto;">
                Transform your static PDF documents into dynamic, interactive learning environments. 
                Powered by state-of-the-art Retrieval-Augmented Generation (RAG) and local LLMs.
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # PLATFORM STATISTICS (Mocked for Showcase)
    # ---------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('''
            <div class="cyber-card" style="text-align: center; border-color: var(--neon-cyan); padding: 15px;">
                <div style="font-size: 2.5rem; color: var(--neon-cyan); font-family: 'Orbitron', sans-serif;">250K+</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Vectors Generated</div>
            </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown('''
            <div class="cyber-card" style="text-align: center; border-color: var(--neon-purple); padding: 15px;">
                <div style="font-size: 2.5rem; color: var(--neon-purple); font-family: 'Orbitron', sans-serif;">&lt;50ms</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Retrieval Latency</div>
            </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown('''
            <div class="cyber-card" style="text-align: center; border-color: var(--success); padding: 15px;">
                <div style="font-size: 2.5rem; color: var(--success); font-family: 'Orbitron', sans-serif;">100%</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Offline Privacy</div>
            </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown('''
            <div class="cyber-card" style="text-align: center; border-color: #FFB800; padding: 15px;">
                <div style="font-size: 2.5rem; color: #FFB800; font-family: 'Orbitron', sans-serif;">Adaptive</div>
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Learning Engine</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # ARCHITECTURE OVERVIEW (Mermaid.js)
    # ---------------------------------------------------------
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'><span class='neon-text-cyan'>Neural Architecture</span> Overview</h2>", unsafe_allow_html=True)
    
    mermaid_code = """
    %%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#050816', 'primaryTextColor': '#F5F7FF', 'primaryBorderColor': '#00F5FF', 'lineColor': '#C800FF', 'secondaryColor': '#0A0F1E', 'tertiaryColor': '#050816'}}}%%
    graph TD
        classDef default fill:#0A0F1E,stroke:#00F5FF,stroke-width:2px,color:#F5F7FF,font-family:Orbitron;
        classDef db fill:#0A0F1E,stroke:#C800FF,stroke-width:2px,color:#F5F7FF,font-family:Orbitron;
        classDef llm fill:#0A0F1E,stroke:#00FF85,stroke-width:2px,color:#F5F7FF,font-family:Orbitron;
        
        A[PDF Documents] --> B(Text Chunking Engine)
        B --> C{Embedding Model<br/>all-MiniLM-L6-v2}
        C -->|Vectors| D[(ChromaDB<br/>Vector Store)]:::db
        
        U((User Query)) --> E{Semantic Retrieval}
        D -->|Top-K Context| E
        
        E --> F[Mistral 7B<br/>Local LLM]:::llm
        F --> G[Adaptive RAG Tutor]
        F --> H[Quiz / Flashcard Generator]
        F --> I[Mermaid Visualizer]
    """
    
    # Render Mermaid using an iframe or html
    mermaid_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; background: rgba(5, 8, 22, 0.4); border: 1px solid rgba(0, 245, 255, 0.15); border-radius: 16px; padding: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); backdrop-filter: blur(12px);">
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
        </script>
        <pre class="mermaid" style="background: transparent; border: none;">
            {mermaid_code}
        </pre>
    </div>
    """
    components.html(mermaid_html, height=500)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # FEATURE SHOWCASE
    # ---------------------------------------------------------
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'><span class='neon-text-purple'>Core Platform</span> Capabilities</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
            <div class="cyber-card" style="min-height: 250px;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🤖</div>
                <h3 style="color: var(--neon-cyan); font-size: 1.3rem;">Adaptive AI Tutor</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Context-aware conversational agent that tailors explanations based on your selected difficulty, length, and learning style (e.g., Technical vs. Storytelling).
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown('''
            <div class="cyber-card" style="min-height: 250px;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">👁️</div>
                <h3 style="color: var(--neon-purple); font-size: 1.3rem;">Visual Explanations</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Automatically synthesizes complex text concepts into visual flowcharts, process maps, and hierarchy diagrams using Mermaid.js integration.
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown('''
            <div class="cyber-card" style="min-height: 250px;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">📝</div>
                <h3 style="color: var(--success); font-size: 1.3rem;">Interactive Assessment</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">
                    Forces active recall through AI-generated Multiple Choice Quizzes and interactive Flashcard decks, perfectly mapped to your uploaded knowledge base.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # GETTING STARTED CTA
    # ---------------------------------------------------------
    st.markdown('''
        <div style="text-align: center; margin-top: 20px;">
            <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 20px;">Ready to initiate the neural synchronization?</p>
            <div style="color: var(--neon-cyan); font-family: 'Orbitron', sans-serif; font-size: 1.2rem; filter: drop-shadow(0 0 10px var(--neon-cyan));">
                Navigate to <b>📂 Upload Notes</b> in the sidebar to begin.
            </div>
        </div>
    ''', unsafe_allow_html=True)
