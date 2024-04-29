from pydantic import BaseModel, ConfigDict
from typing import Optional


class BikeBase(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None


class BikeList(BikeBase):
    id: int
    organisation_id: Optional[int] = None
    price: float
    serial_number: str

    model_config = ConfigDict(from_attributes=True)
