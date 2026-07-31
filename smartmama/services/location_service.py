"""
Geographical Location Tracking Coordination Layer.
"""

import uuid
from sqlalchemy.orm import Session
from smartmama.models.location import Location
from smartmama.repositories import location_repository
from smartmama.schemas.location import LocationCreate, LocationResponse
from typing import List

def create_new_location(db: Session, location_in: LocationCreate) -> LocationResponse:
    """
    Process coordinate input frameworks captured during field sequences.
    """
    db_location = Location(
        location_id=f"LOC-{uuid.uuid4().hex[:12].upper()}",
        location_name=location_in.location_name,
        latitude=location_in.latitude,
        longitude=location_in.longitude
    )

    saved_location = location_repository.create_location(db, db_location)
    return LocationResponse.model_validate(saved_location)


def get_location_by_id(db: Session, location_id: str) -> LocationResponse | None:
    """
    Fetch spatial coordinate targets via structural database index values.
    """
    location = location_repository.get_location_by_id(db, location_id)
    if not location:
        return None
    return LocationResponse.model_validate(location)

def get_multiple_locations(db: Session, skip: int = 0, limit: int = 100) -> List[LocationResponse]:
    """Fetch location list profiles and parse them to output formats."""
    records = location_repository.get_all_locations(db, skip=skip, limit=limit)
    return [LocationResponse.model_validate(r) for r in records]

def update_location_profile(db: Session, location_id: str, location_update: dict) -> LocationResponse | None:
    """Locate a location and safely patch its geographic properties."""
    db_location = location_repository.get_location_by_id(db, location_id)
    if not db_location:
        return None
    updated_record = location_repository.update_location_record(db, db_location, location_update)
    return LocationResponse.model_validate(updated_record)

def remove_location_profile(db: Session, location_id: str) -> bool:
    """Validate location existence parameters and delete the record."""
    db_location = location_repository.get_location_by_id(db, location_id)
    if not db_location:
        return False
    location_repository.delete_location_record(db, db_location)
    return True