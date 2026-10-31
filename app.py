"""Interactive Meta Ads reporting dashboard.

The current data source is a clearly labelled demonstration CSV.
Replace it with live Meta Marketing API data in a later development phase.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_csv
from src.metrics import add_kpis


st.set_page_config(
    page_title="Meta Ads Reporting Automation",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "sample_campaign_data.csv"
CURRENCY = "AED"


@st.cache_data
def get_data() -> pd.DataFrame:
    """Load demonstration reporting data and calculate row-level KPIs."""
    return add_kpis(load_csv(DATA_PATH))


def money(value: float) -> str:
    return f"{CURRENCY} {value:,.2f}"


st.title("Meta Ads Reporting Automation")
st.caption("Campaign performance overview | Marketing analytics workspace")

data = get_data()

st.warning(
    "DEMONSTRATION DATA: These figures are fictional and are used only to "
    "develop and test the dashboard. They are not connected to your Meta ad accounts."
)

with st.sidebar:
    st.header("Report filters")
    min_date = data["date"].min().date()
    max_date = data["date"].max().date()
    selected_dates = st.date_input(
        "Reporting period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    campaigns = sorted(data["campaign_name"].unique().tolist())
    selected_campaigns = st.multiselect(
        "Campaigns",
        options=campaigns,
        default=campaigns,
    )
    st.divider()
    st.caption("Data source: Local demonstration CSV")
    st.caption(f"Available period: {min_date} to {max_date}")

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
elif isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 1:
    start_date = end_date = selected_dates[0]
else:
    start_date = end_date = selected_dates

filtered = data[
    data["date"].dt.date.between(start_date, end_date)
    & data["campaign_name"].isin(selected_campaigns)
].copy()

if filtered.empty:
    st.info("No records match the selected filters. Adjust the date range or campaigns.")
    st.stop()

# Calculate totals first, then derive ratios from totals. Do not average daily ratios.
total_spend = filtered["spend"].sum()
total_impressions = filtered["impressions"].sum()
total_reach = filtered["reach"].sum()
total_clicks = filtered["link_clicks"].sum()
total_leads = filtered["leads"].sum()
overall_ctr = total_clicks / total_impressions * 100 if total_impressions else 0
overall_cpc = total_spend / total_clicks if total_clicks else 0
overall_cpm = total_spend / total_impressions * 1000 if total_impressions else 0
overall_cpl = total_spend / total_leads if total_leads else 0
overall_frequency = total_impressions / total_reach if total_reach else 0

st.subheader("Performance overview")
kpi_cols = st.columns(4)
kpi_cols[0].metric("Amount spent", money(total_spend))
kpi_cols[1].metric("Leads", f"{total_leads:,.0f}")
kpi_cols[2].metric("Cost per lead", money(overall_cpl))
kpi_cols[3].metric("Link CTR", f"{overall_ctr:.2f}%")

detail_cols = st.columns(4)
detail_cols[0].metric("Impressions", f"{total_impressions:,.0f}")
detail_cols[1].metric("Reach", f"{total_reach:,.0f}")
detail_cols[2].metric("Link clicks", f"{total_clicks:,.0f}")
detail_cols[3].metric("Frequency", f"{overall_frequency:.2f}")

st.divider()

daily = (
    filtered.groupby("date", as_index=False)
    .agg(spend=("spend", "sum"), leads=("leads", "sum"), link_clicks=("link_clicks", "sum"))
    .sort_values("date")
)

left_chart, right_chart = st.columns(2)
with left_chart:
    st.subheader("Spend over time")
    spend_chart = px.line(
        daily, x="date", y="spend", markers=True,
        labels={"date": "Date", "spend": f"Spend ({CURRENCY})"},
    )
    st.plotly_chart(spend_chart, use_container_width=True)

with right_chart:
    st.subheader("Leads over time")
    leads_chart = px.bar(
        daily, x="date", y="leads",
        labels={"date": "Date", "leads": "Leads"},
    )
    st.plotly_chart(leads_chart, use_container_width=True)

st.divider()
st.subheader("Campaign comparison")

campaign_summary = (
    filtered.groupby(["campaign_id", "campaign_name"], as_index=False)
    .agg(
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        reach=("reach", "sum"),
        link_clicks=("link_clicks", "sum"),
        leads=("leads", "sum"),
    )
)
campaign_summary["ctr"] = (
    campaign_summary["link_clicks"] / campaign_summary["impressions"].replace(0, pd.NA) * 100
).fillna(0)
campaign_summary["cpc"] = (
    campaign_summary["spend"] / campaign_summary["link_clicks"].replace(0, pd.NA)
).fillna(0)
campaign_summary["cpm"] = (
    campaign_summary["spend"] / campaign_summary["impressions"].replace(0, pd.NA) * 1000
).fillna(0)
campaign_summary["cpl"] = (
    campaign_summary["spend"] / campaign_summary["leads"].replace(0, pd.NA)
).fillna(0)

display_summary = campaign_summary.rename(
    columns={
        "campaign_name": "Campaign",
        "spend": "Spend (AED)",
        "impressions": "Impressions",
        "reach": "Reach",
        "link_clicks": "Link clicks",
        "leads": "Leads",
        "ctr": "CTR (%)",
        "cpc": "CPC (AED)",
        "cpm": "CPM (AED)",
        "cpl": "CPL (AED)",
    }
)
display_columns = [
    "Campaign", "Spend (AED)", "Impressions", "Reach", "Link clicks",
    "Leads", "CTR (%)", "CPC (AED)", "CPM (AED)", "CPL (AED)",
]
st.dataframe(
    display_summary[display_columns].style.format(
        {
            "Spend (AED)": "{:,.2f}",
            "CTR (%)": "{:.2f}",
            "CPC (AED)": "{:,.2f}",
            "CPM (AED)": "{:,.2f}",
            "CPL (AED)": "{:,.2f}",
            "Impressions": "{:,.0f}",
            "Reach": "{:,.0f}",
            "Link clicks": "{:,.0f}",
            "Leads": "{:,.0f}",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Campaign spend")
spend_by_campaign = campaign_summary.sort_values("spend", ascending=False)
campaign_chart = px.bar(
    spend_by_campaign,
    x="campaign_name",
    y="spend",
    color="campaign_name",
    labels={"campaign_name": "Campaign", "spend": f"Spend ({CURRENCY})"},
)
st.plotly_chart(campaign_chart, use_container_width=True)

st.divider()
st.subheader("Export report")
export_data = filtered.drop(columns=["ctr", "cpc", "cpm", "cpl", "frequency"], errors="ignore")
csv_bytes = export_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data (CSV)",
    data=csv_bytes,
    file_name="meta_ads_demo_report.csv",
    mime="text/csv",
)

st.caption(
    f"Calculated from {len(filtered):,} daily campaign records. "
    f"Overall CPC: {money(overall_cpc)} | Overall CPM: {money(overall_cpm)}"
)
