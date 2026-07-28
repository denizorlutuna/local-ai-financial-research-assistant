from app.core.financial_analysis import ANALYSIS_THRESHOLDS

def generate_investment_outlook(company, financial_health, market_risks):
    """
    Generates an overall investment outlook based on
    company information, financial health, and market risks.
    """

    strengths = []
    risks = list(market_risks)
    score = 0

    # Profitability
    if (
    financial_health["profit_margin"]
    > ANALYSIS_THRESHOLDS["strong_profit_margin"]
    ):
        strengths.append("Strong profitability")
        score += 2
    elif (
    financial_health["profit_margin"]
    > ANALYSIS_THRESHOLDS["healthy_profit_margin"]
    ):
        strengths.append("Healthy profitability")
        score += 1
    else:
        risks.append("Low profitability")
        score -= 2

    # Debt
    if (
    financial_health["debt_ratio"]
    < ANALYSIS_THRESHOLDS["healthy_debt_ratio"]
    ):
        strengths.append("Healthy debt level")
        score += 1
    else:
        risks.append("High debt level")
        score -= 1

    # Liquidity
    if (
    financial_health["cash_ratio"]
    > ANALYSIS_THRESHOLDS["strong_cash_ratio"]
    ):
        strengths.append("Strong liquidity")
        score += 1
    else:
        risks.append("Weak liquidity")
        score -= 1

    # Market risks reduce the score
    score -= len(market_risks)

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