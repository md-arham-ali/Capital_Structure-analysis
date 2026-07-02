"""
config.py — single source of project constants (Phase 1 & 2).

Style: explicit hand-written literals over abstraction (style_template.md #2). Every
company, ticker, URL, column rename, and assumption is named by hand here so the rest of
the pipeline stays declarative and every number is auditable in one place.
"""
from pathlib import Path

# ------------------------------------------------------------------------- paths ---
# config.py lives at  <root>/analysis/scripts/config.py  ->  parents[2] == <root>
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW     = PROJECT_ROOT / "data" / "raw"
DATA_CLEANED = PROJECT_ROOT / "data" / "cleaned"
OUTPUT_DIR   = PROJECT_ROOT / "output"

MASTER_DATA_CSV = DATA_CLEANED / "master_data.csv"
RATIOS_CSV      = DATA_CLEANED / "ratios.csv"
MARKET_DATA_CSV = DATA_RAW     / "market_data.csv"
FINANCIALS_CSV  = DATA_RAW     / "financials.csv"
SCHEDULES_CSV   = DATA_RAW     / "schedules.csv"      # expandable-row breakdowns (fetch_schedules.py)
WORKBOOK_XLSX   = OUTPUT_DIR    / "FMCG_Analysis.xlsx"

# cleaned analysis outputs (python mirrors of the Excel sheets)
MARKET_SNAPSHOT_CSV     = DATA_CLEANED / "market_snapshot.csv"
LEVERAGE_THRESHOLD_CSV  = DATA_CLEANED / "leverage_threshold.csv"
CORRELATION_MATRIX_CSV  = DATA_CLEANED / "correlation_matrix.csv"
REGRESSION_RESULTS_CSV  = DATA_CLEANED / "regression_results.csv"
REGRESSION_FITTED_CSV   = DATA_CLEANED / "regression_fitted.csv"
WACC_CSV                = DATA_CLEANED / "wacc.csv"
DCF_CSV                 = DATA_CLEANED / "dcf_valuation.csv"
COMPS_CSV               = DATA_CLEANED / "comps.csv"
SENSITIVITY_CSV         = DATA_CLEANED / "sensitivity.csv"

# archive name for the 24-sheet per-company inspection workbook (pre-analysis build)
CLEANED_SHEETS_XLSX = OUTPUT_DIR / "FMCG_Cleaned_Sheets.xlsx"

# --------------------------------------------------------------------- universe ---
# 8 listed Indian FMCG firms. Names double as the raw filename stem (raw/HUL.xlsx …).
COMPANIES = ["HUL", "ITC", "Dabur", "Marico", "Colgate", "Nestle", "Godrej", "Emami"]

# NSE symbols (verify on Screener — COLPAL = Colgate-Palmolive India, EMAMILTD = Emami).
NSE_SYMBOL = {
    "HUL":     "HINDUNILVR",
    "ITC":     "ITC",
    "Dabur":   "DABUR",
    "Marico":  "MARICO",
    "Colgate": "COLPAL",
    "Nestle":  "NESTLEIND",
    "Godrej":  "GODREJCP",
    "Emami":   "EMAMILTD",
}

# Screener.in company pages (the scraper hits these; statements export from here too).
SCREENER_URL = {name: f"https://www.screener.in/company/{sym}/"
                for name, sym in NSE_SYMBOL.items()}

# Yahoo Finance tickers — alternative programmatic source via the `yfinance` package.
YAHOO_TICKER = {name: f"{sym}.NS" for name, sym in NSE_SYMBOL.items()}

# ----------------------------------------------------------------------- period ---
# RESOLVED: the raw export delivered FY2015–FY2026 (12 FYs), so "recent 5" = FY2022–26.
# Why this window and not the plan's FY2019–24 label:
#   1) it keeps HUL's post-GSK-merger balance-sheet regime consistent (assets jump
#      19,602 → 68,116 Cr in FY2021 — a structural break inside any earlier window);
#   2) the market snapshot is July 2026, so comps/DCF align with FY2026 statements;
#   3) COVID-era depth isn't lost — the extra analyses use the FULL 12-year history.
YEARS       = ["FY2022", "FY2023", "FY2024", "FY2025", "FY2026"]
ALL_PERIODS = [f"FY{y}" for y in range(2015, 2027)]   # full scraped history (extras use this)

