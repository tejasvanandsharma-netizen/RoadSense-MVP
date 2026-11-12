from sqlalchemy import Column, Integer, String, JSON
from database import Base

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