import uuid
from datetime import date
from sqlalchemy import Column, Text, Float, Integer, Date, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from smartmama.database import Base

class VisitLog(Base):
    __tablename__ = "visit_logs"
    visit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mother_id = Column(UUID(as_uuid=True),  nullable=False)      # ForeignKey("mother.mother_id")               
    pregnancy_id = Column(UUID(as_uuid=True),  nullable=False)                 # ForeignKey("pregnancy_tracking.pregnancy_id"),
    visit_date = Column(Date, default=date.today, nullable=False)
    weight = Column(Float, nullable=False)
    gestational_age = Column(Integer, nullable=False)
    systolic_bp = Column(Integer, nullable=False)   
    diastolic_bp = Column(Integer, nullable=False)   
    logged_symptoms = Column(Text, nullable=False)  
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


    