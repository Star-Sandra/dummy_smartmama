"""
Endpoints handling login validation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from smartmama.routers.dependencies import get_db
from smartmama.schemas.auth import LoginRequest, Token
from smartmama.services import auth_service

router = APIRouter(prefix="/auth", tags=["1. Authentication"])

@router.post("/login", response_model=Token, summary="Log into a CHV account")
def login_chv_for_token(payload: LoginRequest, db: Session = Depends(get_db)):
    token_response = auth_service.authenticate_chv(db, payload)
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
        
    return token_response
