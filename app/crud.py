from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app import models


def get_bikes(
    db: Session, skip: int = 0, limit: int = 10, org_id: int | None = None, search: str = ""
) -> list[models.Bikes]:
    """
    Fetches a list of bikes from the database with optional filtering.

    Args:
        db: A SQLAlchemy Session object.
        skip: An integer specifying how many records to skip for pagination.
        limit: An integer specifying the maximum number of records to return.
        org_id: An optional integer representing the organisation ID to filter bikes by.
        search: An optional string to filter bikes by their brand or model, using a case-insensitive match.

    Returns:
        A list of `models.Bikes` objects representing the filtered bikes.
    """
    try:
        query = db.query(models.Bikes)

        if org_id:
            query = query.filter(models.Bikes.organisation_id == org_id)

        if search:
            query = query.filter(
                or_(
                    models.Bikes.brand.ilike(f"%{search}%"),
                    models.Bikes.model.ilike(f"%{search}%"),
                )
            )

        return query.offset(skip).limit(limit).all()

    except SQLAlchemyError as e:
        # Log or handle the error as needed
        raise RuntimeError(f"Database query error: {e}")
