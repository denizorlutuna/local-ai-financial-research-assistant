from app.rag.rag_answer import answer_question


def main():
    query = "What are Apple's main business risks?"

    result = answer_question(
        query=query,
        top_k=5,
    )

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