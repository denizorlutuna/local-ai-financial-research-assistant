def calculate_profit_margin(financials):
    revenue = financials["revenue"]
    net_income = financials["net_income"]

    if revenue == 0:
        return 0

    return (net_income / revenue) * 100

def calculate_debt_ratio(financials):
    assets = financials["total_assets"]
    debt = financials["total_debt"]

    if assets == 0:
        return 0

    return (debt / assets) * 100

def calculate_cash_ratio(financials):
    cash = financials["cash"]
    debt = financials["total_debt"]

    if debt == 0:
        return 0

    return (cash / debt) * 100