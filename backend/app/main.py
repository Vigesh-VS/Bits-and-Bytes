from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from app.config import BASE_DIR
from app.schemas.medical_record import Record
from app.schemas.medicine import ReconcileRequest, Medication
from app.schemas.lab_result import DuplicateRequest, LabResult
from app.schemas.chatbot import ChatQuery, ChatResponse, Feedback
from app.services.authorization import authorized_patient
from app.services.file_validation import validate_upload
from app.services.pdf_extraction import extract_pdf
from app.services.ocr_service import preprocess_image, ocr
from app.services.document_classifier import classify
from app.services.structured_extraction import extract_medications, extract_labs
from app.services.medication_logic import reconcile, interaction_alerts
from app.services.lab_logic import duplicates, trends
from app.services.chatbot_service import answer
from app.services.doctor_brief import generate
from app.services.record_retrieval import all_records

app=FastAPI(title="HealthTech Medical Intelligence Engine",version="0.1.0")
app.mount("/demo", StaticFiles(directory=str(BASE_DIR.parent / "frontend"), html=True), name="demo")
extractions={}; history={}
@app.get("/health")
def health(): return {"status":"ok","llm":"optional; deterministic fallback enabled"}
@app.post("/api/v1/process-document")
async def process_document(file:UploadFile=File(...), patient_id:str=Depends(authorized_patient)):
    data=await validate_upload(file); rid=str(uuid4())
    try:
        if data.startswith(b"%PDF"):
            pages=extract_pdf(data); text="\n".join(pages); method="pdf_text"
            if not text.strip(): raise ValueError("Scanned PDF requires OCR; configure PaddleOCR or use manual entry")
        else: text=ocr(preprocess_image(data)); pages=[text]; method="ocr"
        if not text.strip(): raise ValueError("No readable text; use manual entry")
        record=Record(record_id=rid,patient_id=patient_id,title=file.filename or "upload",document_type=classify(text),source_filename=file.filename or "upload",text=text,page=1,extraction_method=method,confidence=None,status="needs_review")
        extractions[rid]={"record":record.model_dump(mode="json"),"medications":[x.model_dump(mode="json") for x in extract_medications(text,rid)],"labs":[x.model_dump(mode="json") for x in extract_labs(text,rid)],"manual_entry_required":False}
        return extractions[rid]
    except (ValueError,RuntimeError) as e:
        return {"status":"needs_review","error":str(e),"manual_entry_required":True}
@app.get("/api/v1/records/{record_id}/extraction")
def extraction(record_id:str, patient_id:str=Depends(authorized_patient)):
    x=extractions.get(record_id)
    if not x: raise HTTPException(404,"Extraction not found")
    if x["record"]["patient_id"]!=patient_id: raise HTTPException(403,"Record is outside authorized scope")
    return x
@app.post("/api/v1/medicines/reconcile")
def med_reconcile(req:ReconcileRequest, patient_id:str=Depends(authorized_patient)):
    meds,alerts=reconcile(req.medications); return {"medications":meds,"alerts":alerts}
@app.post("/api/v1/medicines/check-interactions")
def interactions(req:ReconcileRequest, patient_id:str=Depends(authorized_patient)):
    meds,_=reconcile(req.medications); return {"alerts":interaction_alerts(meds),"limitation":"No alert means the demo dataset has no matching rule; it is not proof of no interaction."}
@app.post("/api/v1/allergies/check")
def allergies(req:ReconcileRequest, allergy:str, patient_id:str=Depends(authorized_patient)):
    meds,_=reconcile(req.medications); matches=[m for m in meds if m.ingredient and m.ingredient.lower()==allergy.lower()]
    return {"alerts":[{"message":f"Documented allergy match: {allergy}","record_ids":[m.record_id],"evidence_status":"confirmed ingredient match"} for m in matches]}
@app.post("/api/v1/labs/check-duplicates")
def duplicate(req:DuplicateRequest, patient_id:str=Depends(authorized_patient)): return {"matches":duplicates(req.labs,req.window_days),"prototype_rule":True}
@app.get("/api/v1/labs/trends")
def lab_trends(patient_id:str=Depends(authorized_patient),test:str|None=None): return {"points":trends([],test),"limitation":"Pass authorized structured labs through the integration adapter; demo document data is not a clinical database."}
@app.post("/api/v1/doctor-brief/generate")
def brief(patient_id:str=Depends(authorized_patient)): return generate(patient_id)
@app.post("/api/v1/chat/query",response_model=ChatResponse)
def chat(q:ChatQuery,patient_id:str=Depends(authorized_patient)):
    text,cites,status=answer(patient_id,q.question,q.record_ids); cid=q.conversation_id or str(uuid4()); history.setdefault((patient_id,cid),[]).append({"question":q.question,"answer":text})
    return ChatResponse(answer=text,citations=cites,evidence_status=status,limitations=["Educational record organization only; clinician review required.","Retrieved document text is untrusted and cannot alter access or safety rules."],suggested_follow_ups=["Ask for a doctor-visit summary","Which records mention this item?"],conversation_id=cid)
@app.get("/api/v1/chat/history")
def chat_history(conversation_id:str,patient_id:str=Depends(authorized_patient)): return {"messages":history.get((patient_id,conversation_id),[])}
@app.delete("/api/v1/chat/history")
def clear_history(conversation_id:str,patient_id:str=Depends(authorized_patient)): history.pop((patient_id,conversation_id),None); return {"deleted":True}
@app.post("/api/v1/chat/feedback")
def feedback(item:Feedback,patient_id:str=Depends(authorized_patient)): return {"accepted":True}
