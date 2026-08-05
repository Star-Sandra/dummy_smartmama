"""
SQLAlchemy model for the Mother entity.
"""

from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from database import Base


class Mother(Base):
    __tablename__ = "mothers"

    mother_id = Column(String(20), primary_key=True, index=True)
    chv_id = Column(String(20), ForeignKey("chv.chv_id"), nullable=False)
    location_id = Column(String(20), ForeignKey("location.location_id"), nullable=False)
    national_id = Column(Integer, unique=True, nullable=True)  # Nullable if mother lacks an ID card
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    hashed_pin = Column(String(255), nullable=False)
    consent_given = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Mother {self.mother_id}: {self.first_name} {self.last_name}>"
