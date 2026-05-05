## Cleaning Log

### Columns with 90% or greater null rates were dropped, as they are not statistically useful.

The columns that were dropped are:

| Name | Null Rate (%) |
|------|--------------|
| taxi_pick_up_location | 99.03 |
| facility_type | 99.41 |
| bridge_highway_name | 99.34 |
| bridge_highway_segment | 99.34 |
| road_ramp | 99.76 |
| bridge_highway_direction | 99.67 |
| vehicle_type | 99.98 |
| taxi_company_borough | 99.95 |
| due_date | 99.79 |

Since "Unspecified" data in the borough and status columns account for 449 and 35 entries respectively, they were dropped. Similarly, rows with missing longitude and latitude data were also dropped.

The `complaint_type` column contains data labeled inconsistently, where some entries were capitalized while others were not. The data was standardized using `str.title()`.

The `created_date` and `closed_date` columns were stored as strings and were converted to the `datetime` data type. These columns contain conditional null rates:

```
landmark                    45.804360
intersection_street_1       39.004330
intersection_street_2       38.900331
cross_street_1              35.295037
cross_street_2              35.206672
location_type               12.774866
```

## location_type

**Null Rate:** 12.77%

**Finding:** Nulls were mostly concentrated in infrastructure complaint types. These complaint types do not map to a traditional location type.

**Decision:** Retained as null. Exclude from analyses requiring complete location type data.
