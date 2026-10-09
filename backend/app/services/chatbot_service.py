from app.services.record_retrieval import retrieve, citations
URGENT=("chest pain","trouble breathing","suicide","unconscious","stroke")
def answer(patient_id, question, ids=None):
    if any(x in question.lower() for x in URGENT):
        return "Possible urgent symptoms were mentioned. Seek local emergency services now or contact a qualified clinician immediately; this tool cannot assess an emergency.", [], "safety escalation"
    rs=retrieve(patient_id,question,ids)
    if not rs: return "I could not find an authorized record that supports an answer to that question.", [], "no supporting evidence"
    evidence=" ".join(f"{r.title} ({r.document_date or 'date unavailable'}): {r.text[:350]}" for r in rs)
    return "Based on the retrieved authorized records: "+evidence, citations(rs), "retrieved structured/document evidence; OCR text may need review"
