import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://roadsense_db_6ii5_user:bTDWYBMa7yaBHMaTETd371jFiDbBUnce@dpg-dbu93f3rjlhs739vs20g-a.singapore-postgres.render.com/roadsense_db_6ii5?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()