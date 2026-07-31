"""
Community Health Volunteer Management Logic Services Component.
"""

import uuid
from sqlalchemy.orm import Session
from smartmama.core.security import hash_password
from smartmama.models.chv import CHV
from smartmama.repositories import chv_repository
from smartmama.schemas.chv import CHVCreate, CHVResponse
from typing import List

def register_new_chv(db: Session, chv_in: CHVCreate) -> CHVResponse | None:
    """
    Process signup requests, ensure email uniqueness, and encrypt credentials.
    """
    existing = chv_repository.get_chv_by_email(db, chv_in.email)
    if existing:
        return None

    encrypted_pw = hash_password(chv_in.password)

    db_chv = CHV(
        chv_id=f"CHV-{uuid.uuid4().hex[:12].upper()}",
        national_id=chv_in.national_id,
        first_name=chv_in.first_name,
        last_name=chv_in.last_name,
        phone_number=chv_in.phone_number,
        email=chv_in.email,
        hashed_password=encrypted_pw,
        is_active=True
    )

    saved_chv = chv_repository.create_chv(db, db_chv)
    return CHVResponse.model_validate(saved_chv)


def get_chv_profile_by_id(db: Session, chv_id: str) -> CHVResponse | None:
    """
    Retrieve profile details.
    """
    chv = chv_repository.get_chv_by_id(db, chv_id)
    if not chv:
        return None
    return CHVResponse.model_validate(chv)

def get_multiple_chvs(db: Session, skip: int = 0, limit: int = 100) -> List[CHVResponse]:
    """
    Process list fetches.
    """
    records = chv_repository.get_all_chvs(db, skip=skip, limit=limit)
    return [CHVResponse.model_validate(r) for r in records]


def update_chv_profile(db: Session, chv_id: str, chv_update: dict) -> CHVResponse | None:
    """
    Locate account profiles and apply verified patch alterations safely.
    """
    db_chv = chv_repository.get_chv_by_id(db, chv_id)
    if not db_chv:
        return None
    
    if "password" in chv_update and chv_update["password"]:
        from smartmama.core.security import hash_password
        chv_update["hashed_password"] = hash_password(chv_update.pop("password"))

    updated_record = chv_repository.update_chv_record(db, db_chv, chv_update)
    return CHVResponse.model_validate(updated_record)


def remove_chv_profile(db: Session, chv_id: str) -> bool:
    """
    Verify profile existence parameters and execute deletion logic commands.
    """
    db_chv = chv_repository.get_chv_by_id(db, chv_id)
    if not db_chv:
        return False
    chv_repository.delete_chv_record(db, db_chv)
    return True