import streamlit as st
import os

def inject_premium_css():
    """Injects the unified dark neon cyberpunk design system CSS into the app."""
    css_file = os.path.join(os.path.dirname(__file__), "main.css")
    try:
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Failed to load premium theme: CSS file not found at {css_file}")

def apply_premium_theme():
    """Applies the Phase 10 elite UI/UX configuration and styling."""
    st.set_page_config(
        page_title="NeuroLearn AI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    inject_premium_css()
