"""
services/resume_scanner.py
Resume Screening Logic
"""

import PyPDF2
import json
import re
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm.screening_llm import invoke_llm


def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    try:
        if isinstance(pdf_file, str):
            file_obj = open(pdf_file, 'rb')
        else:
            file_obj = pdf_file
        
        pdf_reader = PyPDF2.PdfReader(file_obj)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        if isinstance(pdf_file, str):
            file_obj.close()
        
        return text.strip()
    
    except Exception as e:
        print(f"❌ PDF Error: {str(e)}")
        return ""


def analyze_single_resume(resume_text, job_description):
    """Analyze resume with LLM"""
    
    prompt = f"""You are an ATS expert. Analyze this resume against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide ONLY valid JSON (no extra text):
{{
    "candidate_name": "Full name or 'Not Found'",
    "ats_score": 85,
    "matched_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "experience_years": 5,
    "education": "Degree or 'Not Mentioned'",
    "key_strengths": ["strength1", "strength2"],
    "recommendation": "Strong Match",
    "summary": "Brief summary"
}}

Score 0-100 based on: Skills(40%), Experience(30%), Education(15%), Profile(15%)
"""
    
    try:
        response = invoke_llm(prompt, temperature=0.3, max_tokens=800)
        
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            return {"error": "Failed to parse response"}
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


def screen_resume(pdf_file, job_description):
    """Screen single resume"""
    
    resume_text = extract_text_from_pdf(pdf_file)
    
    if not resume_text:
        return {"success": False, "error": "Failed to extract text"}
    
    analysis = analyze_single_resume(resume_text, job_description)
    
    if "error" in analysis:
        return {"success": False, "error": analysis["error"]}
    
    analysis["success"] = True
    analysis["resume_text"] = resume_text
    
    return analysis


def screen_multiple_resumes(resume_files, job_description):
    """Screen multiple resumes"""
    
    results = []
    
    for idx, resume_file in enumerate(resume_files, 1):
        print(f"🔍 Analyzing {idx}/{len(resume_files)}...")
        
        result = screen_resume(resume_file, job_description)
        
        if result.get("success"):
            result["file_index"] = idx
            if hasattr(resume_file, 'name'):
                result["filename"] = resume_file.name
            else:
                result["filename"] = f"Resume_{idx}.pdf"
            
            results.append(result)
            print(f"   ✅ Score: {result.get('ats_score', 0)}/100")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown')}")
    
    results.sort(key=lambda x: x.get('ats_score', 0), reverse=True)
    
    return results