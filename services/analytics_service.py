import streamlit as st
import json
import logging
from datetime import datetime
from langchain_community.llms import Ollama

OLLAMA_MODEL = "mistral"
logger = logging.getLogger(__name__)

COACH_PROMPT_TEMPLATE = """You are NeuroLearn AI, an expert AI Study Coach.
Analyze the student's current session analytics and provide a personalized learning report.

Student Analytics Data:
---------------------
{analytics_json}
---------------------

Provide your response strictly in the following structure using Markdown:
### 🚨 Weak Concepts Identified
(List 1-2 areas where the student is struggling based on low quiz scores or high question volume)

### 🌟 Strong Concepts
(List 1-2 areas where the student is excelling based on high quiz scores)

### 📈 Recommended Next Steps
(Provide 2-3 specific, actionable study recommendations for the student to improve)

Do not include any conversational filler outside of this structure.
"""

def init_analytics_state():
    """Initializes the session state dictionary for analytics tracking if it doesn't exist."""
    if 'analytics' not in st.session_state:
        st.session_state.analytics = {
            "session_start": datetime.now().isoformat(),
            "total_questions_asked": 0,
            "flashcards_viewed": 0,
            "quizzes_taken": 0,
            "quiz_history": [],  # List of {topic, score, total, percentage, timestamp}
            "topics_studied": {} # Dictionary mapping topic -> interaction count
        }

def track_question(topic="General Chat"):
    """Increments the tutor questions metric."""
    if 'analytics' in st.session_state:
        st.session_state.analytics["total_questions_asked"] += 1
        st.session_state.analytics["topics_studied"][topic] = st.session_state.analytics["topics_studied"].get(topic, 0) + 1

def track_flashcard(topic="General Deck"):
    """Increments the flashcard views metric."""
    if 'analytics' in st.session_state:
        st.session_state.analytics["flashcards_viewed"] += 1
        st.session_state.analytics["topics_studied"][topic] = st.session_state.analytics["topics_studied"].get(topic, 0) + 1

def track_quiz(topic, score, total):
    """Logs a completed quiz result."""
    if 'analytics' in st.session_state:
        st.session_state.analytics["quizzes_taken"] += 1
        st.session_state.analytics["topics_studied"][topic] = st.session_state.analytics["topics_studied"].get(topic, 0) + 1
        
        percentage = (score / total) * 100 if total > 0 else 0
        
        st.session_state.analytics["quiz_history"].append({
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": percentage,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })

def generate_ai_insights():
    """
    Sends the current analytics state to Ollama to generate study recommendations.
    """
    if 'analytics' not in st.session_state:
        return "Not enough data collected yet. Start studying to generate insights!"
        
    data = st.session_state.analytics
    
    # If the user hasn't done anything yet
    if data["total_questions_asked"] == 0 and data["quizzes_taken"] == 0 and data["flashcards_viewed"] == 0:
        return "You haven't started studying in this session yet! Ask the AI Tutor a question, take a quiz, or review flashcards to generate insights."
        
    try:
        # Prepare a summarized JSON string for the LLM
        summary = {
            "questions_asked": data["total_questions_asked"],
            "flashcards_reviewed": data["flashcards_viewed"],
            "quizzes_completed": data["quizzes_taken"],
            "quiz_results": data["quiz_history"],
            "most_frequent_topics": data["topics_studied"]
        }
        
        prompt = COACH_PROMPT_TEMPLATE.format(analytics_json=json.dumps(summary, indent=2))
        
        logger.info(f"Generating AI insights with {OLLAMA_MODEL}...")
        llm = Ollama(model=OLLAMA_MODEL, temperature=0.3)
        return llm.invoke(prompt).strip()
        
    except Exception as e:
        logger.error(f"AI Insights Generation Error: {e}")
        return "Failed to generate AI insights due to an internal error."
