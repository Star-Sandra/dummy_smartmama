"""
Location geocoding coordinate points.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from smartmama.routers.dependencies import get_db, get_current_chv_email
from smartmama.schemas.auth import TokenData
from smartmama.schemas.location import LocationCreate, LocationResponse
from smartmama.services import location_service

router = APIRouter(prefix="/locations", tags=["3. Location coordinates"])


@router.post(
    "/", 
    response_model=LocationResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Record layout location points coordinates metrics"
)
def log_new_location(
    location_in: LocationCreate, 
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_chv_email)
):
    """
    Saves new geographical latitude and longitude coordinates.
    """
    return location_service.create_new_location(db, location_in)


@router.get("/{location_id}", response_model=LocationResponse, summary="Fetch spatial property structures by ID")
def retrieve_location_by_id(
    location_id: str, 
    db: Session = Depends(get_db),
    _: TokenData = Depends(get_current_chv_email)
):
    """
    Queries spatial asset tracking fields stored inside location metrics tables.
    """
    record = location_service.get_location_by_id(db, location_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested location coordinate identifier doesn't match any recorded reference entries."
        )
    return record

@router.get("/", response_model=List[LocationResponse], summary="Retrieve all recorded locations")
def list_all_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: TokenData = Depends(get_current_chv_email)):
    """Returns an array of all spatial reference tracking records."""
    return location_service.get_multiple_locations(db, skip=skip, limit=limit)

@router.put("/{location_id}", response_model=LocationResponse, summary="Modify coordinate fields")
def modify_location_profile(location_id: str, payload: dict, db: Session = Depends(get_db), _: TokenData = Depends(get_current_chv_email)):
    """Dynamically updates field variables for a chosen location node."""
    updated = location_service.update_location_profile(db, location_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Location record not found.")
    return updated

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete location data records")
def delete_location_profile(location_id: str, db: Session = Depends(get_db), _: TokenData = Depends(get_current_chv_email)):
    """Permanently drops target spatial assets matching path elements."""
    success = location_service.remove_location_profile(db, location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location record not found.")
    return None