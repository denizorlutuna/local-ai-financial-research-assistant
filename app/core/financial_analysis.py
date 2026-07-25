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

def generate_company_summary(company):
    summary = []

    market_cap = company.get("market_cap")
    sector = company.get("sector")
    current_price = company.get("current_price")

    if market_cap is not None and market_cap >= 200_000_000_000:
        summary.append("Global market leader")

    if sector == "Technology":
        summary.append("Operates in the technology sector")

    if current_price is not None and current_price >= 100:
        summary.append("High-priced stock")

    if not summary:
        summary.append("Limited analysis available")

    return summary