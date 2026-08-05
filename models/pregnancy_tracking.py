from sqlalchemy import Column, String, DateTime
from database import Base
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class Pregnancy(Base):
    __tablename__ = "pregnancies"

    pregnancy_id = Column(String(20), primary_key=True, index=True)
    expected_delivery_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
