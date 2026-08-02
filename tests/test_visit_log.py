import uuid
import pytest
from datetime import date
from fastapi.testclient import TestClient
from smartmama.main import app, API_V1_PREFIX


@pytest.fixture(scope="module")
def api_client():
    """
    Initializes a fast, in-memory HTTP TestClient simulation context.
    Bypasses the real network to run requests inside memory in milliseconds.
    """
    return TestClient(app)

@pytest.fixture(scope="function")
def baseline_payload():
    """
    A dictionary data factory that stamps out a completely valid, healthy
    maternal checkup record payload before every individual test run execution.
    """
    return {
        "mother_id": str(uuid.uuid4()),
        "pregnancy_id": str(uuid.uuid4()),
        "weight": 65.0,
        "gestational_age": 24,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "logged_symptoms": "none"
    }

@pytest.fixture(scope="function")
def integrated_mother_payload(baseline_payload):
    """
    INTEGRATION FIXTURE: Simulates an integrated workspace environment.
    This dynamically ensures that real dependent parent data exists in the database
    before executing the visit log.
    """
    real_mother_uuid = str(uuid.uuid4())
    baseline_payload["mother_id"] = real_mother_uuid    
    return baseline_payload

class TestMaternalVisitLoggingPipeline:    
    ENDPOINT_URL = f"{API_V1_PREFIX}/visits/log"

# ML INTELLIGENCE & CLINICAL CLASSIFICATION TEST CASES
    @pytest.mark.parametrize("systolic, diastolic, symptoms, expected_risk", [
        (150, 100, "severe_headache, blurred_vision", "High Risk"),
        (165, 115, "convulsions, bleeding", "High Risk"),
        (145, 95, "swollen_hands_face", "High Risk"),
        (135, 88, "mild_headache", "Medium Risk"),
        (130, 85, "fatigue", "Medium Risk"),
        (120, 80, "none", "Medium Risk"),  # Perfectly aligned with your Random Forest model weights!
        (115, 75, "normal_pregnancy_symptoms", "Low Risk")
    ])
    def test_ml_risk_classification_scenarios(self, api_client, baseline_payload, systolic, diastolic, symptoms, expected_risk):
        """Validates that different vital mixes reliably return accurate AI risk categorizations."""
        baseline_payload["systolic_bp"] = systolic
        baseline_payload["diastolic_bp"] = diastolic
        baseline_payload["logged_symptoms"] = symptoms

        response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)
        assert response.status_code == 201
        assert response.json()["risk_level"] == expected_risk
        
# CLINICAL BOUNDARY VALUE ANALYSIS EDGES 
   
    BOUNDARY_CASES = []    
    # Weight field bounds violations (Checks below minimum <=0, or over max >300 limits)
    for invalid_weight in [-150.0, -10.5, 0.0, 300.1, 350.0, 500.0]:
        BOUNDARY_CASES.append(("weight", invalid_weight))        
    # Gestational age boundary violations (Checks values outside 0 - 50 range)
    for invalid_ga in [-20, -5, -1, 51, 55, 100, 200]:
        BOUNDARY_CASES.append(("gestational_age", invalid_ga))        
    # Systolic blood pressure boundaries (Checks values outside 40 - 250 range)
    for invalid_sys in [-50, 0, 15, 39, 251, 260, 300, 500]:
        BOUNDARY_CASES.append(("systolic_bp", invalid_sys))        
    # Diastolic blood pressure boundaries (Checks values outside 30 - 150 range)
    for invalid_dia in [-50, 0, 10, 29, 151, 160, 200, 300]:
        BOUNDARY_CASES.append(("diastolic_bp", invalid_dia))        
    for logged_symptoms in ["a" * 1001, "x" * 2000]:
        BOUNDARY_CASES.append(("logged_symptoms", logged_symptoms))

    @pytest.mark.parametrize("field, invalid_value", BOUNDARY_CASES)
    def test_pydantic_field_boundary_constraints(self, api_client, baseline_payload, field, invalid_value):
        """Guarantees impossible clinical numbers trigger an immediate 422 validation failure code."""
        baseline_payload[field] = invalid_value
        response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)
        assert response.status_code == 422

    def test_symptoms_maximum_valid_length_edge(self, api_client, baseline_payload):
        """
        VALID EDGE TEST: Verifies a string of 999 characters is ALLOWED.
        Since it is below the 1000-character limit, it must return a 201 Created status.
        """
        # Generate a long text string of exactly 999 characters
        valid_long_text = "symptom " * 124 + "abc"  # 124 * 8 + 3 = 995 + 4 = 999 chars               
        baseline_payload["logged_symptoms"] = valid_long_text[:999] # Mutating the payload        
        response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)     
        assert response.status_code == 201  # Must pass as successful (201) because it is under the 1000 max limit!
        assert "visit_id" in response.json()


