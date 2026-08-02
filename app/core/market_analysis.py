import pandas as pd

def calculate_volatility(historical_data):
    if historical_data is None or historical_data.empty:
        return None

    daily_returns = historical_data["Close"].pct_change().dropna()

    if daily_returns.empty:
        return None

    annual_volatility = daily_returns.std() * (252 ** 0.5)

    return round(annual_volatility * 100, 2)


def calculate_max_drawdown(historical_data):
    if historical_data is None or historical_data.empty:
        return None

    close_prices = historical_data["Close"].dropna()

    if close_prices.empty:
        return None

    running_max = close_prices.cummax()
    drawdowns = (close_prices - running_max) / running_max
    max_drawdown = drawdowns.min()

    return round(max_drawdown * 100, 2)


def analyze_price_trend(historical_data):
    if historical_data is None or historical_data.empty:
        return "Unknown"

    close_prices = historical_data["Close"].dropna()

    if close_prices.empty:
        return "Unknown"

    start_price = close_prices.iloc[0]
    end_price = close_prices.iloc[-1]

    price_change = ((end_price - start_price) / start_price) * 100

    if price_change > 10:
        return "Bullish"
    elif price_change < -10:
        return "Bearish"
    else:
        return "Sideways"


def analyze_market_risk(volatility):
    if volatility is None:
        return "Unknown"

    if volatility < 20:
        return "Low"
    elif volatility < 35:
        return "Medium"
    else:
        return "High"