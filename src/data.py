from sodapy import Socrata
import pandas as pd

limit = 50000
offset = 0 
all_data = []
client = Socrata("data.cityofnewyork.us", None,timeout=60)

while len(all_data) < 150000:
    chunk = client.get(
        "erm2-nwe9",
        limit=limit,
        offset=offset,
        where="created_date >= '2023-01-01T00:00:00' AND created_date <= '2023-12-31T23:59:59'"
    )
    
    if not chunk:
        break
    
    all_data.extend(chunk)
    offset += limit
    print(f"Pulled {len(all_data)} rows so far...")

print(f"Done. Total rows: {len(all_data)}")

# Convert and save
df = pd.DataFrame.from_records(all_data)
df.to_csv("nyc311_2023.csv", index=False)
print("Saved to nyc311_2023.csv")