import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sales Analytics & Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

# Connect to SQLite database
@st.cache_data
def load_data():
    conn = sqlite3.connect("database/superstore.db")
    
    # Query monthly summary
    df_summary = pd.read_sql_query("SELECT * FROM monthly_sales_summary", conn)
    
    # Query forecasts if available
    try:
        df_forecast = pd.read_sql_query("SELECT * FROM sales_forecasts", conn)
    except:
        df_forecast = pd.DataFrame()
        
    conn.close()
    return df_summary, df_forecast

df_summary, df_forecast = load_data()

st.title("📊 Retail Sales Analytics & Demand Forecasting")
st.markdown("Interactive dashboard querying live data directly from **SQLite** database.")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_category = st.sidebar.multiselect(
    "Select Category:",
    options=df_summary["category"].unique(),
    default=df_summary["category"].unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region:",
    options=df_summary["region"].unique(),
    default=df_summary["region"].unique()
)

# Apply filters
df_filtered = df_summary[
    (df_summary["category"].isin(selected_category)) & 
    (df_summary["region"].isin(selected_region))
]

# --- KPI METRICS CARDS ---
st.divider()
col1, col2, col3, col4 = st.columns(4)

total_sales = df_filtered["total_sales"].sum()
total_profit = df_filtered["total_profit"].sum()
total_orders = df_filtered["total_orders"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# --- CHARTS SECTION ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Monthly Revenue Trend")
    df_trend = df_filtered.groupby("sales_month")["total_sales"].sum().reset_index()
    fig_trend = px.line(
        df_trend, 
        x="sales_month", 
        y="total_sales", 
        markers=True,
        labels={"sales_month": "Month", "total_sales": "Revenue ($)"}
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("Sales by Category")
    df_cat = df_filtered.groupby("category")["total_sales"].sum().reset_index()
    fig_cat = px.pie(
        df_cat, 
        values="total_sales", 
        names="category", 
        hole=0.4
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# --- FORECASTING SECTION ---
st.divider()
st.subheader("🔮 Demand Forecast vs Actuals")

if not df_forecast.empty:
    fig_forecast = px.line(
        df_forecast, 
        x="sales_month", 
        y="forecast_sales", 
        color="type",
        line_dash="type",
        markers=True,
        labels={"sales_month": "Month", "forecast_sales": "Sales ($)", "type": "Type"}
    )
    st.plotly_chart(fig_forecast, use_container_width=True)
else:
    st.info("Run the forecasting cell inside your Jupyter Notebook to generate predictions into SQLite.")

# --- RAW SQL QUERY EXPLORER ---
st.divider()
with st.expander("🔍 SQL Query Playground (Query SQLite Live)"):
    user_query = st.text_area(
        "Enter custom SQL Query against 'superstore.db':",
        "SELECT sales_month, category, SUM(total_sales) as sales FROM monthly_sales_summary GROUP BY sales_month, category LIMIT 10;"
    )
    if st.button("Run SQL Query"):
        try:
            conn = sqlite3.connect("database/superstore.db")
            query_result = pd.read_sql_query(user_query, conn)
            conn.close()
            st.dataframe(query_result)
        except Exception as e:
            st.error(f"SQL Error: {e}")