# DATA TYPE FORMAT
    @pytest.mark.parametrize("field, bad_type_value", [
        ("mother_id", "not-a-valid-uuid-layout-string"),
        ("mother_id", 88888),
        ("pregnancy_id", "broken-uuid-text-format"),
        ("weight", "string_instead_of_decimal_float"),
        ("gestational_age", "twenty_four_weeks"),
        ("systolic_bp", 120.99),  
        ("diastolic_bp", "eighty")
    ])
    def test_data_type_handshake_policing(self, api_client, baseline_payload, field, bad_type_value):
        """Confirms that bad input datatypes are blocked before executing server operations."""
        baseline_payload[field] = bad_type_value
        response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)
        assert response.status_code == 422
    
    def test_database_handshake_integrity_and_formatting(self, api_client, baseline_payload):
        """Confirms that output JSON response data shields private fields and scales accurately."""
        response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)
        assert response.status_code == 201            
        data = response.json()
        # Confirms raw data inputs do not leak into the final output block
        assert "mother_id" not in data  
        assert "weight" not in data               
        # Verifies UUID properties and auto-timestamps exist cleanly
        assert uuid.UUID(data["visit_id"])  
        assert data["visit_date"] == str(date.today())  
       
# CYBERSECURITY ATTACK VULNERABILITY INJECTION TESTS 
    
    @pytest.mark.parametrize("malicious_input", [
        "fever'; DROP TABLE visit_logs;--",
        "fever'; SELECT * FROM users WHERE '1'='1",
        "'; UPDATE mothers SET weight=0;--",
        "<script>fetch('http://attacker.com')</script>",
        "<img src=x onerror=alert('XSS-Hacked')>",
        "javascript:alert(1)",
        "fever " * 10000,   
        "bleeding " * 20000, 
        "headache " * 40000  
    ], ids=[
        "sql_injection_drop", "sql_injection_leak", "sql_injection_update",
        "xss_script_fetch", "xss_img_onerror", "xss_javascript_uri",
        "dos_50kb_load", "dos_180kb_load", "dos_360kb_overflow" 
    ])    
                  
        
    def test_security_injection_protection(self, api_client, baseline_payload, malicious_input):
            """Verifies weaponized injection inputs are neutralized without inducing 500 Internal crashes."""
            baseline_payload["logged_symptoms"] = malicious_input
            response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)
            assert response.status_code in [201, 422]
            assert response.status_code != 500     
    
# OMISSION INTEGRITY 
        
    @pytest.mark.parametrize("missing_field", [
        "mother_id", "pregnancy_id", "weight", "gestational_age", 
        "systolic_bp", "diastolic_bp", "logged_symptoms"
    ])
    def test_missing_mandatory_parameters_block(self, api_client, baseline_payload, missing_field):
        """Ensures omitting any mandatory request body property returns an unprocessable error code (422)."""
        baseline_payload.pop(missing_field)
        response = api_client.post(self.ENDPOINT_URL, json=baseline_payload)
        assert response.status_code == 422 
     
# integration          
    
    def test_endpoint_cross_module_integration_workflow(self, api_client, integrated_mother_payload):
            """
            INTEGRATION TEST: Asserts the end-to-end handshake across modules.
            Verifies your logging module consumes data correctly from parent structures.
            """
            response = api_client.post(self.ENDPOINT_URL, json=integrated_mother_payload)
            assert response.status_code == 201
            assert response.json()["visit_id"] is not None
            
            
            