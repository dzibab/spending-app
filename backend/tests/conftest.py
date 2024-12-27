import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.db.models import Base
from backend.db.session import get_db
from backend.main import app


@pytest_asyncio.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Override the get_db dependency
    async def override_get_db():
        async with TestingSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    # Yield the session for use in tests
    async with TestingSessionLocal() as session:
        yield session

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
