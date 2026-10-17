# Foreign Portfolio Investor (FPI) Sectoral Allocation & Flows Dataset

[![Fortnightly Update](https://github.com/prathmeshgupta/fpi-sectoral-allocation-and-flows/actions/workflows/update.yml/badge.svg)](https://github.com/prathmeshgupta/fpi-sectoral-allocation-and-flows/actions/workflows/update.yml)
[![Format: Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-blue.svg)](output/fpi_sectoral_flows.parquet)
[![Format: CSV](https://img.shields.io/badge/Format-CSV-green.svg)](output/fpi_sectoral_flows.csv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An institutional quantitative dataset capturing official **Fortnightly Foreign Portfolio Investor (FPI / FII) Assets Under Custody (AUC)** and net equity investment flows across 20+ SEBI industrial sectors.

In Indian quantitative macro and tactical asset allocation, foreign capital sector rotation serves as the leading indicator for multi-week relative sector performance.

---

## Dataset Schema (`output/fpi_sectoral_flows.parquet` / `.csv`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `fortnight_date` | `string` | ISO-8601 Fortnight Ending Date (`YYYY-MM-DD`) |
| `sector_name` | `string` | SEBI / NSDL Official Sector Classification |
| `equity_auc_cr` | `int64` | Foreign Portfolio Investor Equity Assets Under Custody in INR Crores |
| `net_equity_inflow_cr` | `int64` | Net FPI equity purchases (+) or sales (-) in INR Crores during the fortnight |
| `fpi_sector_weight_pct` | `float64` | Sector percentage of total foreign equity holdings in India |
| `source` | `string` | Provenance identifier (`NSDL_FORTNIGHTLY_SECTOR_REPORTS`) |

---

## Quick Start (Python / Polars / DuckDB)

```python
import polars as pl

# Read directly from GitHub Raw Parquet
url = "https://github.com/prathmeshgupta/fpi-sectoral-allocation-and-flows/raw/main/output/fpi_sectoral_flows.parquet"
df = pl.read_parquet(url)

# Display latest top 5 sectors by FPI allocation
latest_dt = df["fortnight_date"].max()
top_sectors = df.filter(pl.col("fortnight_date") == latest_dt).head(5)
print(top_sectors.select(["sector_name", "equity_auc_cr", "fpi_sector_weight_pct", "net_equity_inflow_cr"]))
```
