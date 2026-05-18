import streamlit as st
from styles.theme import apply_premium_theme
from services.analytics_service import init_analytics_state

# Import component modules (we will create these next)
from components import home, upload, tutor_chat_ui, diagram_ui, quiz_ui, flashcard_ui, analytics_dashboard, chunk_viewer, embedding_dashboard, vector_dashboard

def main():
    # Apply global premium theme and configuration
    apply_premium_theme()
    
    # Initialize analytics
    init_analytics_state()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1 class='neon-text-cyan'>NeuroLearn AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-muted);'>Advanced Visual Learning Assistant</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation selection
        pages = {
            "🏠 Home": home.render,
            "📂 Upload Notes": upload.render,
            "✂️ Data Chunking": chunk_viewer.render,
            "🧠 Vector Generation": embedding_dashboard.render,
            "🗄️ Database & Retrieval": vector_dashboard.render,
            "🤖 AI Tutor": tutor_chat_ui.render,
            "👁️ Visual Explanations": diagram_ui.render,
            "📝 Quiz Generator": quiz_ui.render,
            "🗂️ Flashcards": flashcard_ui.render,
            "📊 Study Analytics": analytics_dashboard.render
        }
        
        selection = st.radio("Navigation", list(pages.keys()), label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("<div style='text-align: center; color: var(--text-muted); font-size: 0.8rem;'>System Status: <span style='color: var(--neon-cyan);'>Online</span></div>", unsafe_allow_html=True)

    # Render the selected page
    pages[selection]()

if __name__ == "__main__":
    main()
