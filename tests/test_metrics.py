import pandas as pd
import pytest

from src.metrics import add_kpis


def test_add_kpis_calculates_expected_values():
    sample = pd.DataFrame(
        {
            "spend": [100.0],
            "impressions": [10000],
            "reach": [5000],
            "link_clicks": [200],
            "leads": [10],
        }
    )

    result = add_kpis(sample)

    assert result.loc[0, "ctr"] == pytest.approx(2.0)
    assert result.loc[0, "cpc"] == pytest.approx(0.5)
    assert result.loc[0, "cpm"] == pytest.approx(10.0)
    assert result.loc[0, "cpl"] == pytest.approx(10.0)
    assert result.loc[0, "frequency"] == pytest.approx(2.0)


def test_add_kpis_handles_zero_denominators():
    sample = pd.DataFrame(
        {
            "spend": [0.0],
            "impressions": [0],
            "reach": [0],
            "link_clicks": [0],
            "leads": [0],
        }
    )

    result = add_kpis(sample)

    assert result.loc[0, "ctr"] == 0
    assert result.loc[0, "cpc"] == 0
    assert result.loc[0, "cpm"] == 0
    assert result.loc[0, "cpl"] == 0
    assert result.loc[0, "frequency"] == 0
