import os
from groq import Groq

# 1. Try to load dotenv only if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 2. Get the key from the Environment (Render or Local)
api_key = os.environ.get("GROQ_API_KEY")

# 3. Don't let the app crash at the top level! 
# We initialize the client inside the function instead.

def get_nova_response(user_query, history=None):
    if not api_key:
        return "Oga, the GROQ_API_KEY is missing on the server! Add it to Render Settings > Environment."

    if history is None:
        history = []
        
    client = Groq(api_key=api_key)
    
    messages = [
        {"role": "system", "content": "You are Nova-Pilot, a helpful customer support agent for NovaPay Ltd."}
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
        return completion.choices.message.content

    except Exception as e:
        print(f"Groq Wahala: {e}")
        return f"Network dey slow or API issue: {str(e)}"