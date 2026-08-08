"""
core/llm/screening_llm.py
Hugging Face LLM for Resume Screening
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from the root .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Global model instance
_llm_instance = None


def get_llm():
    """
    Returns the LLM instance (Singleton pattern)
    """
    global _llm_instance
    
    if _llm_instance is None:
        print("🔄 Loading Llama 3.1 model for resume screening (via Groq)...")
        
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env file!")
        
        _llm_instance = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            temperature=0.7,
            max_tokens=500
        )
        
        print("✅ Resume screening model loaded!")
    
    return _llm_instance


def invoke_llm(prompt, temperature=0.7, max_tokens=500):
    """
    Call LLM with prompt
    """
    llm = get_llm()
    llm.temperature = temperature
    llm.max_tokens = max_tokens
    
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print("Testing model...")
    test_prompt = "Say 'Model ready!' in one sentence."
    response = invoke_llm(test_prompt)
    print(f"Response: {response}")