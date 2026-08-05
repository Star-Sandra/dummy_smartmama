"""
Core Authentication Business Service Layer.
"""

from sqlalchemy.orm import Session
from smartmama.core.security import verify_password, create_access_token
from smartmama.repositories import chv_repository
from smartmama.schemas.auth import LoginRequest, Token


def authenticate_chv(db: Session, credentials: LoginRequest) -> Token | None:
    """
    Verify login credentials and return an access token.
    """
    chv = chv_repository.get_chv_by_email(db, credentials.email)
    if not chv or not chv.is_active:
        return None

    if not verify_password(credentials.password, chv.hashed_password):
        return None

    token_data = {"sub": chv.email, "chv_id": chv.chv_id}
    access_token = create_access_token(data=token_data)

    return Token(access_token=access_token, token_type="bearer")
