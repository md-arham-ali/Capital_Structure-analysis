"""
cleaning.py — Phase 1C data-cleaning helpers.

Background logic for `clean_data.ipynb` / `clean_schedules.ipynb` (Instruction #3:
heavy logic lives here, the notebooks just drive/inspect it).
"""
import re
from pathlib import Path

import pandas as pd


def split_by_column(df, column):
    """Split df into one DataFrame per unique value of `column`.

    Returns a dict {value: DataFrame}, keyed by each unique value of `column`.
    """
    groups = {value: group.copy() for value, group in df.groupby(column, sort=False)}
    print(f"split_by_column({column!r}): {len(groups)} groups from {df.shape[0]} rows")
    for value, group in groups.items():
        print(f"  {value!s:12s} {group.shape[0]:4d} rows")
    return groups


def drop_column(df, column):
    """Drop `column` from df in place if present (returns df for chaining)."""
    if column in df.columns:
        df.drop(columns=column, inplace=True)
    return df


def add_key_column(df, name="key"):
    """Add `key` = '<LineItem>_<Period>' (e.g. 'Sales_FY2024') to df in place.

    Gives every metric-year a unique handle for later pivoting / lookup.
    """
    df[name] = df["LineItem"].astype(str) + "_" + df["Period"].astype(str)
    return df


def pivot_line_items(df, periods=None):
    """Reshape a long sub_df to wide: LineItem -> columns, Period -> rows, Value -> cells.

    Column headers carry the line item's unit in brackets, e.g. 'Sales(in Cr)' — read
    from the sub_df's `Unit` column (each LineItem maps to one unit: Cr / % / Rs).
    `periods` (e.g. config.YEARS) filters the rows to those periods, in that order;
    None keeps every period. Assumes (LineItem, Period) is unique within df.
    """
    wide = df.pivot(index="Period", columns="LineItem", values="Value")
    if periods is not None:
        wide = wide.reindex(periods)          # keep only these periods, in this order
    wide.columns.name = None                  # drop the leftover 'LineItem' axis label
    if "Unit" in df.columns:                  # tag each header with its unit -> 'Sales(in Cr)'
        unit = df.groupby("LineItem")["Unit"].first()
        wide.columns = [f"{col}(in {unit[col]})" for col in wide.columns]
    print(f"pivot_line_items: {wide.shape[0]} periods x {wide.shape[1]} line items")
    return wide


def parse_number(text):
    """'₹ 5,12,345 Cr.' / '1.88 %' / '30,806' -> float ; None if no number present."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    match = re.search(r"-?\d[\d,]*\.?\d*", str(text).replace("\xa0", " "))
    return float(match.group(0).replace(",", "")) if match else None


def clean_market_snapshot(df):
    """market_data.csv (raw ₹/%/x strings) -> numeric per-firm snapshot frame.

    Keeps Company and parses each headline figure to float. Columns carry the same
    '(in <unit>)' tag as the statement CSVs so units stay visible downstream.
    """
    SNAPSHOT_COLUMNS = {                       # raw label   -> (clean name, unit)
        "Market Cap":     ("Market Cap",     "Cr"),
        "Current Price":  ("Current Price",  "Rs"),
        "Book Value":     ("Book Value",     "Rs"),
        "Face Value":     ("Face Value",     "Rs"),
        "Stock P/E":      ("Stock P/E",      "x"),
        "Dividend Yield": ("Dividend Yield", "%"),
        "ROCE":           ("ROCE",           "%"),
        "ROE":            ("ROE",            "%"),
    }
    out = pd.DataFrame({"Company": df["Company"]})
    for raw, (name, unit) in SNAPSHOT_COLUMNS.items():
        if raw in df.columns:
            out[f"{name}(in {unit})"] = df[raw].map(parse_number)
        else:
            print(f"  ⚠ snapshot column missing: {raw}")
    print(f"clean_market_snapshot: {out.shape[0]} firms x {out.shape[1]} cols")
    return out


def save_wide(wide, base_dir):
    """Save nested {company: {section: DataFrame}} to base_dir/<company>/<section>.csv.

    One folder per company (8), one CSV per section (3) -> 24 files. The Period index
    is kept. Folders are created as needed. Returns the count of files written.
    """
    base_dir = Path(base_dir)
    written = 0
    for company, sections in wide.items():
        folder = base_dir / company
        folder.mkdir(parents=True, exist_ok=True)
        for section, df in sections.items():
            path = folder / f"{section}.csv"
            df.to_csv(path)                   # index=True -> Period stays as first column
            written += 1
            print(f"  wrote {path.relative_to(base_dir.parent)}  ({df.shape[0]}x{df.shape[1]})")
    print(f"save_wide: {written} files under {base_dir}")
    return written
