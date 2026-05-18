import streamlit as st
import os

def inject_custom_css():
    """Injects custom CSS from styles/main.css into the Streamlit app."""
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "main.css")
    try:
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at {css_file}")

def apply_theme():
    """Sets page config and applies CSS."""
    st.set_page_config(
        page_title="NeuroLearn AI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    inject_custom_css()
