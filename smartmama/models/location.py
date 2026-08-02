"""
SQLAlchemy model for the Location entity.
"""

from sqlalchemy import Column, String, Numeric
from smartmama.database import Base


class Location(Base):
    __tablename__ = "location"

    location_id = Column(String(20), primary_key=True, index=True)
    location_name = Column(String(100), nullable=False)
    
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)

    def __repr__(self) -> str:
        return f"<Location {self.location_id}: {self.location_name}>"
