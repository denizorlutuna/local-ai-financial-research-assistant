from pathlib import Path

from app.rag.document_loader import extract_pdf_pages
from app.rag.text_splitter import split_pages_into_chunks
from app.rag.vector_store import store_document_chunks


def index_document(file_path: str, document_name: str | None = None):
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    if document_name is None:
        document_name = pdf_path.name

    pages = extract_pdf_pages(pdf_path)

    chunks = split_pages_into_chunks(pages)

    stored_count = store_document_chunks(
        chunks=chunks,
        document_name=document_name,
    )

    return {
        "status": "completed",
        "document_name": document_name,
        "page_count": len(pages),
        "chunk_count": stored_count,
    }