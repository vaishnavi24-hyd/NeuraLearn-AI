import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_radar_chart():
    categories = ['Machine Learning', 'Biology', 'History', 'Math', 'Physics']
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[85, 40, 70, 90, 60],
        theta=categories,
        fill='toself',
        name='Current Mastery',
        line=dict(color='#00f3ff'),
        fillcolor='rgba(0, 243, 255, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.1)',
                linecolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                linecolor='rgba(255, 255, 255, 0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        margin=dict(l=40, r=40, t=20, b=20),
    )
    return fig

def create_activity_heatmap():
    z = np.random.randint(0, 10, size=(7, 10))
    fig = go.Figure(data=go.Heatmap(
        z=z,
        colorscale=[[0, 'rgba(0,0,0,0)'], [1, '#b026ff']],
        showscale=False,
        xgap=2,
        ygap=2
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=150
    )
    return fig

def render():
    st.markdown("<h2 class='neon-text-purple'>Neural Study Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted);'>Track your cognitive progression and knowledge retention over time.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Domain Mastery Radar")
        st.plotly_chart(create_radar_chart(), use_container_width=True)
        
    with col2:
        st.markdown("### Learning Activity Heatmap")
        st.plotly_chart(create_activity_heatmap(), use_container_width=True)
        
        st.markdown("### Recent Milestones")
        st.markdown('''
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px;">
                    <span style="color: var(--neon-cyan);">[System]</span> Mastered CNN concept cluster. <span style="color: var(--text-muted); font-size: 0.8rem;">(2h ago)</span>
                </li>
                <li style="margin-bottom: 10px;">
                    <span style="color: var(--neon-cyan);">[System]</span> Uploaded 'Bio Chapter 4'. Neural mapping complete. <span style="color: var(--text-muted); font-size: 0.8rem;">(1d ago)</span>
                </li>
                <li style="margin-bottom: 10px;">
                    <span style="color: var(--neon-purple);">[Alert]</span> Spaced repetition due for 'Krebs Cycle'. <span style="color: var(--text-muted); font-size: 0.8rem;">(Pending)</span>
                </li>
            </ul>
        ''', unsafe_allow_html=True)
