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
    "Analyze company fundamentals, market risk, "
    "price performance, and AI-generated insights."
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
        with st.spinner("Collecting data and generating AI analysis..."):
            result = start_research(ticker)

        if result["status"] == "error":
            st.error(result["summary"])
        else:
            st.success("Analysis completed.")
            st.text(result["summary"])