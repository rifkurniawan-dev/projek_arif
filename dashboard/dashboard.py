import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

# Fungsi untuk memuat data
def load_data():
    if not (os.path.exists("day.csv") and os.path.exists("hour.csv")):
        st.error("File 'day.csv' dan/atau 'hour.csv' tidak ditemukan. Unggah file di bawah ini.")
        day_file = st.file_uploader("Unggah file day.csv", type=["csv"])
        hour_file = st.file_uploader("Unggah file hour.csv", type=["csv"])
        
        if day_file is None or hour_file is None:
            st.stop()
        
        day_df = pd.read_csv(day_file)
        hour_df = pd.read_csv(hour_file)
    else:
        day_df = pd.read_csv("day.csv")
        hour_df = pd.read_csv("hour.csv")

    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    
    # Menggabungkan kedua dataframe
    merged_df = pd.merge(hour_df, day_df, how="outer", on="instant")
    
    return merged_df

# Memuat data
data = load_data()

# Membuat kolom datetime dari dteday_x dan hr
data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')

# Mencari rentang waktu data
min_date = data["dteday_x"].min()
max_date = data["dteday_x"].max()

# Sidebar untuk filter tanggal
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input('Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date])

# Memfilter data berdasarkan rentang waktu yang dipilih
filtered_data = data[(data["dteday_x"] >= str(start_date)) & (data["dteday_x"] <= str(end_date))]

# Fungsi pembantu untuk membuat DataFrame penyewaan harian
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday_x').agg({
        "instant": "nunique",
        "cnt_x": "sum"
    }).reset_index()
    
    daily_rentals_df.rename(columns={
        "instant": "rental_count",
        "cnt_x": "revenue"
    }, inplace=True)
    
    return daily_rentals_df

# Fungsi untuk penyewaan berdasarkan musim
def create_byseason_df(df):
    byseason_df = df.groupby(by="season_x").instant.nunique().reset_index()
    byseason_df.rename(columns={"instant": "rental_count"}, inplace=True)
    return byseason_df

# Fungsi untuk penyewaan berdasarkan cuaca
def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit_x").instant.nunique().reset_index()
    byweather_df.rename(columns={"instant": "rental_count"}, inplace=True)
    return byweather_df

# Membuat DataFrame yang dibutuhkan
daily_rentals_df = create_daily_rentals_df(filtered_data)
byseason_df = create_byseason_df(filtered_data)
byweather_df = create_byweather_df(filtered_data)

# Bagian utama dashboard
st.header('Dashboard Analisis Penyewaan Sepeda :sparkles:')

col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df['rental_count'].sum()
    st.metric("Total Penyewaan", value=total_rentals)

with col2:
    total_revenue = format_currency(daily_rentals_df['revenue'].sum(), "USD", locale='en_US')
    st.metric("Total Pendapatan", value=total_revenue)

# Plot Tren Penyewaan Harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_rentals_df["dteday_x"], daily_rentals_df["rental_count"], marker='o', linewidth=2, color="#90CAF9")
ax.set_title("Tren Penyewaan Harian", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
st.pyplot(fig)

st.subheader("Pengaruh Musim dan Cuaca")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="season_x", y="rental_count", data=byseason_df, palette="Set2", ax=ax)
    ax.set_title("Jumlah Penyewaan Berdasarkan Musim", fontsize=16)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="weathersit_x", y="rental_count", data=byweather_df, palette="Blues", ax=ax)
    ax.set_title("Jumlah Penyewaan Berdasarkan Cuaca", fontsize=16)
    st.pyplot(fig)
