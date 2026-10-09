# HealthTech Medical Intelligence Engine

Local-first FastAPI service for **synthetic demo medical-record organization**. It is not a diagnostic, prescribing, or emergency service.

## Run

Windows: `cd backend; py -3.11 -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt; uvicorn app.main:app --reload`

Linux/macOS: `cd backend && python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload`

Run tests: `pytest -q`. Interactive API docs: `http://127.0.0.1:8000/docs`.

## Firebase integration boundary

All protected endpoints require an authorization dependency. `X-Authorized-Patient` is an intentionally insecure **demo-only stand-in**. Role 2 must replace `app/services/authorization.py` with an adapter that verifies Firebase ID tokens server-side and resolves a short-lived, unexpired, non-revoked record/share scope. The browser must never choose the patient scope. The service accepts bytes only after that trusted layer authorizes Storage access; it creates no public links and stores no unrestricted original documents.

Example query:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/query -H "X-Authorized-Patient: demo-patient-001" -H "Content-Type: application/json" -d "{\"question\":\"What is my HbA1c?\"}"
```

The OpenAPI page provides typed JSON examples for every endpoint. The document endpoint accepts multipart `file`; failures return `needs_review` and a manual-entry fallback. PDFs use embedded-text extraction first. OCR is optional: install PaddleOCR separately (`pip install paddleocr`) and download its models; without it image/scanned-PDF OCR returns an explicit fallback state. Ollama is intentionally optional; this MVP's chat fallback is deterministic evidence retrieval. If added, its output must be schema/citation validated before display.

## Data and limitations

All files under `app/data/` are fictional synthetic demo data. CSV drug mappings/rules and lab ranges are small, traceable demonstration datasets—not comprehensive clinical references. An absent alert never proves absence of an interaction. Report-specific lab ranges take priority. Potential duplicates are prototype matching rules, not advice to skip tests. Do not upload real patient data to this demo.

## API contract

Endpoints: `/health`, `/api/v1/process-document`, `/api/v1/records/{record_id}/extraction`, medicines reconciliation/interactions, allergies, lab duplicate/trends, doctor brief, and chat query/history/feedback. Responses include source record IDs and citations where facts are returned. See `/docs` for generated request/response schemas.
