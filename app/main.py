from typing import Any
from fastapi import FastAPI, APIRouter, Depends
from sqlmodel import Session, create_engine, SQLModel
from contextlib import asynccontextmanager
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy_utils import create_database, database_exists
import logging
from sqlalchemy import text
from app.core.dependencies import get_db
from app.core.config import get_env_variable
from app.api.main import api_router

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

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.getLogger().handlers = [logging.StreamHandler()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logging.info("Starting up... creating database tables")
    try:
        create_db_and_tables()
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

    yield

    logging.info("Application shutting down...")

    # Explicitly close sessions
    engine.dispose()  # This closes the connection pool, terminating all active sessions

app = FastAPI(lifespan=lifespan)


def read_sql_file(file_path: str) -> str:
    """
    Reads an SQL script file and returns its content as a string.
    """
    with open(file_path, "r") as sql_file:
        sql_content = sql_file.read()
    return sql_content


def create_db_and_tables():
    if not database_exists(DATABASE_URI):
        create_database(DATABASE_URI)  # Create current database if not exists

    # Create tables defined in SQLModel metadata
    SQLModel.metadata.create_all(bind=engine)

    try:
        # Test the database connection
        with Session(engine) as session:
            session.execute(text("SELECT 1"))

        # Read and execute SQL script files here
        sql_content = read_sql_file("/workspace/data/dump.sql")
        session.execute(text(sql_content))

        # Commit changes to apply them
        session.commit()

    except OperationalError as oe:
        session.rollback()  # Roll back partial changes
        logging.error(f"Database connection error: {oe}")
    except DatabaseError as de:
        session.rollback()  # Roll back partial changes
        logging.error(f"Database initialization error: {de}")
    except Exception as e:
        session.rollback()  # Roll back partial changes
        logging.error(f"General error during initialization: {e}")


@router.get("/")
def read_index(db: Session = Depends(get_db)) -> Any:
    # Using 'execute' with 'scalars' for executing raw SQL statements
    # and then convert the results to a Pythonic format.
    try:
        result = db.execute(text("SELECT 1")).scalars().first()
        return {
            "database_connected": result == 1,  # type: ignore
        }
    except Exception as e:
        logging.error(f"Database connection error: {e}")

        return {
            "database_connected": False,
        }


app.include_router(router)
app.include_router(api_router, prefix="/api/v1")

# TODO: Reevaluate the project structure.