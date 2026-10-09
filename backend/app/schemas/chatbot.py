from pydantic import BaseModel, Field
from .medical_record import Citation

class ChatQuery(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    conversation_id: str | None = None
    record_ids: list[str] | None = None

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    evidence_status: str
    limitations: list[str]
    suggested_follow_ups: list[str]
    conversation_id: str

class Feedback(BaseModel):
    conversation_id: str
    helpful: bool
    comment: str | None = Field(default=None, max_length=1000)
