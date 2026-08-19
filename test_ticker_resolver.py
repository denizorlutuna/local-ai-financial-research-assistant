from app.ai.ticker_resolver import resolve_ticker


def main():
    queries = [
        "What is NVIDIA's current financial health?",
        "Analyze Tesla stock.",
        "What is Apple's market cap?",
        "Tell me about MSFT valuation.",
    ]

    for query in queries:
        ticker = resolve_ticker(query)

        print(f"Query: {query}")
        print(f"Ticker: {ticker}")
        print("-" * 50)


if __name__ == "__main__":
    main()
    