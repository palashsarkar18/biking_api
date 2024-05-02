import pytest

from sqlalchemy import create_engine, text
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy.orm import Session

from app.core.config import get_env_variable
from app.core.db import create_db_and_tables
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


@pytest.fixture(scope="session")
def setup_test_database():
    """Creates and cleans up the test database."""
    if database_exists(DATABASE_TEST_URI):
        drop_database(DATABASE_TEST_URI)

    create_database(DATABASE_TEST_URI)
    Base.metadata.create_all(bind=test_engine)

    yield  # Run tests

    drop_database(DATABASE_TEST_URI)


@pytest.mark.usefixtures("setup_test_database")
def test_create_db_and_tables():

    # Call the function
    create_db_and_tables(DATABASE_TEST_URI,
                         test_engine,
                         "/workspace/tests/core/dump.sql")

    # Check if tables are created (use valid queries or inspection)
    with Session(test_engine) as session:
        result_bikes = session.execute(text("SELECT * FROM bikes")).fetchall()
        result_organisations = session.execute(
            text("SELECT * FROM organisations")
            ).fetchall()
        assert len(result_bikes) == 2
        assert len(result_organisations) == 1
