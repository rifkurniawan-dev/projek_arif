import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper functions

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "instant": "day_count",
        "cnt": "total_rentals"
    }, inplace=True)

    return daily_rentals_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={"cnt": "total_rentals"}, inplace=True)

    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    byweather_df.rename(columns={"cnt": "total_rentals"}, inplace=True)

    return byweather_df

def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").cnt.mean().reset_index()
    byhour_df.rename(columns={"cnt": "avg_rentals"}, inplace=True)

    return byhour_df

# Load cleaned data

hour_df = pd.read_csv("hour.csv")
day_df = pd.read_csv("day.csv")

# Convert date columns
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Filter data by date range
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input('Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date])

filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]

# Prepare dataframes

daily_rentals_df = create_daily_rentals_df(filtered_day_df)
byseason_df = create_byseason_df(filtered_day_df)
byweather_df = create_byweather_df(filtered_day_df)
byhour_df = create_byhour_df(hour_df)

# Dashboard Content

st.header('Bike Rental Dashboard :bike:')
st.subheader('Daily Rentals')

col1, col2 = st.columns(2)

with col1:
    total_days = daily_rentals_df['day_count'].sum()
    st.metric("Total Days Recorded", value=total_days)

with col2:
    total_rentals = daily_rentals_df['total_rentals'].sum()
    st.metric("Total Rentals", value=total_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_rentals_df['dteday'], daily_rentals_df['total_rentals'], marker='o', color="#90CAF9")
st.pyplot(fig)

st.subheader('Rentals by Season')
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='total_rentals', data=byseason_df, palette="Blues", ax=ax)
st.pyplot(fig)

st.subheader('Rentals by Weather Conditions')
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weathersit', y='total_rentals', data=byweather_df, palette="Blues", ax=ax)
st.pyplot(fig)

st.subheader('Average Rentals by Hour')
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='hr', y='avg_rentals', data=byhour_df, marker='o', color="#90CAF9")
st.pyplot(fig)
