from datetime import date
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.medicine import Medication
from app.schemas.lab_result import LabResult
from app.services.medication_logic import reconcile, interaction_alerts
from app.services.lab_logic import duplicates

def test_brand_duplicate_and_interaction():
    meds,_=reconcile([Medication(record_id="a",original_name="Glucophage",strength="500 mg"),Medication(record_id="b",original_name="metformin",strength="500 mg")])
    assert meds[0].ingredient=="metformin"
    meds,_=reconcile([Medication(record_id="a",original_name="Prinivil"),Medication(record_id="b",original_name="Advil")])
    assert interaction_alerts(meds)
def test_duplicate_window():
    labs=[LabResult(record_id="a",test_name="HbA1c",value=7.0,collection_date=date(2025,1,1)),LabResult(record_id="b",test_name="HbA1c",value=7.2,collection_date=date(2025,1,20))]
    assert len(duplicates(labs,30))==1 and not duplicates(labs,10)
def test_chat_scope_and_no_evidence():
    c=TestClient(app); h={"X-Authorized-Patient":"demo-patient-001"}
    r=c.post("/api/v1/chat/query",headers=h,json={"question":"What is my HbA1c?"}); assert r.status_code==200 and r.json()["citations"]
    r=c.post("/api/v1/chat/query",headers=h,json={"question":"Tell me about unrelated surgery"}); assert r.json()["evidence_status"]=="no supporting evidence"
def test_auth_required(): assert TestClient(app).get("/api/v1/chat/history?conversation_id=x").status_code==401
