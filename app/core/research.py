from app.core.financial_analysis import (classify_market_cap, generate_company_summary, analyze_financial_health, analyze_risks)
from app.data.market_data import get_company_info
from app.utils.formatter import format_market_cap, format_price
from app.core.investment_analysis import generate_investment_outlook
from app.data.market_data import get_historical_prices
from app.core.financial_analysis import calculate_price_performance


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

    historical_data = get_historical_prices(company["ticker"])
    analysis = generate_company_summary(company, historical_data)
    financial_health = analyze_financial_health(company)
    risks = analyze_risks(company)

    investment_outlook = generate_investment_outlook(
        company,
        financial_health,
        risks
    )
 
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

    if historical_data:
        yearly_return = calculate_price_performance(historical_data)
    else:
        yearly_return = None

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
            + "\n\nPrice Performance:\n"
            + (
                f"Start Price: {format_price(historical_data['start_price'])}\n"
                f"Current Price: {format_price(historical_data['end_price'])}\n"
                f"Highest Price: {format_price(historical_data['highest_price'])}\n"
                f"Lowest Price: {format_price(historical_data['lowest_price'])}\n"
                f"1-Year Return: {yearly_return:.2f}%"
                if historical_data and yearly_return is not None
                else "Historical price data is unavailable."
            )
            + "\n\nFinancial Health:\n"
            + f"Profit Margin: {profit_margin_text}\n"
            + f"Debt Ratio: {debt_ratio_text}\n"
            + f"Cash Ratio: {cash_ratio_text}\n"
            + "\n".join(
                f"- {item}" for item in financial_health["analysis"]
            )
            + "\n\nRisk Analysis:\n"
            + (
                "\n".join(f"- {risk}" for risk in risks)
                if risks
                else "- No major valuation or price risks identified"
            )
            + "\n\nInvestment Outlook:\n"
            + "Strengths:\n"
            + (
                "\n".join(
                    f"- {item}" for item in investment_outlook["strengths"]
                )
                if investment_outlook["strengths"]
                else "- No major strengths identified"
            )
            + "\n\nRisks:\n"
            + (
                "\n".join(
                    f"- {item}" for item in investment_outlook["risks"]
                )
                if investment_outlook["risks"]
                else "- No major risks identified"
            )
            + f"\n\nScore: {investment_outlook['score']}\n"
            + f"Recommendation: {investment_outlook['recommendation']}"
        )
    }