from typing import Any
from fastapi import FastAPI, APIRouter, Depends
from sqlmodel import Session, create_engine, SQLModel
from contextlib import asynccontextmanager

from sqlalchemy import text
from .api.api_v1.endpoints import bikes, amortization
from .dependencies import get_db
from .helpers import get_env_variable

POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_SERVER = get_env_variable("POSTGRES_SERVER")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
               f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(str(DATABASE_URI), pool_pre_ping=True)

app = FastAPI()
router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up... creating database tables")
    try:
        create_db_and_tables()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

    yield

    # TODO: Optionally add shutdown logic
    print("Application shutting down...")

    # Explicitly close sessions
    engine.dispose()  # This closes the connection pool, terminating all active sessions

app.lifespan = lifespan


def create_db_and_tables():
    # TODO: Add error handling around the database initialization to manage 
    # cases where the connection fails or credentials are incorrect.
    SQLModel.metadata.create_all(bind=engine)

# def get_db() -> Generator[Session, None, None]:  # pragma: no cover
#     with Session(engine) as session:
#         yield session


@router.get("/")
def read_index(db: Session = Depends(get_db)) -> Any:
    # Using 'execute' with 'scalars' for executing raw SQL statements
    # and then convert the results to a Pythonic format.
    result = db.execute(text("SELECT 1")).scalars().first()
    return {
        "database_connected": result == 1,  # type: ignore
    }


app.include_router(router)
app.include_router(bikes.router, prefix="/api/v1")
app.include_router(amortization.router, prefix="/api/v1")

# TODO: Reevaluate the project structure.