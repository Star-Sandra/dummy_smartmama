from sqlalchemy.orm import Session
from models.chv import CHV

class CHVRepository:
    def __init__(self):
        self.model = CHV

    def get(self, db: Session, id:str):
        return db.get(CHV, id)

    def get_by_email(self, db: Session, email: str):
        return db.query(CHV).filter(CHV.email == email).first()

    def get_all(self, db: Session):
        return db.query(CHV).all()

    def create(self, db: Session, data: dict):
        obj = CHV(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: CHV, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: CHV):
        db.delete(db_obj)
        db.commit()

chv_repository = CHVRepository()