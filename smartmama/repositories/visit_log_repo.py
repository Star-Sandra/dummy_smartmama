from sqlalchemy.orm import Session
from smartmama.models.visit_log import VisitLog
from smartmama.schemas.visit_log import VisitLogCreate

class VisitRepository:
    @staticmethod
    def create_visit_log(db: Session, obj_in: VisitLogCreate) -> VisitLog:
        """
        Takes validated Pydantic data, stages it for insertion, 
        and allows PostgreSQL to trigger its automated server defaults.
        """
        db_obj = VisitLog(                 #database object
            mother_id=obj_in.mother_id,
            pregnancy_id=obj_in.pregnancy_id,
            weight=obj_in.weight,
            gestational_age=obj_in.gestational_age,
            systolic_bp=obj_in.systolic_bp,
            diastolic_bp=obj_in.diastolic_bp,
            logged_symptoms=obj_in.logged_symptoms
        )
        db.add(db_obj)       # Stage the data in the current DB session
        db.commit()          # Write the record permanently and fire server-side defaults
        db.refresh(db_obj)   # Pull back auto-generated values from PostgreSQL
        return db_obj
