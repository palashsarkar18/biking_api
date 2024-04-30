import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session
from typing import Any

from app.api.main import api_router
from app.core.db import create_db_and_tables, get_db, engine

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
    engine.dispose()

app = FastAPI(lifespan=lifespan)


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