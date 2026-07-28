from app.core.greeting import greet_company
from app.core.research import start_research


def main():
    print("Local AI Financial Research Assistant")

    ticker = input("Enter a stock ticker (e.g. AAPL): ").strip().upper()

    if not ticker:
        print("Error: Stock ticker cannot be empty.")
        return

    research_result = start_research(ticker)

    if research_result["status"] == "error":
        print("\nResearch failed.")
        print(research_result["summary"])
        return

    message = greet_company(ticker)
    print(f"\n{message}")

    print("\nResearch status:", research_result["status"])
    print("\nSummary:")
    print(research_result["summary"])


if __name__ == "__main__":
    main()