from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class MotherBase(BaseModel):
    first_name: str 
    last_name: str
    phone_number: str
    date_of_birth: date
    expected_delivery_date: date
    consent_given: bool

class MotherCreate(MotherBase):
    location_id: Optional[str] = None
    pin: str

class MotherUpdate(BaseModel):
    phone_number: Optional[str] = None
    expected_delivery_date: Optional[date] = None
    consent_given: Optional[bool] = None

class MotherRead(MotherBase):
    model_config = ConfigDict(from_attributes=True)

    mother_id: str
    chv_id: UUID
    location_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime