import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st  # Menggunakan alias 'st'
import os

sns.set(style='darkgrid')

# Load data
file_path = "dashboard/hour_day.csv"
if os.path.exists(file_path):
    hour_day_df = pd.read_csv(file_path)
else:
    st.error(f"File '{file_path}' tidak ditemukan. Pastikan file ada di folder 'dashboard'.")
    st.stop()

# Konversi kolom tanggal ke tipe datetime
if 'dteday_x' in hour_day_df.columns:
    hour_day_df["dteday_x"] = pd.to_datetime(hour_day_df["dteday_x"])
else:
    st.error("Kolom 'dteday_x' tidak ditemukan di dalam file CSV.")
    st.stop()

# Mengurutkan dan mereset index berdasarkan tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Fungsi untuk membuat seasonal influence
def create_seasonal_influence(df):
    seasonal_influence = df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
    return seasonal_influence

# Fungsi untuk membuat weather influence
def create_weather_influence(df):
    weather_influence = df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
    return weather_influence

# Filter rentang tanggal dari sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    
    # Mengambil rentang tanggal dari user
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data sesuai dengan rentang tanggal yang dipilih
main_df = hour_day_df[(hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
                      (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))]

# Menyiapkan data visualisasi
seasonal_influence = create_seasonal_influence(main_df)
weather_influence = create_weather_influence(main_df)

st.title("Analisis Penyewaan Sepeda")
st.subheader("Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda")
st.dataframe(seasonal_influence)

st.subheader("Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda")
st.dataframe(weather_influence)
