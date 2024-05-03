import pytest
from sqlalchemy.exc import SQLAlchemyError
from app.crud import get_bikes


@pytest.fixture
def mock_session():
    """
    Creates a mock session object
    """
    class MockSession:
        def query(self, *args, **kwargs):
            raise SQLAlchemyError("Mocked error")

    return MockSession()


def mck_sqlachemyerror():
    return SQLAlchemyError("Mocked error")


def test_get_bikes_database_error(mock_session):
    """
    Test get_bikes function handling of database errors.
    """
    with pytest.raises(RuntimeError) as exc_info:
        get_bikes(db=mock_session, skip=0, limit=10)
    assert "Database query error" in str(exc_info.value), "Should handle the SQLAlchemyError properly"
