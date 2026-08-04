import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.research import start_research


st.set_page_config(
    page_title="Local AI Financial Research Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("Local AI Financial Research Assistant")
st.caption(
    "Local company analysis powered by market data and Ollama."
)

ticker = st.text_input(
    "Company ticker",
    placeholder="AAPL, MSFT, NVDA...",
).strip().upper()

analyze_button = st.button(
    "Run Analysis",
    type="primary",
    use_container_width=True,
)

if analyze_button:
    if not ticker:
        st.warning("Please enter a company ticker.")
    else:
        with st.spinner(
            "Collecting market data and generating AI analysis..."
        ):
            result = start_research(ticker)

        if result["status"] == "error":
            st.error(result["summary"])
        else:
            data = result["data"]
            company = data["company"]
            price = data["price_performance"]
            market = data["market_analysis"]
            health = data["financial_health"]
            outlook = data["investment_outlook"]

            st.success("Analysis completed.")

            st.subheader(
                f"{company['name']} ({company['ticker']})"
            )
            st.caption(
                f"{company['sector']} · {company['industry']} · "
                f"{company['company_size']}"
            )

            metric_1, metric_2, metric_3, metric_4 = st.columns(4)

            metric_1.metric(
                "Current Price",
                company["current_price"],
            )
            metric_2.metric(
                "Market Cap",
                company["market_cap"],
            )
            metric_3.metric(
                "1-Year Return",
                price["yearly_return"],
            )
            metric_4.metric(
                "Recommendation",
                outlook["recommendation"],
            )

            overview_tab, ai_tab, report_tab = st.tabs(
                [
                    "Overview",
                    "AI Analysis",
                    "Full Report",
                ]
            )

            with overview_tab:
                st.subheader("Market Analysis")

                market_1, market_2, market_3, market_4 = st.columns(4)

                market_1.metric(
                    "Volatility",
                    market["volatility"],
                )
                market_2.metric(
                    "Maximum Drawdown",
                    market["max_drawdown"],
                )
                market_3.metric(
                    "Trend",
                    market["trend"],
                )
                market_4.metric(
                    "Risk Level",
                    market["risk_level"],
                )

                st.subheader("Financial Health")

                health_1, health_2, health_3 = st.columns(3)

                health_1.metric(
                    "Profit Margin",
                    health["profit_margin"],
                )
                health_2.metric(
                    "Debt Ratio",
                    health["debt_ratio"],
                )
                health_3.metric(
                    "Cash Ratio",
                    health["cash_ratio"],
                )

                left_column, right_column = st.columns(2)

                with left_column:
                    st.markdown("### Strengths")

                    strengths = outlook["strengths"]

                    if strengths:
                        for item in strengths:
                            st.success(item)
                    else:
                        st.info("No major strengths identified.")

                with right_column:
                    st.markdown("### Risks")

                    risks = outlook["risks"]

                    if risks:
                        for item in risks:
                            st.warning(item)
                    else:
                        st.info("No major risks identified.")

                st.markdown("### Price Range")

                price_1, price_2, price_3 = st.columns(3)

                price_1.metric(
                    "Start Price",
                    price["start_price"],
                )
                price_2.metric(
                    "52-Week High",
                    price["highest_price"],
                )
                price_3.metric(
                    "52-Week Low",
                    price["lowest_price"],
                )

            with ai_tab:
                st.subheader("AI Financial Analysis")
                st.markdown(data["ai_analysis"])

            with report_tab:
                st.subheader("Complete Research Report")
                st.text(result["summary"])