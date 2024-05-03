import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing import Generator

from app.core.config import get_env_variable
from app.main import app, get_db
from app.models import Base

# Initialize database configuration
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_SERVER = get_env_variable("POSTGRES_SERVER")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DATABASE_TEST_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
               f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}_test"

test_engine = create_engine(DATABASE_TEST_URI, pool_pre_ping=True)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Creates a clean test database every time the tests run.

    Drops the existing database, creates a new one, and sets up the necessary tables.
    """
    # Drop existing database if it exists
    if database_exists(DATABASE_TEST_URI):
        drop_database(DATABASE_TEST_URI)

    create_database(DATABASE_TEST_URI)  # Create a new empty database
    Base.metadata.create_all(bind=test_engine)  # Create tables

    yield  # Run tests

    # Drop the database after tests
    if database_exists(DATABASE_TEST_URI):
        drop_database(DATABASE_TEST_URI)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Provides a database session for use in tests.

    Overrides the default session dependency in the app to use this session.
    """
    with Session(test_engine) as session:
        app.dependency_overrides[get_db] = lambda: session
        yield session

    # Clear the override after the session closes
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Provides a test client for making API calls.
    """
    with TestClient(app) as test_client:
        yield test_client
