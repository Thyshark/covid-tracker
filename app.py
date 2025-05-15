import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="COVID-19 Global Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data  # Cache for performance
def load_data():
    return pd.read_csv('data/owid-covid-data.csv', parse_dates=['date'])

df = load_data()

# Sidebar controls
st.sidebar.header("Controls")
countries = st.sidebar.multiselect(
    "Select countries",
    df['location'].unique(),
    default=["United States", "India", "Brazil", "Germany", "Kenya"]
)

metrics = st.sidebar.selectbox(
    "Select metric",
    ["total_cases", "total_deaths", "people_vaccinated_per_hundred"]
)

# Date range selector
max_date = df['date'].max()
min_date = df['date'].min()
start_date, end_date = st.sidebar.date_input(
    "Date range",
    value=(max_date - timedelta(days=180), max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter data
filtered_df = df[
    (df['location'].isin(countries)) &
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
]

# Main content
st.title("🌍 COVID-19 Global Data Tracker")

# Metrics overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Countries", len(countries))
with col2:
    st.metric("Time Period", f"{start_date} to {end_date}")
with col3:
    st.metric("Latest Data", max_date.strftime("%Y-%m-%d"))

# Plot
fig = px.line(
    filtered_df,
    x='date',
    y=metrics,
    color='location',
    title=f"{metrics.replace('_', ' ').title()} Over Time",
    labels={metrics: metrics.replace('_', ' ').title()}
)
st.plotly_chart(fig, use_container_width=True)

# Data table
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df[['date', 'location', metrics]].sort_values('date', ascending=False))