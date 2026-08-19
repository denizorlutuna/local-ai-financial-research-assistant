from app.ai.ollama_client import generate_response


def generate_market_answer(query: str, research_result: dict) -> str:
    if research_result.get("status") != "completed":
        return research_result.get(
            "summary",
            "Unable to complete market analysis.",
        )

    data = research_result["data"]

    prompt = f"""
You are a financial research assistant.

Answer the user's question using ONLY the financial data provided below.

Do not include unrelated sections.
Do not invent information.
If the requested information is unavailable, say so clearly.
Keep the answer concise but useful.

User question:
{query}

Financial data:
{data}
"""

    return generate_response(prompt)