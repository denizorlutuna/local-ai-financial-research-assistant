from app.core.financial_analysis import (
    classify_market_cap,
    generate_company_summary,
    analyze_financial_health,
)
from app.data.market_data import get_company_info
from app.utils.formatter import format_market_cap, format_price


def start_research(company_name):
    try:
        company = get_company_info(company_name)
    except Exception as error:
        return {
            "status": "error",
            "summary": f"Unable to retrieve company data: {error}"
        }

    if not company or company.get("name") is None:
        return {
            "status": "error",
            "summary": f"Company not found for ticker: {company_name}"
        }

    analysis = generate_company_summary(company)
    financial_health = analyze_financial_health(company)

    profit_margin_text = (
        f"{financial_health['profit_margin']}%"
        if financial_health["profit_margin"] is not None
        else "Not available"
    )

    debt_ratio_text = (
        f"{financial_health['debt_ratio']}%"
        if financial_health["debt_ratio"] is not None
        else "Not available"
    )

    cash_ratio_text = (
        f"{financial_health['cash_ratio']}%"
        if financial_health["cash_ratio"] is not None
        else "Not available"
    )

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
            + f"Profit Margin: {profit_margin_text}\n"
            + f"Debt Ratio: {debt_ratio_text}\n"
            + f"Cash Ratio: {cash_ratio_text}\n"
            + "\n".join(
                f"- {item}" for item in financial_health["analysis"]
            )
        )
    }