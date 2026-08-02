"""
SQLAlchemy model for the Community Health Volunteer (CHV) entity.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from smartmama.database import Base

class CHV(Base):
    __tablename__ = "chv"

    chv_id = Column(String(20), primary_key=True, index=True)
    national_id = Column(Integer, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<CHV {self.chv_id}: {self.first_name} {self.last_name}>"
