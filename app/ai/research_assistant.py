from app.ai.query_router import route_query
from app.ai.ticker_resolver import resolve_ticker
from app.ai.ollama_client import generate_response
from app.rag.rag_answer import answer_question
from app.core.research import start_research
from app.ai.market_answer import generate_market_answer


def process_query(
    query: str,
    document_name: str | None = None,
    top_k: int = 5,
    conversation_history: list | None = None,
):
    route = route_query(
        query=query,
        conversation_history=conversation_history,
    )

    if route == "market_data":
        ticker = resolve_ticker(
            query=query,
            conversation_history=conversation_history,
        )

        research_result = start_research(ticker)

        answer = generate_market_answer(
            query=query,
            research_result=research_result,
        )

        return {
            "route": "market_data",
            "ticker": ticker,
            "answer": answer,
            "data": research_result.get("data"),
        }

    if route == "rag":
        rag_result = answer_question(
            query=query,
            top_k=top_k,
            document_name=document_name,
            conversation_history=conversation_history,
        )

        return {
            "route": "rag",
            "answer": rag_result["answer"],
            "sources": rag_result["sources"],
        }

    if route == "general":
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
You are a financial research assistant.

Answer the user's current question clearly and concisely.

The current question may be a follow-up to the previous conversation.

Use the conversation history only when necessary to understand
references such as:
- it
- this
- that
- this concept
- that ratio
- this metric

Do not invent facts from the conversation history.

Conversation History:
{history_text if history_text else "No previous conversation."}

Current Question:
{query}
"""

        answer = generate_response(prompt)

        return {
            "route": "general",
            "answer": answer,
        }

    raise ValueError(f"Unsupported route: {route}")