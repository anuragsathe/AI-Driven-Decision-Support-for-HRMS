# 📄 HRMS AI - Resume Screening & Chatbot System

> **AI-Powered ATS Resume Screening with Intelligent Chatbot** - Automate resume analysis, rank candidates, and interact with an AI chatbot for deeper insights.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Features

### 🎯 **ATS Resume Screening**
- 📤 **Bulk Upload**: Process multiple PDF resumes simultaneously
- 🤖 **AI Scoring**: Intelligent ATS scoring (0-100) using Llama 3.1 70B
- 📊 **Smart Ranking**: Automatically rank candidates by match quality
- 📄 **Pagination**: Clean, organized results with customizable page size
- 💾 **Export**: Download results as CSV for further analysis

### 💬 **AI Chatbot Assistant**
- 🤖 **Context-Aware**: Ask questions about any screened resume
- 💡 **Suggested Questions**: Pre-built queries for quick insights
- ⚡ **Fast Responses**: Powered by Groq Llama 3.3 70B (Versatile)
- 📝 **Chat History**: Track conversation flow for each candidate
- 🎯 **Smart Analysis**: Get strengths, weaknesses, and recommendations

### 🔧 **Technical Highlights**
- 🚀 **FastAPI Backend**: RESTful API with async support
- 🎨 **Streamlit Frontend**: Beautiful, responsive UI
- 🧠 **Dual AI Models**: 
  - Llama 3.1 70B for resume screening
  - Llama 3.3 70B for chatbot interactions
- 🔌 **Groq API**: Ultra-fast LLM inference
- 📦 **Modular Design**: Clean, maintainable code structure

---

## 🏗️ Project Structure

```
hrms-ai-resume-screening/
│
├── api/
│   └── main.py                    # FastAPI server (3 endpoints)
│
├── frontend/
│   └── app.py                     # Streamlit UI
│
├── modules/
│   ├── resume_screening.py        # ATS screening logic
│   └── resume_chatbot.py          # Chatbot logic
│
├── models/
│   ├── model_loader.py            # Llama 3.1 70B (screening)
│   └── chatbot_model_loader.py    # Llama 3.3 70B (chatbot)
│
├── .env                           # Environment variables (API keys)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## 🎮 Usage

### Option 1: Streamlit UI (Recommended)

```bash
streamlit run frontend/app.py
```

Then open: `http://localhost:8501`

**Steps:**
1. Paste job description in left panel
2. Upload PDF resumes (multiple files supported)
3. Click **"🚀 Analyze All Resumes"**
4. View ranked results with scores
5. Click **"💬 Chat"** on any resume to start conversation

---

### Option 2: FastAPI Backend

```bash
cd api
python main.py
```

API runs at: `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

#### 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/resume/screen` | POST | Screen multiple resumes |
| `/api/chatbot/questions` | GET | Get suggested questions |
| `/api/chatbot/ask` | POST | Ask chatbot about resume |

#### Example: Screen Resumes

```python
import requests

files = [
    ('resumes', open('resume1.pdf', 'rb')),
    ('resumes', open('resume2.pdf', 'rb'))
]

data = {
    'job_description': 'Senior Python Developer with 3+ years experience...'
}

response = requests.post(
    'http://localhost:8000/api/resume/screen',
    files=files,
    data=data
)

print(response.json())
```

#### Example: Chatbot Query

```python
import requests

payload = {
    "question": "What are this candidate's key strengths?",
    "resume_context": {
        "candidate_name": "John Doe",
        "resume_text": "...",
        "job_description": "...",
        "ats_score": 85,
        # ... other context fields
    }
}

response = requests.post(
    'http://localhost:8000/api/chatbot/ask',
    json=payload
)

print(response.json())
```

---

## 📊 Scoring System

| Score Range | Status | Color |
|-------------|--------|-------|
| 80-100 | 🟢 STRONG MATCH | Green |
| 60-79 | 🟡 GOOD MATCH | Yellow |
| 40-59 | 🟠 WEAK MATCH | Orange |
| 0-39 | 🔴 NOT SUITABLE | Red |

### Scoring Criteria:
- **Skills Match**: 40%
- **Experience Relevance**: 30%
- **Education Fit**: 15%
- **Overall Profile Strength**: 15%

---

## 🤖 AI Models

### Resume Screening
- **Model**: Llama 3.1 70B Versatile
- **Provider**: Groq
- **Temperature**: 0.3 (focused, consistent)
- **Max Tokens**: 800

### Chatbot
- **Model**: Llama 3.3 70B Versatile
- **Provider**: Groq
- **Temperature**: 0.7 (balanced)
- **Max Tokens**: 500

---

## 💡 Example Questions for Chatbot

- "Why is this candidate a good match?"
- "Tell me about their work experience"
- "What projects have they worked on?"
- "What are their technical skills?"
- "What skills are they missing?"
- "What is their educational background?"
- "What are the weak points or concerns?"
- "Should we interview this candidate?"
- "What are their key strengths?"
- "How many years of relevant experience do they have?"

---
