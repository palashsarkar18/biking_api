import pytest

from app.core.config import get_env_variable


def test_get_env_variable_existing(monkeypatch):
    """
    Test retrieving an existing environment variable.
    """
    monkeypatch.setenv("EXISTING_VAR", "test_value")

    result = get_env_variable("EXISTING_VAR")
    assert result == "test_value"


def test_get_env_variable_missing():
    """
    Test raising an error when an environment variable is missing.
    """
    with pytest.raises(EnvironmentError):
        get_env_variable("MISSING_VAR")
