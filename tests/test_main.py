from fastapi.testclient import TestClient

from app.main import app


def test_index() -> None:
    """Tests the main '/' endpoint."""
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200

    info = response.json()
    assert "database_connected" in info
    assert info["database_connected"] is True
