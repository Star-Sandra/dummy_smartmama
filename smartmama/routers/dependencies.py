"""
Basic dependencies for database sessions and secure header token verification.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from smartmama.core.config import settings
from smartmama.database import SessionLocal
from smartmama.schemas.auth import TokenData

header_scheme = APIKeyHeader(name="token", auto_error=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_chv_email(token: str = Depends(header_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid session token. Please log in first.",
    )
    
    if not token:
        raise credentials_exception
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except JWTError:
        raise credentials_exception
