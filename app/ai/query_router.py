from app.ai.ollama_client import generate_response


VALID_ROUTES = {
    "market_data",
    "rag",
    "general",
}


def route_query(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    prompt = f"""
You are a query router for a financial research assistant.

Classify the user's question into exactly ONE of these routes:

market_data
Use when the user asks about a publicly traded company, stock,
financial metrics, valuation, market performance, risk, profitability,
price, market cap, trend, volatility, or investment analysis.

rag
Use when the user asks about an uploaded document, PDF, report,
annual report, 10-K, or information mentioned inside a document.

general
Use for general financial concepts, explanations, definitions,
or questions that do not require company market data or documents.

Return ONLY one of these exact values:
market_data
rag
general

Do not explain your choice.

Question:
{query}
"""

    route = generate_response(prompt).strip().lower()

    if route not in VALID_ROUTES:
        return "general"

    return route