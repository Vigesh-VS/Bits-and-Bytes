from datetime import date
from typing import Literal
from pydantic import BaseModel

class Medication(BaseModel):
    record_id: str
    original_name: str
    ingredient: str | None = None
    brand_name: str | None = None
    strength: str | None = None
    formulation: str | None = None
    dose: str | None = None
    route: str | None = None
    frequency: str | None = None
    start_date: date | None = None
    stop_date: date | None = None
    status: Literal["active", "stopped", "replaced", "uncertain", "historical"] = "uncertain"
    match_confidence: Literal["confirmed", "uncertain", "unknown"] = "unknown"

class ReconcileRequest(BaseModel):
    medications: list[Medication]
