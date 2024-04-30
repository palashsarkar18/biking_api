from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_amortization_calculation():
    response = client.get("/api/v1/amortization/?plan_type=starter&bike_price=2000")
    assert response.status_code == 200
    data = response.json()
    assert data['leasing_duration'] > 0
    assert 'total_interest_paid' in data
    assert 'amortization_table' in data
    assert len(data['amortization_table']) > 0  # Ensure table isn't empty


def test_amortization_invalid_plan():
    response = client.get("/api/v1/amortization/?plan_type=unknown&bike_price=2000")
    assert response.status_code == 404  # Expecting an error for an unknown plan
