from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./spendings.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class Spending(Base):
    __tablename__ = "spendings"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Integer)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Spending Tracker!"}

@app.post("/add/")
def add_spending(description: str, amount: int):
    db = SessionLocal()
    new_spending = Spending(description=description, amount=amount)
    db.add(new_spending)
    db.commit()
    db.refresh(new_spending)
    return new_spending
