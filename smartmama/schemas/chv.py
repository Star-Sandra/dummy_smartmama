"""
Pydantic schemas for Community Health Volunteer (CHV) input validation and serialization.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class CHVBase(BaseModel):
    """
    Shared attributes for Community Health Volunteer records.
    """
    national_id: int = Field(..., description="CHV government identity document number registry token")
    first_name: str = Field(..., max_length=50, description="Legal given name identification profile value")
    last_name: str = Field(..., max_length=50, description="Legal family surname identity validation criteria")
    phone_number: str = Field(..., max_length=12, description="Active primary Safaricom or Airtel communications line identifier code")
    email: EmailStr = Field(..., description="Unique contact mailbox address mapped to account workspace records")


class CHVCreate(CHVBase):
    """
    Input schema defining initial manual enrollment criteria details.
    """
    password: str = Field(..., min_length=6, description="Plaintext password sequence bound to background security hashing logic workflows")


class CHVResponse(CHVBase):
    """
    Output model structural definition rendering out account statuses to system users.
    """
    chv_id: str = Field(..., description="Unique generated system administrative identifier primary token string")
    is_active: bool = Field(..., description="Status metric determining system platform user authorization operational access conditions")
    created_at: datetime = Field(..., description="Automatic record timestamp log initialization tracking coordinate parameter")

    model_config = {
        "from_attributes": True
    }
