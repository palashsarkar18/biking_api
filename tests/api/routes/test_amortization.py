from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def validate_amortization_response(data: dict):
    """
    Validates that an amortization response has all necessary fields
    and that the amortization table isn't empty.
    """
    assert data['leasing_duration'] > 0, "Leasing duration must be positive."
    assert 'total_interest_paid' in data, "Missing 'total_interest_paid'."
    assert 'amortization_table' in data, "Missing 'amortization_table'."
    assert len(data['amortization_table']) > 0, "Amortization table is empty."


def test_amortization_starter_calculation():
    """
    Tests the amortization endpoint with a 'starter' plan.
    """
    response = client.get(
        "/api/v1/amortization/?plan_type=starter&bike_price=2000"
    )
    assert response.status_code == 200, f"Request failed: {response.text}"

    # Validate response structure
    data = response.json()
    validate_amortization_response(data)


def test_amortization_pro_calculation():
    """
    Tests the amortization endpoint with a 'pro' plan.
    """
    response = client.get(
        "/api/v1/amortization/?plan_type=pro&bike_price=2000"
    )
    assert response.status_code == 200, f"Request failed: {response.text}"

    # Validate response structure
    data = response.json()
    validate_amortization_response(data)


def test_amortization_enterprise_calculation():
    """
    Tests the amortization endpoint with an 'enterprise' plan.
    """
    response = client.get(
        "/api/v1/amortization/?plan_type=enterprise&bike_price=2000"
    )
    assert response.status_code == 200, f"Request failed: {response.text}"

    # Validate response structure
    data = response.json()
    validate_amortization_response(data)


def test_amortization_invalid_plan():
    """
    Tests the amortization endpoint handling an unknown plan.
    """
    response = client.get(
        "/api/v1/amortization/?plan_type=unknown&bike_price=2000"
    )
    assert response.status_code == 404, "Expected 404 status for an unknown plan."


def test_amortization_error():
    """
    Tests the amortization endpoint handling a totally invalid plan type.
    """
    response = client.get("/api/v1/amortization",
                          params={"plan_type": "invalid", "bike_price": 2000})

    assert response.status_code == 404, "Expected 404 status for an invalid plan."
    assert response.json() == {"detail": "Plan not found"}
