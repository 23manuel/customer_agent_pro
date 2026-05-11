import os
import time
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

load_dotenv()

# --- 1. INITIALIZATION ---
print("--- [1/3] Loading Embeddings & Index ---")
start_init = time.time()

# Force CPU for stability on local Windows
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs=model_kwargs)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Correct path to find faiss_index in the parent folder
INDEX_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "faiss_index"))

vector_store = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print(f"Engine Ready in {time.time() - start_init:.2f}s")

def get_answer_with_score(query):
    # --- 2. SEARCH ---
    print("--- [2/3] Searching Policy Database ---")
    start_search = time.time()
    results = vector_store.similarity_search_with_score(query, k=3)
    
    # Extract score correctly (handle tuples)
    best_match = results
    raw_score = best_match
    while isinstance(raw_score, (tuple, list)):
        raw_score = raw_score
    score = float(raw_score)
    
    print(f"Search Finished in {time.time() - start_search:.2f}s (Score: {score:.4f})")
    
    # Safety Check
    if score > 1.2:
        return "ESCALATE", "Abeg, this one pass my power. Let me get a human to help.", score
    
    context_text = "\n\n".join([res.page_content for res in results])
    
    # --- 3. GENERATION ---
    print("--- [3/3] Generating Nova-Pilot Response ---")
    start_api = time.time()
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant", # Using the live model
            messages=[
                {"role": "system", "content": "You are Nova-Pilot, a Senior Support Agent for NovaPay. Use the context to answer professionally. If query is in Pidgin, respond in professional Lagos Pidgin."},
                {"role": "user", "content": f"CONTEXT FROM POLICY:\n{context_text}\n\nUSER QUERY: {query}"}
            ],
            temperature=0.2,
        )
        # FIXED: Correct way to access message content
        final_answer = completion.choices.message.content
        print(f"Response Ready in {time.time() - start_api:.2f}s")
        return "SUCCESS", final_answer, score
        
    except Exception as e:
        return "ERROR", f"Wahala with Groq: {str(e)}", score

if __name__ == "__main__":
    user_query = "I wan refund but I no get receipt, wetin I go do?" 
    print(f"\nSTARTING REQUEST: {user_query}")
    
    status, result, score = get_answer_with_score(user_query)
    
    print(f"\n--- FINAL STATUS: {status} ---")
    print(f"NOVA-PILOT:\n{result}\n")