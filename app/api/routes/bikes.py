from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.crud import get_bikes
from app.schemas import BikeList

router = APIRouter()


@router.get("/", response_model=List[BikeList])
def read_bikes(
    skip: int = 0,
    limit: int = 10,
    org_id: int = None,
    search: str = None,
    db: Session = Depends(get_db)
):
    bikes = get_bikes(db, skip=skip, limit=limit, org_id=org_id, search=search)
    return bikes
