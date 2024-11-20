from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from src.db.models import Currency, Category
from src.enums import CurrencyEnum, CategoryEnum


DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def initialize_default_data(db: AsyncSession):
    # Initialize default currencies
    for currency in CurrencyEnum:
        result = await db.execute(select(Currency).where(Currency.name == currency.value))
        if result.scalar_one_or_none() is None:  # Only add if not exists
            new_currency = Currency(name=currency.value)
            db.add(new_currency)

    # Initialize default categories
    for category in CategoryEnum:
        result = await db.execute(select(Category).where(Category.name == category.value))
        if result.scalar_one_or_none() is None:  # Only add if not exists
            new_category = Category(name=category.value)
            db.add(new_category)

    await db.commit()
