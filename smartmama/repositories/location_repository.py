"""
Repository layer for Location database operations.
"""

from sqlalchemy.orm import Session
from smartmama.models.location import Location
from typing import List

def get_location_by_id(db: Session, location_id: str) -> Location | None:
    return db.query(Location).filter(Location.location_id == location_id).first()

def create_location(db: Session, location_obj: Location) -> Location:
    db.add(location_obj)
    db.commit()
    db.refresh(location_obj)
    return location_obj

def get_all_locations(db: Session, skip: int = 0, limit: int = 100) -> List[Location]:
    """Retrieve multiple locations."""
    return db.query(Location).offset(skip).limit(limit).all()

def update_location_record(db: Session, db_location: Location, update_data: dict) -> Location:
    """Update fields on an existing location record."""
    for key, value in update_data.items():
        setattr(db_location, key, value)
    db.commit()
    db.refresh(db_location)
    return db_location

def delete_location_record(db: Session, db_location: Location) -> None:
    """Permanently delete a location record from the database."""
    db.delete(db_location)
    db.commit()