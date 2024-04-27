from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Organisations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    business_id: str
    bikes: List["Bikes"] = Relationship(back_populates="organisation")


class Bikes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organisation_id: int = Field(foreign_key="organisations.id")
    brand: str
    model: Optional[str] = None
    price: float
    serial_number: str
    organisation: Organisations = Relationship(back_populates="bikes")

# TODO: Check why there are 'bike' and 'bikes' tables, and 'organisation' and 'organisations' tables.