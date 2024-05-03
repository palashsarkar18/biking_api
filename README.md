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

## API Endpoints Documentation
This API provides endpoints for managing bikes and calculating amortization schedules. Below is a detailed guide on how to use each endpoint, including example requests and descriptions of the parameters and expected responses.

### Bikes Endpoint
**Base URL for bikes**: `/api/v1/bikes`

**Get All Bikes**
* URL: `/api/v1/bikes`
* Method: GET
* Description: Retrieve a list of bikes with optional pagination and filtering.
* Query Parameters:
  * `skip`: Number of records to skip for pagination (default is 0).
  * `limit`: Maximum number of records to return (default is 10).
  * `org_id`: Optional; filter bikes by organization ID.
  * `search`: Optional; search term to filter bikes by brand or model.
* Example Request:
  ```
  GET /api/v1/bikes?skip=0&limit=10
  ```

* Example Response:
```
[
  {
    "brand": "Scott",
    "model": "null",
    "id": 1,
    "organisation_id": 18,
    "price": 794.46,
    "serial_number": "ZGDX-75142854"
  },
  {
    "brand": "Scott",
    "model": "null",
    "id": 2,
    "organisation_id": 12,
    "price": 6420.8,
    "serial_number": "XSCL-25662526"
  },
  {
    "brand": "Cervelo",
    "model": "null",
    "id": 3,
    "organisation_id": 1,
    "price": 1097.89,
    "serial_number": "DFZX-39094249"
  },
  {
    "brand": "Trek",
    "model": "null",
    "id": 4,
    "organisation_id": 25,
    "price": 4531.13,
    "serial_number": "TYYQ-32090583"
  },
  {
    "brand": "Giant",
    "model": "null",
    "id": 5,
    "organisation_id": 13,
    "price": 400.03,
    "serial_number": "WFKA-53009895"
  },
  {
    "brand": "Scott",
    "model": "null",
    "id": 6,
    "organisation_id": 48,
    "price": 10509.43,
    "serial_number": "BWSK-90173206"
  },
  {
    "brand": "Canyon",
    "model": "null",
    "id": 7,
    "organisation_id": 4,
    "price": 8270.05,
    "serial_number": "IFWG-23783383"
  },
  {
    "brand": "Cervelo",
    "model": "null",
    "id": 8,
    "organisation_id": 27,
    "price": 8101.22,
    "serial_number": "FWPV-55825063"
  },
  {
    "brand": "Specialized",
    "model": "null",
    "id": 9,
    "organisation_id": 41,
    "price": 8975.31,
    "serial_number": "JSHR-05243624"
  },
  {
    "brand": "Cervelo",
    "model": "null",
    "id": 10,
    "organisation_id": 31,
    "price": 10480.37,
    "serial_number": "NQTU-96918046"
  }
]
```
### Amortization Endpoint

**Base URL for amortization**: `/api/v1/amortization`

**Calculate Amortization**
* URL: `/api/v1/amortization`
* Method: GET
* Description: Calculates the payment schedule based on the bike price and a selected plan.
* Query Parameters:
  * `plan_type`: Type of the plan (e.g., starter, pro, enterprise).
  * `bike_price`: Price of the bike for which the amortization is calculated.

* Example Request:
  ```
  GET /api/v1/amortization?plan_type=starter&bike_price=2000
  ```

