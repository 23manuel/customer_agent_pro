import os
from groq import Groq

# 1. Look for the key directly in the system (Render Environment)
api_key = os.environ.get("GROQ_API_KEY")

# 2. Only use dotenv as a fallback for your local PC
if not api_key:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
    except ImportError:
        pass

# 3. Don't "raise" a hard error here, just handle it in the function
client = None
if api_key:
    client = Groq(api_key=api_key)

def get_nova_response(user_query, history=None):
    if not client:
        return "System error: Groq API Key is missing on the server. Check Render Environment settings."
            
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