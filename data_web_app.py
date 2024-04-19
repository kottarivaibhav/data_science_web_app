import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load data
DATA_URL = "datacrash.csv"
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    return data

# Load data
data = load_data()

# Sidebar for filter options
st.sidebar.title("Filter Options")
hour = st.sidebar.slider("Select Hour of Day", 0, 23, 12)
modes = st.sidebar.multiselect("Select Mode(s) of Transportation", data['VEHICLE_TYPE_1'].unique())

# Filter data
filtered_data = data[data['CRASH_DATE_CRASH_TIME'].dt.hour == hour]
if modes:
    filtered_data = filtered_data[filtered_data['VEHICLE_TYPE_1'].isin(modes)]

# Map view of accidents
st.title("Motor Vehicle Collisions in NYC")
st.map(filtered_data)

# Time distribution of accidents
st.subheader("Accidents by Hour of Day")
hourly_distribution = filtered_data.groupby(filtered_data['CRASH_DATE_CRASH_TIME'].dt.hour).size()
st.bar_chart(hourly_distribution)

# Mode of transportation breakdown
if modes:
    st.subheader("Accidents by Mode of Transportation")
    mode_distribution = filtered_data['VEHICLE_TYPE_1'].value_counts()
    st.bar_chart(mode_distribution)

# Raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_data)
