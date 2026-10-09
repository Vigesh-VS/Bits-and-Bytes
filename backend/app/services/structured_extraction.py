import re
from app.schemas.medicine import Medication
from app.schemas.lab_result import LabResult

MEDS = re.compile(r"(?im)^\s*(?:rx[:\s]*)?([A-Za-z][A-Za-z0-9 -]{2,40})\s+(\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml))\s*(?:[-–]\s*)?([^\n]*)")
LABS = re.compile(r"(?im)^\s*([A-Za-z][A-Za-z0-9 ()/%-]{2,50})\s*[:=]\s*(\d+(?:\.\d+)?)\s*([A-Za-z/%]+)?")

def extract_medications(text: str, record_id: str) -> list[Medication]:
    return [Medication(record_id=record_id, original_name=n.strip(), strength=s.strip(), frequency=f.strip() or None,
                       status="uncertain", match_confidence="unknown") for n,s,f in MEDS.findall(text)]
def extract_labs(text: str, record_id: str) -> list[LabResult]:
    return [LabResult(record_id=record_id, test_name=n.strip(), value=float(v), unit=u or None) for n,v,u in LABS.findall(text)]
