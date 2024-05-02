import logging

from fastapi.testclient import TestClient

from app.core.db import get_db
from app.main import app

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.getLogger().handlers = [logging.StreamHandler()]


def mock_get_db():
    return Exception("Database connection error")


def test_index() -> None:
    """
    Tests the main '/' endpoint.
    """
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200

    info = response.json()
    assert "database_connected" in info
    assert info["database_connected"] is True


def test_database_connection_failure(monkeypatch):
    """
    Tests '/' endpoint handling a database connection error.
    """
    # Override get_db dependency
    app.dependency_overrides[get_db] = mock_get_db

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"database_connected": False}

    # Clear override
    app.dependency_overrides.clear()
