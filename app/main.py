import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Any

from app.api.main import api_router
from app.core.db import create_db_and_tables, get_db, engine

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.getLogger().handlers = [logging.StreamHandler()]

# Define the main FastAPI application
app = FastAPI()

# Define a router for managing routes
router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for managing the app's lifecycle.

    This function handles startup and shutdown logic for the FastAPI application.
    """
    # Startup logic
    logging.info("Starting up.")
    try:
        create_db_and_tables()
    except Exception as e:
        logging.error(f"Error initializing tables: {e}")

    yield

    # Shutdown logic
    logging.info("Application shutting down...")
    engine.dispose()  # Closes the connection pool and terminates all active sessions

app = FastAPI(lifespan=lifespan)


@router.get("/")
def read_index(db: Session = Depends(get_db)) -> Any:
    """
    Main endpoint to check database connectivity.

    :param db: Database session dependency
    :return: JSON response indicating whether the database is connected
    """
    try:
        # Using 'execute' with 'scalars' for executing raw SQL statements
        # and converting the results to a Pythonic format.
        result = db.execute(text("SELECT 1")).scalars().first()
        return {"database_connected": result == 1}  # type: ignore
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return {"database_connected": False}


# Include the routes
app.include_router(router)
app.include_router(api_router, prefix="/api/v1")
