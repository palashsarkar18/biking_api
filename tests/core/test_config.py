import pytest

from app.core.config import get_env_variable


def test_get_env_variable_existing(monkeypatch):
    """
    Test retrieving an existing environment variable.

    This sets up an environment variable using monkeypatch and verifies that
    get_env_variable() returns the correct value.
    """
    # Set up an environment variable for testing
    monkeypatch.setenv("EXISTING_VAR", "test_value")

    # Retrieve it using the function
    result = get_env_variable("EXISTING_VAR")
    assert result == "test_value"


def test_get_env_variable_missing():
    """
    Test raising an error when an environment variable is missing.

    This verifies that get_env_variable() raises an EnvironmentError when
    trying to retrieve a non-existent variable.
    """
    with pytest.raises(EnvironmentError):
        get_env_variable("MISSING_VAR")
