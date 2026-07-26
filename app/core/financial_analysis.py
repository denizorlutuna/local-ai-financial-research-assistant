from app.core.financial_metrics import (calculate_profit_margin, calculate_debt_ratio, calculate_cash_ratio)


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

def generate_company_summary(company):
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

    if not summary:
        summary.append("Limited analysis available")

    return summary

def analyze_financial_health(financials):
    profit_margin = calculate_profit_margin(financials)
    debt_ratio = calculate_debt_ratio(financials)
    cash_ratio = calculate_cash_ratio(financials)

    analysis = []

    if profit_margin >= 20:
        analysis.append("✅ Strong profitability.")
    elif profit_margin >= 10:
        analysis.append("🟡 Moderate profitability.")
    else:
        analysis.append("🔴 Weak profitability.")

    if debt_ratio < 50:
        analysis.append("✅ Healthy debt level.")
    else:
        analysis.append("🔴 High debt level.")

    if cash_ratio >= 30:
        analysis.append("✅ Strong liquidity.")
    else:
        analysis.append("🟡 Limited liquidity.")

    return {
        "profit_margin": round(profit_margin, 2),
        "debt_ratio": round(debt_ratio, 2),
        "cash_ratio": round(cash_ratio, 2),
        "analysis": analysis,
    }