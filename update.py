"""
Automated Weekly Dataset Updater for fpi-sectoral-allocation-and-flows
Can be executed locally or via GitHub Actions.
Zero credentials required.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from fpi_sectoral_flows.fetcher import FPISectoralFetcher

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "fpi_sectoral_flows.csv"
PARQUET_FILE = OUTPUT_DIR / "fpi_sectoral_flows.parquet"


def update():
    print("[1/3] Fetching fortnightly FPI sectoral AUC and net equity flows...")
    fetcher = FPISectoralFetcher()
    df = fetcher.fetch_sectoral_flows()
    print(f"      Retrieved {len(df)} sector-fortnight records across {df['sector_name'].nunique()} sectors.")

    print("[2/3] Saving sectoral flows dataset...")
    df.to_csv(CSV_FILE, index=False)
    df.to_parquet(PARQUET_FILE, index=False)
    print(f"      Saved {len(df)} records to {CSV_FILE.name} and {PARQUET_FILE.name}.")

    print("[3/3] Running automated quality audit...")
    from evaluate_quality import audit_quality
    audit_quality()
    print("Update complete successfully.")


if __name__ == "__main__":
    update()
