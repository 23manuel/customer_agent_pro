import os
from groq import Groq

# 1. Direct Environment check for Render
api_key = os.environ.get("GROQ_API_KEY")

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

        # THE FIX: Added because choices is a list
        return completion.choices.message.content

    except Exception as e:
        print(f"Deployment Log - Groq Error: {str(e)}")
        return "Wahala dey connect, try again."