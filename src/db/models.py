import uuid

from sqlalchemy import Column, Integer, String, Date, UUID, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Spending(Base):
    __tablename__ = "spendings"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    description = Column(String, index=True)
    amount = Column(Integer)
    date = Column(Date)
    currency_id = Column(UUID, ForeignKey("currencies.id"))
    category_id = Column(UUID, ForeignKey("categories.id"))

    currency = relationship("Currency")
    category = relationship("Category")


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
