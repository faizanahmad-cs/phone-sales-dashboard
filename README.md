# 📱 Top-Selling Phones by Company — Year-wise Analytics Dashboard

An interactive dashboard analyzing smartphone sales trends across major companies
(Apple, Samsung, Xiaomi, Vivo, Oppo, OnePlus, Google, Realme) from 2019–2025, with
year-over-year growth analysis and next-year demand forecasting.

🔗 **Live demo:** [your-streamlit-link-here](https://your-username-phone-sales-dashboard.streamlit.app)

---

## Features
- **Market Share Evolution** — units sold and revenue trends by company over time
- **Company × Year Heatmap** — instantly see which company led which year
- **Growth Rate Analysis** — ranks companies by average year-over-year % growth (distinct from total volume leaders)
- **Next-Year Forecast** — linear-trend projection with a historical + forecast overlay chart
- **Interactive Filters** — year range, company selection, and units vs. revenue toggle

## Tech Stack
| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data handling | Pandas, NumPy |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Deployment | Streamlit Community Cloud |

## Project Structure
```
phone_sales_dashboard/
├── app.py                 # Main dashboard app
├── generate_data.py       # Synthetic dataset generator
├── phone_sales.csv        # Generated dataset
├── requirements.txt       # Python dependencies
└── .streamlit/
    └── config.toml        # Dashboard theme settings
```

## Run It Locally
```bash
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```

## Notes
Sales figures are synthetically generated (via `generate_data.py`) to demonstrate the
full analytics pipeline end-to-end — the same structure can be pointed at real
sales/CRM data without any changes to the dashboard logic.
