import streamlit as st
from utils.styling import apply_theme

# Import component modules (we will create these next)
from components import home, upload, tutor, visuals, quiz, flashcards, analytics

def main():
    # Apply global theme and configuration
    apply_theme()

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1 class='neon-text-cyan'>NeuroLearn AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-muted);'>Advanced Visual Learning Assistant</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation selection
        pages = {
            "🏠 Home": home.render,
            "📂 Upload Notes": upload.render,
            "🤖 AI Tutor": tutor.render,
            "👁️ Visual Explanations": visuals.render,
            "📝 Quiz Generator": quiz.render,
            "🗂️ Flashcards": flashcards.render,
            "📊 Study Analytics": analytics.render
        }
        
        selection = st.radio("Navigation", list(pages.keys()), label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("<div style='text-align: center; color: var(--text-muted); font-size: 0.8rem;'>System Status: <span style='color: var(--neon-cyan);'>Online</span></div>", unsafe_allow_html=True)

    # Render the selected page
    pages[selection]()

if __name__ == "__main__":
    main()
