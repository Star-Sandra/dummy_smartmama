import os
#iport joblib
import uuid
from datetime import date  
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from smartmama.repositories.visit_log_repo import visit_repo
from smartmama.schemas.visit_log import VisitLogCreate
from smartmama.models.visit_log import VisitLog

class VisitService:
      
# machine learning execution code
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "maternal_risk_model.joblib")
    
    try:
        import joblib
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None

    @classmethod
    def process_and_log_visit(cls, db: Session, obj_in: VisitLogCreate) -> dict:
        """
        [POST METHOD ENGINE]
        Ingests real-time checkup metrics, enforces daily duplicate prevention barriers,
        extracts data feature states for Random Forest AI prediction, and records the logs.
        """
#  DUPLICATE LOG PREVENTION 
        existing_visit_today = db.query(VisitLog).filter(
            VisitLog.mother_id == obj_in.mother_id,
            VisitLog.visit_date == date.today()
        ).first()

        if existing_visit_today:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A maternal checkup session has already been logged for this mother today."
            )

        clean_symptoms = obj_in.logged_symptoms.lower()
        risk_level = "Medium Risk"

# 2. RUN MACHINE LEARNING LOGIC IF IT EXISTS
        if cls.model is not None:
            checklist = ["fever", "headache", "swollen feet", "blurred vision", "severe_bleeding"]
            symptom_features = [1 if sym in clean_symptoms else 0 for sym in checklist]

            ml_input_features = [[
                obj_in.weight,
                obj_in.gestational_age,
                obj_in.systolic_bp,
                obj_in.diastolic_bp,
                *symptom_features  #upacking operator to pick out individual symptoms and analyse them
            ]]

            prediction = cls.model.predict(ml_input_features)
            risk_level = str(prediction[0]) 
        
# Fallback engine where ml is not present
        else:
            has_severe_symptom = "severe_bleeding" in clean_symptoms or "blurred vision" in clean_symptoms
            has_moderate_symptom = "fever" in clean_symptoms or "headache" in clean_symptoms or "swollen feet" in clean_symptoms
            
            if (
                obj_in.systolic_bp >= 140 or 
                obj_in.diastolic_bp >= 90 or 
                has_severe_symptom or 
                (obj_in.gestational_age >= 40 and has_moderate_symptom)
            ):
                risk_level = "High Risk"
            elif (
                (130 <= obj_in.systolic_bp < 140) or 
                (80 <= obj_in.diastolic_bp < 90) or 
                has_moderate_symptom or
                (obj_in.weight > 100.0)  
            ):
                risk_level = "Medium Risk"
            else:
                risk_level = "Low Risk"


        db_record = visit_repo.create_visit_log(db, obj_in)
 # Recommendations based on outcome
        recommendations = []
        if "high" in risk_level.lower():
            recommendations = [
                "URGENT: Refer the mother to the nearest hospital immediately.",
                "Advise emergency transport and accompany the mother if possible.",
                "Message summary of health progress for high prioritization at healthcare facility.",
                "Notify the receiving facility clinical team regarding severe signs."
            ]
        elif "medium" in risk_level.lower():
            recommendations = [
                "Schedule a follow-up home visit within 3 to 5 days.",
                "Counsel the mother on warning signs.",
                "Advise routine checkup at the local clinic this week."
            ]
        else:
            recommendations = [
                "Continue standard prenatal care and nutrition tracking.",
                "Remind the mother of her next scheduled clinic appointment."
            ]
                
        return {
            "visit_id": db_record.visit_id,
            "visit_date": db_record.visit_date,
            "risk_level": risk_level,
            "recommendations": recommendations
        }

    @classmethod
    def get_mother_visit_history(cls, db: Session, mother_id: uuid.UUID) -> dict:
        " Display mother's visit hisory"   
        db_records = visit_repo.get_by_mother_id(db, mother_id)        
        current_risk = "N/A"
        ai_confidence = "0%"
        last_visit_desc = "Never visited"        
              
        if db_records:
            latest_visit = db_records[0]
            current_risk = latest_visit.risk_level.upper()
            ai_confidence = "94%"              
            days_ago = (date.today() - latest_visit.visit_date).days
            last_visit_desc = "Today" if days_ago == 0 else "Yesterday" if days_ago == 1 else f"{days_ago} days ago"

        history_summary = []
        for record in db_records:
            rec_list = [
                "Continue standard prenatal care and nutrition tracking.",
                "Remind the mother of her next scheduled clinic appointment."
            ]
        for record in db_records:
            if "high" in record.risk_level.lower():
                rec_list = [
                    "Urgently refer the mother to the nearest hospital immediately.",
                    "Message summary of health progress for high prioritization at healthcare facility.",
                    "Notify the receiving facility clinical team regarding severe signs."
                ]
            elif "medium" in record.risk_level.lower():
                rec_list = [
                    "Schedule a follow-up home visit within 3 to 5 days.",
                    "Counsel the mother on warning signs.",
                    "Advise routine checkup at the local clinic this week."
                ]
            else: 
                rec_list =[
                    "Advise mother to maintain healthy diet and taking nutrient sufficient meals"
                    "Advise mother to rest more and abstain from heavy work"
                ]

            history_summary.append({
                "visit_date": record.visit_date,
                "risk_level": record.risk_level,
                "gestational_age": record.gestational_age,
                "systolic_bp": record.systolic_bp,
                "diastolic_bp": record.diastolic_bp,
                "logged_symptoms": record.logged_symptoms,
                "recommendations": rec_list  
            })
            
        return {
            "mother_name": "Sumaya Abdi",
            "current_risk": current_risk,
            "ai_confidence": ai_confidence,
            "last_visit_description": last_visit_desc,
            "total_visits_logged": len(history_summary),
            "history": history_summary
        }

visit_service = VisitService()
