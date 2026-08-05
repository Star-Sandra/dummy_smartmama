import os
from datetime import datetime, timedelta, timezone

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from sqlalchemy.orm import Session
 
from database import get_db
from repositories.chv_repository import chv_repository
 
load_dotenv()
 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

FAILED_ATTEMPTS_TRACKER = {}
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
LOCKOUT_DURATION_MINUTES = int(os.getenv("LOCKOUT_DURATION_MINUTES", "5"))
 
bearer_scheme = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
 
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
 
def create_access_token(subject: str, token_type: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "type": token_type, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
 
def get_current_chv(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
 
    if payload.get("type") != "chv":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
 
    chv = chv_repository.get(db, payload["sub"])
    if not chv or not chv.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="CHV account not found or inactive")
 
    return chv

def check_login_attempts(email: str):
    now = datetime.now()
    
    if email in FAILED_ATTEMPTS_TRACKER:
        tracking = FAILED_ATTEMPTS_TRACKER[email]
        
        if tracking["lockout_until"] and now < tracking["lockout_until"]:
            remaining_time = int((tracking["lockout_until"] - now).total_seconds())
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many failed login attempts. Account locked. Try again in {remaining_time} seconds."
            )
            
        if tracking["lockout_until"] and now >= tracking["lockout_until"]:
            FAILED_ATTEMPTS_TRACKER[email] = {"count": 0, "lockout_until": None}

def log_failed_login(email: str):
    now = datetime.now()
    
    if email not in FAILED_ATTEMPTS_TRACKER:
        FAILED_ATTEMPTS_TRACKER[email] = {"count": 1, "lockout_until": None}
    else:
        FAILED_ATTEMPTS_TRACKER[email]["count"] += 1
        
    if FAILED_ATTEMPTS_TRACKER[email]["count"] >= MAX_LOGIN_ATTEMPTS:
        FAILED_ATTEMPTS_TRACKER[email]["lockout_until"] = now + timedelta(minutes=LOCKOUT_DURATION_MINUTES)

def clear_failed_logins(email: str):
    if email in FAILED_ATTEMPTS_TRACKER:
        del FAILED_ATTEMPTS_TRACKER[email]