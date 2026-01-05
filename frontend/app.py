"""
frontend/app.py
Streamlit UI
"""

import streamlit as st
import sys
import os
import pandas as pd
import math

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.resume_screening import screen_multiple_resumes
from modules.resume_chatbot import get_chatbot_response, get_suggested_questions, format_resume_context

# Page config
st.set_page_config(
    page_title="HRMS AI",
    page_icon="📄",
    layout="wide"
)

# Session state
if 'results' not in st.session_state:
    st.session_state.results = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'results_per_page' not in st.session_state:
    st.session_state.results_per_page = 10
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .score-high {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin-bottom: 15px;
    }
    .score-medium {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 15px;
    }
    .score-low {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📄 ATS Resume Screening + AI Chatbot</p>', unsafe_allow_html=True)
st.markdown("### 🎯 Screen Resumes & Chat with Candidates")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.session_state.results_per_page = st.selectbox(
        "Results per page:",
        [5, 10, 15, 20, 25],
        index=1
    )
    
    st.markdown("---")
    
    if st.session_state.chat_active and st.session_state.chat_context:
        st.success(f"💬 Chatting with: {st.session_state.chat_context.get('candidate_name', 'Unknown')}")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("❌ Close Chat", use_container_width=True):
            st.session_state.chat_active = False
            st.session_state.chat_context = None
            st.session_state.chat_history = []
            st.rerun()
        
        st.divider()
        st.caption(f"💬 Messages: {len(st.session_state.chat_history)}")
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    st.info("""
    **Resume Screening:**
    - Multiple PDF upload
    - AI scoring (0-100)
    - Ranked results
    
    **AI Chatbot:**
    - Ask about resume
    - Fast responses
    - Context-aware
    """)

# Chat view
if st.session_state.chat_active and st.session_state.chat_context:
    
    st.title("🤖 Resume AI Chatbot")
    st.caption(f"**{st.session_state.chat_context.get('candidate_name', 'Unknown')}** | Score: {st.session_state.chat_context.get('ats_score', 0)}/100")
    
    st.markdown("---")
    
    # Display messages
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['message'])
    
    # Suggested questions
    if len(st.session_state.chat_history) == 0:
        st.markdown("---")
        st.subheader("💡 Suggested Questions")
        
        suggestions = get_suggested_questions()[:6]
        
        cols = st.columns(2)
        for idx, suggestion in enumerate(suggestions):
            with cols[idx % 2]:
                if st.button(f"💬 {suggestion}", key=f"suggest_{idx}", use_container_width=True):
                    st.session_state.chat_history.append({
                        "role": "user",
                        "message": suggestion
                    })
                    
                    with st.spinner("🤖 Thinking..."):
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
                            "message": f"❌ Error: {response.get('error', 'Unknown')}"
                        })
                    
                    st.rerun()
    
    # User input
    user_question = st.chat_input("Type your question...")
    
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
                    error_msg = f"❌ Error: {response.get('error', 'Unknown')}"
                    st.markdown(error_msg)
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'message': error_msg
                    })
        
        st.rerun()

