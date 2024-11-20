# models.py
from sqlalchemy import Column, Integer, String, Date, UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Spending(Base):
    __tablename__ = "spendings"
    id = Column(UUID, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Integer)
    date = Column(Date)
    currency = Column(String)
    category = Column(String)
