"""
Maternal Registration Profiles Execution Logic Components.
"""

import uuid
from sqlalchemy.orm import Session
from smartmama.core.security import hash_password
from smartmama.models.mother import Mother
from smartmama.repositories import mother_repository, chv_repository, location_repository
from smartmama.schemas.mother import MotherCreate, MotherResponse
from typing import List

def register_new_mother(db: Session, mother_in: MotherCreate) -> MotherResponse | None:
    """
    Coordinate maternal profile onboarding and enforce database constraints.
    """
    chv_check = chv_repository.get_chv_by_id(db, mother_in.chv_id)
    if not chv_check:
        return None

    loc_check = location_repository.get_location_by_id(db, mother_in.location_id)
    if not loc_check:
        return None

    duplicate = mother_repository.get_mother_by_phone(db, mother_in.phone_number)
    if duplicate:
        return None

    encrypted_pin = hash_password(mother_in.pin)

    db_mother = Mother(
        mother_id=f"MOM-{uuid.uuid4().hex[:12].upper()}",
        chv_id=mother_in.chv_id,
        location_id=mother_in.location_id,
        national_id=mother_in.national_id,
        first_name=mother_in.first_name,
        last_name=mother_in.last_name,
        phone_number=mother_in.phone_number,
        date_of_birth=mother_in.date_of_birth,
        hashed_pin=encrypted_pin,
        consent_given=mother_in.consent_given
    )

    saved_mother = mother_repository.create_mother(db, db_mother)
    return MotherResponse.model_validate(saved_mother)


def get_mother_profile_by_id(db: Session, mother_id: str) -> MotherResponse | None:
    """
    Retrieve expectant patient parameters matching database keys.
    """
    mother = mother_repository.get_mother_by_id(db, mother_id)
    if not mother:
        return None
    return MotherResponse.model_validate(mother)

def get_multiple_mothers(db: Session, skip: int = 0, limit: int = 100) -> List[MotherResponse]:
    """Retrieve and serialize data shapes across stored demographic charts."""
    records = mother_repository.get_all_mothers(db, skip=skip, limit=limit)
    return [MotherResponse.model_validate(r) for r in records]

def update_mother_profile(db: Session, mother_id: str, mother_update: dict) -> MotherResponse | None:
    """Verify presence criteria and update fields on patient profiles safely."""
    db_mother = mother_repository.get_mother_by_id(db, mother_id)
    if not db_mother:
        return None
        
    # Securely hash access PIN updates before storing in database
    if "pin" in mother_update and mother_update["pin"]:
        from smartmama.core.security import hash_password
        mother_update["hashed_pin"] = hash_password(mother_update.pop("pin"))
        
    updated_record = mother_repository.update_mother_record(db, db_mother, mother_update)
    return MotherResponse.model_validate(updated_record)

def remove_mother_profile(db: Session, mother_id: str) -> bool:
    """Verify demographic token availability parameters and delete charts."""
    db_mother = mother_repository.get_mother_by_id(db, mother_id)
    if not db_mother:
        return False
    mother_repository.delete_mother_record(db, db_mother)
    return True