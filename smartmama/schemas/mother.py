"""
Pydantic schemas for Expectant Mother configuration details management records.
"""

from datetime import date
from pydantic import BaseModel, Field

class MotherBase(BaseModel):
    """
    Shared attributes representing registered expectant medical profile targets.
    """
    chv_id: str = Field(..., description="Associated monitoring agent Community Health Volunteer administrative parent link index")
    location_id: str = Field(..., description="Associated physical tracking location reference node record index mapping coordinates")
    national_id: int | None = Field(None, description="Optional national verification identification status token data element metrics")
    first_name: str = Field(..., max_length=50, description="Expectant mother patient legal given identification profile name")
    last_name: str = Field(..., max_length=50, description="Expectant mother patient legal family validation identity surname")
    phone_number: str = Field(..., max_length=12, description="Primary mobile communications contact network link routing indicator sequence")
    date_of_birth: date = Field(..., description="Historical birth records chronological calendar target marker calculating age structures")
    consent_given: bool = Field(..., description="Explicit legal indicator authorizing clinical health record storage authorization updates")


class MotherCreate(MotherBase):
    """
    Input structural definitions processing active entry profile requests.
    """
    pin: str = Field(..., min_length=4, max_length=6, description="Plaintext access PIN code processed by encryption utility context wrappers")


class MotherResponse(MotherBase):
    """
    Output schema processing clean serializations omitting masked security components.
    """
    mother_id: str = Field(..., description="Unique database identity framework identifier primary entity field index reference")

    model_config = {
        "from_attributes": True
    }
