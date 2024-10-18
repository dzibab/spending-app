from sqlalchemy import Column, Integer, Float, String, DateTime

from app.db.session import Base


class Spending(Base):
    __tablename__ = "spendings"

    id = Column(Integer, primary_key=True, index=True)  # Ensure there's an id column
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    currency = Column(String, nullable=False)
    category = Column(String, nullable=False)