# ----------------------------------------------- raw -> canonical column names ---
# FINALISED against the real scrape (28 statement metrics + schedule breakdowns).
#   Left = raw row label (cleaned CSVs carry it as "<label>(in <unit>)" — the unit
#   suffix is stripped before this map is applied), right = canonical name downstream.
COLUMN_RENAME = {
    # income statement (12)
    "Sales":                        "Revenue",
    "Expenses":                     "Expenses",
    "Operating Profit":             "OperatingProfit",
    "OPM %":                        "OPMPct",
    "Other Income":                 "OtherIncome",
    "Interest":                     "InterestExpense",
    "Depreciation":                 "Depreciation",
    "Profit before tax":            "PBT",
    "Tax %":                        "TaxPct",
    "Net Profit":                   "NetProfit",
    "EPS in Rs":                    "EPS",
    "Dividend Payout %":            "DividendPayoutPct",
    # balance sheet (10)
    "Equity Capital":               "ShareCapital",
    "Reserves":                     "Reserves",
    "Borrowings":                   "TotalDebt",
    "Other Liabilities":            "OtherLiabilities",
    "Total Liabilities":            "TotalLiabilities",
    "Fixed Assets":                 "FixedAssets",
    "CWIP":                         "CWIP",
    "Investments":                  "Investments",
    "Other Assets":                 "OtherAssets",
    "Total Assets":                 "TotalAssets",
    # cash flow (6)
    "Cash from Operating Activity": "OperatingCashFlow",
    "Cash from Investing Activity": "InvestingCashFlow",
    "Cash from Financing Activity": "FinancingCashFlow",
    "Net Cash Flow":                "NetCashFlow",
    "Free Cash Flow":               "FreeCashFlow",
    "CFO/OP":                       "CFOtoOP",
    # schedule breakdowns (fetch_schedules.py — expandable "+" rows)
    "Cash Equivalents":             "Cash",
    "Inventories":                  "Inventories",
    "Trade receivables":            "TradeReceivables",
    "Loans n Advances":             "LoansAdvances",
    "Other asset items":            "OtherAssetItems",
    "Trade Payables":               "TradePayables",
    "Advance from Customers":       "CustomerAdvances",
    "Other liability items":        "OtherLiabilityItems",
    "Fixed assets purchased":       "FixedAssetsPurchased",   # true capex (negative sign)
    "Fixed assets sold":            "FixedAssetsSold",
    "Dividends paid":               "DividendsPaid",
    # market snapshot
    "Market Cap":                   "MarketCap",
    "Current Price":                "CurrentPrice",
    "Face Value":                   "FaceValue",
    "Stock P/E":                    "StockPE",
    "Book Value":                   "BookValue",
    "Dividend Yield":               "DividendYieldPct",
    "ROCE":                         "ScreenerROCEPct",
    "ROE":                          "ScreenerROEPct",
}

# Canonical columns the cleaned master_data.csv must expose (the downstream contract).
# Derived during the master build (build_master.py):
#   TotalEquity = ShareCapital + Reserves            EBIT   = PBT + InterestExpense
#   EBITDA      = EBIT + Depreciation                TaxRate = TaxPct / 100
#   Capex       = OperatingCashFlow - FreeCashFlow   NetBorrowing = ΔTotalDebt
#   CurrentAssets ≈ Inventories + TradeReceivables + Cash          (schedule items)
#   CurrentLiabilities ≈ OtherLiabilities            (non-debt liabilities; FMCG ≈ current)
CANONICAL_COLUMNS = [
    "Company", "Year",
    "Revenue", "Expenses", "OperatingProfit", "OtherIncome", "InterestExpense",
    "Depreciation", "PBT", "TaxPct", "TaxRate", "NetProfit", "EBIT", "EBITDA",
    "EPS", "DividendPayoutPct",
    "TotalAssets", "TotalEquity", "TotalDebt", "OtherLiabilities",
    "CurrentAssets", "CurrentLiabilities", "Cash", "Inventories", "TradeReceivables",
    "TradePayables",
    "OperatingCashFlow", "InvestingCashFlow", "FinancingCashFlow", "FreeCashFlow",
    "Capex", "NetBorrowing", "DividendsPaid",
    "SharesOutstanding",
]

# --------------------------------------------------------------- leverage bands ---
# D/E classification used by Capital Structure (2C) and Leverage Threshold (2D).
LEVERAGE_BANDS = {
    "Low":  (0.0, 0.3),            # D/E < 0.3
    "Mid":  (0.3, 0.7),            # 0.3 <= D/E <= 0.7
    "High": (0.7, float("inf")),   # D/E > 0.7
}

# ------------------------------------------------------------ WACC assumptions ---
# Phase 2E. These mirror the blue/yellow assumption cells in the Excel WACC sheet.
RISK_FREE_RATE      = 0.070        # ~10Y India G-Sec yield
EQUITY_RISK_PREMIUM = 0.055        # standard India equity risk premium

# Equity beta per firm. ⚠ PLACEHOLDERS — replace with Screener / Trendlyne values.
BETA = {
    "HUL":     0.55,
    "ITC":     0.75,
    "Dabur":   0.60,
    "Marico":  0.55,
    "Colgate": 0.65,
    "Nestle":  0.50,
    "Godrej":  0.70,
    "Emami":   0.65,
}

# ------------------------------------------------------------- DCF assumptions ---
# Phase 4A/4B/4D. Mirrored as blue assumption cells on the DCF / Sensitivity sheets.
FORECAST_YEARS  = 5            # explicit FCFF/FCFE forecast horizon
FCFF_BASE_YEARS = 3            # base-year flow = mean of the last N FYs (smooths one-offs)
TERMINAL_GROWTH = 0.04         # Gordon terminal g — long-run nominal India growth proxy
GROWTH_CAP      = 0.15         # ceiling on the historical-CAGR forecast growth rate
GROWTH_FLOOR    = 0.03         # floor — a shrinking-FCFF base year shouldn't force decay

# Sensitivity grid (Phase 4D): WACC offsets around base ±200bps, terminal g 1%..5%.
SENS_WACC_OFFSETS   = [-0.020, -0.015, -0.010, -0.005, 0.000,
                        0.005,  0.010,  0.015,  0.020]
SENS_TERMINAL_RATES = [0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045, 0.050]
