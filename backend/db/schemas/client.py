from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = "postgresql://fakestoredb_user:wGvMbnSFH7WwSNyYuEit4Xu8mWhYtFPa@dpg-d8pm37rtqb8s738ajtq0-a/fakestoredb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
