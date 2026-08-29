"""
STEP 1: Generate synthetic phone sales data.
Run this file first: python generate_data.py
It creates 'phone_sales.csv' in the same folder.
"""

import numpy as np
import pandas as pd

np.random.seed(42)  # keeps results consistent every time you run it

# ---- Settings you can tweak ----
companies = ['Apple', 'Samsung', 'Xiaomi', 'Vivo', 'Oppo', 'OnePlus', 'Google', 'Realme']
years = list(range(2019, 2026))  # 2019 to 2025

# Each company gets a random "starting size" and a random growth/decline trend
company_profile = {}
for company in companies:
    base_units = np.random.randint(3_000_000, 20_000_000)   # starting yearly units
    yearly_growth = np.random.uniform(-0.05, 0.20)           # -5% to +20% growth per year
    base_price = np.random.randint(150, 1000)                # average price in $
    company_profile[company] = {
        'base_units': base_units,
        'growth': yearly_growth,
        'base_price': base_price
    }

records = []
for company in companies:
    profile = company_profile[company]
    for i, year in enumerate(years):
        # units grow/shrink each year based on the trend, plus small random noise
        units = profile['base_units'] * ((1 + profile['growth']) ** i)
        units = units * np.random.uniform(0.92, 1.08)  # add noise
        units = int(max(units, 0))

        # price drifts slightly upward each year, plus noise
        price = profile['base_price'] * (1 + 0.03 * i) * np.random.uniform(0.95, 1.05)
        price = round(price, 2)

        revenue = round(units * price, 2)

        records.append({
            'company': company,
            'year': year,
            'units_sold': units,
            'avg_price': price,
            'revenue': revenue
        })

df = pd.DataFrame(records)
df.to_csv('phone_sales.csv', index=False)

print("Done! 'phone_sales.csv' created with", len(df), "rows.")
print(df.head(10))