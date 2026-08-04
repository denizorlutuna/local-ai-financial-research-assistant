from pathlib import Path

import chromadb

from app.rag.embedding_client import generate_embeddings


VECTOR_DB_PATH = Path("data/vector_store")
COLLECTION_NAME = "financial_documents"


def get_collection():
    VECTOR_DB_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_PATH)
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine",
        },
    )


def store_document_chunks(
    chunks,
    document_name,
):
    if not chunks:
        raise ValueError(
            "No chunks were provided."
        )

    collection = get_collection()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    ids = []
    metadata = []

    safe_document_name = (
        document_name
        .replace(" ", "_")
        .replace("/", "_")
    )

    for index, chunk in enumerate(chunks):
        ids.append(
            f"{safe_document_name}-{index}"
        )

        metadata.append(
            {
                "document_name": document_name,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadata,
    )

    return len(chunks)