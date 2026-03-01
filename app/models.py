"""
SQLAlchemy ORM models.
"""

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class Retailer(Base):
    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    stores = relationship("Store", back_populates="retailer")


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    retailer_id = Column(Integer, ForeignKey("retailers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    retailer = relationship("Retailer", back_populates="stores")