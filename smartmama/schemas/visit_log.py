import uuid
from datetime import date
from typing import List
from pydantic import BaseModel, Field


class VisitLogCreate(BaseModel):
    mother_id: uuid.UUID = Field(
        ..., 
        description="References the mother being visited."
    )
    pregnancy_id: uuid.UUID = Field(
        ..., 
        description="References the pregnancy associated with the visit."
    )
    weight: float = Field(
        ..., 
        gt=0, 
        le=300, 
        description="The weight of the mother since the last visit"
    )
    gestational_age: int = Field(
        ..., 
        ge=0, 
        le=50, 
        description="Gestational age recorded during the visit."
    )
    systolic_bp: int = Field(
        ..., 
        ge=40, 
        le=250, 
        description="Stores the high number from a blood pressure check when the heart is pumping."
    )
    diastolic_bp: int = Field(
        ..., 
        ge=30, 
        le=150, 
        description="Stores the low number from a blood pressure check when the heart is at rest."
    )
    logged_symptoms: str = Field(
        ..., 
        max_length=1000, 
        description="The mother's captured symptoms"
    )
     

class VisitLogResponse(BaseModel):
    visit_id: uuid.UUID = Field(..., description="Unique identifier for each household visit.")
    visit_date: date = Field(..., description="Date when the household visit was conducted.")
    risk_level: str = Field(..., description="The calculated Random Forest classification result.")
    recommendations: List[str] = Field(..., description="Actionable clinical steps for the CHV to follow.")

    class Config:
        from_attributes = True

