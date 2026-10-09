from datetime import date
from typing import Literal
from pydantic import BaseModel, Field

DocumentType = Literal["prescription", "lab_report", "discharge_summary", "scan_report", "other"]
Status = Literal["pending", "processing", "needs_review", "completed", "failed"]

class Citation(BaseModel):
    record_id: str
    title: str
    record_date: date | None = None
    page: int | None = None
    excerpt: str
    extraction_method: str = "structured"

class Record(BaseModel):
    record_id: str
    patient_id: str
    title: str
    document_type: DocumentType
    document_date: date | None = None
    source_filename: str
    text: str = ""
    page: int | None = None
    status: Status = "completed"
    extraction_method: str = "manual"
    confidence: float | None = Field(default=None, ge=0, le=1)
