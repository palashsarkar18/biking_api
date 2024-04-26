FROM python:3.11

WORKDIR /workspace

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"
RUN poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml poetry.lock* /workspace/
RUN poetry install --no-interaction

COPY ./app /workspace/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
