import io
import numpy as np
from PIL import Image, ImageOps, ImageFilter

def preprocess_image(data: bytes) -> bytes:
    try:
        image = Image.open(io.BytesIO(data)).convert("L")
        image = ImageOps.autocontrast(image).filter(ImageFilter.SHARPEN)
        out = io.BytesIO(); image.save(out, "PNG"); return out.getvalue()
    except Exception as e:
        raise ValueError("Image is corrupt or unreadable; use manual entry") from e

def ocr(data: bytes) -> str:
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        raise RuntimeError("OCR is unavailable. Install PaddleOCR or use manual entry.")
    image = np.array(Image.open(io.BytesIO(data)).convert("RGB"))
    result = PaddleOCR(lang="en", use_angle_cls=True).ocr(image, cls=True)
    lines = result[0] if result else []
    return "\n".join(line[1][0] for line in lines if line and len(line) > 1)
