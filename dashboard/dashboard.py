# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import warnings

# Mengabaikan peringatan agar tampilan lebih bersih
warnings.filterwarnings("ignore", category=FutureWarning)

sns.set(style='dark')

# Asumsikan `hour_day_df` sudah ada di memori
if 'hour_day_df' not in locals():
    st.error("❌ DataFrame 'hour_day_df' tidak ditemukan. Pastikan sudah dimuat sebelumnya.")
    st.stop()

# Konversi kolom tanggal ke tipe datetime
try:
    hour_day_df["dteday_x"] = pd.to_datetime(hour_day_df["dteday_x"])
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat mengonversi kolom 'dteday_x' menjadi datetime: {e}")
    st.stop()

# Mengurutkan dan mereset index berdasarkan tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

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
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
]

st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Menampilkan metrik total penyewaan dan pendapatan
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_penyewa = main_df['cnt_x'].sum()
        st.metric("Total Penyewa", value=total_penyewa)
with col2:
    if 'cnt_x' in main_df.columns:
        total_pendapatan = format_currency(main_df['cnt_x'].sum(), 'USD', locale='en_US')
        st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda (Data Terintegrasi dengan Rentang Tanggal)
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')

main_df['Musim'] = main_df['season_x'].map({
    1: 'Musim Dingin',
    2: 'Musim Semi',
    3: 'Musim Panas',
    4: 'Musim Gugur'
})

# Mengelompokkan data berdasarkan musim dari main_df yang sudah difilter oleh rentang tanggal
seasonal_influence = main_df.groupby('Musim')['cnt_x'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='Musim', y='cnt_x', data=seasonal_influence, palette="Blues")
plt.title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
plt.xlabel('Musim', fontsize=14)
plt.ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf() 

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda (Data Terintegrasi dengan Rentang Tanggal)
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')

main_df['Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df)
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf() 
