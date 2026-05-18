import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.analytics_service import generate_ai_insights

def render():
    st.markdown("<h2 class='neon-text-cyan'>Learning Analytics & Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Track your academic performance and receive AI-driven study coaching.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Check if analytics exist
    if 'analytics' not in st.session_state or st.session_state.analytics.get('total_questions_asked', 0) == 0 and st.session_state.analytics.get('quizzes_taken', 0) == 0 and st.session_state.analytics.get('flashcards_viewed', 0) == 0:
        st.markdown('''
            <div style="text-align: center; margin-top: 60px; margin-bottom: 60px;">
                <div class="empty-state-icon">📊</div>
                <h3 style="color: var(--text-main);">Telemetry Offline</h3>
                <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">
                    The analytics core is currently idle. Interact with the AI Tutor, complete a Quiz, or review Flashcards to begin generating real-time learning insights.
                </p>
            </div>
        ''', unsafe_allow_html=True)
        return
        
    data = st.session_state.analytics
    
    # ---------------------------------------------------------
    # TOP LEVEL KPI METRICS
    # ---------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
            <div class="cyber-card" style="text-align: center; border-color: var(--neon-cyan);">
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Questions Asked</div>
                <div style="font-size: 2rem; font-weight: 700; color: var(--neon-cyan);">{data["total_questions_asked"]}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''
            <div class="cyber-card" style="text-align: center; border-color: var(--neon-purple);">
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Quizzes Taken</div>
                <div style="font-size: 2rem; font-weight: 700; color: var(--neon-purple);">{data["quizzes_taken"]}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'''
            <div class="cyber-card" style="text-align: center; border-color: #00ff80;">
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Flashcards Reviewed</div>
                <div style="font-size: 2rem; font-weight: 700; color: #00ff80;">{data["flashcards_viewed"]}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col4:
        # Calculate Average Score
        avg_score = 0
        if data["quiz_history"]:
            total_pct = sum([q["percentage"] for q in data["quiz_history"]])
            avg_score = total_pct / len(data["quiz_history"])
            
        color = "#00ff80" if avg_score >= 70 else "var(--neon-purple)"
        if avg_score == 0 and not data["quiz_history"]:
            color = "var(--text-muted)"
            
        st.markdown(f'''
            <div class="cyber-card" style="text-align: center; border-color: {color};">
                <div style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase;">Avg Quiz Score</div>
                <div style="font-size: 2rem; font-weight: 700; color: {color};">{avg_score:.1f}%</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # VISUALIZATIONS (PLOTLY)
    # ---------------------------------------------------------
    vcol1, vcol2 = st.columns(2)
    
    with vcol1:
        st.markdown("### Topic Mastery Focus")
        if data["topics_studied"]:
            df_topics = pd.DataFrame(list(data["topics_studied"].items()), columns=["Topic", "Interactions"])
            fig = px.pie(
                df_topics, 
                values='Interactions', 
                names='Topic',
                hole=0.4,
                color_discrete_sequence=["#00F5FF", "#C800FF", "#00FF85", "#FFB800"]
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8a95a5"),
                margin=dict(t=30, b=10, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No topic data tracked yet.")
            
    with vcol2:
        st.markdown("### Quiz Performance Trend")
        if data["quiz_history"]:
            df_scores = pd.DataFrame(data["quiz_history"])
            # Create a simple line chart
            fig2 = px.line(
                df_scores, 
                x=df_scores.index, 
                y='percentage',
                markers=True,
                hover_data=['topic', 'timestamp']
            )
            fig2.update_traces(line_color="#00f3ff", marker=dict(color="#b026ff", size=10))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8a95a5"),
                xaxis_title="Quiz Attempt",
                yaxis_title="Score (%)",
                yaxis_range=[0, 105],
                margin=dict(t=30, b=10, l=10, r=10)
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Take a quiz to visualize your performance trends.")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # AI STUDY COACH (MISTRAL INSIGHTS)
    # ---------------------------------------------------------
    st.markdown("### 🤖 Neural Study Coach")
    st.markdown("<p style='color: var(--text-muted); font-size: 0.9rem;'>Generating personalized insights based on your learning telemetry...</p>", unsafe_allow_html=True)
    
    if st.button("Generate Performance Report", type="primary"):
        with st.spinner("Analyzing performance metrics and constructing feedback..."):
            insights_md = generate_ai_insights()
            
            st.markdown(f'''
                <div class="cyber-card" style="padding: 30px; border-left: 4px solid var(--neon-purple); background: rgba(176, 38, 255, 0.05);">
                    {insights_md}
                </div>
            ''', unsafe_allow_html=True)
