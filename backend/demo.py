"""Quick offline synthetic demonstration: run API first, then python demo.py."""
import json, urllib.request
request=urllib.request.Request("http://127.0.0.1:8000/api/v1/chat/query",data=json.dumps({"question":"What is my HbA1c?"}).encode(),headers={"Content-Type":"application/json","X-Authorized-Patient":"demo-patient-001"},method="POST")
print(urllib.request.urlopen(request).read().decode())
