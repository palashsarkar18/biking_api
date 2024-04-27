from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session
from typing import Generator

# Assuming SQLModel which wraps SQLAlchemy
DATABASE_URL = "postgresql://postgres:db580f2e939baa98cb393fa1b680c6b17072ff1b42b0669f575c0f93e525a8d3@db:5432/vapaus" # TODO: Get the password from the environment
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
