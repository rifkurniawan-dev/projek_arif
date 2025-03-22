import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

dashboard = "dashboard/hour_day.csv"
if os.path.exists(dashboard):
    hour_day_df = pd.read_csv(dashboard)
else:
    st.error(f"❌ File '{dashboard}' tidak ditemukan. Pastikan file ada di folder 'dashboard'.")
    st.stop()

# Konversi kolom tanggal ke tipe datetime
if 'dteday_x' in hour_day_df.columns:
    hour_day_df["dteday_x"] = pd.to_datetime(hour_day_df["dteday_x"])
else:
    st.error("❌ Kolom 'dteday_x' tidak ditemukan di dalam file CSV.")
    st.stop()

# Mengurutkan dan mereset index berdasarkan tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Pemetaan musim dan cuaca
musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
weather_mapping = {
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
}

# Filter rentang tanggal dari sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    st.title('Filter Data')
    
    # Mengambil rentang tanggal dari user
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Pilih Musim
    selected_season = st.selectbox(
        'Pilih Musim',
        options=hour_day_df['season_x'].unique(),
        format_func=lambda x: musim_mapping.get(x, "Tidak Diketahui")
    )
    
    # Pilih Cuaca
    selected_weather = st.selectbox(
        'Pilih Kondisi Cuaca',
        options=hour_day_df['weathersit_x'].unique(),
        format_func=lambda x: weather_mapping.get(x, "Tidak Diketahui")
    )

# Filter data sesuai dengan rentang tanggal yang dipilih
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
]

# Filter data berdasarkan pilihan user
filtered_data = main_df[
    (main_df['season_x'] == selected_season) & 
    (main_df['weathersit_x'] == selected_weather)
]

st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Menampilkan metrik total penyewaan dan pendapatan
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_orders 
