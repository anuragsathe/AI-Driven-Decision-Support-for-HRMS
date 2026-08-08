"""
core/llm/chatbot_llm.py
Groq Llama 3.3 70B for Chatbot
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Disable warnings
warnings.filterwarnings("ignore")

# Global model instance
_chatbot_model = None


def get_chatbot_model():
    """
    Returns Groq Llama 3.3 70B model
    """
    global _chatbot_model
    
    if _chatbot_model is None:
        print("🔄 Loading Groq Llama 3.3 70B for chatbot...")
        
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not groq_api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env file!")
        
        _chatbot_model = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500
        )
        
        print("✅ Groq chatbot model loaded!")
    
    return _chatbot_model


def invoke_chatbot(prompt, temperature=0.7, max_tokens=500):
    """
    Call Groq chatbot with prompt
    """
    try:
        model = get_chatbot_model()
        model.temperature = temperature
        model.max_tokens = max_tokens
        
        prompt_template = ChatPromptTemplate.from_template("{input}")
        chain = prompt_template | model | StrOutputParser()
        
        response = chain.invoke({"input": prompt})
        return response.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print("Testing chatbot model...")
    test_prompt = "Say 'Chatbot ready!' in one sentence."
    response = invoke_chatbot(test_prompt)
    print(f"Response: {response}")