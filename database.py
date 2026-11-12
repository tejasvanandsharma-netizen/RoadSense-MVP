from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file banayenge
SQLALCHEMY_DATABASE_URL = "sqlite:///./roadsense.db"

# Engine setup (connect_args={"check_same_thread": False} SQLite ke liye zaroori hai FastAPI mein)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()