from sqlalchemy.orm import Session
from . import models
from sqlalchemy import or_


def get_bikes(db: Session, skip: int = 0, limit: int = 10, org_id: int = None,
              search: str = ""):
    query = db.query(models.Bikes)
    print(query)
    if org_id:
        query = query.filter(models.Bikes.organisation_id == org_id)
    if search:
        query = query.filter(
            or_(
                models.Bikes.brand.ilike(f"%{search}%"), 
                models.Bikes.model.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()