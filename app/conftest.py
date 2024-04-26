from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, SQLModel

from app.main import app, get_db

DATABASE_URI = "postgresql://postgres:db580f2e939baa98cb393fa1b680c6b17072ff1b42b0669f575c0f93e525a8d3@db:5432/vapaus_test"

engine = create_engine(DATABASE_URI)


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    """
    Create a clean test database every time the tests are run.
    """
    assert not database_exists(
        DATABASE_URI
    ), "Test database already exists. Aborting tests."
    create_database(DATABASE_URI)
    SQLModel.metadata.create_all(bind=engine)
    yield  # Run the tests
    drop_database(DATABASE_URI)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        app.dependency_overrides[get_db] = lambda: db
        yield session


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
