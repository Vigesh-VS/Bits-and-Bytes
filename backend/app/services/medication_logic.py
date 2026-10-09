import csv
from pathlib import Path
from app.config import DATA_DIR
from app.schemas.medicine import Medication
from app.schemas.alerts import Alert

def refs():
    with open(DATA_DIR / "brand_generic.csv", newline="", encoding="utf-8") as f: return list(csv.DictReader(f))
def normalize(m: Medication) -> Medication:
    name=m.original_name.lower().strip()
    for r in refs():
        if name in (r["brand"].lower(), r["ingredient"].lower()):
            return m.model_copy(update={"ingredient":r["ingredient"], "brand_name": r["brand"] if name==r["brand"].lower() else m.brand_name, "match_confidence":"confirmed"})
    return m
def reconcile(meds: list[Medication]):
    normalized=[normalize(m) for m in meds]; alerts=[]
    for i,a in enumerate(normalized):
        for b in normalized[i+1:]:
            if a.ingredient and a.ingredient == b.ingredient:
                kind="exact duplicate" if a.strength == b.strength else "possible conflicting dose"
                alerts.append(Alert(type="medication_discrepancy",severity="review",message=f"{kind}: {a.ingredient}. Confirm with clinician; no medication change is recommended.",record_ids=[a.record_id,b.record_id],evidence_status="confirmed ingredient match"))
    return normalized, alerts
def interaction_alerts(meds: list[Medication]):
    by={m.ingredient.lower():m for m in meds if m.ingredient and m.match_confidence=="confirmed"}; found=[]
    with open(DATA_DIR / "drug_interactions.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["ingredient_a"] in by and r["ingredient_b"] in by:
                found.append(Alert(type="possible_interaction",severity=r["severity"],message=r["description"],record_ids=[by[r["ingredient_a"]].record_id,by[r["ingredient_b"]].record_id],evidence_status="demo rule; clinician review required",source=r["source"]))
    return found
