import os
from groq import Groq

# 1. Direct Environment check for Render
api_key = os.environ.get("GROQ_API_KEY")

# 2. Local fallback
if not api_key:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
    except ImportError:
        pass

def get_nova_response(user_query, history=None):
    if not api_key:
        return "Oga, check Render Settings. GROQ_API_KEY is missing!"

    try:
        client = Groq(api_key=api_key)
        messages = [{"role": "system", "content": "You are Nova-Pilot, a support agent for Nova Pay."}]
        
        if history:
            messages.extend(history)
            
        messages.append({"role": "user", "content": user_query})

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )

        # THE FIX: Accessing the content correctly
        # completion.choices is a list, so we access index
        return completion.choices[0].message.content

    except Exception as e:
        # This will print the exact error to your Render Logs
        print(f"Deployment Log - Groq Error: {str(e)}")
        return "Network dey slow or AI vexed, abeg try again."