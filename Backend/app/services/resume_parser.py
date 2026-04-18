import pymupdf


def parse_pdf(file_bytes: bytes) -> dict:
    """Extract text and metadata from a PDF resume using PyMuPDF."""
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")

    pages = []
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({
            "page_number": page_num + 1,
            "text": text.strip(),
        })
        full_text += text + "\n"

    metadata = doc.metadata
    doc.close()

    return {
        "total_pages": len(pages),
        "metadata": {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
        },
        "pages": pages,
        "full_text": full_text.strip(),
    }


def parse_docx(file_bytes: bytes) -> dict:
    """Extract text from a DOCX resume using PyMuPDF."""
    doc = pymupdf.open(stream=file_bytes, filetype="docx")

    pages = []
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({
            "page_number": page_num + 1,
            "text": text.strip(),
        })
        full_text += text + "\n"

    doc.close()

    return {
        "total_pages": len(pages),
        "metadata": {},
        "pages": pages,
        "full_text": full_text.strip(),
    }
