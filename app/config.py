from dotenv import load_dotenv
import os

load_dotenv()


def get_env_variable(name: str) -> str:
    """
    Retrieve an environment variable or raise an exception if it's missing.
    """
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value
