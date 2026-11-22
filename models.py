from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

# 1. USERS TABLE (Naya)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="learner") # 'learner' or 'admin'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to track user's tests
    test_results = relationship("TestResult", back_populates="user")

# 2. QUESTIONS TABLE (Purana wala)
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, index=True)
    timestamp = Column(String)
    hazard_description = Column(String)
    mcq = Column(String)
    options = Column(JSON)
    correct_answer = Column(String)
    explanation = Column(String)

# 3. TEST RESULTS TABLE (Naya)
class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)
    total_questions = Column(Integer)
    date_taken = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="test_results")