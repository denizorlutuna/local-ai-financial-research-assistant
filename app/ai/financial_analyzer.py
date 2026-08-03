from app.ai.ollama_client import generate_response


def generate_ai_financial_analysis(base_summary):
    prompt = f"""
You are a financial research assistant.

Use only the report below.

Your task is not to repeat the report.
Interpret the relationship between profitability, liquidity,
valuation, price momentum, volatility, and market risk.
Do not infer the investor's time horizon or personal profile.
If investor suitability cannot be determined from the report, say so explicitly.

Write these sections:

Overall Assessment:
Financial Strengths:
Key Risks:
Investor Suitability:
Final View:

Keep the answer under 220 words.
Do not invent information.
Do not give guaranteed investment advice.

Financial Report:
{base_summary}
"""

    return generate_response(prompt)