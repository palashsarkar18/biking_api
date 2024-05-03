import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str) -> str:
    """
    Retrieve an environment variable or raise an exception if it's missing.

    Args:
        name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the environment variable.

    Raises:
        EnvironmentError: If the specified environment variable is missing or empty.
    """
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value
