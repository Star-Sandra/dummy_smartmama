"""
Maternal clinical configuration demographical monitoring routers.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from smartmama.routers.dependencies import get_db, get_current_chv_email
from smartmama.schemas.auth import TokenData
from smartmama.schemas.mother import MotherCreate, MotherResponse
from smartmama.services import mother_service

router = APIRouter(prefix="/mothers", tags=["4. Expectant Mothers Registration"])

@router.post(
    "/", 
    response_model=MotherResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Onboard an expectant mother tracking configuration"
)
def onboard_mother_profile(
    mother_in: MotherCreate, 
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_chv_email)
):
    """
    Registers a new expectant mother in the system.
    Verifies that the provided CHV and location structural link tokens exist before completing the register transaction.
    Requires a valid bearer login token session.
    """
    profile = mother_service.register_new_mother(db, mother_in)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile creation rejected."
        )
    return profile


@router.get("/{mother_id}", response_model=MotherResponse, summary="Fetch mother identity profile matching target keys")
def retrieve_mother_demographics_by_id(
    mother_id: str, 
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_chv_email)
):
    """
    Retrieves the clinical enrollment details for a mother 
    """
    profile = mother_service.get_mother_profile_by_id(db, mother_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The target maternal reference could not be located."
        )
    return profile

@router.get("/", response_model=List[MotherResponse], summary="Retrieve all monitored mother entities")
def list_all_mothers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: TokenData = Depends(get_current_chv_email)):
    """Returns lists matching demographic registers inside databases."""
    return mother_service.get_multiple_mothers(db, skip=skip, limit=limit)

@router.put("/{mother_id}", response_model=MotherResponse, summary="Modify maternal charts parameters")
def modify_mother_profile(mother_id: str, payload: dict, db: Session = Depends(get_db), _: TokenData = Depends(get_current_chv_email)):
    """Update profile metrics for an active monitored mother record."""
    updated = mother_service.update_mother_profile(db, mother_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Maternal target reference index not found.")
    return updated

@router.delete("/{mother_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Purge mother profile records")
def delete_mother_profile(mother_id: str, db: Session = Depends(get_db), _: TokenData = Depends(get_current_chv_email)):
    """Permanently drops records tracking patient data charts fields."""
    success = mother_service.remove_mother_profile(db, mother_id)
    if not success:
        raise HTTPException(status_code=404, detail="Maternal target reference index not found.")
    return None