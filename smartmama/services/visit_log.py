import os # For Random Forest model
import joblib  # For Random Forest model 
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from smartmama.repositories.visit_log_repo import VisitRepository
from smartmama.schemas.visit_log import VisitLogCreate
from smartmama.models.visit_log import VisitLog

class VisitService:
  
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "maternal_risk_model.joblib")
    
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None

    @classmethod
    def process_and_log_visit(cls, db: Session, obj_in: VisitLogCreate) -> dict: #type hinting
        """ Processes input data to calculate risk status of a mother."""
        clean_symptoms = obj_in.logged_symptoms.lower()
       #random forest logic
        if cls.model is not None:
            checklist = ["fever", "headache", "swollen feet", "blurred vision", "severe_bleeding"]
            symptom_features = [1 if sym in clean_symptoms else 0 for sym in checklist]

            ml_input_features = [[
                obj_in.weight,
                obj_in.gestational_age,
                obj_in.systolic_bp,
                obj_in.diastolic_bp,
                *symptom_features
            ]]

            prediction = cls.model.predict(ml_input_features)
            risk_level = str(prediction[0]) 
        else:
           #hardcoded engine
            has_severe_symptom = "severe_bleeding" in clean_symptoms or "blurred vision" in clean_symptoms
            has_moderate_symptom = "fever" in clean_symptoms or "headache" in clean_symptoms or "swollen feet" in clean_symptoms
            #high risk logic
            if (
                obj_in.systolic_bp >= 140 or 
                obj_in.diastolic_bp >= 90 or 
                has_severe_symptom or 
                (obj_in.gestational_age >= 40 and has_moderate_symptom)
            ):
                risk_level = "High Risk"

            # medium risk logic
            elif (
                (130 <= obj_in.systolic_bp < 140) or 
                (80 <= obj_in.diastolic_bp < 90) or 
                has_moderate_symptom or
                (obj_in.weight > 100.0)  
            ):
                risk_level = "Medium Risk"

            # low risk logic
            else:
                risk_level = "Low Risk"

        db_record = VisitRepository.create_visit_log(db, obj_in)
        recommendations = []
        if "high" in risk_level.lower():
                            recommendations = [
                                "URGENT: Refer the mother to the nearest hospital immediately.",
                                "Advise emergency transport and accompany the mother if possible.",
                                "Message summary of health progress for high prioritization at healthcare facility"
                                "Notify the receiving facility clinical team regarding severe signs."
                            ]
        elif "medium" in risk_level.lower():
                            recommendations = [
                                "Schedule a follow-up home visit within 3 to 5 days.",
                                "Counsel the mother on warning signs",
                                "Advise routine checkup at the local clinic this week."
                            ]
        else:
                            recommendations = [
                                "Continue standard prenatal care and nutrition tracking.",
                                "Remind the mother of her next scheduled clinic appointment."
                            ]
                
                      #display the following to the CHV
        return {
                            "visit_id": db_record.visit_id,
                            "visit_date": db_record.visit_date,
                            "risk_level": risk_level,
                            "recommendations": recommendations
                        }
                       

                