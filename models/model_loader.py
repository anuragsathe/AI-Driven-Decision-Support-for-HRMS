"""
models/model_loader.py
Hugging Face LLM for Resume Screening
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from models/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Global model instance
_llm_instance = None


def get_llm():
    """
    Returns the LLM instance (Singleton pattern)
    """
    global _llm_instance
    
    if _llm_instance is None:
        print("🔄 Loading Llama 3.1 model for resume screening...")
        
        api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        
        if not api_key:
            raise ValueError("❌ HUGGINGFACEHUB_API_TOKEN not found in .env file!")
        
        _llm_instance = ChatOpenAI(
            model="meta-llama/Llama-3.1-8B-Instruct",
            base_url="https://router.huggingface.co/v1",
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