import json
from app.config import DATA_DIR
from app.schemas.medical_record import Record, Citation

def all_records(): return [Record(**x) for x in json.loads((DATA_DIR / "synthetic_records.json").read_text())]
def retrieve(patient_id:str, question:str, ids:list[str]|None=None):
    terms={x.lower() for x in question.replace("?", "").split() if len(x)>2}
    records=[r for r in all_records() if r.patient_id==patient_id and (not ids or r.record_id in ids)]
    ranked=sorted(records,key=lambda r:sum(t in (r.title+' '+r.text).lower() for t in terms),reverse=True)
    return [r for r in ranked if sum(t in (r.title+' '+r.text).lower() for t in terms)][:5]
def citations(records):
    return [Citation(record_id=r.record_id,title=r.title,record_date=r.document_date,page=r.page,excerpt=r.text[:180],extraction_method=r.extraction_method) for r in records]