else:
    # Normal view
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Job Description")
        job_description = st.text_area(
            "Paste job description:",
            height=350,
            value=st.session_state.job_description,
            placeholder="Job Title: Senior Developer\n\nRequirements:\n- 3+ years Python\n- Django/Flask\n- SQL databases..."
        )
        st.session_state.job_description = job_description
    
    with col2:
        st.subheader("📤 Upload Resumes")
        
        uploaded_files = st.file_uploader(
            "Select PDFs:",
            type=['pdf'],
            accept_multiple_files=True,
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} resume(s)")
            
            with st.expander("📁 Files"):
                for idx, file in enumerate(uploaded_files, 1):
                    st.write(f"{idx}. {file.name}")
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        analyze_button = st.button(
            "🚀 Analyze Resumes",
            use_container_width=True,
            type="primary"
        )
    
    if analyze_button:
        if not job_description.strip():
            st.error("⚠️ Enter job description!")
            st.stop()
        
        if not uploaded_files:
            st.error("⚠️ Upload resumes!")
            st.stop()
        
        st.session_state.current_page = 1
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text(f"🔄 Analyzing {len(uploaded_files)} resumes...")
        
        with st.spinner("Processing..."):
            results = screen_multiple_resumes(uploaded_files, job_description)
            progress_bar.progress(100)
            status_text.text(f"✅ Complete! {len(results)} analyzed.")
        
        if not results:
            st.error("❌ No resumes processed")
            st.stop()
        
        st.session_state.results = results
        st.rerun()
    
    # Results
    if st.session_state.results:
        results = st.session_state.results
        total_results = len(results)
        results_per_page = st.session_state.results_per_page
        total_pages = math.ceil(total_results / results_per_page)
        
        if st.session_state.current_page > total_pages:
            st.session_state.current_page = total_pages
        
        st.markdown("---")
        st.header("📊 Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total", total_results)
        with col2:
            avg_score = sum(r.get('ats_score', 0) for r in results) / total_results
            st.metric("Avg Score", f"{avg_score:.1f}/100")
        with col3:
            strong = sum(1 for r in results if r.get('ats_score', 0) >= 80)
            st.metric("Strong (≥80)", strong)
        with col4:
            good = sum(1 for r in results if 60 <= r.get('ats_score', 0) < 80)
            st.metric("Good (60-79)", good)
        
        st.markdown("---")
        
        # Pagination
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️ First", disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page = 1
                st.rerun()
        with col2:
            if st.button("◀️ Prev", disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page -= 1
                st.rerun()
        with col3:
            st.markdown(
                f'<p style="text-align:center;font-size:1.1rem;">Page {st.session_state.current_page} of {total_pages}</p>',
                unsafe_allow_html=True
            )
        with col4:
            if st.button("Next ▶️", disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page += 1
                st.rerun()
        with col5:
            if st.button("Last ⏭️", disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page = total_pages
                st.rerun()
        
        st.markdown("---")
        
        start_idx = (st.session_state.current_page - 1) * results_per_page
        end_idx = min(start_idx + results_per_page, total_results)
        
        for rank in range(start_idx, end_idx):
            result = results[rank]
            global_rank = rank + 1
            score = result.get('ats_score', 0)
            
            if score >= 80:
                status = "🟢 STRONG"
                css_class = "score-high"
            elif score >= 60:
                status = "🟡 GOOD"
                css_class = "score-medium"
            elif score >= 40:
                status = "🟠 WEAK"
                css_class = "score-low"
            else:
                status = "🔴 NOT SUITABLE"
                css_class = "score-low"
            
            with st.container():
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.subheader(f"#{global_rank} - {result.get('candidate_name', 'Unknown')}")
                with col2:
                    st.metric("Score", f"{score}/100")
                with col3:
                    st.markdown(f"**{status}**")
                with col4:
                    if st.button("💬 Chat", key=f"chat_{global_rank}"):
                        resume_context = format_resume_context(
                            result,
                            result.get('resume_text', ''),
                            st.session_state.job_description
                        )
                        st.session_state.chat_active = True
                        st.session_state.chat_context = resume_context
                        st.session_state.chat_history = []
                        st.rerun()
                
                st.markdown(f"**📄 File:** {result.get('filename', 'Unknown')}")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.write(f"**Exp:** {result.get('experience_years', 'N/A')} yrs")
                with col_b:
                    st.write(f"**Edu:** {result.get('education', 'N/A')}")
                with col_c:
                    st.write(f"**Rec:** {result.get('recommendation', 'N/A')}")
                
                with st.expander("📋 Details"):
                    st.markdown("**✅ Matched Skills**")
                    matched = result.get('matched_skills', [])
                    if matched:
                        st.success(", ".join(matched))
                    else:
                        st.info("None")
                    
                    st.markdown("**❌ Missing Skills**")
                    missing = result.get('missing_skills', [])
                    if missing:
                        st.warning(", ".join(missing))
                    else:
                        st.success("All present!")
                    
                    st.markdown("**💪 Strengths**")
                    strengths = result.get('key_strengths', [])
                    if strengths:
                        for s in strengths:
                            st.write(f"• {s}")
                    
                    st.markdown("**📝 Summary**")
                    st.info(result.get('summary', 'N/A'))
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Bottom pagination
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️", key="first_b", disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page = 1
                st.rerun()
        with col2:
            if st.button("◀️", key="prev_b", disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page -= 1
                st.rerun()
        with col3:
            page_input = st.number_input("Jump:", min_value=1, max_value=total_pages, 
                                         value=st.session_state.current_page, key="jump")
            if page_input != st.session_state.current_page:
                st.session_state.current_page = page_input
                st.rerun()
        with col4:
            if st.button("▶️", key="next_b", disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page += 1
                st.rerun()
        with col5:
            if st.button("⏭️", key="last_b", disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page = total_pages
                st.rerun()
        
        st.markdown("---")
        
        # Export
        st.subheader("💾 Export")
        
        df_data = []
        for rank, result in enumerate(results, 1):
            df_data.append({
                "Rank": rank,
                "Name": result.get('candidate_name', 'Unknown'),
                "Score": result.get('ats_score', 0),
                "Experience": f"{result.get('experience_years', 'N/A')} yrs",
                "Education": result.get('education', 'N/A'),
                "Matched": ", ".join(result.get('matched_skills', [])),
                "Missing": ", ".join(result.get('missing_skills', [])),
                "Recommendation": result.get('recommendation', 'N/A'),
                "File": result.get('filename', 'Unknown')
            })
        
        df = pd.DataFrame(df_data)
        csv = df.to_csv(index=False)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.download_button("📥 Download CSV", csv, "results.csv", "text/csv", use_container_width=True)
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.results = []
                st.session_state.current_page = 1
                st.rerun()

st.markdown("---")
st.markdown('<div style="text-align:center;color:gray;"><p>Powered by Llama AI</p></div>', unsafe_allow_html=True)