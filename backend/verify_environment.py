"""Read-only preflight for optional local AI dependencies."""
import importlib.util
import json
import os
import shutil
import urllib.request

def available(module): return importlib.util.find_spec(module) is not None
result = {
    "paddleocr_installed": available("paddleocr"),
    "pymupdf_installed": available("fitz"),
    "opencv_installed": available("cv2"),
    "ollama_cli": bool(shutil.which("ollama")),
    "ollama_server": False,
    "ollama_models": [],
}
try:
    with urllib.request.urlopen(os.getenv("OLLAMA_URL", "http://localhost:11434") + "/api/tags", timeout=2) as response:
        result["ollama_server"] = response.status == 200
        result["ollama_models"] = [m["name"] for m in json.load(response).get("models", [])]
except Exception:
    pass
print(json.dumps(result, indent=2))
