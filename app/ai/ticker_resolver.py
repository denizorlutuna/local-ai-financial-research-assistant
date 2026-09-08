from app.ai.ollama_client import generate_response


def resolve_ticker(
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
You extract stock ticker symbols from financial questions.

The current question may be a follow-up to the previous conversation.

Use the conversation history when necessary to resolve references
such as:
- it
- its
- this company
- that company
- this stock
- that stock

Return ONLY the ticker symbol.
Do not explain anything.
Do not add punctuation.

Examples:
Apple -> AAPL
Microsoft -> MSFT
NVIDIA -> NVDA
Tesla -> TSLA
Amazon -> AMZN

Conversation History:
{history_text if history_text else "No previous conversation."}

Current Question:
{query}
"""

    ticker = generate_response(prompt).strip().upper()

    if not ticker:
        raise ValueError("Unable to resolve ticker.")

    return ticker