from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def validate_bikes_response(bikes: list):
    """
    Validates that each bike entry has essential keys.
    """
    for bike in bikes:
        assert 'id' in bike, f"Missing 'id' in bike: {bike}"
        assert 'organisation_id' in bike, f"Missing 'organisation_id' in bike: {bike}"
        assert 'brand' in bike, f"Missing 'brand' in bike: {bike}"
        assert 'model' in bike, f"Missing 'model' in bike: {bike}"
        assert 'price' in bike, f"Missing 'price' in bike: {bike}"
        assert 'serial_number' in bike, f"Missing 'serial_number' in bike: {bike}"


def test_read_bikes():
    """
    Tests retrieving all bikes.
    """
    response = client.get("/api/v1/bikes/")
    assert response.status_code == 200, f"Request failed: {response.text}"

    # Validate response structure
    bikes = response.json()
    assert isinstance(bikes, list), "Response is not a list of bikes"
    validate_bikes_response(bikes)


def test_bikes_pagination():
    """
    Tests bike pagination by skip and limit.
    """
    response = client.get("/api/v1/bikes/?skip=0&limit=2")
    assert response.status_code == 200, f"Request failed: {response.text}"

    bikes = response.json()
    assert len(bikes) == 2, "Pagination limit not respected"
    validate_bikes_response(bikes)


def test_bikes_filter_by_organization():
    """
    Tests filtering bikes by organization ID.
    """
    response = client.get("/api/v1/bikes/?org_id=1")
    assert response.status_code == 200, f"Request failed: {response.text}"

    bikes = response.json()
    # Check all bikes belong to org_id 1
    assert all(bike['organisation_id'] == 1 for bike in bikes), "Not all bikes belong to org_id 1"
    validate_bikes_response(bikes)


def test_bikes_search_by_brand():
    """
    Tests searching for bikes by brand.
    """
    response = client.get("/api/v1/bikes/?search=Giant")
    assert response.status_code == 200, f"Request failed: {response.text}"

    bikes = response.json()
    # Check at least one bike matches the brand
    assert any("Giant" in bike['brand'] for bike in bikes), "No bike matches the brand 'Giant'"
    validate_bikes_response(bikes)
