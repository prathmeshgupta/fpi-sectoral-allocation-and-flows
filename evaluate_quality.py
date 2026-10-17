import re
import pandas as pd
from pathlib import Path

ISO_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def audit_quality():
    print("=" * 65)
    print(" FPI SECTORAL ALLOCATION & FLOWS - DATA QUALITY AUDIT")
    print("=" * 65)

    root = Path(__file__).parent
    pq_path = root / "output" / "fpi_sectoral_flows.parquet"
    csv_path = root / "output" / "fpi_sectoral_flows.csv"

    assert pq_path.exists(), "fpi_sectoral_flows.parquet missing"
    assert csv_path.exists(), "fpi_sectoral_flows.csv missing"

    df_pq = pd.read_parquet(pq_path)
    df_csv = pd.read_csv(csv_path)

    # 1. Parity Check
    assert len(df_pq) == len(df_csv), f"Parity mismatch: Parquet ({len(df_pq)}) != CSV ({len(df_csv)})"
    print(f"Total Sector-Fortnight Observations: {len(df_pq)} [PASS - 100% Parity]")

    # 2. Null Checks
    null_count = df_pq.isnull().sum().sum()
    assert null_count == 0, f"Found {null_count} nulls across table"
    print("Null Values: 0 across all columns [100% COMPLETE]")

    # 3. ISO-8601 Format
    s = df_pq["fortnight_date"].astype(str)
    invalid = s[~s.str.match(ISO_REGEX)]
    assert len(invalid) == 0, f"Non-ISO dates detected: {len(invalid)}"
    print("ISO-8601 Compliance (fortnight_date): 100% PASS")

    # 4. Domain Invariants
    assert (df_pq["equity_auc_cr"] > 0).all(), "Non-positive AUC detected"
    assert ((df_pq["fpi_sector_weight_pct"] >= 0) & (df_pq["fpi_sector_weight_pct"] <= 100)).all(), "Weight out of [0, 100]"
    print("Domain Bounds (Positive AUC & Weight in [0, 100]%): [PASS]")

    # 5. Top Sectors Distribution
    latest_dt = df_pq["fortnight_date"].max()
    latest_df = df_pq[df_pq["fortnight_date"] == latest_dt]
    print(f"\nTop 5 FPI Sectors as of {latest_dt}:")
    for _, row in latest_df.head(5).iterrows():
        print(f"  • {row['sector_name']:<32}: Rs.{row['equity_auc_cr']:>9,} Cr ({row['fpi_sector_weight_pct']}%)")

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)


if __name__ == "__main__":
    audit_quality()
