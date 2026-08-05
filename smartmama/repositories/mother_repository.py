from sqlalchemy.orm import Session
from models.mother import Mother
from schemas.mother import MotherCreate, MotherUpdate
from security import hash_password
from uuid import UUID

class MotherRepository:
    def __init__(self):
        self.model = Mother

    def get(self, db: Session, mother_id: str) -> Mother:
        return db.get(Mother, mother_id)

    def get_all(self, db: Session):
        return db.query(Mother).all()

    def get_all_by_chv(self, db: Session, chv_id: UUID):
        return db.query(Mother).filter(Mother.chv_id == chv_id).all()

    def create(self, db: Session, data: MotherCreate, chv_id: UUID) -> Mother:
        hashed_pin = hash_password(data.pin)
        payload = data.model_dump(exclude={"pin"})
        db_obj = Mother(
            chv_id=chv_id,
            location_id=data.location_id,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
            date_of_birth=data.date_of_birth,
            expected_delivery_date=data.expected_delivery_date,
            consent_given=data.consent_given,
            pin_hash=hashed_pin
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Mother, data: MotherUpdate) -> Mother:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Mother):
        db.delete(db_obj)
        db.commit()

mother_repository = MotherRepository()