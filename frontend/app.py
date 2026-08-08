"""
frontend/app.py
Professional HRMS AI Resume Screening System
Modern dark-themed Streamlit UI with glassmorphism, refined typography, and polished UX
"""

import streamlit as st
import sys
import os
import pandas as pd
import math
from datetime import datetime

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.resume_scanner import screen_multiple_resumes
from services.chat_assistant import get_chatbot_response, get_suggested_questions, format_resume_context

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ATS Resume Screening",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DESIGN TOKENS - DARK PROFESSIONAL THEME
# ============================================================================

# Modern dark color palette - professional enterprise design
COLORS = {
    # Backgrounds
    "bg_primary": "#0a0e14",      # Deep navy-black (main background)
    "bg_secondary": "#11141f",    # Card backgrounds
    "bg_elevated": "#16192a",     # Elevated surfaces (hover, focus)
    
    # Accents - modern cyan-blue (tech-forward)
    "primary": "#0ea5e9",         # Primary accent
    "primary_light": "#06b6d4",   # Lighter variant
    "primary_dark": "#0369a1",    # Darker variant
    "primary_faint": "#082f49",   # Very subtle background
    
    # Status colors
    "success": "#10b981",         # Emerald green
    "success_bg": "#064e3b",      # Dark emerald bg
    "warning": "#f59e0b",         # Amber
    "warning_bg": "#78350f",      # Dark amber bg
    "danger": "#ef4444",          # Red
    "danger_bg": "#7f1d1d",       # Dark red bg
    
    # Text
    "text_primary": "#f1f5f9",    # Light text
    "text_secondary": "#94a3b8",  # Muted text
    "text_tertiary": "#64748b",   # Even more muted
    
    # Borders & Dividers
    "border": "#1e293b",          # Subtle borders
    "border_light": "#475569",    # Lighter borders
    "border_focus": "#0ea5e9",    # Focus state
}

# Score thresholds with refined dark theme styling
SCORE_CONFIG = {
    "high": {
        "min": 80,
        "label": "Strong Match",
        "badge": "🟢",
        "color_bg": COLORS["success_bg"],
        "color_border": COLORS["success"],
        "color_text": "#d1fae5"
    },
    "medium": {
        "min": 60,
        "label": "Good Match",
        "badge": "🟡",
        "color_bg": COLORS["warning_bg"],
        "color_border": COLORS["warning"],
        "color_text": "#fef3c7"
    },
    "low": {
        "min": 40,
        "label": "Fair Match",
        "badge": "🟠",
        "color_bg": "#8b5a00",
        "color_border": "#f59e0b",
        "color_text": "#fcd34d"
    },
    "very_low": {
        "min": 0,
        "label": "Not Suitable",
        "badge": "🔴",
        "color_bg": COLORS["danger_bg"],
        "color_border": COLORS["danger"],
        "color_text": "#fecaca"
    }
}

# ============================================================================
# CUSTOM STYLING - DARK THEME WITH GLASSMORPHISM
# ============================================================================

