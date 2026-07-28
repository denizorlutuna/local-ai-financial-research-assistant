def generate_investment_outlook(company, financial_health):
    """
    Generates an overall investment outlook based on
    company information and financial health.
    """

    strengths = []
    risks = []
    score = 0

        # Profitability
    if financial_health["profit_margin"] > 20:
        strengths.append("Strong profitability")
        score += 2
    elif financial_health["profit_margin"] > 10:
        strengths.append("Healthy profitability")
        score += 1
    else:
        risks.append("Low profitability")
        score -= 2

    # Debt
    if financial_health["debt_ratio"] < 50:
        strengths.append("Healthy debt level")
        score += 1
    else:
        risks.append("High debt level")
        score -= 1

    # Liquidity
    if financial_health["cash_ratio"] > 50:
        strengths.append("Strong liquidity")
        score += 1
    else:
        risks.append("Weak liquidity")
        score -= 1

        # Recommendation
    if score >= 4:
        recommendation = "Buy"
    elif score >= 1:
        recommendation = "Hold"
    else:
        recommendation = "Sell"

    return {
        "strengths": strengths,
        "risks": risks,
        "score": score,
        "recommendation": recommendation,
        "summary": ""
    }