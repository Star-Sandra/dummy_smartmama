from sqlalchemy.orm import Session
from repositories.mother_repository import mother_repository
from schemas.mother import MotherCreate, MotherUpdate
from uuid import UUID

def register_mother(db: Session, data: MotherCreate, chv_id: UUID):
    return mother_repository.create(db, data, chv_id)

def fetch_mother(db: Session, mother_id: str):
    from fastapi import HTTPException, status
    mother = mother_repository.get(db, mother_id)
    if not mother:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mother profile not found")
    return mother

def fetch_all_mothers(db: Session):
    return mother_repository.get_all(db)

def fetch_chv_mothers(db: Session, chv_id: UUID):
    return mother_repository.get_all_by_chv(db, chv_id)

def update_mother(db: Session, mother_id: str, data: MotherUpdate):
    mother = fetch_mother(db, mother_id)
    return mother_repository.update(db, mother, data)

def remove_mother(db: Session, mother_id: str):
    mother = fetch_mother(db, mother_id)
    mother_repository.delete(db, mother)
    return {"detail": "Mother profile deleted successfully"}
