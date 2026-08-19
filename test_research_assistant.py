from app.ai.research_assistant import process_query


def main():
    query = "What is NVIDIA's current financial health?"

    result = process_query(query)

    print(f"Query: {query}")
    print(f"Route: {result['route']}")
    print(f"Ticker: {result.get('ticker')}")
    print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()