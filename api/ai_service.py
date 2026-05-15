import os
import re
import json
from dotenv import load_dotenv
from groq import Groq
from .models import AccountRequest, PriceComparison

# Load environment variables
load_dotenv()

# Load improved prompt if exists
try:
    with open('improved_system_prompt.json', 'r') as f:
        improved_data = json.load(f)
        IMPROVED_SYSTEM_PROMPT = improved_data['prompt']
except FileNotFoundError:
    IMPROVED_SYSTEM_PROMPT = None

# 1. Direct Environment check for Render
api_key = os.environ.get("GROQ_API_KEY")

def is_business_query(query):
    """Check if query needs document retrieval"""
    business_keywords = [
        'policy', 'refund', 'account', 'fee', 'charge', 'limit',
        'transfer', 'payment', 'loan', 'credit', 'support', 'help',
        'complaint', 'issue', 'problem', 'how', 'what', 'when', 'where'
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in business_keywords)

def get_document_answer(query):
    """Get answer from policy documents using lightweight search"""
    try:
        from ai_engine.rag_pipeline import get_answer_with_score
        status, response, score = get_answer_with_score(query)
        if status == "SUCCESS" and score > 0.1:
            return response
    except Exception as e:
        print(f"Document search error: {e}")
    return None

def get_nova_response(user_query, history=None):
    if not api_key:
        return "Oga, check Render Settings. GROQ_API_KEY is missing!"

    try:
        # Check if this is a business query that needs document retrieval
        if is_business_query(user_query):
            doc_answer = get_document_answer(user_query)
            if doc_answer:
                return doc_answer

        client = Groq(api_key=api_key)
        system_prompt = IMPROVED_SYSTEM_PROMPT or """You are Nova-Pilot, a highly skilled Client Support Specialist for Nova Pay.
        You help clients create accounts, compare prices, and handle complex discussions flawlessly.
        Be conversational, helpful, and remember context from previous interactions.
        Always aim to provide personalized, retentive responses that make clients feel valued."""

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            messages.extend(history[-10:])  # Keep last 10 messages for context

        messages.append({"role": "user", "content": user_query})

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f"Deployment Log - Groq Error: {str(e)}")
        return "Wahala dey connect, try again."

def create_account(user_message):
    # Extract email and phone from message
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', user_message)
    phone_match = re.search(r'\b\d{10,11}\b', user_message)
    
    if email_match and phone_match:
        email = email_match.group()
        phone = phone_match.group()
        # Create account request
        AccountRequest.objects.create(user_id='anonymous', email=email, phone=phone)
        return f"Account creation request submitted! We'll contact you at {email} or {phone} within 24 hours to complete setup."
    else:
        return "To create an account, please provide your email address and phone number."

def compare_prices(user_message):
    # Simple price comparison - in real app, this would query a database
    comparisons = PriceComparison.objects.all()[:5]  # Get recent comparisons
    if comparisons:
        response = "Here are our current price comparisons:\n"
        for comp in comparisons:
            response += f"- {comp.product_name}: Nova Pay ${comp.nova_price} vs {comp.competitor_name} ${comp.competitor_price}\n"
        return response
    else:
        return "Price comparison data is being updated. Please check back soon!"