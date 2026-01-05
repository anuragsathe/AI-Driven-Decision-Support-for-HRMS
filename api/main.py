"""
api/main.py
FastAPI Server for Resume Screening + Chatbot
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.resume_screening import screen_multiple_resumes
from modules.resume_chatbot import get_chatbot_response, get_suggested_questions

# Initialize FastAPI app
app = FastAPI(
    title="HRMS AI - Resume Screening + Chatbot API",
    description="ATS-based resume screening with intelligent chatbot",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """
    Health check endpoint
    
    Returns:
        dict: API status and available endpoints
    """
    return {
        "status": "active",
        "message": "HRMS AI Resume Screening + Chatbot API",
        "version": "2.0.0",
        "endpoints": {
            "health": "/",
            "screen_resumes": "/api/resume/screen",
            "suggested_questions": "/api/chatbot/questions"
        }
    }


@app.get("/health")
def health_check():
    """
    Simple health check
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "HRMS AI API"}


@app.post("/api/resume/screen")
async def screen_resumes_endpoint(
    resumes: List[UploadFile] = File(..., description="List of PDF resume files"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Screen multiple resumes against job description
    
    Args:
        resumes: List of PDF file uploads
        job_description: Job description text
    
    Returns:
        JSON with sorted screening results
    """
    
    try:
        # Validate and prepare files
        pdf_files = []
        
        for resume in resumes:
            # Check file extension
            if not resume.filename.endswith('.pdf'):
                continue
            
            # Read file content
            file_content = await resume.read()
            
            # Create file-like object
            from io import BytesIO
            pdf_file = BytesIO(file_content)
            pdf_file.name = resume.filename
            
            pdf_files.append(pdf_file)
        
        # Validate we have at least one PDF
        if not pdf_files:
            return {
                "success": False,
                "error": "No valid PDF files found. Please upload PDF resumes only.",
                "total_resumes": 0,
                "results": []
            }
        
        # Screen all resumes
        print(f"📊 Screening {len(pdf_files)} resumes...")
        results = screen_multiple_resumes(pdf_files, job_description)
        print(f"✅ Screening complete! {len(results)} resumes processed.")
        
        return {
            "success": True,
            "total_resumes": len(results),
            "results": results,
            "message": f"Successfully screened {len(results)} resumes"
        }
    
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return {
            "success": False,
            "error": f"Server error: {str(e)}",
            "total_resumes": 0,
            "results": []
        }


@app.get("/api/chatbot/questions")
def get_questions_endpoint():
    """
    Get suggested questions for chatbot
    
    Returns:
        JSON with list of suggested questions
    """
    try:
        questions = get_suggested_questions()
        
        return {
            "success": True,
            "total_questions": len(questions),
            "questions": questions
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get questions: {str(e)}",
            "questions": []
        }


@app.post("/api/chatbot/ask")
async def chatbot_ask_endpoint(
    question: str = Form(..., description="Question about the resume"),
    candidate_name: str = Form(..., description="Candidate name"),
    resume_text: str = Form(..., description="Full resume text"),
    job_description: str = Form(..., description="Job description"),
    ats_score: int = Form(..., description="ATS score"),
    matched_skills: str = Form(default="", description="Comma-separated matched skills"),
    missing_skills: str = Form(default="", description="Comma-separated missing skills"),
    experience_years: str = Form(default="N/A", description="Years of experience"),
    education: str = Form(default="N/A", description="Education"),
):
    """
    Ask chatbot a question about a candidate's resume
    
    Args:
        question: User's question
        candidate_name: Name of candidate
        resume_text: Full resume text
        job_description: Job description
        ats_score: ATS score (0-100)
        matched_skills: Comma-separated skills
        missing_skills: Comma-separated skills
        experience_years: Years of experience
        education: Education level
    
    Returns:
        JSON with chatbot response
    """
    
    try:
        # Prepare resume context
        resume_context = {
            "candidate_name": candidate_name,
            "resume_text": resume_text,
            "job_description": job_description,
            "ats_score": ats_score,
            "matched_skills": matched_skills.split(",") if matched_skills else [],
            "missing_skills": missing_skills.split(",") if missing_skills else [],
            "experience_years": experience_years,
            "education": education
        }
        
        # Get chatbot response
        response = get_chatbot_response(question, resume_context)
        
        return response
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Chatbot error: {str(e)}",
            "answer": None
        }


# Run server
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting HRMS AI API Server")
    print("="*60)
    print("📊 Resume Screening + Chatbot API")
    print("🔗 API Docs: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")