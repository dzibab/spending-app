import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.session import Base, get_db
from app.db.models import Spending as SpendingDB
from app.main import app

# Create a new SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Session fixture for individual test cases
@pytest.fixture(scope="function")
def session():
    """
    Creates a new database session for each test function.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def clear_spendings(session):
    # Clear the spending table before each test
    session.query(SpendingDB).delete()
    session.commit()  # Commit the changes to the database


# Override the get_db dependency in FastAPI and provide the client
@pytest.fixture(scope="function")
def client(session):
    """
    Creates a FastAPI TestClient and overrides the get_db dependency
    to use the session fixture.
    """
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # Override FastAPI's get_db dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clear the overrides after the test
    app.dependency_overrides.clear()


# Setup and teardown for the test database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Create tables before running tests and drop them after all tests are finished.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
