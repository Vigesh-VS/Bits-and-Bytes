from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.config import MAX_UPLOAD_BYTES

ALLOWED = {"application/pdf", "image/png", "image/jpeg"}
MAGIC = {b"%PDF": "application/pdf", b"\x89PNG": "image/png", b"\xff\xd8\xff": "image/jpeg"}

async def validate_upload(file: UploadFile) -> bytes:
    payload = await file.read()
    if not payload or len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(422, "File is empty or exceeds configured size limit")
    actual = next((kind for magic, kind in MAGIC.items() if payload.startswith(magic)), None)
    if actual not in ALLOWED:
        raise HTTPException(415, "Only valid PDF, PNG, and JPEG documents are supported")
    return payload
