from pydantic import BaseModel, ConfigDict


class BikeBase(BaseModel):
    """
    Defines the base schema for a bike.

    Attributes:
        brand: Optional string representing the bike's brand.
        model: Optional string representing the bike's model.
    """
    brand: str | None = None
    model: str | None = None

    # Enables converting from SQLAlchemy ORM objects to Pydantic models
    model_config = ConfigDict(from_attributes=True)


class BikeList(BikeBase):
    """
    Extends BikeBase to include additional information for a bike list.

    Attributes:
        id: An integer representing the bike's ID.
        organisation_id: Optional integer representing the organisation ID to which the bike belongs.
        price: A float representing the bike's price.
        serial_number: A string representing the bike's serial number.
    """
    id: int
    organisation_id: int | None = None
    price: float
    serial_number: str

    # Enables converting from SQLAlchemy ORM objects to Pydantic models
    model_config = ConfigDict(from_attributes=True)
