from app.rag.rag_answer import answer_question


def main():
    query = "What are Microsoft's main business risks?"

    result = answer_question(
        query=query,
        top_k=5,
        document_name="microsoft_10k_2025.pdf",
    )

    print(f"Question: {query}")

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- {source['document_name']} | "
            f"Page {source['page_number']} | "
            f"distance: {source['distance']:.4f}"
        )


if __name__ == "__main__":
    main()