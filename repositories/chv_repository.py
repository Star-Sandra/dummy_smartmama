"""
Repository layer for CHV database operations.
"""

from sqlalchemy.orm import Session
from smartmama.models.chv import CHV
from typing import List

def get_chv_by_id(db: Session, chv_id: str) -> CHV | None:
    return db.query(CHV).filter(CHV.chv_id == chv_id).first()


def get_chv_by_email(db: Session, email: str) -> CHV | None:
    return db.query(CHV).filter(CHV.email == email).first()


def create_chv(db: Session, chv_obj: CHV) -> CHV:
    db.add(chv_obj)
    db.commit()
    db.refresh(chv_obj)
    return chv_obj

def get_all_chvs(db: Session, skip: int = 0, limit: int = 100) -> List[CHV]:
    """
    Retrieve multiple CHV profiles with pagination.
    """
    return db.query(CHV).offset(skip).limit(limit).all()


def update_chv_record(db: Session, db_chv: CHV, update_data: dict) -> CHV:
    """
    Modify values to an existing database instance.
    """
    for key, value in update_data.items():
        setattr(db_chv, key, value)
    db.commit()
    db.refresh(db_chv)
    return db_chv


def delete_chv_record(db: Session, db_chv: CHV) -> None:
    """
    Permanently delete a CHV record from the database.
    """
    db.delete(db_chv)
    db.commit()