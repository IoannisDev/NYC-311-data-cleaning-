# NYC 311 Service Requests — Data Cleaning

A data cleaning project using NYC 311 service request data. The goal is to take raw API data and produce a reliable, analysis-ready dataset — handling nulls, inconsistent categorization, type conversion, and feature engineering.

---

## Dataset

- **Source:** [NYC Open Data — 311 Service Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9)
- **Date Range:** January 1–20, 2023
- **Raw Rows:** 150,000
- **Clean Rows:** 146,064
- **Columns:** 44 → 35

---

## Project Structure

```
├── data/
│   ├── raw/               # Original data pulled from the API
│   └── cleaned/           # Cleaned output
├── notebooks/
│   └── data_cleaning.ipynb
├── reports/
│   ├── profiling_report.md
│   └── cleaning_log.md
├── src/
│   └── data.py            # Socrata API ingestion script
├── .env                   # Local environment variables (not committed)
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file at the project root:

```
PROJECT_DIR=/your/path/to/project
```

---

## How to Run

**1. Ingest data**
```bash
python src/data.py
```

**2. Clean data**

Open and run `notebooks/data_cleaning.ipynb` top to bottom (Kernel → Restart & Run All).

---

## Key Cleaning Decisions

- Dropped 9 columns with ≥ 99% null rate (specialty fields with no analytical value)
- Dropped rows where `borough` or `status` == `"Unspecified"` (~1.9% of data)
- Standardized `complaint_type` casing with `.str.title()`
- Engineered `resolution_time` from `closed_date - created_date`
- Dropped rows with negative resolution times (data entry errors)

Full details in [reports/profiling_report.md](reports/profiling_report.md).

---

## Known Limitations

- Data covers January 1–20, 2023 only due to a 150,000 row API cap
- `city` column excluded from analysis — inconsistent granularity (neighborhoods mixed with boroughs)

