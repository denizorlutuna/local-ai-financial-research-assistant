def format_market_cap(value):
    if value is None:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    return str(value)

def format_price(value, currency="USD"):
    if value is None:
        return "N/A"

    if currency == "USD":
        return f"${value:.2f}"

    return f"{value:.2f} {currency}"


def format_ratio(value):
    if value is None:
        return "N/A"

    return f"{value:.2f}"