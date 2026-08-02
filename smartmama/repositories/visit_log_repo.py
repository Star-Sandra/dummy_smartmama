import uuid
from datetime import date
from sqlalchemy.orm import Session
from smartmama.models.visit_log import VisitLog
from smartmama.schemas.visit_log import VisitLogCreate

class VisitLogRepository:
    def __init__(self):
       self.model = VisitLog

    def create_visit_log(self, db: Session, obj_in: VisitLogCreate) -> VisitLog:
        """Saves a brand new independent maternal checkup record row."""
        visit_data = obj_in.model_dump()
        visit_data["visit_id"] = uuid.uuid4()
        visit_data["visit_date"] = date.today()
        db_record = VisitLog(**visit_data)
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    def get_by_mother_id(self, db: Session, mother_id: uuid.UUID):
        """Fetches historical logs chronologically via instance lookup."""
        return db.query(self.model).filter(
            self.model.mother_id == mother_id
        ).order_by(self.model.visit_date.desc()).all()

    def check_duplicate_today(self, db: Session, mother_id: uuid.UUID, current_date: date) -> VisitLog:
        """Checks for duplicate daily entries."""
        return db.query(self.model).filter(
            self.model.mother_id == mother_id,
            self.model.visit_date == current_date
        ).first()


visit_repo = VisitLogRepository()







    
