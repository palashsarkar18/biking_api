import logging

from sqlalchemy import text
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

from app.core.config import get_env_variable

# Initialize database configuration
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_SERVER = get_env_variable("POSTGRES_SERVER")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
               f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.getLogger().handlers = [logging.StreamHandler()]


def get_db() -> Generator[Session, None, None]:
    """Provides a database session for use in dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_sql_file(file_path: str) -> str:
    """
    Reads an SQL script file and returns its content as a string.
    """
    with open(file_path, "r") as sql_file:
        sql_content = sql_file.read()
    return sql_content


def create_db_and_tables(
        uri: str = DATABASE_URI,
        eng: Engine = engine,
        file_path: str = "/workspace/data/dump.sql"
        ):
    """
    Initializes the database and tables, managing errors.
    """
    if not database_exists(uri):
        create_database(uri)  # Create current database if not exists

    # Create tables defined in SQLModel metadata
    SQLModel.metadata.create_all(bind=eng)

    try:
        with Session(eng) as session:
            session.execute(text("SELECT 1"))

            # Read and execute SQL script files
            sql_content = read_sql_file(file_path)
            session.execute(text(sql_content))

            session.commit()
    except OperationalError as oe:
        session.rollback()
        logging.error(f"Database connection error: {oe}")
    except DatabaseError as de:
        session.rollback()
        logging.error(f"Database initialization error: {de}")
    except Exception as e:
        session.rollback()
        logging.error(f"General error during initialization: {e}")
