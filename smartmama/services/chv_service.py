
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.chv_repository import chv_repository
from schemas.chv import CHVLogin, CHVSignup
from security import create_access_token, hash_password, verify_password, check_login_attempts, log_failed_login, clear_failed_logins

def signup(db: Session, data: CHVSignup) -> str:
    if chv_repository.get_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
 
    payload = data.model_dump(exclude={"password"})
    payload["hashed_password"] = hash_password(data.password)
    chv = chv_repository.create(db, payload)
 
    return create_access_token(subject=str(chv.chv_id), token_type="chv")

def login(db: Session, data: CHVLogin) -> str:
    check_login_attempts(data.email)

    chv = chv_repository.get_by_email(db, data.email)

    if not chv or not chv.hashed_password or not verify_password(data.password, chv.hashed_password):
        log_failed_login(data.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not chv.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

    clear_failed_logins(data.email)
    
    return create_access_token(subject=str(chv.chv_id), token_type="chv")