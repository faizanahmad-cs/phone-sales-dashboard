import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(
    page_title="Phone Sales Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS for a more professional look ----------
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1c2333 0%, #161a23 100%);
        border: 1px solid #2a3040;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 6px;
    }
    .metric-label {
        font-size: 13px;
        color: #9aa4b2;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #FAFAFA;
    }
    .metric-sub {
        font-size: 12px;
        color: #6b7280;
        margin-top: 2px;
    }
    .insight-box {
        background: rgba(255, 75, 75, 0.08);
        border-left: 4px solid #FF4B4B;
        border-radius: 6px;
        padding: 14px 18px;
        margin-top: 10px;
    }
    div[data-testid="stMetricValue"] { font-size: 26px; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 Top-Selling Phones by Company — Year-wise Analytics")
st.caption("Tracks company-wise phone sales trends and forecasts next year's demand.")

# ---------- Load data ----------
@st.cache_data
def load_data():
    return pd.read_csv("phone_sales.csv")

df = load_data()

# ---------- Sidebar filters ----------
with st.sidebar:
    st.header("🔎 Filters")
    year_min, year_max = int(df.year.min()), int(df.year.max())
    year_range = st.slider("Year range", year_min, year_max, (year_min, year_max))

    all_companies = sorted(df.company.unique())
    selected_companies = st.multiselect("Companies", all_companies, default=all_companies)

    st.divider()
    metric_choice = st.radio("Rank companies by", ["Units Sold", "Revenue"], horizontal=False)
    st.divider()
    st.caption("Data is synthetic, generated for demo purposes.")

filtered = df[
    (df.year.between(year_range[0], year_range[1]))
    & (df.company.isin(selected_companies))
]

if filtered.empty:
    st.warning("No data for the selected filters. Adjust the sidebar options.")
    st.stop()

metric_col = "units_sold" if metric_choice == "Units Sold" else "revenue"

# ---------- Forecast logic (linear trend) ----------
def predict_next_year(company_df: pd.DataFrame, col: str) -> float:
    x = company_df["year"].values
    y = company_df[col].values
    if len(x) < 2:
        return float(y[-1])
    coeffs = np.polyfit(x, y, 1)
    next_year = x.max() + 1
    predicted = np.polyval(coeffs, next_year)
    return max(predicted, 0)

def growth_rate(company_df: pd.DataFrame) -> float:
    """Average year-over-year % growth in units sold."""
    company_df = company_df.sort_values("year")
    pct = company_df["units_sold"].pct_change().dropna()
    return pct.mean() * 100 if len(pct) else 0.0

pred_rows, growth_rows = [], []
for company in df.company.unique():
    cdf = df[df.company == company]
    pred_rows.append({
        "company": company,
        "predicted_year": int(cdf.year.max() + 1),
        "predicted_units": int(predict_next_year(cdf, "units_sold")),
        "predicted_revenue": predict_next_year(cdf, "revenue"),
    })
    growth_rows.append({"company": company, "avg_yoy_growth_%": round(growth_rate(cdf), 1)})

pred_df = pd.DataFrame(pred_rows)
growth_df = pd.DataFrame(growth_rows).sort_values("avg_yoy_growth_%", ascending=False)

# ---------- KPI row (custom styled cards) ----------
total_units = filtered.units_sold.sum()
total_revenue = filtered.revenue.sum()
top_company = filtered.groupby("company").units_sold.sum().idxmax()
fastest_grower = growth_df.iloc[0]
fastest_grower_rate = fastest_grower["avg_yoy_growth_%"]

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "Total Units Sold", f"{total_units:,.0f}", None),
    (c2, "Total Revenue", f"${total_revenue:,.0f}", None),
    (c3, "Top Company (units)", top_company, "Highest total volume in range"),
    (c4, "Fastest Growing", f"{fastest_grower.company}", f"+{fastest_grower_rate:.1f}% avg YoY growth"),
]
for col, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-sub">{sub}</div>' if sub else ''}
        </div>
        """, unsafe_allow_html=True)

st.markdown(
    f'<div class="insight-box">ℹ️ <b>Note:</b> "Fastest Growing" ranks companies by average '
    f'<i>percentage</i> year-over-year growth — a smaller company can top this even if a '
    f'bigger company (like the Top Company) sells far more total units. See the '
    f'<b>Growth Rates</b> tab for the full comparison.</div>',
    unsafe_allow_html=True,
)

st.write("")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Share", "🔥 Heatmap", "🔮 Predictions", "⚡ Growth Rates"])

with tab1:
    st.subheader("Market Share Evolution")
    fig1 = px.area(
        filtered, x="year", y=metric_col, color="company",
        title=f"{metric_choice} by Company Over Time",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig1.update_layout(hovermode="x unified", legend_title_text="")
    st.plotly_chart(fig1, use_container_width=True)

    fig1b = px.line(
        filtered, x="year", y=metric_col, color="company", markers=True,
        title=f"{metric_choice} Trend Lines",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig1b.update_layout(legend_title_text="")
    st.plotly_chart(fig1b, use_container_width=True)

with tab2:
    st.subheader("Company × Year Sales Heatmap")
    pivot = filtered.pivot_table(index="company", columns="year", values=metric_col, aggfunc="sum")
    fig2 = px.imshow(
        pivot, text_auto=".2s", aspect="auto",
        color_continuous_scale="Reds",
        labels=dict(color=metric_choice),
        template="plotly_dark",
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    year_label = int(pred_df.predicted_year.iloc[0])
    st.subheader(f"Forecast for {year_label}")
    st.caption("Linear-trend projection based on each company's full historical sales (not affected by sidebar filters).")

    pred_sorted = pred_df.sort_values("predicted_units", ascending=False)
    fig3 = px.bar(
        pred_sorted, x="company", y="predicted_units", color="company",
        text_auto=".2s", template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Predicted Units Sold — {year_label}",
    )
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    # Historical + forecast overlay for the top predicted company
    top_pred_company = pred_sorted.iloc[0]["company"]
    hist = df[df.company == top_pred_company].sort_values("year")
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=hist.year, y=hist.units_sold, mode="lines+markers", name="Actual"))
    fig4.add_trace(go.Scatter(
        x=[hist.year.max(), year_label],
        y=[hist.units_sold.iloc[-1], pred_sorted.iloc[0]["predicted_units"]],
        mode="lines+markers", name="Forecast", line=dict(dash="dash"),
    ))
    fig4.update_layout(
        title=f"{top_pred_company}: Historical Trend + {year_label} Forecast",
        template="plotly_dark", hovermode="x unified",
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.dataframe(
        pred_sorted.rename(columns={
            "company": "Company", "predicted_year": "Forecast Year",
            "predicted_units": "Predicted Units", "predicted_revenue": "Predicted Revenue ($)"
        }),
        use_container_width=True, hide_index=True,
    )

with tab4:
    st.subheader("Average Year-over-Year Growth Rate (%)")
    st.caption("This is % growth, not absolute volume — a useful complement to the Predictions tab.")
    fig5 = px.bar(
        growth_df, x="company", y="avg_yoy_growth_%", color="avg_yoy_growth_%",
        color_continuous_scale="RdYlGn", template="plotly_dark",
        text_auto=".1f",
    )
    fig5.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig5, use_container_width=True)
    st.dataframe(growth_df.rename(columns={"company": "Company", "avg_yoy_growth_%": "Avg YoY Growth (%)"}),
                 use_container_width=True, hide_index=True)

st.divider()

# ---------- Auto-generated insight text ----------
top_pred = pred_df.sort_values("predicted_units", ascending=False).iloc[0]
st.markdown(f"""
<div class="insight-box">
📌 <b>Insight:</b> Based on current trends, <b>{top_pred.company}</b> is projected to lead by volume with
approximately <b>{top_pred.predicted_units:,.0f} units</b> in {int(top_pred.predicted_year)}, while
<b>{fastest_grower.company}</b> is growing fastest in percentage terms
(<b>+{fastest_grower_rate:.1f}%</b> avg YoY).
</div>
""", unsafe_allow_html=True)

st.caption("Built with Streamlit · Data is synthetic, generated for demo purposes ")