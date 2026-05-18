import streamlit as st
import time
from services.quiz_service import generate_quiz

def render():
    st.markdown("<h2 class='neon-text-cyan'>Neural Quiz Generator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Test your knowledge with AI-generated, context-grounded assessments.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize session state for quiz
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'current_q_idx' not in st.session_state:
        st.session_state.current_q_idx = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'answered_current' not in st.session_state:
        st.session_state.answered_current = False
        
    # Configuration Panel (only show if no quiz is active)
    if not st.session_state.quiz_data:
        st.markdown("### Quiz Configuration")
        with st.container():
            st.markdown("<div class='cyber-card' style='padding: 20px;'>", unsafe_allow_html=True)
            topic = st.text_input("Quiz Topic / Focus Area", placeholder="e.g., Backpropagation")
            col1, col2 = st.columns(2)
            with col1:
                difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced", "Exam-Oriented"])
            with col2:
                num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=3)
                
            st.markdown("<div class='btn-cyan' style='margin-top: 15px;'>", unsafe_allow_html=True)
            if st.button("Generate Neural Quiz", use_container_width=True):
                if not topic:
                    st.warning("Please enter a topic.")
                else:
                    with st.spinner("Extracting RAG Context & Synthesizing Questions..."):
                        quiz_data = generate_quiz(topic, num_questions, difficulty)
                        
                        if quiz_data:
                            st.session_state.quiz_data = quiz_data
                            st.session_state.current_q_idx = 0
                            st.session_state.score = 0
                            st.session_state.quiz_completed = False
                            st.session_state.answered_current = False
                            st.rerun()
                        else:
                            st.error("Failed to generate quiz. The knowledge core may lack sufficient context on this topic, or the LLM failed to structure the response.")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
    # Active Quiz UI
    elif not st.session_state.quiz_completed:
        quiz = st.session_state.quiz_data
        idx = st.session_state.current_q_idx
        question = quiz[idx]
        
        st.markdown(f"### Question {idx + 1} of {len(quiz)}")
        st.progress((idx) / len(quiz))
        
        st.markdown(f'''
            <div class="cyber-card" style="padding: 20px; border-color: var(--neon-cyan); margin-bottom: 20px;">
                <h4 style="margin-top:0;">{question['question']}</h4>
            </div>
        ''', unsafe_allow_html=True)
        
        # Display options
        selected_option = st.radio("Select your answer:", question['options'], key=f"q_{idx}")
        
        # Action Buttons
        st.markdown("<div style='display: flex; gap: 10px; margin-top: 20px;'>", unsafe_allow_html=True)
        
        if not st.session_state.answered_current:
            if st.button("Submit Answer", type="primary"):
                st.session_state.answered_current = True
                if selected_option == question['correct_answer']:
                    st.session_state.score += 1
                st.rerun()
        else:
            # Show feedback
            is_correct = selected_option == question['correct_answer']
            if is_correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{question['correct_answer']}**")
                
            st.info(f"**Explanation:** {question['explanation']}")
            
            if st.button("Next Question"):
                if idx + 1 < len(quiz):
                    st.session_state.current_q_idx += 1
                    st.session_state.answered_current = False
                else:
                    st.session_state.quiz_completed = True
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

    # Quiz Results
    else:
        st.markdown("### Neural Assessment Complete")
        
        total = len(st.session_state.quiz_data)
        score = st.session_state.score
        percentage = (score / total) * 100
        
        color = "var(--neon-cyan)" if percentage >= 70 else "var(--neon-purple)"
        
        st.markdown(f'''
            <div class="cyber-card" style="text-align: center; padding: 40px; border-color: {color};">
                <h1 style="color: {color}; font-size: 3rem; margin-bottom: 10px;">{score} / {total}</h1>
                <h3 style="color: var(--text-muted);">Accuracy: {percentage:.1f}%</h3>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("Generate New Quiz"):
            st.session_state.quiz_data = None
            st.rerun()
