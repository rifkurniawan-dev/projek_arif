# -*- coding: utf-8 -*-
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

# Filter data sesuai dengan rentang tanggal yang dipilih
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
]

# Filter data berdasarkan pilihan user
filtered_data = main_df[
    (main_df['season_x'] == selected_season) & 
    (main_df['weathersit_x'] == weather_influence)
]

st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Menampilkan metrik total penyewaan dan pendapatan
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_orders = main_df['cnt_x'].sum()
        st.metric("Total Penyewa", value=total_orders)
with col2:
    if 'cnt_x' in main_df.columns:
        total_pendapatan = format_currency(main_df['cnt_x'].sum(), 'USD', locale='en_US')
        st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_influence = hour_day_df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
seasonal_influence['Musim'] = seasonal_influence['season_x'].map(musim_mapping)

plt.figure(figsize=(10, 6))
sns.barplot(x='Musim', y='cnt_x', data=seasonal_influence, palette="Blues")
plt.title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
plt.xlabel('Musim', fontsize=14)
plt.ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()  # Membersihkan plot setelah ditampilkan

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
weather_influence = hour_day_df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
weather_mapping = {
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
}
weather_influence['Cuaca'] = weather_influence['weathersit_x'].map(weather_mapping)
plt.figure(figsize=(12, 6))
sns.boxplot(x='weathersit', y='cnt', data=hour_df)
plt.title('pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca (weathersit)')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(plt)

