import yfinance as yf


def get_latest_value(financial_table, row_name):
    if financial_table.empty or row_name not in financial_table.index:
        return None

    return financial_table.loc[row_name].iloc[0]


def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    balance_sheet = stock.balance_sheet

    return {
        "name": info.get("longName"),
        "ticker": ticker.upper(),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "website": info.get("website"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),

        # Financial data
        "revenue": info.get("totalRevenue"),
        "net_income": info.get("netIncomeToCommon"),
        "total_assets": get_latest_value(
            balance_sheet,
            "Total Assets"
        ),
        "total_debt": info.get("totalDebt"),
        "cash": info.get("totalCash"),
    }