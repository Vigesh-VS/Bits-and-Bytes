# HealthTech Medical Intelligence Engine 🩺

A local-first FastAPI service designed for **synthetic demo medical-record organization and intelligence**. This system acts as a smart engine to parse medical documents, reconcile medications, analyze lab results, and provide intelligent assistance through a conversational interface.

> **Disclaimer:** This is a demonstration prototype. It is not a diagnostic, prescribing, or emergency service. All data processed must be synthetic demo data.

---

## 🌟 Key Features

### 1. Intelligent Document Processing
*   **PDF Extraction**: Accurately extracts textual information from digital PDFs (via `PyMuPDF` and `pdfplumber`).
*   **Image & Scanned Document OCR**: Fallback processing for images and scanned documents using integrated `PaddleOCR` and `OpenCV` preprocessing.
*   **Automated Data Structuring**: Automatically extracts medications and lab results from raw text using NLP rule-matching.
*   **Document Classification**: Intelligently classifies uploaded records based on their textual content.

### 2. Medication Management & Safety
*   **Medicines Reconciliation**: Deduplicates and organizes medications across multiple uploaded medical records.
*   **Drug-Drug Interaction Checking**: Cross-references medications against a synthetic database to flag potential interactions and safety alerts.
*   **Allergy Matcher**: Actively scans extracted medication ingredients against a patient's documented allergies to prevent adverse events.

### 3. Lab Result Analytics
*   **Duplicate Detection**: Identifies overlapping or duplicate lab tests within customizable time windows (e.g., repeating the same blood test within 3 days).
*   **Trend Analysis**: Aggregates lab data over time to visualize patient health trends for specific metrics.

### 4. Clinician Support Tools
*   **Doctor Brief Generation**: Generates a secure, structured patient summary aggregating recent documents, medications, and active alerts to save clinicians time during chart review.

### 5. Conversational AI (Chatbot)
*   **Patient Query Engine**: A deterministic conversational interface allowing patients to ask questions about their own records (e.g., *"What is my HbA1c?"*).
*   **Evidence-Based Retrieval**: Answers are strictly backed by document citations with source record IDs to prevent hallucinations.
*   **Chat History & Feedback**: Maintains session history and accepts feedback on responses for future fine-tuning.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   *(Optional)* PaddleOCR for image/scanned PDF processing

### Run Locally (Windows)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run Locally (Linux/macOS)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Accessing the App
*   **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **Tests:** Run `pytest -q` to execute the core logic test suite.

---

## 🔒 Security & Firebase Integration Boundary

All protected endpoints require an authorization dependency. Currently, `X-Authorized-Patient` is used as an intentionally insecure **demo-only stand-in**. 

**For Production / Role 2 Implementation:**
You must replace `app/services/authorization.py` with an adapter that verifies **Firebase ID tokens** server-side. The service must resolve a short-lived, unexpired, non-revoked record/share scope. The browser must never choose the patient scope directly.

**Example Secure Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/query \
  -H "X-Authorized-Patient: demo-patient-001" \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is my HbA1c?\"}"
```

---

## ⚠️ Data & Limitations
All files under `app/data/` (like CSV drug mappings and JSON records) are fictional synthetic demo datasets. They are **not comprehensive clinical references**. An absent alert in the demo dataset never proves the absence of a real-life medical interaction. **Do not upload real patient data to this demo.**
