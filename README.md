# Capital Structure & Valuation Analysis — Indian FMCG (FY2022–FY2026)

Does capital structure explain profitability and valuation across 8 listed Indian FMCG
firms — and where is the optimal leverage band? A four-phase, formula-driven analysis
(data prep → modelling → statistics → valuation) built as a recruiter-facing portfolio
piece. Every number traces back to a public source (Screener.in standalone statements,
FY2015–FY2026 scraped July 2026).

> **Status: Not complete.** Data fetched & cleaned, python pipeline run, the 14-sheet


## Companies
HUL · ITC · Dabur · Marico · Colgate (India) · Nestle (India) · Godrej Consumer · Emami


## Setup
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run order (full rebuild)
```
# 1. fetch (bulk rate-limited: 1.2s delay, session reuse, retries w/ backoff)
python analysis/scripts/scrape_market_data.py    # → raw/market_data.csv + financials.csv

# 2. clean (notebooks drive cleaning.py) → data/cleaned/<Company>/*.csv + market_snapshot.csv
jupyter nbconvert --execute --inplace analysis/notebooks/clean_data.ipynb
```

## Layout
```
analysis/scripts/    config + fetch + cleaning + ratios/threshold/corr/OLS/valuation + Excel build
analysis/notebooks/  process · clean_data · statistical · valuation (executed)
data/raw/            scraped financials.csv, market_data.csv
data/cleaned/        per-firm P&L/BS/CF/
output/              FMCG_Analysis.xlsx (formula-driven) 
docs/                requirements checklist · data sources · explanation 
```

