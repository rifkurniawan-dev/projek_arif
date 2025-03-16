import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

def load_data():
    day_df = 'data/day.csv'
    hour_df = 'data/hour.csv'
    
    try:
        if os.path.exists(day_df) and os.path.exists(hour_df):
            day_df = pd.read_csv(day_df)
            hour_df = pd.read_csv(hour_df)
            merged_df = pd.merge(hour_df, day_df, how="outer", on="instant")
            return merged_df
        else:
            st.error("One or both of the required files (day.csv or hour.csv) are missing.")
            return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None
# Memuat data
data = load_data()
if data is not None:
    # Properly indent this block of code
    data['dteday_x'] = pd.to_datetime(data['dteday_x'], errors='coerce')
    data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')
    
# Pastikan kolom 'dteday_x' dalam format datetime
# Cek apakah ada nilai yang tidak dapat dikonversi
data['dteday_x'] = pd.to_datetime(data['dteday_x'], errors='coerce')

# Tangani nilai yang hilang setelah konversi, misalnya dengan menghapus baris yang memiliki nilai NaT
data = data.dropna(subset=['dteday_x'])

# Pastikan kolom 'hr' ada dan dalam format yang sesuai
data['hr'] = data['hr'].fillna(0).astype(int)

# Membuat kolom datetime dari 'dteday_x' dan 'hr'
data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')

# Mencari rentang waktu data
min_date = pd.to_datetime(data["dteday_x"].min()).date()
max_date = pd.to_datetime(data["dteday_x"].max()).date()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    if min_date and max_date:  # Mengecek apakah min_date dan max_date berhasil ditemukan
        start_date, end_date = st.date_input(
            'Rentang Waktu', 
            min_value=min_date, 
            max_value=max_date, 
            value=[min_date, max_date]  # Pastikan ini sesuai dengan format datetime.date
        )
# Memfilter data berdasarkan rentang waktu yang dipilih
filtered_data = data[(data["dteday_x"] >= pd.to_datetime(start_date)) & (data["dteday_x"] <= pd.to_datetime(end_date))]

# Fungsi pembantu untuk membuat DataFrame penyewaan harian
def create_daily_rentals_df(df):
    # Gunakan resample dengan 'dteday_x' yang sudah dalam format datetime
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
