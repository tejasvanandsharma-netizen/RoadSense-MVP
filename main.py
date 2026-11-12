from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware # Yeh naya line hai
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel
import models
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RoadSense AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str

@app.get("/api/get-random-test")
def get_random_test(db: Session = Depends(get_db)):
    # 10 random questions uthayenge
    questions = db.query(models.Question).order_by(func.random()).limit(10).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found in database")
    
    response = []
    for q in questions:
        response.append({
            "id": q.id,
            "video_id": q.video_id,
            "timestamp": q.timestamp,
            "mcq": q.mcq,
            "options": q.options
        })
    return {"test_data": response}

@app.post("/api/submit-answer")
def submit_answer(data: AnswerSubmit, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == data.question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    
    is_correct = (q.correct_answer.strip() == data.selected_option.strip())
    
    return {
        "is_correct": is_correct,
        "correct_answer": q.correct_answer,
        "explanation": q.explanation
    }