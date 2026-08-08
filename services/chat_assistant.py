"""
services/chat_assistant.py
Chatbot Logic with Groq
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm.chatbot_llm import invoke_chatbot


def get_suggested_questions():
    """Return suggested questions"""
    return [
        "Why is this candidate a good match?",
        "Tell me about their work experience",
        "What projects have they worked on?",
        "What are their technical skills?",
        "What skills are they missing?",
        "What is their educational background?",
        "What are the weak points?",
        "Should we interview this candidate?",
        "What are their key strengths?",
        "How many years of experience?"
    ]


def build_chat_prompt(question, resume_context, chat_history=None):
    """Build prompt with context"""
    
    candidate_name = resume_context.get('candidate_name', 'Unknown')
    resume_text = resume_context.get('resume_text', '')
    job_description = resume_context.get('job_description', '')
    ats_score = resume_context.get('ats_score', 0)
    matched_skills = resume_context.get('matched_skills', [])
    missing_skills = resume_context.get('missing_skills', [])
    experience_years = resume_context.get('experience_years', 'N/A')
    education = resume_context.get('education', 'N/A')
    
    history_text = ""
    if chat_history and len(chat_history) > 0:
        history_text = "\n\nPREVIOUS CONVERSATION:\n"
        recent = chat_history[-4:] if len(chat_history) > 4 else chat_history
        
        for msg in recent:
            role = "HR" if msg.get('role') == 'user' else "Assistant"
            history_text += f"{role}: {msg.get('message', '')}\n"
    
    prompt = f"""You are an HR assistant. Answer professionally and concisely.

CANDIDATE: {candidate_name}

RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:1000]}

ATS ANALYSIS:
- Score: {ats_score}/100
- Matched: {', '.join(matched_skills[:10]) if matched_skills else 'None'}
- Missing: {', '.join(missing_skills[:5]) if missing_skills else 'None'}
- Experience: {experience_years} years
- Education: {education}
{history_text}

QUESTION: {question}

INSTRUCTIONS:
- Answer in 3-5 sentences
- Base on resume only
- Be honest
- If info missing, say so
- Use examples

ANSWER:"""
    
    return prompt


def get_chatbot_response(question, resume_context, chat_history=None):
    """Get chatbot response"""
    
    try:
        prompt = build_chat_prompt(question, resume_context, chat_history)
        
        response = invoke_chatbot(prompt, temperature=0.5, max_tokens=500)
        
        return {
            "success": True,
            "answer": response,
            "question": question
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed: {str(e)}",
            "question": question
        }


def format_resume_context(result_data, resume_text, job_description):
    """Format context for chatbot"""
    
    return {
        "candidate_name": result_data.get('candidate_name', 'Unknown'),
        "resume_text": resume_text,
        "job_description": job_description,
        "ats_score": result_data.get('ats_score', 0),
        "matched_skills": result_data.get('matched_skills', []),
        "missing_skills": result_data.get('missing_skills', []),
        "experience_years": result_data.get('experience_years', 'N/A'),
        "education": result_data.get('education', 'N/A'),
        "key_strengths": result_data.get('key_strengths', []),
        "recommendation": result_data.get('recommendation', 'N/A'),
        "summary": result_data.get('summary', 'N/A'),
        "filename": result_data.get('filename', 'Unknown')
    }


if __name__ == "__main__":
    print("Suggested Questions:")
    for i, q in enumerate(get_suggested_questions(), 1):
        print(f"{i}. {q}")