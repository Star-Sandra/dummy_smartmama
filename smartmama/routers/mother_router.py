from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database import get_db
from security import get_current_chv
from schemas.mother import MotherCreate, MotherUpdate, MotherRead
from services import mother_service

router = APIRouter(prefix="/mothers", tags=["Mothers"])

@router.post("/mother", response_model=MotherRead, status_code=status.HTTP_201_CREATED)
def create_mother(data: MotherCreate, db: Session = Depends(get_db), current_chv = Depends(get_current_chv)):
    return mother_service.register_mother(db, data, current_chv.chv_id)

@router.get("/assigned_mothers", response_model=List[MotherRead])
def view_mothers_assigned_to_me(db: Session = Depends(get_db), current_chv = Depends(get_current_chv)):
    return mother_service.fetch_chv_mothers(db, current_chv.chv_id)

@router.get("/{id}", response_model=MotherRead)
def get_mother_profile(id: UUID, db: Session = Depends(get_db), current_chv = Depends(get_current_chv)):
    return mother_service.fetch_mother(db, str(id))

@router.patch("/{id}", response_model=MotherRead)
def update_mother(id: UUID, data: MotherUpdate, db: Session = Depends(get_db), current_chv = Depends(get_current_chv)):
    return mother_service.update_mother(db, str(id), data)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_mother(id: UUID, db: Session = Depends(get_db), current_chv = Depends(get_current_chv)):
    return mother_service.remove_mother(db, str(id))