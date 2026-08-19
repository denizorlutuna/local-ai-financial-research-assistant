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
):
    route = route_query(query)

    if route == "market_data":
        ticker = resolve_ticker(query)

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
        )

        return {
            "route": "rag",
            "answer": rag_result["answer"],
            "sources": rag_result["sources"],
        }

    if route == "general":
        prompt = f"""
You are a financial research assistant.

Answer the following question clearly and concisely.

Question:
{query}
"""

        answer = generate_response(prompt)

        return {
            "route": "general",
            "answer": answer,
        }

    raise ValueError(f"Unsupported route: {route}")