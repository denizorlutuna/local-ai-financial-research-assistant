from app.rag.vector_store import get_collection


def main():
    collection = get_collection()

    results = collection.get(
        include=["metadatas"]
    )

    document_names = set()

    for metadata in results["metadatas"]:
        document_names.add(
            metadata["document_name"]
        )

    print("Documents in vector store:")

    for document_name in document_names:
        print(f"- {document_name}")


if __name__ == "__main__":
    main()