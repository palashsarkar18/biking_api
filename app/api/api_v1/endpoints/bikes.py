from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ....dependencies import get_db
from ....crud import get_bikes
from ....schemas import BikeList

router = APIRouter()

@router.get("/bikes/", response_model=List[BikeList])
def read_bikes(
    skip: int = 0, 
    limit: int = 10, 
    org_id: int = None, 
    search: str = None, 
    db: Session = Depends(get_db)
):
    bikes = get_bikes(db, skip=skip, limit=limit, org_id=org_id, search=search)
    return bikes
