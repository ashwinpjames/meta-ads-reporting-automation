# Meta Ads Reporting Automation

A Python-based marketing analytics dashboard for exploring Meta Ads performance. The project is being developed in stages, starting with a clearly labelled demonstration dataset and later adding live Meta Marketing API data.

> **Important:** The current dashboard uses fictional demonstration data. It is not connected to a live Meta Ads account, and the displayed figures must not be treated as business results.

## Current features

- Streamlit dashboard with date and campaign filters
- KPI calculations: CTR, CPC, CPM, CPL and frequency
- Spend and lead trend charts
- Campaign-level performance comparison
- Filtered CSV export
- Input data validation and automated KPI tests

## Technology

- Python
- Pandas
- Streamlit
- Plotly
- Requests
- python-dotenv
- OpenPyXL
- Pytest

## Run locally

### 1. Clone the repository

```powershell
git clone https://github.com/ashwinpjames/meta-ads-reporting-automation.git
cd meta-ads-reporting-automation
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the dashboard

```powershell
streamlit run app.py
```

The local dashboard normally opens at `http://localhost:8501`.

### 5. Run tests

```powershell
pytest
```

## Project structure

```text
meta-ads-reporting-automation/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── sample_campaign_data.csv
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   └── metrics.py
├── tests/
│   └── test_metrics.py
└── reports/
```

## Development roadmap

- [x] Repository and Python environment foundation
- [x] Demonstration dataset and initial dashboard
- [x] KPI calculations and input validation
- [ ] Automated test coverage for data validation
- [ ] Live Meta Marketing API extraction
- [ ] Multi-account reporting and scheduled refresh
- [ ] Excel export and report generation
- [ ] HubSpot CRM integration and lead-quality analysis

## Security

- Never commit `.env` files, access tokens, passwords or private customer data.
- Use `.env.example` only as a template.
- Keep demonstration data clearly identified.
- Use authorised Meta permissions and account access for live reporting.

## License

MIT
