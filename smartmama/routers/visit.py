from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from smartmama.routers.dependencies import get_db  
from smartmama.schemas.visit_log import VisitLogCreate, VisitLogResponse
from smartmama.services.visit_log import VisitService
# from smartmama.models.visit_log import VisitLog



router = APIRouter(
    prefix="/visits",
    tags=["Maternal Visit Logs"]
)

@router.post("/log", response_model=VisitLogResponse, status_code=status.HTTP_201_CREATED)
def log_maternal_visit(visit_in: VisitLogCreate, db: Session = Depends(get_db)):
    " Logs a mother's symptoms & calculates risk levels."
   # responsible for the dict output to displayed to CHV
    return VisitService.process_and_log_visit(db, visit_in)



