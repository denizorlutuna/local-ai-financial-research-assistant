from pathlib import Path

from pypdf import PdfReader


def extract_pdf_pages(file_path):
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    if not pages:
        raise ValueError(
            "No readable text was found in the PDF."
        )

    return pages