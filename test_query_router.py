from app.ai.query_router import route_query


def main():
    queries = [
        "Is Tesla expensive right now?",
        "How risky is NVIDIA?",
        "Should I be concerned about Apple's valuation?",
        "What cybersecurity risks are discussed in this PDF?",
        "Summarize the risks mentioned in the annual report.",
        "What does P/E ratio mean?",
        "Explain diversification.",
    ]

    for query in queries:
        route = route_query(query)

        print(f"Query: {query}")
        print(f"Route: {route}")
        print("-" * 60)


if __name__ == "__main__":
    main()