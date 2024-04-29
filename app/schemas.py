from pydantic import BaseModel
from typing import Optional


class BikeBase(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None


class BikeList(BikeBase):
    id: int
    organisation_id: Optional[int] = None
    price: float
    serial_number: str

    class Config:
        orm_mode = True