from app.ai.ollama_client import generate_response


def resolve_ticker(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    prompt = f"""
You extract stock ticker symbols from financial questions.

Return ONLY the ticker symbol.
Do not explain anything.
Do not add punctuation.

Examples:
Apple -> AAPL
Microsoft -> MSFT
NVIDIA -> NVDA
Tesla -> TSLA
Amazon -> AMZN

Question:
{query}
"""

    ticker = generate_response(prompt).strip().upper()

    if not ticker:
        raise ValueError("Unable to resolve ticker.")

    return ticker