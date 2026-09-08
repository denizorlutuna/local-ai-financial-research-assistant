from app.ai.ollama_client import generate_response


VALID_ROUTES = {
    "market_data",
    "rag",
    "general",
}


def route_query(
    query: str,
    conversation_history: list | None = None,
) -> str:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    history_text = ""

    if conversation_history:
        recent_messages = conversation_history[-6:]

        history_parts = []

        for message in recent_messages:
            role = message.get("role", "unknown")
            content = message.get("content", "")

            history_parts.append(
                f"{role}: {content}"
            )

        history_text = "\n".join(history_parts)

    prompt = f"""
You are a query router for a financial research assistant.

Classify the user's current question into exactly ONE of these routes:

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

The current question may be a follow-up to the previous conversation.

Use the conversation history only when necessary to understand
references such as:
- it
- its
- this company
- that stock
- this report
- the document

Return ONLY one of these exact values:
market_data
rag
general

Do not explain your choice.

Conversation History:
{history_text if history_text else "No previous conversation."}

Current Question:
{query}
"""

    route = generate_response(prompt).strip().lower()

    if route not in VALID_ROUTES:
        return "general"

    return route