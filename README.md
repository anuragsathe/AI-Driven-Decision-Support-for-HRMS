# 📄 HRMS AI - Resume Screening & Chatbot System

> **AI-Powered ATS Resume Screening with Intelligent Chatbot** - Automate resume analysis, rank candidates, and interact with an AI chatbot for deeper insights.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

The HRMS AI system seamlessly merges Applicant Tracking System (ATS) methodology with the power of Large Language Models (LLMs) to streamline the recruitment process. It allows recruiters to upload bulk resumes in PDF format, evaluates them against a specified job description, provides a matching rank score ranging from 0 to 100, and enables instant conversational access via an AI-powered Chatbot to query detailed aspects of each candidate's resume.

---

## ✨ Key Features

### 🎯 **ATS Resume Screening**
- 📤 **Bulk Upload**: Process multiple PDF resumes simultaneously to save time.
- 🤖 **AI Scoring**: Intelligent ATS scoring (0-100) combining assessments of Skills (40%), Experience (30%), Education (15%), and Overall Profile (15%).
- 📊 **Smart Ranking**: Automatically ranks candidates from strongest to weakest match.
- 📄 **Pagination & Clean UI**: Easily navigate through large applicant datasets with customizable page sizes.
- 💾 **Export Capabilities**: Download the analyzed screening results as a CSV for offline review and records.

### 💬 **AI Chatbot Assistant**
- 🤖 **Context-aware Queries**: Ask detailed questions about any screened applicant directly relying on their resume's context.
- 💡 **Suggested Questions**: Integrated quick-action questions for immediate insights.
- ⚡ **Fast Responses**: Uses high-speed conversational LLMs for real-time natural language answers.
- 📝 **Chat History**: Maintains conversation flow uniquely for each candidate interactively.
- 🎯 **Smart Analysis**: Ascertain deeper qualitative data such as strengths, weaknesses, and potential red flags.

---

## 🏗️ Technical Architecture

The application is structured into a modular robust layer comprising a FastAPI backend and a Streamlit frontend UI.

```text
AI-Driven-Decision-Support-for-HRMS/
├── api/
│   └── main.py                    # FastAPI server & route handlers
├── frontend/
│   └── app.py                     # Streamlit User Interface
├── services/
│   ├── resume_scanner.py          # Core ATS screening logic and orchestration
│   └── chat_assistant.py          # Chatbot logic and prompt formulations
├── core/
│   └── llm/
│       ├── screening_llm.py       # Hugging Face LLM initialization (Screening)
│       └── chatbot_llm.py         # Groq LLM initialization (Chatbot)
├── .env                           # Environment variables config (create this)
├── requirements.txt               # Dependencies required for both APIs and Frontend
└── README.md                      # Project documentation
```

### 🧠 Pre-integrated AI Models
- **Resume Screening**: `meta-llama/Llama-3.1-8B-Instruct` (via Hugging Face Provider)
- **Interactive Chatbot**: `llama-3.3-70b-versatile` (via Groq Provider)

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
- Python 3.8 or higher.
- Obtain API keys required for interactions:
  - **Hugging Face Token** for LLM Inference execution.
  - **Groq API Key** for the fast-action Chatbot workflow.

### 2️⃣ Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <your-repo-url>
   cd AI-Driven-Decision-Support-for-HRMS
   ```
2. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Depending on your environment, you may also need to install `langchain-groq` separately if missing: `pip install langchain-groq`)*

### 3️⃣ Environment Variable Setup
Create a `.env` file at the root of the project directory (you can copy `.env.example`), and define the credentials:
```env
HUGGINGFACEHUB_API_TOKEN="your_huggingface_token_here"
GROQ_API_KEY="your_groq_api_key_here"
```

---

## 🎮 Usage 

You have flexible choices to run the application depending on whether you are working with the Web Interface or integrating the endpoints over HTTP.

### Option 1: Run the Streamlit UI (Recommended)
Launch the graphical browser-based interface:
```bash
streamlit run frontend/app.py
```
* **Step 1:** The interface will open at `http://localhost:8501`.
* **Step 2:** Provide the target Job Description in the left pane text area.
* **Step 3:** Upload one or more `.pdf` candidate resumes.
* **Step 4:** Click **"🚀 Analyze Resumes"** and view ranked candidate metrics.
* **Step 5:** Press **"💬 Chat"** on any analyzed candidate to begin a context-aware chat!

### Option 2: Run the FastAPI Backend 
Ideal if you want to integrate the core analysis logic via a RESTful API into an alternate frontend framework.
```bash
python api/main.py
```
* The backend server launches at `http://localhost:8000`.
* Interactive Swagger API Documentation will be accessible natively at: `http://localhost:8000/docs`.

### 📡 Available API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | `GET` | Retrieve API Health Status & Info |
| `/api/resume/screen` | `POST` | Process & Score multiple Resumes PDFs concurrently |
| `/api/chatbot/questions` | `GET` | Fetch preset recommended questions for HR queries |
| `/api/chatbot/ask` | `POST` | Trigger AI Chatbot with candidate-specific queries |

---

## 📊 Evaluation Criteria

The system automatically categorizes applicants into four structured bands based on holistic resume extraction scores:
- 🟢 **STRONG MATCH** (80-100)
- 🟡 **GOOD MATCH** (60-79)
- 🟠 **WEAK MATCH** (40-59)
- 🔴 **NOT SUITABLE** (0-39)

**Matching Algorithm Weighted Distribution:** 
*Skills Coverage (40%) • Experience Relevance (30%) • Educational Matching (15%) • Application Quality (15%)*

---

<div align="center">
  <i>Developed to revolutionize Technical Recruitment with intelligent ATS methodologies.</i>
</div>
