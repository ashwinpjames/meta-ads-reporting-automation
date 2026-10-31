"""Load and validate reporting data from local CSV files."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "date",
    "campaign_name",
    "adset_name",
    "ad_name",
    "spend",
    "impressions",
    "reach",
    "link_clicks",
    "leads",
}


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file and validate the reporting schema."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    data = pd.read_csv(file_path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    if data["date"].isna().any():
        raise ValueError("The CSV contains invalid or empty dates.")

    numeric_columns = ["spend", "impressions", "reach", "link_clicks", "leads"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
        if data[column].isna().any() or (data[column] < 0).any():
            raise ValueError(f"Column '{column}' must contain non-negative numbers.")

    return data
