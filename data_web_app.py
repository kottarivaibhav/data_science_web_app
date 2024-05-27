import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests

# Load data from the API endpoint
DATA_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

@st.cache_data
def load_data():
    response = requests.get(DATA_URL)
    data = response.json()
    df = pd.DataFrame(data)
    # Assuming the columns are named 'crash_date' and 'crash_time' in the JSON response
    df['CRASH DATE'] = pd.to_datetime(df['crash_date'])
    df['CRASH TIME'] = pd.to_datetime(df['crash_time']).dt.time
    df['CRASH DATE & TIME'] = pd.to_datetime(df['CRASH DATE'].astype(str) + ' ' + df['CRASH TIME'].astype(str))
    df.dropna(subset=['latitude', 'longitude'], inplace=True)
    return df

# Load data
data = load_data()

# Sidebar for filter options
st.sidebar.title("Filter Options")
hour = st.sidebar.slider("Select Hour of Day", 0, 23, 12)
modes = st.sidebar.multiselect("Select Mode(s) of Transportation", data['vehicle_type_code1'].unique())

# Filter data
filtered_data = data[data['CRASH DATE & TIME'].dt.hour == hour]
if modes:
    filtered_data = filtered_data[filtered_data['vehicle_type_code1'].isin(modes)]

# Map view of accidents
st.title("Motor Vehicle Collisions in NYC")
st.map(filtered_data[['latitude', 'longitude']])

# Time distribution of accidents
st.subheader("Accidents by Hour of Day")
hourly_distribution = filtered_data.groupby(filtered_data['CRASH DATE & TIME'].dt.hour).size()
st.bar_chart(hourly_distribution)

# Mode of transportation breakdown
if modes:
    st.subheader("Accidents by Mode of Transportation")
    mode_distribution = filtered_data['vehicle_type_code1'].value_counts()
    st.bar_chart(mode_distribution)

# Raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_data)
