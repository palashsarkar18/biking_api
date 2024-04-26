from fastapi.testclient import TestClient


def test_index(client: TestClient) -> None:
    r = client.get("/")
    info = r.json()
    assert r.status_code == 200
    assert info["database_connected"] is True
