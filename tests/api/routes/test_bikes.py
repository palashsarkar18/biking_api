from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_bikes():
    response = client.get("/api/v1/bikes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of bikes


def test_bikes_pagination():
    response = client.get("/api/v1/bikes/?skip=0&limit=2")
    assert len(response.json()) == 2  # Check if pagination limit is respected


def test_bikes_filter_by_organization():
    response = client.get("/api/v1/bikes/?org_id=1")
    # All bikes should belong to org_id 1
    assert all(bike['organisation_id'] == 1 for bike in response.json())


def test_bikes_search_by_brand():
    response = client.get("/api/v1/bikes/?search=Giant")
    # At least one bike should match the brand
    assert any("Giant" in bike['brand'] for bike in response.json())
