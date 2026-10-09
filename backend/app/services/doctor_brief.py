from app.services.record_retrieval import all_records
def generate(patient_id):
    rs=sorted([r for r in all_records() if r.patient_id==patient_id],key=lambda r:r.document_date or __import__('datetime').date.min,reverse=True)
    return {"title":"Doctor Brief — review aid only", "patient_scope":patient_id, "summary":"Synthetic-record summary generated from authorized documents. Confirm all details against originals.", "records":[{"title":r.title,"date":str(r.document_date) if r.document_date else None,"type":r.document_type,"source":r.source_filename} for r in rs], "uncertainties":["OCR/extracted fields require patient or clinician confirmation.","This brief does not diagnose or recommend treatment."]}
