from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database import get_db
from security import get_current_chv, Token
from schemas.chv import CHVLogin, CHVRead, CHVSignup, CHVPartialUpdate
from services import chv_service
from repositories.chv_repository import chv_repository
 
router = APIRouter(prefix="/auth/chv", tags=["Chv authentication & profile"])
 
@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(data: CHVSignup, db: Session = Depends(get_db)):
    token = chv_service.signup(db, data)
    return Token(access_token=token, token_type="bearer")
 
@router.post("/login", response_model=Token)
def login(data: CHVLogin, db: Session = Depends(get_db)):
    token = chv_service.login(db, data)
    return Token(access_token=token, token_type="bearer")
 
@router.get("/current_chv", response_model=CHVRead)
def get_current_chv(current_chv=Depends(get_current_chv)):
    return current_chv

@router.patch("/patch_current_chv", response_model=CHVRead)
def patch_profile(data: CHVPartialUpdate, db: Session = Depends(get_db), current_chv=Depends(get_current_chv)):
    update_dict = data.model_dump(exclude_unset=True)
    return chv_repository.update(db, current_chv, update_dict)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_chv(id: UUID, db: Session = Depends(get_db), current_chv=Depends(get_current_chv)):
    chv = chv_repository.get(db, str(id))
    if not chv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="CHV not found")
    chv_repository.delete(db, chv)
    return {"detail": "CHV profile deleted successfully"}