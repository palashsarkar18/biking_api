from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, SQLModel

from app.main import app, get_db
from app.helpers import get_env_variable

POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_SERVER = get_env_variable("POSTGRES_SERVER")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
               f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}-test"

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

# TODO:

# 1. Check why conftest file is not running with pytest.
# 2. Check why vapaus-test was defined as such.