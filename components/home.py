import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_placeholder_chart():
    """Creates a futuristic placeholder chart using Plotly."""
    # Generate some random placeholder data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
    y2 = np.cos(x) + np.random.normal(0, 0.1, 100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        mode='lines',
        name='Knowledge Graph Density',
        line=dict(color='#00f3ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 243, 255, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        mode='lines',
        name='Neural Activation',
        line=dict(color='#b026ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(176, 38, 255, 0.1)'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(0, 243, 255, 0.1)', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0, 243, 255, 0.1)', zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def render():
    # Hero Section
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'><span class='neon-text-cyan'>NeuroLearn</span> <span class='neon-text-purple'>AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: var(--text-muted); margin-top: 10px; margin-bottom: 40px;'>Empowering cognitive growth through visually immersive AI.</p>", unsafe_allow_html=True)
    
    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('''
            <div class="cyber-card" style="text-align: center;">
                <div class="card-value">2.4M</div>
                <div class="card-text">Nodes Mapped</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <div class="cyber-card" style="text-align: center;">
                <div class="card-value neon-text-purple">98%</div>
                <div class="card-text">Concept Retention</div>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown('''
            <div class="cyber-card" style="text-align: center;">
                <div class="card-value">15k</div>
                <div class="card-text">Active Learners</div>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown('''
            <div class="cyber-card" style="text-align: center;">
                <div class="card-value neon-text-purple">24/7</div>
                <div class="card-text">AI Availability</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("### System Dashboard Overview")
    
    # Chart Section
    st.plotly_chart(create_placeholder_chart(), use_container_width=True)
    
    # Feature Cards
    st.markdown("### Platform Modules")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.markdown('''
            <div class="cyber-card">
                <div class="card-title">Neural Upload</div>
                <p class="card-text">Ingest PDFs and lecture notes into the quantum knowledge base.</p>
                <div style="margin-top: 15px;"><span style="color: var(--neon-cyan); border: 1px solid var(--neon-cyan); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">Ready</span></div>
            </div>
        ''', unsafe_allow_html=True)

    with f_col2:
        st.markdown('''
            <div class="cyber-card">
                <div class="card-title">Cognitive Visuals</div>
                <p class="card-text">Auto-generate dynamic flowcharts and concept maps instantly.</p>
                <div style="margin-top: 15px;"><span style="color: var(--neon-purple); border: 1px solid var(--neon-purple); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">Initializing...</span></div>
            </div>
        ''', unsafe_allow_html=True)

    with f_col3:
        st.markdown('''
            <div class="cyber-card">
                <div class="card-title">Adaptive Quizzes</div>
                <p class="card-text">Test your knowledge against AI-calibrated difficulty curves.</p>
                 <div style="margin-top: 15px;"><span style="color: var(--text-muted); border: 1px solid var(--text-muted); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">Standby</span></div>
            </div>
        ''', unsafe_allow_html=True)
