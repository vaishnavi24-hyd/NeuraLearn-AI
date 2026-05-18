import streamlit as st
import random
from services.flashcard_service import generate_flashcards
from services.analytics_service import track_flashcard

def render():
    st.markdown("<h2 class='neon-text-purple'>Neural Flashcards</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Rapid active recall testing using AI-generated definition mappings.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize session state for flashcards
    if 'flashcard_data' not in st.session_state:
        st.session_state.flashcard_data = None
    if 'current_fc_idx' not in st.session_state:
        st.session_state.current_fc_idx = 0
    if 'is_flipped' not in st.session_state:
        st.session_state.is_flipped = False

    # Configuration Panel (only show if no deck is active)
    if not st.session_state.flashcard_data:
        # Polished Empty State Onboarding
        st.markdown('''
            <div style="text-align: center; margin-bottom: 30px;">
                <div class="empty-state-icon">🗂️</div>
                <h3 style="color: var(--text-main);">No Active Deck</h3>
                <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
                    Synthesize a new deck of interactive flashcards based on your uploaded documents. Perfect for rapid active recall testing.
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("### Deck Configuration")
        with st.container():
            st.markdown("<div class='cyber-card' style='padding: 30px; border-color: var(--neon-purple);'>", unsafe_allow_html=True)
            topic = st.text_input("Flashcard Topic / Concept", placeholder="e.g., Forward Pass vs Backward Pass")
            num_cards = st.slider("Number of Cards", min_value=3, max_value=15, value=5)
                
            st.markdown("<div class='btn-purple' style='margin-top: 15px;'>", unsafe_allow_html=True)
            if st.button("Synthesize Flashcard Deck", use_container_width=True):
                if not topic:
                    st.warning("Please enter a topic.")
                else:
                    with st.spinner("Extracting Concepts & Synthesizing Deck..."):
                        fc_data = generate_flashcards(topic, num_cards)
                        
                        if fc_data:
                            st.session_state.flashcard_data = fc_data
                            st.session_state.current_fc_idx = 0
                            st.session_state.is_flipped = False
                            st.session_state.last_fc_topic = topic
                            st.rerun()
                        else:
                            st.error("Failed to generate flashcards. The knowledge core may lack sufficient context on this topic.")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
    # Active Flashcard UI
    else:
        deck = st.session_state.flashcard_data
        idx = st.session_state.current_fc_idx
        card = deck[idx]
        
        st.markdown(f"### Card {idx + 1} of {len(deck)}")
        
        # Determine what to show based on flip state
        content = card['back'] if st.session_state.is_flipped else card['front']
        label = "ANSWER" if st.session_state.is_flipped else "QUESTION / CONCEPT"
        color = "var(--neon-cyan)" if st.session_state.is_flipped else "var(--neon-purple)"
        
        # Display the card
        st.markdown(f'''
            <div class="cyber-card" style="
                min-height: 250px; 
                display: flex; 
                flex-direction: column;
                justify-content: center; 
                align-items: center; 
                text-align: center; 
                padding: 40px; 
                border-color: {color};
                margin-bottom: 30px;
                transition: all 0.3s ease;
            ">
                <div style="font-size: 0.8rem; color: {color}; letter-spacing: 2px; margin-bottom: 20px;">{label}</div>
                <h3 style="margin: 0; line-height: 1.5;">{content}</h3>
            </div>
        ''', unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
                st.session_state.current_fc_idx -= 1
                st.session_state.is_flipped = False
                st.rerun()
                
        with col2:
            flip_label = "Show Question" if st.session_state.is_flipped else "Show Answer"
            if st.button(f"🔄 {flip_label}", use_container_width=True, type="primary"):
                st.session_state.is_flipped = not st.session_state.is_flipped
                if st.session_state.is_flipped:
                    # Track analytics only when showing the answer
                    track_flashcard(st.session_state.get('last_fc_topic', 'General Flashcards'))
                st.rerun()
                
        with col3:
            if st.button("Next ➡️", use_container_width=True, disabled=(idx == len(deck) - 1)):
                st.session_state.current_fc_idx += 1
                st.session_state.is_flipped = False
                st.rerun()
                
        st.markdown("---")
        
        col_end1, col_end2 = st.columns(2)
        with col_end1:
            if st.button("🔀 Shuffle Deck"):
                random.shuffle(st.session_state.flashcard_data)
                st.session_state.current_fc_idx = 0
                st.session_state.is_flipped = False
                st.rerun()
        with col_end2:
            if st.button("❌ Close Deck"):
                st.session_state.flashcard_data = None
                st.rerun()
