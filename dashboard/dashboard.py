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
    try:
        # Hanya lakukan pemrosesan jika data berhasil dimuat
        data['dteday_x'] = pd.to_datetime(data['dteday_x'], errors='coerce')
        data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')

        # Tangani nilai yang hilang setelah konversi
        data = data.dropna(subset=['dteday_x'])

        # Pastikan kolom 'hr' ada dan dalam format yang sesuai
        data['hr'] = data['hr'].fillna(0).astype(int)

        # Membuat kolom datetime dari 'dteday_x' dan 'hr'
        data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')

        # Mencari rentang waktu data
        min_date = data["dteday_x"].min().date() if not data["dteday_x"].isna().all() else None
        max_date = data["dteday_x"].max().date() if not data["dteday_x"].isna().all() else None

        if min_date and max_date:
            # Sidebar untuk filter tanggal
            with st.sidebar:
                st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
                start_date, end_date = st.date_input(
                    'Rentang Waktu',
                    min_value=min_date,
                    max_value=max_date,
                    value=[min_date, max_date]
                )
        else:
            st.error("Rentang tanggal tidak valid. Pastikan data yang diupload mengandung kolom tanggal yang valid.")

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam pemrosesan data: {e}")

else:
    st.error("Data gagal dimuat. Pastikan file day.csv dan hour.csv tersedia di folder data.")


# Konversi start_date dan end_date menjadi datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
# Filter data
filtered_data = data[(data["dteday_x"] >= start_date) & (data["dteday_x"] <= end_date)]
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

plt.figure(figsize=(10, 5))
sns.barplot(
    x='dteday_x',
    y='day_count',
    hue='season',
    data=monthly_day_df,
    palette="Set2"
)
plt.title("Jumlah Penyewaan Sepeda per Musim dan Bulan (2011-2012)", loc="center", fontsize=20)
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Jumlah Penyewaan", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
st.plot()


plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=hour_df, color="#72BCD4")
plt.title('Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
plt.xlabel('Musim', fontsize=14)
plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=14)
plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])
st.plot()


"""bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda"""

bygeder_df = hour_day_df.groupby(by="weathersit_x").cnt_x.sum().reset_index()
bygeder_df.rename(columns={
    "cnt_x": "total_rentals"
}, inplace=True)
bygeder_df

plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit_x', y='cnt_x', data=hour_day_df, hue='weathersit_x', palette="Blues", dodge=False, legend=False)
plt.title("Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda", fontsize=20)
plt.xlabel("Kondisi Cuaca", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.xticks(rotation=30, fontsize=10)
plt.yticks(fontsize=10)
st.plot()
