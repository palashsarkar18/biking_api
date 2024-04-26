# Vapaus backend assignment

Congratulations on making it this far!
This assignment is meant to test your backend coding skills. If you have any question about this assignment, feel free to get in touch with us directly.

Good luck! :)

## Setup

To make you started faster, we are providing a simple Docker setup composed of two containers, one
for the PostgreSQL database and one for the API. This should work as is, but please edit the Docker configuration if you need to.

To start the containers you can do:

```shell session
docker compose up -d --build
```

To make sure everything is working properly you can go to: [http://localhost:8080/docs](http://localhost:8080/docs)
You should see an API's documentation page.

This project uses [Poetry](https://python-poetry.org/) to manage dependencies, to add a dependency simply do:

```shell session
poetry add <package name>
```

or to execute it from inside the Docker container:

```shell session
docker exec <container name> poetry add <package name>
```

Once you have managed to create the tables, you can find a dump in the data folder to populate it.

We also provide a minimal API setup (including tests setup), but please update it to fit your needs and practises, we provide it to get you started faster, but we expect the code to be better organised than that as the current setup doesn't follow best practises.

## Requirements

You’ll have to build a simple API using Python and [FastAPI](https://fastapi.tiangolo.com/).
You’ll have to use PostgreSQL for the database and either
[SQLModel](https://sqlmodel.tiangolo.com/) or [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM.

The API you need to build will use the following two entities:

### Organisation

An organisation has the following attributes:

- id
- name
- business ID

### Bike

A bike has the following attributes:

- id
- organisation ID
- brand
- model
- price
- serial number

Except for the model that is optional, all these attributes are mandatory. The serial number must be unique.
The brand is one of a fixed set of values: Canyon, Trek, Cannondale, Specialized, Giant, Orbea, Scott, Santa Cruz and Cervelo.

You can find seed data in the data folder.

### API requirements

Please create the two following endpoints:

- a first one to read a paginated list of bikes that can optionally be filtered by organisation (given an organisation id) or by partially matching brands or model (from a string input)

- a second one that would calculate the amortisation table for a contract. This is basically a simplified version of something we have in our codebase.
  When leasing a bike from us, the user will have a contract with the following parameters (the values are examples, in this case we are using the Starter plan, more about plans later):
  - Cost of the bike (Principal): 2000€
  - Residual value: 5% of the principal = 100€ (2000 \* 0.05)
  - Annual interest rate: 12% = 0.12 (as a decimal)
  - Monthly payment : 100€
    The monthly payment is composed of a part that will go toward paying back the principal and a part that is the monthly interest. The monthly interest rate is calculated by dividing the annual interest by 12. In this case the annual interest rate is 12%, so the monthly interest rate is 12/12 = 1% = 0.01
    The initial loan balance is the cost of the bike minus the residual value. In this case 2000 - 100 = 1900€

Example: if you have a 2000€ contract at an annual interest rate of 12%, the first monthly payment would be 100€ of which `1900 * 0.01 = 19€` (initial loan balance \* monthly interest rate) would be as interest and 81€ would go toward the repayment of the principal. For the second month `1819 * 0.01 = 18.19€` would be paid as interest and 81.81€ would go toward paying back the principal. An so on until the principal is fully paid.

The amortisation table is the breakdown of the repayment month per month

It would take the following inputs:

- a plan (you can find the plans in the plans.py file)
- a bike price

It should return an object with the following properties:

- leasing duration in months
- total interest paid (sum of the monthly interest payments)
- residual value
- amortisation table (which is a list of objects)
  - month number
  - loan balance
  - monthly interest payment
  - monthly principal repayment

About the plans: they are parameters that condition the contract with the user. They will define the maximum price for a bike (max principal), the annual interest rate, the residual percentage used to calculate the residual value, the maximum duration in months and the monthly payment.

If you feel like you need to use some library to help you with that - it's fine.

## Evaluation criteria

Your assignment will be evaluated on the following criteria:

- Project structure: Provide a well-organized FastAPI project.
- Documentation: Include a README file explaining the project, setup process, and how to test the endpoints.
- Code quality: Follow coding best practices and include comments where appropriate
