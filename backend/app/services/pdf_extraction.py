import fitz

def extract_pdf(data: bytes) -> list[str]:
    try:
        doc = fitz.open(stream=data, filetype="pdf")
        pages = [p.get_text("text").strip() for p in doc]
        doc.close()
        return pages
    except Exception as e:
        raise ValueError("PDF could not be safely parsed") from e
