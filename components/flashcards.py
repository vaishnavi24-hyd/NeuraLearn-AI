import streamlit as st

def render():
    st.markdown("<h2 class='neon-text-cyan'>Spaced Repetition Flashcards</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Review key concepts using optimized spaced repetition algorithms.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    deck = st.selectbox("Select Deck", ["All Topics", "Machine Learning Deck", "Biology Deck"])
    
    # Mock Flashcard Interface
    st.markdown("<div style='display: flex; justify-content: center; margin-top: 40px;'>", unsafe_allow_html=True)
    
    # Flashcard CSS Animation Placeholder
    st.markdown('''
        <style>
        .flip-card {
            background-color: transparent;
            width: 600px;
            height: 300px;
            perspective: 1000px;
            margin: 0 auto;
        }
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            box-shadow: 0 10px 20px rgba(0, 243, 255, 0.2);
            border-radius: 15px;
        }
        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
            border: 2px solid var(--neon-cyan);
            background: var(--card-bg);
            padding: 20px;
        }
        .flip-card-front {
            color: var(--text-main);
        }
        .flip-card-back {
            color: var(--neon-cyan);
            transform: rotateY(180deg);
        }
        </style>

        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <h2 style="font-family: 'Inter', sans-serif;">What is Backpropagation?</h2>
                    <p style="position: absolute; bottom: 10px; color: var(--text-muted); font-size: 0.8rem;">(Hover to flip)</p>
                </div>
                <div class="flip-card-back">
                    <p style="font-size: 1.2rem;">An algorithm used to calculate derivatives of the error function with respect to the weights of a neural network, allowing for weight adjustment during training.</p>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Rating Buttons
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.button("Again (1m)", use_container_width=True)
    with c2:
        st.button("Hard (10m)", use_container_width=True)
    with c3:
        st.button("Good (1d)", use_container_width=True)
    with c4:
        st.button("Easy (4d)", use_container_width=True)
