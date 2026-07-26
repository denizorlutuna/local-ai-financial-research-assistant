from app.core.financial_analysis import (
    classify_market_cap,
    generate_company_summary,
    analyze_financial_health,
)
from app.data.market_data import get_company_info
from app.utils.formatter import format_market_cap, format_price


def start_research(company_name):
    company = get_company_info(company_name)

    if company["name"] is None:
        return {
            "status": "error",
            "summary": "Company not found."
        }

    analysis = generate_company_summary(company)
    financial_health = analyze_financial_health(company)

    return {
        "status": "completed",
        "summary": (
            f"Company: {company['name']}\n"
            f"Ticker: {company['ticker']}\n"
            f"Sector: {company['sector']}\n"
            f"Industry: {company['industry']}\n"
            f"Current Price: {format_price(company['current_price'])}\n"
            f"Market Cap: {format_market_cap(company['market_cap'])}\n"
            f"Company Size: {classify_market_cap(company['market_cap'])}\n\n"
            f"Quick Analysis:\n"
            + "\n".join(f"- {item}" for item in analysis)
            + "\n\nFinancial Health:\n"
            + f"Profit Margin: {financial_health['profit_margin']}%\n"
            + f"Debt Ratio: {financial_health['debt_ratio']}%\n"
            + f"Cash Ratio: {financial_health['cash_ratio']}%\n"
            + "\n".join(
                f"- {item}" for item in financial_health["analysis"]
            )
        )
    }