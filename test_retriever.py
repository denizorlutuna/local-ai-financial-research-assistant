from app.rag.retriever import search_similar_chunks


def main():
    query = "What are Apple's main business risks?"

    results = search_similar_chunks(
        query=query,
        top_k=5,
    )

    print(f"Query: {query}")
    print(f"Results found: {len(results)}")

    for index, result in enumerate(
        results,
        start=1,
    ):
        print("\n" + "=" * 60)
        print(f"Result {index}")
        print(f"Page: {result['page_number']}")
        print(f"Chunk: {result['chunk_index']}")
        print(f"Distance: {result['distance']}")
        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()