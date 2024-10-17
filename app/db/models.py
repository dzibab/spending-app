from sqlalchemy import Column, Float, String, DateTime, Integer

from .session import Base


class Spending(Base):
    __tablename__ = "spendings"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)          # Amount as Float for monetary values
    date = Column(DateTime, nullable=False)         # Changed to DateTime for full timestamp
    currency = Column(String, nullable=False)        # Currency code (e.g., USD, EUR)
    category = Column(String, nullable=False)        # Category of spending (e.g., Food, Travel)
