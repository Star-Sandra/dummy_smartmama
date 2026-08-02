
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from smartmama.database import get_db
from smartmama.schemas.visit_log import VisitLogCreate, VisitLogResponse, MotherVisitHistoryResponse
from smartmama.services.visit_log import visit_service

router = APIRouter(
    prefix="/visits", 
    tags=["Maternal Visit Logs"]
)

@router.post(
    "/", 
    response_model=VisitLogResponse, 
    status_code=status.HTTP_201_CREATED  
)
def log_maternal_visit(data: VisitLogCreate, db: Session = Depends(get_db)):
    """Ingests a new maternal checkup form submission."""
    return visit_service.process_and_log_visit(db, data)


@router.get(
    "/history/mother/{mother_id}", 
    response_model=MotherVisitHistoryResponse,
    status_code=status.HTTP_200_OK
)
def get_maternal_history(mother_id: uuid.UUID, db: Session = Depends(get_db)):
    """Pulls a mother's entire chronological checkup history."""
    return visit_service.get_mother_visit_history(db, mother_id)
