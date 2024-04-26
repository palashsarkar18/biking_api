from typing import Any, Generator
from fastapi import FastAPI, APIRouter, Depends

from sqlmodel import Session, create_engine
from sqlalchemy import text


DATABASE_URI = "postgresql://postgres:db580f2e939baa98cb393fa1b680c6b17072ff1b42b0669f575c0f93e525a8d3@db:5432/vapaus"

engine = create_engine(str(DATABASE_URI), pool_pre_ping=True)


def get_db() -> Generator[Session, None, None]:  # pragma: no cover
    with Session(engine) as session:
        yield session


app = FastAPI()
router = APIRouter()


@router.get("/")
def read_index(db: Session = Depends(get_db)) -> Any:
    return {
        "database_connected": db.exec(text("SELECT 1")).first()[0] == 1,  # type: ignore
    }


app.include_router(router)
