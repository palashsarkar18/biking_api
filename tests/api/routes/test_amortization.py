from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_amortization_starter_calculation():
    response = client.get(
        "/api/v1/amortization/?plan_type=starter&bike_price=2000"
        )
    assert response.status_code == 200
    data = response.json()
    assert data['leasing_duration'] > 0
    assert 'total_interest_paid' in data
    assert 'amortization_table' in data
    assert len(data['amortization_table']) > 0  # Ensure table isn't empty


def test_amortization_pro_calculation():
    response = client.get(
        "/api/v1/amortization/?plan_type=pro&bike_price=2000"
        )
    assert response.status_code == 200
    data = response.json()
    assert data['leasing_duration'] > 0
    assert 'total_interest_paid' in data
    assert 'amortization_table' in data
    assert len(data['amortization_table']) > 0  # Ensure table isn't empty


def test_amortization_enterprise_calculation():
    response = client.get(
        "/api/v1/amortization/?plan_type=enterprise&bike_price=2000"
        )
    assert response.status_code == 200
    data = response.json()
    assert data['leasing_duration'] > 0
    assert 'total_interest_paid' in data
    assert 'amortization_table' in data
    assert len(data['amortization_table']) > 0  # Ensure table isn't empty


def test_amortization_invalid_plan():
    response = client.get(
        "/api/v1/amortization/?plan_type=unknown&bike_price=2000"
        )
    assert response.status_code == 404


def test_amortization_error():
    """
    Tests amortization endpoint handling an invalid plan.
    """
    client = TestClient(app)

    response = client.get("/api/v1/amortization",
                          params={"plan_type": "invalid", "bike_price": 2000})

    assert response.status_code == 404
    assert response.json() == {"detail": "Plan not found"}
