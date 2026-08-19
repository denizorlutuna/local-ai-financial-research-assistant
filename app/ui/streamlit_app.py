import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.ai.research_assistant import process_query
from app.rag.document_indexer import index_document


st.set_page_config(
    page_title="Local AI Financial Research Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("Local AI Financial Research Assistant")

st.caption(
    "Ask questions about companies, financial data, "
    "uploaded reports, or general finance concepts."
)

st.divider()

st.subheader("Upload Financial Document")

uploaded_file = st.file_uploader(
    "Upload a PDF report",
    type=["pdf"],
)

if uploaded_file is not None:
    documents_dir = PROJECT_ROOT / "documents"
    documents_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = documents_dir / uploaded_file.name

    if (
        st.session_state.get("indexed_document")
        != uploaded_file.name
    ):
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        try:
            with st.spinner(
                "Indexing document and creating embeddings..."
            ):
                index_result = index_document(
                    file_path=file_path,
                    document_name=uploaded_file.name,
                )

            st.session_state["indexed_document"] = (
                uploaded_file.name
            )

            st.success(
                f"{index_result['document_name']} indexed successfully. "
                f"{index_result['page_count']} pages and "
                f"{index_result['chunk_count']} chunks processed."
            )

        except Exception as error:
            st.error(
                f"Unable to index document: {error}"
            )

active_document = st.session_state.get(
    "indexed_document"
)

if active_document:
    st.caption(
        f"Active document: {active_document}"
    )

st.subheader("Ask the Financial Assistant")

query = st.text_input(
    "Question",
    placeholder=(
        "How risky is NVIDIA? "
        "What does P/E ratio mean? "
        "What risks are discussed in this report?"
    ),
)

ask_button = st.button(
    "Ask Assistant",
    type="primary",
    use_container_width=True,
)

if ask_button:
    if not query.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Analyzing your question..."):
                result = process_query(
                    query=query,
                    document_name=active_document,
                )

            route = result.get("route", "unknown")

            st.success("Analysis completed.")

            st.caption(
                f"Detected route: {route}"
            )

            st.subheader("Answer")

            answer = result.get(
                "answer",
                "No answer was generated.",
            )

            st.markdown(answer)

            if route == "market_data":
                ticker = result.get("ticker")

                if ticker:
                    st.caption(
                        f"Resolved ticker: {ticker}"
                    )

                data = result.get("data")

                if data:
                    company = data.get("company", {})
                    price = data.get(
                        "price_performance",
                        {},
                    )
                    market = data.get(
                        "market_analysis",
                        {},
                    )
                    health = data.get(
                        "financial_health",
                        {},
                    )
                    outlook = data.get(
                        "investment_outlook",
                        {},
                    )

                    st.divider()

                    st.subheader(
                        f"{company.get('name', 'Company')} "
                        f"({company.get('ticker', ticker or 'N/A')})"
                    )

                    company_info = (
                        f"{company.get('sector', 'N/A')} · "
                        f"{company.get('industry', 'N/A')} · "
                        f"{company.get('company_size', 'N/A')}"
                    )

                    st.caption(company_info)

                    metric_1, metric_2, metric_3, metric_4 = (
                        st.columns(4)
                    )

                    metric_1.metric(
                        "Current Price",
                        company.get(
                            "current_price",
                            "Not available",
                        ),
                    )

                    metric_2.metric(
                        "Market Cap",
                        company.get(
                            "market_cap",
                            "Not available",
                        ),
                    )

                    metric_3.metric(
                        "1-Year Return",
                        price.get(
                            "yearly_return",
                            "Not available",
                        ),
                    )

                    metric_4.metric(
                        "Recommendation",
                        outlook.get(
                            "recommendation",
                            "Not available",
                        ),
                    )

                    overview_tab, financial_tab = st.tabs(
                        [
                            "Market Overview",
                            "Financial Health",
                        ]
                    )

                    with overview_tab:
                        market_1, market_2, market_3, market_4 = (
                            st.columns(4)
                        )

                        market_1.metric(
                            "Volatility",
                            market.get(
                                "volatility",
                                "Not available",
                            ),
                        )

                        market_2.metric(
                            "Maximum Drawdown",
                            market.get(
                                "max_drawdown",
                                "Not available",
                            ),
                        )

                        market_3.metric(
                            "Trend",
                            market.get(
                                "trend",
                                "Not available",
                            ),
                        )

                        market_4.metric(
                            "Risk Level",
                            market.get(
                                "risk_level",
                                "Not available",
                            ),
                        )

                        st.markdown("### Price Range")

                        price_1, price_2, price_3 = st.columns(3)

                        price_1.metric(
                            "Start Price",
                            price.get(
                                "start_price",
                                "Not available",
                            ),
                        )

                        price_2.metric(
                            "52-Week High",
                            price.get(
                                "highest_price",
                                "Not available",
                            ),
                        )

                        price_3.metric(
                            "52-Week Low",
                            price.get(
                                "lowest_price",
                                "Not available",
                            ),
                        )

                    with financial_tab:
                        health_1, health_2, health_3 = (
                            st.columns(3)
                        )

                        health_1.metric(
                            "Profit Margin",
                            health.get(
                                "profit_margin",
                                "Not available",
                            ),
                        )

                        health_2.metric(
                            "Debt Ratio",
                            health.get(
                                "debt_ratio",
                                "Not available",
                            ),
                        )

                        health_3.metric(
                            "Cash Ratio",
                            health.get(
                                "cash_ratio",
                                "Not available",
                            ),
                        )

                        left_column, right_column = (
                            st.columns(2)
                        )

                        with left_column:
                            st.markdown("### Strengths")

                            strengths = outlook.get(
                                "strengths",
                                [],
                            )

                            if strengths:
                                for item in strengths:
                                    st.success(item)
                            else:
                                st.info(
                                    "No major strengths identified."
                                )

                        with right_column:
                            st.markdown("### Risks")

                            risks = outlook.get(
                                "risks",
                                [],
                            )

                            if risks:
                                for item in risks:
                                    st.warning(item)
                            else:
                                st.info(
                                    "No major risks identified."
                                )

            if route == "rag":
                sources = result.get(
                    "sources",
                    [],
                )

                st.divider()
                st.subheader("Sources")

                if sources:
                    for source in sources:
                        document = source.get(
                            "document_name",
                            "Unknown document",
                        )

                        page = source.get(
                            "page_number",
                            "N/A",
                        )

                        distance = source.get(
                            "distance",
                        )

                        if distance is not None:
                            st.write(
                                f"**{document}** — "
                                f"Page {page} — "
                                f"similarity distance: "
                                f"{distance:.4f}"
                            )
                        else:
                            st.write(
                                f"**{document}** — "
                                f"Page {page}"
                            )

                else:
                    st.info(
                        "No sources were returned."
                    )

        except Exception as error:
            st.error(
                f"Unable to process the question: {error}"
            )