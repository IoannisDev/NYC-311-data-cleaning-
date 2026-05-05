# NYC 311 Service Requests Data Cleaning Report

**Dataset:** NYC Open Data, 311 Service Requests  
**Source:** data.cityofnewyork.us  
**Date Range:** January 1–20, 2023  
**Raw Rows:** 150,000  
**Final Rows:** 146064  
**Columns (raw):** 44  
**Columns (clean):** 35 

---

## Tools Used
- Python, pandas
- Socrata API for data ingestion
- Jupyter Notebook

---

## 1. Data Acquisition

**Method:** Socrata API with pagination (limit 100,000 rows per request)  
**Reason for API over portal export:** Portal export timed out on large dataset  
**Row limit applied:** 300,000 cap to manage local memory  
**Actual rows pulled:** 150,000  

---

## 2. Profiling Findings

### 2.1 High-Null Columns
The following columns had 99%+ null rates and were dropped.
They are specialty fields that only apply to a small subset of complaint types:

| Column | Null Rate |
|--------|-----------|
| vehicle_type | 99.98% |
| taxi_company_borough | 99.95% |
| due_date | 99.79% |
| road_ramp | 99.76% |
| bridge_highway_direction | 99.67% |
| facility_type | 99.41% |
| bridge_highway_segment | 99.34% |
| bridge_highway_name | 99.34% |
| taxi_pick_up_location | 99.03% |

### 2.2 Conditional Null Columns
The following columns have high null rates but are not randomly missing.
They are only populated for specific complaint types:

| Column | Null Rate | Notes |
|--------|-----------|-------|
| descriptor_2 | 55.6% | Specialty field, kept but excluded from analysis |
| landmark | 45.8% | Only populated for park-related complaints |
| intersection_street_1/2 | ~39% | Populated when no street address exists |
| cross_street_1/2 | ~35% | Same as above |

### 2.3 Date Columns
`created_date` and `closed_date` were stored as strings in ISO format.
Both converted to datetime.

### 2.4 Categorical Issues
| Column | Issue Found |
|--------|-------------|
| complaint_type | Mixed casing (ALL CAPS vs Title Case) |
| borough | Contained "Unspecified" values |
| status | Contained "Unspecified" values |
| city | Inconsistent — neighborhoods listed as cities, "NEW YORK" and "MANHATTAN" overlap. Excluded from analysis, borough used instead |

### 2.5 Duplicates
- Full duplicate rows: 0
- Duplicate unique_key: 0

---

## 3. Cleaning Steps

### Step 1 — Drop High-Null Columns
**Action:** Dropped 9 columns with 99%+ null rate  
**Reason:** No analytical value, specialty fields irrelevant to general analysis  

### Step 2 — Drop Unspecified Values
**Action:** Dropped rows where borough or status == "Unspecified"  
**Rows before:** 150,000  
**Rows after:** 147,117  
**Rows removed:** 2,883 (1.9%)  
**Reason:** Unspecified values provide no analytical value and represent a negligible portion of the dataset  

### Step 3 — Standardize Casing
**Action:** Applied `.str.title()` to `complaint_type`  
**Reason:** Inconsistent casing would cause duplicate categories in any groupby analysis  

### Step 4 — Convert Date Columns
**Action:** Converted `created_date` and `closed_date` from string to datetime  
**Reason:** Required for time-based calculations  

### Step 5 — Engineer Resolution Time
**Action:** Created `resolution_time = closed_date - created_date`  
**Reason:** Adds analytical value — measures agency response speed  

### Step 6 — Drop Negative Resolution Times
**Action:** Dropped rows where `resolution_time` < 0  
**Rows removed:** 1,019  
**Reason:** Data error — closed_date cannot precede created_date  

---

## 4. Final Validation

| Check | Result |
|-------|--------|
| Final row count | 146064 |
| Duplicate unique_key | 0 |
| Negative resolution times | 0 |
| Date range | Jan 1 – Jan 20, 2023 |
| Null rate — core columns | 0% |

---

## 5. Known Limitations

- Dataset covers January 1–20 2023 only due to API row cap of 300,000
- `city` column excluded from analysis due to inconsistent granularity
- `descriptor_2` retained but excluded from analysis — 55.6% null
- Negative resolution times dropped rather than investigated — likely upstream data entry errors

---

## 6. Output

**File:** `nyc311_clean.csv`  
**Rows:** 146098 
**Columns:** 35  
**Location:** `/data/nyc311_clean.csv`