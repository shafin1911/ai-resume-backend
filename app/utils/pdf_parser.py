import fitz  # PyMuPDF
import pdfplumber


def extract_text_pymupdf(pdf_path: str) -> str:
    """Extract text from a PDF using PyMuPDF"""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text


def extract_text_pdfplumber(pdf_path: str) -> str:
    """Extract text from a PDF using pdfplumber"""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(
            [page.extract_text() for page in pdf.pages if page.extract_text()]
        )
    return text


def parse_experience(text: str) -> str:
    """Extract and format relevant experience from the parsed text"""
    lines = text.split("\n")
    experience_lines = [
        line
        for line in lines
        # if "experience" in line.lower() or "work history" in line.lower()
    ]
    return "\n".join(experience_lines)


def extract_experience_from_pdf(pdf_path: str) -> str:
    """Extract structured experience from a PDF resume"""
    text = extract_text_pymupdf(pdf_path) or extract_text_pdfplumber(pdf_path)
    return parse_experience(text)
