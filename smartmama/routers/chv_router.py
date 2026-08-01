"""
Community Health Volunteers management routing.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from smartmama.routers.dependencies import get_db, get_current_chv_email
from smartmama.schemas.auth import TokenData
from smartmama.schemas.chv import CHVCreate, CHVResponse
from smartmama.services import chv_service

router = APIRouter(prefix="/chvs", tags=["2. Community Health Volunteers (CHVs)"])

@router.post(
    "/", 
    response_model=CHVResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Enroll a new CHV"
)
def create_chv_account(chv_in: CHVCreate, db: Session = Depends(get_db)):
    new_profile = chv_service.register_new_chv(db, chv_in)
    if not new_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed."
        )
    return new_profile


@router.get("/", response_model=List[CHVResponse], summary="Retrieve all CHVs")
def list_all_chvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns an array tracking all Community Health Volunteers currently registered.
    """
    return chv_service.get_multiple_chvs(db, skip=skip, limit=limit)


@router.get("/{chv_id}", response_model=CHVResponse, summary="Get a specific CHV by ID")
def get_single_chv(chv_id: str, db: Session = Depends(get_db)):
    """
    Fetch a single volunteer record matching the provided system identifier.
    """
    profile = chv_service.get_chv_profile_by_id(db, chv_id)
    if not profile:
        raise HTTPException(status_code=404, detail="CHV profile record not found.")
    return profile


@router.put("/{chv_id}", response_model=CHVResponse, summary="Modify/Update a CHV profile")
def modify_chv_profile(chv_id: str, payload: dict, db: Session = Depends(get_db)):
    """
    Update field properties dynamically for a targeted CHV record index.
    """
    updated_profile = chv_service.update_chv_profile(db, chv_id, payload)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Cannot update. CHV record not found.")
    return updated_profile


@router.delete("/{chv_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a CHV profile")
def delete_chv_profile(chv_id: str, db: Session = Depends(get_db)):
    """
    Permanently delete a target user profile record matching the ID path parameters.
    """
    success = chv_service.remove_chv_profile(db, chv_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cannot delete. CHV record not found.")
    return None