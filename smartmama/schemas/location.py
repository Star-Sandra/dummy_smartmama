"""
Pydantic schemas for Location coordinate properties structural definitions.
"""

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    """
    Shared spatial attributes tracking targeted maternal residential coordinates.
    """
    location_name: str = Field(..., max_length=100, description="Specific community settlement center name or residential estate entry label")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Exact numerical spatial coordinate parameter for geocoding tracking layout indexes")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Exact numerical longitudinal coordinate dimension parameter mapping values safely")


class LocationCreate(LocationBase):
    """
    Input boundary parameters format layout during baseline registration sequences.
    """
    pass


class LocationResponse(LocationBase):
    """
    Output structured model layout exposing database tracking information endpoints.
    """
    location_id: str = Field(..., description="Unique generated spatial reference tracking record token primary layout index")

    model_config = {
        "from_attributes": True
    }
