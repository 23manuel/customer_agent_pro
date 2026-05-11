# api/ai_service.py
import os
from dotenv import load_dotenv # Add this
from groq import Groq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Manually point to the .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH) # Force load from the root .env

# Now fetch the key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found! Check your .env file in the root folder.")

client = Groq(api_key=api_key)
# ... keep the rest of your code the same

def get_nova_response(user_query, history=None):
    if history is None:
        history = []
        
    messages = [
        {"role": "system", "content": "You are Nova-Pilot, a helpful customer support agent for Terranova Spaces."}
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": user_query})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=30.0 
        )
        
        # The Standard Way: One clear shot to the message content
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Groq Wahala: {e}")
        return "Network dey slow or API issue, abeg try again."