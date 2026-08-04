from pathlib import Path

from app.rag.document_loader import extract_pdf_pages
from app.rag.text_splitter import split_pages_into_chunks
from app.rag.vector_store import store_document_chunks


PDF_PATH = Path("documents/sample.pdf")


def main():
    pages = extract_pdf_pages(PDF_PATH)

    print(f"Pages found: {len(pages)}")

    chunks = split_pages_into_chunks(pages)

    print(f"Chunks created: {len(chunks)}")
    print("Creating embeddings and storing chunks...")

    stored_count = store_document_chunks(
        chunks=chunks,
        document_name=PDF_PATH.name,
    )

    print(
        f"Stored {stored_count} chunks successfully."
    )


if __name__ == "__main__":
    main()