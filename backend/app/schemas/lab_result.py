from datetime import date
from pydantic import BaseModel

class LabResult(BaseModel):
    record_id: str
    test_name: str
    standardized_test: str | None = None
    value: float | str | None = None
    unit: str | None = None
    reference_range: str | None = None
    abnormal_flag: str | None = None
    collection_date: date | None = None
    laboratory: str | None = None

class DuplicateRequest(BaseModel):
    labs: list[LabResult]
    window_days: int = 30
