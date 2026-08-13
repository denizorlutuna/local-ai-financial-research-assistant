from pathlib import Path

from app.rag.document_loader import extract_pdf_pages
from app.rag.text_splitter import split_pages_into_chunks
from app.rag.vector_store import store_document_chunks


DOCUMENTS_DIR = Path("documents")


def index_document(pdf_path):
    print(f"\nIndexing: {pdf_path.name}")

    pages = extract_pdf_pages(pdf_path)

    print(f"Pages found: {len(pages)}")

    chunks = split_pages_into_chunks(pages)

    print(f"Chunks created: {len(chunks)}")
    print("Creating embeddings and storing chunks...")

    stored_count = store_document_chunks(
        chunks=chunks,
        document_name=pdf_path.name,
    )

    print(
        f"Stored {stored_count} chunks successfully."
    )


def main():
    pdf_files = list(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"PDF files found: {len(pdf_files)}")

    for pdf_path in pdf_files:
        index_document(pdf_path)


if __name__ == "__main__":
    main()