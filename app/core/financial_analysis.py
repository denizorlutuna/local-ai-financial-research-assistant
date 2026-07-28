from app.core.financial_metrics import (calculate_profit_margin, calculate_debt_ratio, calculate_cash_ratio)

ANALYSIS_THRESHOLDS = {
    "high_pe_ratio": 30,
    "near_52_week_high": 0.95,
    "strong_profit_margin": 20,
    "healthy_profit_margin": 10,
    "healthy_debt_ratio": 50,
    "strong_cash_ratio": 50,
}

def classify_market_cap(market_cap):
    if market_cap is None:
        return "Unknown"

    if market_cap >= 200_000_000_000:
        return "Mega Cap"

    if market_cap >= 10_000_000_000:
        return "Large Cap"

    if market_cap >= 2_000_000_000:
        return "Mid Cap"

    if market_cap >= 300_000_000:
        return "Small Cap"

    return "Micro Cap"

def analyze_market_cap(company):
    market_cap = company.get("market_cap")

    if market_cap is not None and market_cap >= 200_000_000_000:
        return "Global market leader"

    return None

def analyze_pe_ratio(company):
    pe_ratio = company.get("pe_ratio")

    if pe_ratio is None:
        return None

    if pe_ratio >= 35:
        return "Stock may be highly valued based on its P/E ratio"

    if pe_ratio >= 20:
        return "Stock has a relatively high P/E ratio"

    if pe_ratio >= 10:
        return "Stock has a moderate P/E ratio"

    if pe_ratio > 0:
        return "Stock has a relatively low P/E ratio"

    return "P/E ratio may indicate unusual earnings conditions"

def analyze_price_position(company):
    current_price = company.get("current_price")
    high = company.get("fifty_two_week_high")
    low = company.get("fifty_two_week_low")

    if None in (current_price, high, low):
        return None

    range_size = high - low

    if range_size <= 0:
        return None

    position = (current_price - low) / range_size

    if position >= 0.8:
        return "Stock is trading close to its 52-week high"

    if position <= 0.2:
        return "Stock is trading close to its 52-week low"

    return "Stock is trading within its normal yearly range"

def generate_company_summary(company, historical_data=None):
    summary = []

    market_cap_analysis = analyze_market_cap(company)
    if market_cap_analysis:
        summary.append(market_cap_analysis)

    pe_analysis = analyze_pe_ratio(company)
    if pe_analysis:
        summary.append(pe_analysis)

    price_position = analyze_price_position(company)
    if price_position:
        summary.append(price_position)

    sector = company.get("sector")
    current_price = company.get("current_price")

    if sector == "Technology":
        summary.append("Operates in the technology sector")

    if current_price is not None and current_price >= 100:
        summary.append("High-priced stock")

    if historical_data:
        yearly_return = calculate_price_performance(historical_data)

        if yearly_return >= 30:
            summary.append("Strong one-year price momentum")
        elif yearly_return >= 10:
            summary.append("Positive one-year price performance")
        elif yearly_return >= 0:
            summary.append("Stable one-year price performance")
        else:
            summary.append("Negative one-year price performance")

    if not summary:
        summary.append("Limited analysis available")

    return summary

def analyze_financial_health(financials):
    try:
        profit_margin = calculate_profit_margin(financials)
    except (TypeError, KeyError, ZeroDivisionError):
        profit_margin = None

    try:
        debt_ratio = calculate_debt_ratio(financials)
    except (TypeError, KeyError, ZeroDivisionError):
        debt_ratio = None

    try:
        cash_ratio = calculate_cash_ratio(financials)
    except (TypeError, KeyError, ZeroDivisionError):
        cash_ratio = None

    analysis = []

    if profit_margin is None:
        analysis.append("Profitability data is unavailable.")
    elif profit_margin >= 20:
        analysis.append("Strong profitability.")
    elif profit_margin >= 10:
        analysis.append("Moderate profitability.")
    else:
        analysis.append("Weak profitability.")

    if debt_ratio is None:
        analysis.append("Debt data is unavailable.")
    elif debt_ratio < 50:
        analysis.append("Healthy debt level.")
    else:
        analysis.append("High debt level.")

    if cash_ratio is None:
        analysis.append("Liquidity data is unavailable.")
    elif cash_ratio >= 30:
        analysis.append("Strong liquidity.")
    else:
        analysis.append("Limited liquidity.")

    return {
        "profit_margin": (
            round(profit_margin, 2) if profit_margin is not None else None
        ),
        "debt_ratio": (
            round(debt_ratio, 2) if debt_ratio is not None else None
        ),
        "cash_ratio": (
            round(cash_ratio, 2) if cash_ratio is not None else None
        ),
        "analysis": analysis,
    }

def calculate_price_performance(historical_data):
    start_price = historical_data["start_price"]
    end_price = historical_data["end_price"]

    return ((end_price - start_price) / start_price) * 100

def analyze_risks(company):
    risks = []

    pe_ratio = company.get("pe_ratio")
    current_price = company.get("current_price")
    fifty_two_week_high = company.get("fifty_two_week_high")

    if (
    pe_ratio is not None
    and pe_ratio > ANALYSIS_THRESHOLDS["high_pe_ratio"]
    ):
        risks.append("High valuation based on P/E ratio")

    if (
        current_price is not None
        and fifty_two_week_high is not None
        and current_price >= fifty_two_week_high * ANALYSIS_THRESHOLDS["near_52_week_high"]
    ):
        risks.append("Stock is trading close to its 52-week high")

    return risks