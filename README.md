## Description
This project is a FastAPI application designed to manage biking information, including operations for bike and amortization calculations. It utilizes SQLAlchemy for ORM and runs within Docker containers for easier development and deployment.

## Project Structure
```
/
├── app/                       # Application source files
│   ├── api/                   # API route handlers
│   │   ├── routes/            # Specific routes for different API endpoints
│   │   │   ├── bikes.py       # Routes for bike-related operations
│   │   │   └── amortization.py# Routes for amortization calculations
│   │   └── main.py            # Main router that includes all the routes
│   ├── core/                  # Core application configurations and database management
│   │   ├── config.py          # Configuration management, e.g., environment variables
│   │   └── db.py              # Database connection and operations
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas for request validation and response formatting
│   ├── crud.py                # CRUD utilities
│   └── main.py                # Main method
├── tests/                     # Test suite for the application
│   ├── api/                   # Tests for API endpoints
│   │   ├── routes/            # Tests for route-specific logic
│   │   │   ├── test_bikes.py  # Tests for bike routes
│   │   │   └── test_amortization.py  # Tests for amortization routes
│   ├── core/                  # Core functionality tests
│   |   └── test_config.py     # Tests for configuration management
│   ├── test_integration.py    # Integration tests for the entire application
│   ├── test_main.py           # Tests for main application functionality
│   └── conftest.py            # Pytest fixtures and test setup configurations
├── docker-compose.yml         # Docker Compose file to orchestrate containers
├── Dockerfile                 # Dockerfile for building the application image
├── pyproject.toml             # Project dependencies and configurations
├── poetry.lock                # Lock file for dependencies
└── README.md                  # This README file

```

## Running the Project

### Requirements
* Docker
* Docker Compose

### Setup and Running
1. Build and Run Containers
      ```
      docker-compose up -d --build
      ```
This command builds the application and starts all services defined in docker-compose.yml.

2. Access the API:
     * The API will be available at http://localhost:8080.

### Running Tests

1. Execute Tests
```
docker-compose run --rm tests
```
This command executes the test suite within a Docker container specifically designed for running tests.

### Useful Docker Commands
* Stop containers
```
docker-compose down
```

* View logs
```
docker-compose logs
```

* Rebuild Containers:
```
docker-compose up --build --force-recreate
```

## Lint with Flake8
To ensure the code adheres to Python style standards, run flake8 as follows:
```
flake8 .
```

## Type checking with mypy
To maintain high code quality and prevent type-related errors, `mypy` is used:
```
mypy app/
mypy test/
```







