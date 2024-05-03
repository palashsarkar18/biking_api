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
    org_id: int | None = None,
    search: str | None = "",
    db: Session = Depends(get_db)
) -> List[BikeList]:
    """
    Retrieve a list of bikes with optional filtering and pagination.

    Args:
        skip (int): The number of records to skip for pagination.
        limit (int): The maximum number of records to return.
        org_id (Optional[int]): An optional organization ID to filter the bikes by organization.
        search (Optional[str]): An optional string to partially match against bike brands or models.
        db (Session): The database session provided by the dependency injection system.

    Returns:
        List[BikeList]: A list of bikes that match the filtering and pagination criteria.
    """
    bikes = get_bikes(db, skip=skip, limit=limit, org_id=org_id, search=search)
    # Convert SQLAlchemy model instances to Pydantic model instances
    return [BikeList.model_validate(bike) for bike in bikes]
