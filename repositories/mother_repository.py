"""
Repository layer for Mother database operations.
"""

from sqlalchemy.orm import Session
from smartmama.models.mother import Mother
from typing import List

def get_mother_by_id(db: Session, mother_id: str) -> Mother | None:
    return db.query(Mother).filter(Mother.mother_id == mother_id).first()

def get_mother_by_phone(db: Session, phone_number: str) -> Mother | None:
    return db.query(Mother).filter(Mother.phone_number == phone_number).first()

def create_mother(db: Session, mother_obj: Mother) -> Mother:
    db.add(mother_obj)
    db.commit()
    db.refresh(mother_obj)
    return mother_obj

def get_all_mothers(db: Session, skip: int = 0, limit: int = 100) -> List[Mother]:
    """Retrieve multiple patient entries from baseline records."""
    return db.query(Mother).offset(skip).limit(limit).all()

def update_mother_record(db: Session, db_mother: Mother, update_data: dict) -> Mother:
    """Update profile metrics for an active monitored mother record."""
    for key, value in update_data.items():
        setattr(db_mother, key, value)
    db.commit()
    db.refresh(db_mother)
    return db_mother

def delete_mother_record(db: Session, db_mother: Mother) -> None:
    """Drop mother's reference entries from system tables."""
    db.delete(db_mother)
    db.commit()