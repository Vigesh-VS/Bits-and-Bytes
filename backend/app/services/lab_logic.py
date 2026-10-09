from app.schemas.lab_result import LabResult
def duplicates(labs:list[LabResult], days:int):
    out=[]
    ordered=sorted([x for x in labs if x.collection_date],key=lambda x:x.collection_date)
    for i,a in enumerate(ordered):
        for b in ordered[i+1:]:
            same=(a.standardized_test or a.test_name).lower()==(b.standardized_test or b.test_name).lower()
            delta=(b.collection_date-a.collection_date).days
            if same and delta<=days: out.append({"earlier":a.model_dump(mode="json"),"later":b.model_dump(mode="json"),"rationale":f"Exact name match within prototype {days}-day window", "match":"exact", "limitation":"Repeated tests can be clinically necessary; never skip clinician-ordered testing."})
    return out
def trends(labs:list[LabResult], test:str|None=None):
    rows=[x for x in labs if isinstance(x.value,float) and (not test or x.test_name.lower()==test.lower())]
    return [x.model_dump(mode="json") for x in sorted(rows,key=lambda x:x.collection_date or __import__('datetime').date.min)]
