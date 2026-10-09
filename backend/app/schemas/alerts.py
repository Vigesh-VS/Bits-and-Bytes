from pydantic import BaseModel

class Alert(BaseModel):
    type: str
    severity: str
    message: str
    record_ids: list[str]
    evidence_status: str
    source: str | None = None
