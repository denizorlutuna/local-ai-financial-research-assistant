from app.core.greeting import greet_company
from app.core.research import start_research


def main():
    print("🚀 Local AI Financial Research Assistant")

    ticker = input("Enter a stock ticker (e.g. AAPL): ").strip().upper()

    message = greet_company(ticker)
    print(message)

    research_result = start_research(ticker)

    print("Research status:", research_result["status"])
    print("Summary:")
    print(research_result["summary"])


if __name__ == "__main__":
    main()