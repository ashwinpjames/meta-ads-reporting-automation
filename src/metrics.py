"""Reusable marketing KPI calculations."""

from __future__ import annotations

import pandas as pd


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Divide two series, returning zero where the denominator is zero."""
    result = numerator.div(denominator.where(denominator.ne(0)))
    return result.fillna(0)


def add_kpis(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of reporting data with calculated marketing KPIs.

    Expected input columns:
    spend, impressions, reach, link_clicks, leads
    """
    required = {"spend", "impressions", "reach", "link_clicks", "leads"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    result = data.copy()
    result["ctr"] = safe_divide(result["link_clicks"] * 100, result["impressions"])
    result["cpc"] = safe_divide(result["spend"], result["link_clicks"])
    result["cpm"] = safe_divide(result["spend"] * 1000, result["impressions"])
    result["cpl"] = safe_divide(result["spend"], result["leads"])
    result["frequency"] = safe_divide(result["impressions"], result["reach"])
    return result
