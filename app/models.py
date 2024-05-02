from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Define the base class
Base = declarative_base()


class Organisations(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    business_id = Column(String, nullable=False)

    # Relationship to Bikes
    bikes = relationship("Bikes", back_populates="organisation")


class Bikes(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    brand = Column(String, nullable=False)
    model = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    serial_number = Column(String, nullable=False)

    # Relationship to Organisations
    organisation = relationship("Organisations", back_populates="bikes")
