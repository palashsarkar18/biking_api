from pydantic import BaseModel, ConfigDict


class BikeBase(BaseModel):
    brand: str | None = None
    model: str | None = None


class BikeList(BikeBase):
    id: int
    organisation_id: int | None = None
    price: float
    serial_number: str

    model_config = ConfigDict(from_attributes=True)
