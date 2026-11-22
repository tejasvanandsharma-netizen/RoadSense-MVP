from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from datetime import timedelta
import models
from database import engine, SessionLocal, Base
import auth # Naya auth file import kiya

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RoadSense AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://roadsense-mvp.netlify.app", "http://localhost:5500", "http://127.0.0.1:5500"],
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

# ==========================================
# PYDANTIC MODELS (Data Validation ke liye)
# ==========================================
class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    
    class Config:
        from_attributes = True # Pydantic v2 ke liye

class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================================
# PURANE ROUTES (Test & Questions)
# ==========================================
@app.get("/api/get-random-test")
def get_random_test(db: Session = Depends(get_db)):
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


# ==========================================
# NAYE ROUTES (Authentication)
# ==========================================
@app.post("/api/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check karo email pehle se exist karti hai ya nahi
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Naya user banao aur password hash karo
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        full_name=user.full_name,
        role="learner" # By default sab learner honge
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # User ko email se dhoondo
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # Password verify karo
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Login successful! Ab JWT Token banao
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}