import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Testing connection to Groq with Llama 3.1...")
try:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # <--- UPDATED MODEL NAME
        messages=[{"role": "user", "content": "Hello, respond with one word: 'Success'"}],
        timeout=10.0
    )
    print(f"RESPONSE: {completion.choices.message.content}")
except Exception as e:
    print(f"WAI HALA! Connection failed: {e}")