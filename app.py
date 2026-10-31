"""Streamlit entry point for Meta Ads Reporting Automation."""

import streamlit as st


st.set_page_config(
    page_title="Meta Ads Reporting Automation",
    page_icon="📊",
    layout="wide",
)

st.title("Meta Ads Reporting Automation")
st.caption("A Python-powered workspace for campaign performance analysis.")

st.info(
    "The dashboard foundation is ready. The next development step is "
    "loading a clearly labelled demonstration dataset, followed by the "
    "Meta Marketing API integration."
)

st.subheader("Planned reporting metrics")
columns = st.columns(4)
for column, label in zip(
    columns,
    ["Amount spent", "Impressions", "Link clicks", "Leads"],
):
    column.metric(label, "—", help="Will populate when reporting data is connected.")

st.markdown(
    """
    ### Development status
    - [x] Repository and application foundation
    - [ ] Sample reporting dataset
    - [ ] Data validation and KPI calculations
    - [ ] Campaign performance dashboard
    - [ ] Meta Marketing API integration
    - [ ] Excel and CSV exports
    - [ ] HubSpot CRM integration
    """
)
