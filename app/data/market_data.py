import yfinance as yf


def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

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
    }