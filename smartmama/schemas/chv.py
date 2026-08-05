from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

class CHVSignup(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    password: str

class CHVLogin(BaseModel):
    email: EmailStr
    password: str

class CHVRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    chv_id: UUID
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: EmailStr
    is_active: bool
    created_at: datetime

class CHVPartialUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active_name: Optional[str] = None