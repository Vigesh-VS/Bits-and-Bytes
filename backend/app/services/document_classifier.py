def classify(text: str) -> str:
    lower = text.lower()
    if any(x in lower for x in ("rx", "tablet", "capsule", "prescription")): return "prescription"
    if any(x in lower for x in ("reference range", "laboratory", "specimen", "hba1c")): return "lab_report"
    if "discharge" in lower: return "discharge_summary"
    if any(x in lower for x in ("scan", "impression", "radiology")): return "scan_report"
    return "other"
