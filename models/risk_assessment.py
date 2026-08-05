from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    risk_id = Column(String(3), primary_key=True, index=True)
    pregnancy_id = Column(String(20), ForeignKey("pregnancies.pregnancy_id"), nullable=False)
    risk_level = Column(String(10), nullable=False)
    confidence_score = Column(Float, nullable=False)
    link_url = Column(String(255), nullable=False)
    pdf_password = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
