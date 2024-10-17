from sqlalchemy import Column, Integer, String

from .session import Base


class Spending(Base):
    __tablename__ = "spendings"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Integer)
