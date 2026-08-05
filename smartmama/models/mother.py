import uuid

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Mother(Base):
    __tablename__ = "mothers"

    mother_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chv_id = Column(ForeignKey("chvs.chv_id"), nullable=False)
    location_id = Column(ForeignKey("location.location_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(12), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    expected_delivery_date=Column(Date, nullable=False)
    hashed_pin = Column(String(255), nullable=False)
    consent_given = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    chv = relationship("CHV", back_populates="mothers")
    # location = relationship("Location", back_populates="mothers")