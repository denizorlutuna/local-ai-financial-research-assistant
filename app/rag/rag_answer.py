from app.rag.retriever import search_similar_chunks

def answer_question(query, top_k=5):
    results = search_similar_chunks(query, top_k=top_k)
    
    if not results:
        return {
            "answer": "No relevant information was found.",
            "sources": [],
        }

    context_parts = []

    for result in results:
        context_parts.append(result["text"])

    context = "\n\n".join(context_parts)

    answer = (
        "Relevant information found in the document:\n\n"
        f"{context}"
    )

    sources = []

    for result in results:
        sources.append(
            {
                "page_number": result["page_number"],
                "distance": result["distance"],
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }


def main():
    query = "What are Apple's main business risks?"

    result = answer_question(query)

    print(f"Question: {query}")
    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- Page {source['page_number']}, "
            f"distance: {source['distance']:.4f}"
        )


if __name__ == "__main__":
    main()