"""Boundary implemented by Role 2. Demo header is deliberately not Firebase auth."""
from fastapi import Header, HTTPException

def authorized_patient(x_authorized_patient: str | None = Header(default=None)) -> str:
    # Replace this dependency with Role 2's verified Firebase-token/share-scope adapter.
    if not x_authorized_patient:
        raise HTTPException(401, "Missing trusted authorization context")
    return x_authorized_patient

def enforce_scope(patient_id: str, allowed_patient: str) -> None:
    if patient_id != allowed_patient:
        raise HTTPException(403, "Record is outside authorized scope")