* Example Response:
```
{
  "leasing_duration": 22,
  "total_interest_paid": 217.8,
  "residual_value": 100,
  "amortization_table": [
    {
      "month_number": 1,
      "loan_balance": 1819,
      "monthly_interest_payment": 19,
      "monthly_principal_repayment": 81
    },
    {
      "month_number": 2,
      "loan_balance": 1737.19,
      "monthly_interest_payment": 18.19,
      "monthly_principal_repayment": 81.81
    },
    {
      "month_number": 3,
      "loan_balance": 1654.56,
      "monthly_interest_payment": 17.37,
      "monthly_principal_repayment": 82.63
    },
    {
      "month_number": 4,
      "loan_balance": 1571.11,
      "monthly_interest_payment": 16.55,
      "monthly_principal_repayment": 83.45
    },
    {
      "month_number": 5,
      "loan_balance": 1486.82,
      "monthly_interest_payment": 15.71,
      "monthly_principal_repayment": 84.29
    },
    {
      "month_number": 6,
      "loan_balance": 1401.69,
      "monthly_interest_payment": 14.87,
      "monthly_principal_repayment": 85.13
    },
    {
      "month_number": 7,
      "loan_balance": 1315.7,
      "monthly_interest_payment": 14.02,
      "monthly_principal_repayment": 85.98
    },
    {
      "month_number": 8,
      "loan_balance": 1228.86,
      "monthly_interest_payment": 13.16,
      "monthly_principal_repayment": 86.84
    },
    {
      "month_number": 9,
      "loan_balance": 1141.15,
      "monthly_interest_payment": 12.29,
      "monthly_principal_repayment": 87.71
    },
    {
      "month_number": 10,
      "loan_balance": 1052.56,
      "monthly_interest_payment": 11.41,
      "monthly_principal_repayment": 88.59
    },
    {
      "month_number": 11,
      "loan_balance": 963.09,
      "monthly_interest_payment": 10.53,
      "monthly_principal_repayment": 89.47
    },
    {
      "month_number": 12,
      "loan_balance": 872.72,
      "monthly_interest_payment": 9.63,
      "monthly_principal_repayment": 90.37
    },
    {
      "month_number": 13,
      "loan_balance": 781.44,
      "monthly_interest_payment": 8.73,
      "monthly_principal_repayment": 91.27
    },
    {
      "month_number": 14,
      "loan_balance": 689.26,
      "monthly_interest_payment": 7.81,
      "monthly_principal_repayment": 92.19
    },
    {
      "month_number": 15,
      "loan_balance": 596.15,
      "monthly_interest_payment": 6.89,
      "monthly_principal_repayment": 93.11
    },
    {
      "month_number": 16,
      "loan_balance": 502.11,
      "monthly_interest_payment": 5.96,
      "monthly_principal_repayment": 94.04
    },
    {
      "month_number": 17,
      "loan_balance": 407.13,
      "monthly_interest_payment": 5.02,
      "monthly_principal_repayment": 94.98
    },
    {
      "month_number": 18,
      "loan_balance": 311.21,
      "monthly_interest_payment": 4.07,
      "monthly_principal_repayment": 95.93
    },
    {
      "month_number": 19,
      "loan_balance": 214.32,
      "monthly_interest_payment": 3.11,
      "monthly_principal_repayment": 96.89
    },
    {
      "month_number": 20,
      "loan_balance": 116.46,
      "monthly_interest_payment": 2.14,
      "monthly_principal_repayment": 97.86
    },
    {
      "month_number": 21,
      "loan_balance": 17.63,
      "monthly_interest_payment": 1.16,
      "monthly_principal_repayment": 98.84
    },
    {
      "month_number": 22,
      "loan_balance": 0,
      "monthly_interest_payment": 0.18,
      "monthly_principal_repayment": 17.63
    }
  ]
}
```

## API Usage
This section describes how to interact with the API, including examples of how to paginate through bike listings and calculate amortization.

### Bikes Endpoint
The bikes endpoint supports pagination and filtering by organization ID and search query (for bike brands or models).

#### Pagination
You can paginate the bike listings by specifying skip and limit parameters:

* First page (first 10 bikes):
  ```
  GET /api/v1/bikes?skip=0&limit=10
  ```

* Second page (next 10 bikes):
  ```
  GET /api/v1/bikes?skip=10&limit=10
  ```
Replace `10` with another number to change the number of items per page.

#### Filtering
* Filter by organization ID:
  ```
  GET /api/v1/bikes?org_id=1
  ```

* Search for bikes by brand or model_
  ```
  GET /api/v1/bikes?search=Giant
  ```

### Amortization Endpoint
The amortization endpoint calculates the payment schedule based on the bike price and a selected plan.

Calculate amortization for a starter plan:
```
GET /api/v1/amortization?plan_type=starter&bike_price=2000
```

## Database Schema
`Organisations` table
* This table stores information about various organizations. Each organization can own multiple bikes.
* Columns:
  * `id` (Integer): The primary key for the organization.
  * `name` (String): The name of the organization, cannot be null.
  * `business_id` (String): A unique business identifier for the organization, cannot be null.

`Bikes` table
* This table holds details about bikes. Each bike is associated with one organization, establishing a many-to-one relationship with the `Organisations` table.
* Columns:
  * `id` (Integer): The primary key for the bike.
  * `organisation_id` (Integer): A foreign key that links each bike to its owning organization. It references the `id` column of the Organisations table.
  * `brand` (String): The brand of the bike, cannot be null.
  * `model` (String): The model of the bike, can be null.
  * `price` (Float): The price of the bike, cannot be null.
  * `serial_number` (String): A unique identifier for the bike, cannot be null.

### Relationships
* One-to-Many Relationship: Each Organisation can own multiple Bikes, but each Bike is owned by only one Organisation. This relationship is managed through the organisation_id in the Bikes table, which acts as a foreign key pointing to the id of an Organisation.
* **NOTE** I edited the `data/dump.sql` file to move the `organisations` rows before the `bikes` row. I also added the 50th organisation.

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
mypy tests/
```







