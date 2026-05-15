import os
import time
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Lightweight policy search - no heavy ML models for free tier
_policy_content = None
_groq_client = None

def _load_policy_content():
    """Load policy document content for lightweight search"""
    global _policy_content

    if _policy_content is None:
        policy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "policy.txt")
        try:
            with open(policy_path, 'r', encoding='utf-8') as f:
                _policy_content = f.read()
        except FileNotFoundError:
            _policy_content = "Policy document not found."

    return _policy_content

def _get_groq_client():
    """Lazy load Groq client"""
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _groq_client

def _extract_relevant_sections(query, content, max_sections=3):
    """Extract relevant sections using keyword matching"""
    # Split content into sections (by headers or paragraphs)
    sections = re.split(r'\n\s*\n', content)

    # Score sections based on keyword matches
    query_words = set(query.lower().split())
    scored_sections = []

    for section in sections:
        section_lower = section.lower()
        score = sum(1 for word in query_words if word in section_lower)
        if score > 0:
            scored_sections.append((score, section))

    # Return top matching sections
    scored_sections.sort(reverse=True, key=lambda x: x[0])
    return [section for score, section in scored_sections[:max_sections]]

def get_answer_with_score(query):
    """Lightweight policy search for free tier - no heavy ML models"""
    start_time = time.time()

    # Load policy content
    content = _load_policy_content()

    # Extract relevant sections using simple keyword matching
    relevant_sections = _extract_relevant_sections(query, content)

    if not relevant_sections:
        return "NO_MATCH", "I no find any relevant information for your question. Let me connect you with a human agent.", 0.0

    # Combine relevant sections
    context_text = "\n\n".join(relevant_sections)

    # Calculate a simple relevance score (0.0 to 1.0)
    query_words = set(query.lower().split())
    total_words = len(query_words)
    matched_words = sum(1 for word in query_words if word in context_text.lower())
    score = min(matched_words / total_words, 1.0) if total_words > 0 else 0.0

    print(".2f")

    # Safety check - if score too low, escalate
    if score < 0.1:
        return "ESCALATE", "This question need expert attention. Let me get a human to help you.", score

    # Generate response using Groq
    groq_client = _get_groq_client()

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Nova-Pilot, a Senior Support Agent for NovaPay. Use the provided context to answer customer questions professionally. Keep responses clear and helpful. If query is in Pidgin, respond in professional Lagos Pidgin."},
                {"role": "user", "content": f"CONTEXT FROM POLICY:\n{context_text}\n\nCUSTOMER QUESTION: {query}\n\nAnswer based on the policy context above:"}
            ],
            temperature=0.2,
        )

        final_answer = completion.choices[0].message.content
        total_time = time.time() - start_time
        print(".2f")

        return "SUCCESS", final_answer, score

    except Exception as e:
        return "ERROR", f"Wahala with system: {str(e)}", score

if __name__ == "__main__":
    user_query = "I wan refund but I no get receipt, wetin I go do?"
    print(f"\nSTARTING REQUEST: {user_query}")

    status, result, score = get_answer_with_score(user_query)

    print(f"\n--- FINAL STATUS: {status} ---")
    print(f"NOVA-PILOT:\n{result}\n")