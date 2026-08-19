from app.rag.document_indexer import index_document


def main():
    file_path = "documents/apple_10k_2025.pdf"

    result = index_document(file_path)

    print(f"Status: {result['status']}")
    print(f"Document: {result['document_name']}")
    print(f"Pages: {result['page_count']}")
    print(f"Chunks: {result['chunk_count']}")


if __name__ == "__main__":
    main()
