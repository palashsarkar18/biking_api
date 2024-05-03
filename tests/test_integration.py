import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.core.db import read_sql_file


def populate_database(db: Session, file_path: str):
    """
    Reads SQL content from a file and populates the database.
    """
    sql_content = read_sql_file(file_path)
    db.execute(text(sql_content))
    db.commit()


def get_bikes_response(client: TestClient, params: dict) -> list:
    """
    Helper to get and parse bikes API response.
    """
    response = client.get("/api/v1/bikes", params=params)
    assert response.status_code == 200, f"Request failed: {response.text}"
    return response.json()


@pytest.mark.usefixtures("setup_test_database")  # Ensures test database setup
def test_integration_bikes(client: TestClient, db: Session):
    """
    Tests API functionality with an integration test.
    """

    # Populate the database with initial data
    populate_database(db, "/workspace/tests/core/dump.sql")

    # Test retrieving all bikes
    response_json = get_bikes_response(client, params={})

    # Define expected result for comparison
    expected_json = [
            {
                'brand': 'Scott',
                'model': 'Speedster',
                'id': 1,
                'organisation_id': 1,
                'price': 794.46,
                'serial_number': 'ZGDX-75142854'
            },
            {
                'brand': 'Canyon',
                'model': 'Grizl Al',
                'id': 2,
                'organisation_id': 1,
                'price': 6420.8,
                'serial_number': 'XSCL-25662526'
            }
    ]

    # Compare response with expected result
    assert response_json == expected_json, (
        f"Response {response_json} mismatch."
    )

    # Test searching for bikes by brand
    response_json = get_bikes_response(client, params={"search": "Canyon"})

    # Define expected result for comparison
    expected_json = [
            {
                'brand': 'Canyon',
                'model': 'Grizl Al',
                'id': 2,
                'organisation_id': 1,
                'price': 6420.8,
                'serial_number': 'XSCL-25662526'
            }
    ]

    # Compare response with expected result
    assert response_json == expected_json, (
        f"Response {response_json} does not match expected {expected_json}"
    )

    # Test searching by org_id
    response_json = get_bikes_response(client, params={"org_id": 1})

    expected_json = [
            {
                'brand': 'Scott',
                'model': 'Speedster',
                'id': 1,
                'organisation_id': 1,
                'price': 794.46,
                'serial_number': 'ZGDX-75142854'
            },
            {
                'brand': 'Canyon',
                'model': 'Grizl Al',
                'id': 2,
                'organisation_id': 1,
                'price': 6420.8,
                'serial_number': 'XSCL-25662526'
            }
    ]

    # Compare response with expected result
    assert response_json == expected_json, (
        f"Response {response_json} does not match expected {expected_json}"
    )


@pytest.mark.usefixtures("setup_test_database")
def test_integration_amortization(client: TestClient):
    """
    Tests API functionality for amortization calculation.
    """
    # Define inputs for the amortization endpoint
    inputs = {
        "plan_type": "starter",
        "bike_price": 2000  # Set a bike price for the test
    }

    # Make a GET request to the amortization endpoint
    response = client.get("/api/v1/amortization", params=inputs)

    # Ensure request succeeded
    assert response.status_code == 200, f"Request failed: {response.text}"

    response_json = response.json()

    assert response_json["leasing_duration"] == 22, (
        "Wrong leasing duration"
    )

    assert response_json["residual_value"] == 100, (
        "Wrong residual value"
    )

    assert round(response_json["total_interest_paid"], 2) == round(217.80, 2), (
        "Wrong interest paid"
    )