st.markdown(f"""
    <style>
    /* Import modern typefaces */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Root styles - dark theme foundation */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, {COLORS["bg_primary"]} 0%, {COLORS["bg_secondary"]} 100%);
        color: {COLORS["text_primary"]};
    }}
    
    /* Typography - refined hierarchy */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700;
        color: {COLORS["text_primary"]};
        letter-spacing: -0.02em;
    }}
    
    h1 {{ font-size: 2.5rem; line-height: 1.1; font-weight: 800; }}
    h2 {{ font-size: 2rem; line-height: 1.2; font-weight: 700; }}
    h3 {{ font-size: 1.5rem; line-height: 1.3; font-weight: 700; }}
    h4 {{ font-size: 1.25rem; line-height: 1.4; font-weight: 600; }}
    
    p, span, label {{
        color: {COLORS["text_primary"]};
        line-height: 1.6;
    }}
    
    /* Buttons - modern glassmorphic style */
    .stButton > button {{
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        border-radius: 10px;
        border: 1px solid transparent;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 0.75rem 1.5rem;
        background: {COLORS["bg_secondary"]};
        color: {COLORS["text_primary"]};
        border: 1px solid {COLORS["border"]};
    }}
    
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_dark"]} 100%);
        color: white;
        border: none;
        box-shadow: 0 8px 16px rgba(14, 165, 233, 0.2),
                    0 0 20px rgba(14, 165, 233, 0.1);
    }}
    
    .stButton > button[kind="primary"]:hover {{
        box-shadow: 0 12px 24px rgba(14, 165, 233, 0.3),
                    0 0 30px rgba(14, 165, 233, 0.15);
        transform: translateY(-2px);
        background: linear-gradient(135deg, {COLORS["primary_light"]} 0%, {COLORS["primary"]} 100%);
    }}
    
    .stButton > button[kind="primary"]:active {{
        transform: translateY(0);
    }}
    
    .stButton > button[kind="secondary"] {{
        background: {COLORS["bg_elevated"]};
        color: {COLORS["text_primary"]};
        border: 1px solid {COLORS["border_light"]};
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: {COLORS["bg_elevated"]};
        border-color: {COLORS["primary"]};
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.1);
    }}
    
    .stButton > button:disabled {{
        opacity: 0.5;
        cursor: not-allowed;
    }}
    
    /* Input fields - glassmorphic style */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        background: {COLORS["bg_secondary"]} !important;
        border: 1.5px solid {COLORS["border"]} !important;
        border-radius: 10px !important;
        font-size: 0.95rem;
        padding: 0.75rem;
        color: {COLORS["text_primary"]} !important;
        transition: all 0.2s ease;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: {COLORS["text_tertiary"]};
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {COLORS["primary"]} !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15) !important;
        outline: none !important;
    }}
    
    /* Labels - refined typography */
    label {{
        font-weight: 600;
        color: {COLORS["text_primary"]};
        font-size: 0.95rem;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Sidebar - professional styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS["bg_secondary"]} 0%, {COLORS["bg_primary"]} 100%);
        border-right: 1px solid {COLORS["border"]};
    }}
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2 {{
        color: {COLORS["text_primary"]};
        margin-top: 1.5rem;
    }}
    
    [data-testid="stSidebar"] h1:first-child {{
        margin-top: 0;
    }}
    
    [data-testid="stSidebar"] p {{
        color: {COLORS["text_secondary"]};
    }}
    
    /* Alerts & Info boxes - elevated styling */
    .stAlert {{
        border-radius: 10px;
        border-left: 4px solid;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        background: {COLORS["bg_secondary"]};
        border-color: {COLORS["border"]};
    }}
    
    .stSuccess {{
        background-color: {COLORS["success_bg"]} !important;
        border-left-color: {COLORS["success"]} !important;
        color: {COLORS["text_primary"]} !important;
    }}
    
    .stError {{
        background-color: {COLORS["danger_bg"]} !important;
        border-left-color: {COLORS["danger"]} !important;
        color: {COLORS["text_primary"]} !important;
    }}
    
    .stWarning {{
        background-color: {COLORS["warning_bg"]} !important;
        border-left-color: {COLORS["warning"]} !important;
        color: {COLORS["text_primary"]} !important;
    }}
    
    .stInfo {{
        background-color: {COLORS["primary_faint"]} !important;
        border-left-color: {COLORS["primary"]} !important;
        color: {COLORS["text_primary"]} !important;
    }}
    
    /* Metrics - card styling */
    [data-testid="metric-container"] {{
        background: {COLORS["bg_secondary"]};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {COLORS["border"]};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }}
    
    [data-testid="metric-container"]:hover {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1);
    }}
    
    [data-testid="metric-container"] > div:first-child {{
        color: {COLORS["text_secondary"]};
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.75rem;
    }}
    
    [data-testid="metric-container"] > div:nth-child(2) {{
        color: {COLORS["primary"]};
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }}
    
    /* Chat messages - refined styling */
    .chat-message {{
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease-out;
    }}
    
    .chat-message.user {{
        text-align: right;
    }}
    
    .chat-message.assistant {{
        text-align: left;
    }}
    
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Dividers - elegant separators */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS["border"]}, transparent);
        margin: 2rem 0;
    }}
    
    .separator {{
        height: 1px;
        background: {COLORS["border"]};
        margin: 1rem 0;
    }}
    
    /* Expander - glassmorphic style */
    .streamlit-expanderHeader {{
        border-radius: 10px;
        background: {COLORS["bg_elevated"]};
        border: 1px solid {COLORS["border"]};
        transition: all 0.2s ease;
        padding: 0.75rem;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: {COLORS["bg_elevated"]};
        border-color: {COLORS["primary"]};
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.1);
    }}
    
    .streamlit-expanderHeader p {{
        color: {COLORS["text_primary"]};
        font-weight: 600;
    }}
    
    /* File uploader - enhanced styling */
    .stFileUploadDropzone {{
        border: 2px dashed {COLORS["border_light"]};
        border-radius: 12px;
        background: {COLORS["bg_elevated"]};
        transition: all 0.2s ease;
    }}
    
    .stFileUploadDropzone:hover {{
        border-color: {COLORS["primary"]};
        background: {COLORS["bg_elevated"]};
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.1);
    }}
    
    /* Badge styling */
    .badge {{
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: {COLORS["bg_elevated"]};
        color: {COLORS["text_primary"]};
        border: 1px solid {COLORS["border"]};
    }}
    
    .badge.primary {{
        background: rgba(14, 165, 233, 0.1);
        color: {COLORS["primary"]};
        border-color: {COLORS["primary"]};
    }}
    
    .badge.success {{
        background: rgba(16, 185, 129, 0.1);
        color: {COLORS["success"]};
        border-color: {COLORS["success"]};
    }}
    
    .badge.danger {{
        background: rgba(239, 68, 68, 0.1);
        color: {COLORS["danger"]};
        border-color: {COLORS["danger"]};
    }}
    
    /* Container styling */
    .container {{
        max-width: 100%;
        padding: 0;
    }}
    
    /* Custom card styling for elevated sections */
    .glass-card {{
        background: {COLORS["bg_secondary"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}
    
    .glass-card:hover {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1);
    }}
    
    /* Smooth scroll behavior */
    html {{
        scroll-behavior: smooth;
    }}
    
    /* Selection styling */
    ::selection {{
        background: rgba(14, 165, 233, 0.3);
        color: {COLORS["text_primary"]};
    }}
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

session_defaults = {
    'results': [],
    'current_page': 1,
    'results_per_page': 10,
    'job_description': "",
    'chat_active': False,
    'chat_context': None,
    'chat_history': [],
    'analysis_complete': False,
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_score_category(score: int) -> dict:
    """Determine score category and styling."""
    for key in ["high", "medium", "low", "very_low"]:
        if score >= SCORE_CONFIG[key]["min"]:
            return SCORE_CONFIG[key]
    return SCORE_CONFIG["very_low"]

def render_score_badge(score: int) -> str:
    """Create an HTML badge for scores with modern styling."""
    config = get_score_category(score)
    return f"""
    <div style="
        display: inline-block;
        background: {config['color_bg']};
        color: {config['color_text']};
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        border: 1px solid {config['color_border']};
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    ">
        {config['badge']} {score}/100 — {config['label']}
    </div>
    """

def render_result_card(result: dict, rank: int) -> None:
    """Render a polished result card with modern glassmorphic styling."""
    score = result.get('ats_score', 0)
    config = get_score_category(score)
    candidate_name = result.get('candidate_name', 'Unknown')
    filename = result.get('filename', 'Unknown')
    
    # Card container with glassmorphism
    st.markdown(f"""
    <div style="
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    ">
    """, unsafe_allow_html=True)
    
    # Header row with candidate info
    col1, col2, col3 = st.columns([2, 1, 0.8], gap="medium")
    
    with col1:
        st.markdown(f"<div style='display: flex; align-items: baseline; gap: 0.75rem;'><span style='font-size: 1.75rem; font-weight: 800; color: {COLORS['primary']};'>#{rank}</span><h3 style='margin: 0; padding: 0;'>{candidate_name}</h3></div>", unsafe_allow_html=True)
        st.caption(f"📄 {filename}")
    
    with col2:
        st.markdown(render_score_badge(score), unsafe_allow_html=True)
    
    with col3:
        if st.button("💬 Chat", key=f"chat_{rank}", use_container_width=True):
            resume_context = format_resume_context(
                result,
                result.get('resume_text', ''),
                st.session_state.job_description
            )
            st.session_state.chat_active = True
            st.session_state.chat_context = resume_context
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown(f"<div class='separator'></div>", unsafe_allow_html=True)
    
    # Details metrics
    col_a, col_b, col_c = st.columns(3, gap="medium")
    
    with col_a:
        exp = result.get('experience_years', 'N/A')
        st.metric("Experience", f"{exp} years" if exp != 'N/A' else exp)
    
    with col_b:
        edu = result.get('education', 'N/A')
        st.metric("Education", edu)
    
    with col_c:
        rec = result.get('recommendation', 'N/A')
        st.metric("Recommendation", rec)
    
    # Expandable analysis details
    with st.expander("📊 Detailed Analysis", expanded=False):
        analysis_col1, analysis_col2 = st.columns(2, gap="large")
        
        with analysis_col1:
            st.markdown(f"<p style='color: {COLORS['primary']}; font-weight: 700; font-size: 1rem;'>✅ Matched Skills</p>", unsafe_allow_html=True)
            matched = result.get('matched_skills', [])
            if matched:
                for skill in matched:
                    st.markdown(f"<span class='badge primary' style='margin: 0.25rem 0.5rem 0.25rem 0;'>{skill}</span>", unsafe_allow_html=True)
            else:
                st.info("No skills matched")
        
        with analysis_col2:
            st.markdown(f"<p style='color: {COLORS['danger']}; font-weight: 700; font-size: 1rem;'>❌ Missing Skills</p>", unsafe_allow_html=True)
            missing = result.get('missing_skills', [])
            if missing:
                for skill in missing:
                    st.markdown(f"<span class='badge danger' style='margin: 0.25rem 0.5rem 0.25rem 0;'>{skill}</span>", unsafe_allow_html=True)
            else:
                st.success("All required skills present")
        
        st.divider()
        
        st.markdown(f"<p style='color: {COLORS['primary']}; font-weight: 700; font-size: 1rem;'>💪 Key Strengths</p>", unsafe_allow_html=True)
        strengths = result.get('key_strengths', [])
        if strengths:
            for strength in strengths:
                st.markdown(f"• {strength}")
        else:
            st.info("No strengths data available")
        
        st.divider()
        
        st.markdown(f"<p style='color: {COLORS['text_secondary']}; font-weight: 600; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;'>Summary</p>", unsafe_allow_html=True)
        summary = result.get('summary', 'No summary available')
        st.markdown(f"<p style='color: {COLORS['text_primary']}; line-height: 1.6;'>{summary}</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# PAGE STRUCTURE
# ============================================================================

# Header - modern gradient design
with st.container():
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 12px;
        margin-bottom: 3rem;
        box-shadow: 0 12px 32px rgba(14, 165, 233, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    ">
        <h1 style="color: white; margin: 0 0 0.75rem 0; letter-spacing: -0.02em;">📋 ATS Resume Screening</h1>
        <p style="color: rgba(255, 255, 255, 0.95); margin: 0; font-size: 1.1rem; font-weight: 500;">
            Intelligent AI-powered resume analysis and candidate engagement platform
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar - professional configuration panel
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 0.5rem 0;">
        <h2 style="font-size: 1.2rem; margin: 1.5rem 0 1rem 0; font-weight: 700;">⚙️ Settings</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.results_per_page = st.selectbox(
        "Results per page",
        [5, 10, 15, 20, 25],
        index=1,
        help="Adjust how many results display per page"
    )
    
    st.divider()
    
    if st.session_state.chat_active and st.session_state.chat_context:
        st.markdown(f"""
        <div style="
            background: {COLORS['primary_faint']};
            border: 1px solid {COLORS['primary']};
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <p style="font-weight: 700; color: {COLORS['primary']}; margin: 0 0 0.5rem 0;">💬 Active Chat</p>
            <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0 0 0; font-size: 0.9rem;"><strong>{st.session_state.chat_context.get('candidate_name', 'Unknown')}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            if st.button("❌ Close", use_container_width=True):
                st.session_state.chat_active = False
                st.session_state.chat_context = None
                st.session_state.chat_history = []
                st.rerun()
        
        st.divider()
        st.caption(f"📝 {len(st.session_state.chat_history)} messages in conversation")
    
    st.divider()
    
    with st.expander("ℹ️ About This Tool", expanded=False):
        st.markdown(f"""
        **⚡ Features**
        - 📄 Batch resume analysis
        - 🎯 AI-powered scoring
        - 📊 Detailed ranking
        - 💬 Intelligent chatbot
        - 📥 CSV export
        
        **🚀 Quick Start**
        1. Paste job description
        2. Upload resumes (PDF)
        3. Click "Analyze"
        4. Review & engage
        """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Chat interface
if st.session_state.chat_active and st.session_state.chat_context:
    
    st.markdown(f"""
    <div style="
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    ">
        <h1 style="margin: 0 0 0.5rem 0; color: {COLORS['primary']};">🤖 Candidate Chat</h1>
        <p style="color: {COLORS['text_secondary']}; margin: 0; font-weight: 500;">
            <strong style="color: {COLORS['text_primary']};">{st.session_state.chat_context.get('candidate_name', 'Unknown')}</strong> 
            • Score: <strong style="color: {COLORS['primary']};">{st.session_state.chat_context.get('ats_score', 0)}/100</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages container
    with st.container():
        for message in st.session_state.chat_history:
            with st.chat_message(message['role']):
                st.markdown(message['message'])
    
    # Suggested questions on first message
    if len(st.session_state.chat_history) == 0:
        st.markdown("---")
        st.subheader("💡 Suggested Questions")
        
        suggestions = get_suggested_questions()[:6]
        
        cols = st.columns(2)
        for idx, suggestion in enumerate(suggestions):
            with cols[idx % 2]:
                if st.button(
                    f"💬 {suggestion}",
                    key=f"suggest_{idx}",
                    use_container_width=True
                ):
                    st.session_state.chat_history.append({
                        "role": "user",
                        "message": suggestion
                    })
                    
                    with st.spinner("🤖 Analyzing..."):
                        response = get_chatbot_response(
                            suggestion,
                            st.session_state.chat_context,
                            st.session_state.chat_history
                        )
                    
                    if response['success']:
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "message": response['answer']
                        })
                    else:
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "message": f"❌ Error: {response.get('error', 'Unknown error')}"
                        })
                    
                    st.rerun()
    
    # User input
    st.markdown("---")
    user_question = st.chat_input("Ask anything about this candidate...")
    
    if user_question:
        with st.chat_message('user'):
            st.markdown(user_question)
        
        st.session_state.chat_history.append({
            'role': 'user',
            'message': user_question
        })
        
        with st.chat_message('assistant'):
            with st.spinner('🤖 Thinking...'):
                response = get_chatbot_response(
                    user_question,
                    st.session_state.chat_context,
                    st.session_state.chat_history
                )
                
                if response['success']:
                    st.markdown(response['answer'])
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'message': response['answer']
                    })
                else:
                    error_msg = f"❌ Error: {response.get('error', 'Unknown error')}"
                    st.markdown(error_msg)
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'message': error_msg
                    })
        
        st.rerun()

# Analysis interface
else:
    # Input section - two column layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(f"""
        <div class='glass-card'>
            <h3 style="margin: 0 0 1rem 0; color: {COLORS['primary']};">📋 Job Description</h3>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste the job description",
            height=300,
            value=st.session_state.job_description,
            placeholder="Example:\nJob Title: Senior Software Engineer\n\nRequirements:\n• 5+ years Python experience\n• Django/FastAPI expertise\n• PostgreSQL databases\n• AWS cloud experience",
            label_visibility="collapsed"
        )
        st.session_state.job_description = job_description
    
    with col2:
        st.markdown(f"""
        <div class='glass-card'>
            <h3 style="margin: 0 0 1rem 0; color: {COLORS['primary']};">📤 Upload Resumes</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Select PDF resumes",
            type=['pdf'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} resume(s) ready to analyze")
            
            with st.expander("📁 File List", expanded=False):
                for idx, file in enumerate(uploaded_files, 1):
                    st.caption(f"{idx}. {file.name}")
    
    # Analysis button - centered
    st.markdown("---")
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        analyze_button = st.button(
            "🚀 Analyze Resumes",
            use_container_width=True,
            type="primary"
        )
    
    if analyze_button:
        # Validation
        if not job_description.strip():
            st.error("⚠️ Please enter a job description to proceed")
            st.stop()
        
        if not uploaded_files:
            st.error("⚠️ Please upload at least one resume PDF")
            st.stop()
        
        st.session_state.current_page = 1
        
        # Progress tracking
        progress_container = st.container()
        status_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
        
        with status_container:
            status_text = st.empty()
        
        status_text.info(f"🔄 Analyzing {len(uploaded_files)} resume(s)...")
        
        try:
            results = screen_multiple_resumes(uploaded_files, job_description)
            progress_bar.progress(100)
            status_text.success(f"✅ Analysis complete! Processed {len(results)} resume(s).")
            
            if results:
                st.session_state.results = results
                st.session_state.analysis_complete = True
                st.rerun()
            else:
                st.error("❌ No resumes were processed. Please check your files and try again.")
        
        except Exception as e:
            progress_bar.progress(0)
            st.error(f"❌ Analysis failed: {str(e)}")
    
    # Results section
    if st.session_state.results and st.session_state.analysis_complete:
        results = st.session_state.results
        total_results = len(results)
        results_per_page = st.session_state.results_per_page
        total_pages = max(1, math.ceil(total_results / results_per_page))
        
        if st.session_state.current_page > total_pages:
            st.session_state.current_page = total_pages
        
        # Results header
        st.markdown("---")
        st.markdown(f"<h2 style='margin: 2.5rem 0 1.5rem 0; color: {COLORS['primary']};'>📊 Analysis Results</h2>", unsafe_allow_html=True)
        
        # Key metrics - refined styling
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.metric(
                "Total Resumes",
                total_results,
                help="Total resumes analyzed"
            )
        
        with col2:
            avg_score = sum(r.get('ats_score', 0) for r in results) / total_results
            st.metric(
                "Average Score",
                f"{avg_score:.1f}",
                help="Average ATS score"
            )
        
        with col3:
            strong = sum(1 for r in results if r.get('ats_score', 0) >= 80)
            st.metric(
                "Strong Matches",
                strong,
                help="Resumes scoring 80+"
            )
        
        with col4:
            good = sum(1 for r in results if 60 <= r.get('ats_score', 0) < 80)
            st.metric(
                "Good Matches",
                good,
                help="Resumes scoring 60-79"
            )
        
        # Pagination controls - top
        st.markdown("---")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1], gap="small")
        
        with col1:
            if st.button("⏮️ First", disabled=(st.session_state.current_page == 1), use_container_width=True):
                st.session_state.current_page = 1
                st.rerun()
        
        with col2:
            if st.button("◀️ Prev", disabled=(st.session_state.current_page == 1), use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col3:
            st.markdown(
                f'<div style="text-align: center; padding: 0.5rem; color: {COLORS["text_secondary"]}; font-weight: 600;">Page <span style="color: {COLORS["primary"]};">{st.session_state.current_page}</span> of <span style="color: {COLORS["primary"]};">{total_pages}</span></div>',
                unsafe_allow_html=True
            )
        
        with col4:
            if st.button("Next ▶️", disabled=(st.session_state.current_page == total_pages), use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
        
        with col5:
            if st.button("Last ⏭️", disabled=(st.session_state.current_page == total_pages), use_container_width=True):
                st.session_state.current_page = total_pages
                st.rerun()
        
        st.markdown("---")
        
        # Result cards - paginated
        start_idx = (st.session_state.current_page - 1) * results_per_page
        end_idx = min(start_idx + results_per_page, total_results)
        
        for rank in range(start_idx, end_idx):
            render_result_card(results[rank], rank + 1)
        
        # Pagination controls - bottom
        st.markdown("---")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1], gap="small")
        
        with col1:
            if st.button("⏮️", key="first_b", disabled=(st.session_state.current_page == 1), use_container_width=True):
                st.session_state.current_page = 1
                st.rerun()
        
        with col2:
            if st.button("◀️", key="prev_b", disabled=(st.session_state.current_page == 1), use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col3:
            page_jump = st.number_input(
                "Jump to page",
                min_value=1,
                max_value=total_pages,
                value=st.session_state.current_page,
                key="page_jump",
                label_visibility="collapsed"
            )
            if page_jump != st.session_state.current_page:
                st.session_state.current_page = page_jump
                st.rerun()
        
        with col4:
            if st.button("▶️", key="next_b", disabled=(st.session_state.current_page == total_pages), use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
        
        with col5:
            if st.button("⏭️", key="last_b", disabled=(st.session_state.current_page == total_pages), use_container_width=True):
                st.session_state.current_page = total_pages
                st.rerun()
        
        # Export section - professional styling
        st.markdown("---")
        st.markdown(f"<h3 style='margin: 2rem 0 1.5rem 0; color: {COLORS['primary']};'>💾 Export Results</h3>", unsafe_allow_html=True)
        
        # Prepare CSV export
        df_data = []
        for rank, result in enumerate(results, 1):
            df_data.append({
                "Rank": rank,
                "Name": result.get('candidate_name', 'Unknown'),
                "Score": result.get('ats_score', 0),
                "Experience": result.get('experience_years', 'N/A'),
                "Education": result.get('education', 'N/A'),
                "Matched Skills": ", ".join(result.get('matched_skills', [])),
                "Missing Skills": ", ".join(result.get('missing_skills', [])),
                "Recommendation": result.get('recommendation', 'N/A'),
                "File": result.get('filename', 'Unknown')
            })
        
        df = pd.DataFrame(df_data)
        csv = df.to_csv(index=False)
        
        col1, col2 = st.columns([2, 1], gap="medium")
        
        with col1:
            st.download_button(
                "📥 Download CSV",
                csv,
                f"ats_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.button("🗑️ Clear Results", use_container_width=True):
                st.session_state.results = []
                st.session_state.current_page = 1
                st.session_state.analysis_complete = False
                st.rerun()

# Footer - professional closing
st.markdown("---")
st.markdown(f"""
<div style="
    text-align: center;
    color: {COLORS['text_secondary']};
    padding: 3rem 0;
    font-size: 0.9rem;
">
    <p style="margin: 0; font-weight: 600;">✨ ATS Resume Screening Platform</p>
    <p style="margin: 0.75rem 0 0 0; color: {COLORS['text_tertiary']};">Powered by AI-driven intelligent resume analysis</p>
</div>
""", unsafe_allow_html=True)