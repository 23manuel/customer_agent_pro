from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine.rag_pipeline import get_answer_with_score

app = FastAPI(title="NovaPay Agent API")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "NovaPay AI Engine is Online and ready for traffic!"}

@app.post("/ask")
def ask_ai(request: QueryRequest):
    status, response, score = get_answer_with_score(request.question)
    
    return {
        "status": status,
        "answer": response,
        "confidence_score": round(float(score), 4)
    }