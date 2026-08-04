from app.rag.embedding_client import generate_embeddings
from app.rag.vector_store import get_collection


def search_similar_chunks(
    query,
    top_k=5,
):
    if not query or not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    if top_k <= 0:
        raise ValueError(
            "top_k must be greater than zero."
        )

    collection = get_collection()

    query_embedding = generate_embeddings(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        retrieved_chunks.append(
            {
                "text": document,
                "page_number": metadata["page_number"],
                "chunk_index": metadata["chunk_index"],
                "document_name": metadata["document_name"],
                "distance": distance,
            }
        )

    return retrieved_chunks