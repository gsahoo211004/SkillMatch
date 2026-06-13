import fitz  # pymupdf


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    Returns the full text as a string.
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes (for Streamlit file upload).
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


if __name__ == "__main__":
    # Quick test — pass your own PDF path
    import sys
    if len(sys.argv) > 1:
        text = extract_text_from_pdf(sys.argv[1])
        print(text[:500])
    else:
        print("Usage: python src/nlp/pdf_reader.py path/to/resume.pdf")