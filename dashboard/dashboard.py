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
    st.error(f"❌ File '{file_path}' tidak ditemukan. Pastikan file ada di folder 'dashboard'.")
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

# Fungsi untuk membuat seasonal influence
def create_seasonal_influence(df):
    if 'season_x' in df.columns and 'cnt_x' in df.columns:
        seasonal_influence = df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
        return seasonal_influence
    else:
        st.warning("Kolom 'season_x' atau 'cnt_x' tidak ditemukan dalam DataFrame.")
        return pd.DataFrame()

# Fungsi untuk membuat weather influence
def create_weather_influence(df):
    if 'weathersit_x' in df.columns and 'cnt_x' in df.columns:
        weather_influence = df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
        return weather_influence
    else:
        st.warning("Kolom 'weathersit_x' atau 'cnt_x' tidak ditemukan dalam DataFrame.")
        return pd.DataFrame()

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

st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')
st.subheader('Analisis Harian Penyewaan Sepeda')

# Membuat dua kolom
col1, col2 = st.columns(2)

with col1:
    if 'cnt_x' in main_df.columns:
        total_orders = main_df['cnt_x'].sum() 
        st.metric("Total Orders", value=total_orders)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

with col2:
    # Menampilkan pesan jika kolom 'revenue' tidak ditemukan
    st.warning("Kolom 'revenue' tidak ditemukan dalam main_df. Pastikan dataset sudah diolah dengan benar.")

# Menampilkan pengaruh musim terhadap penyewaan sepeda
st.subheader('Pengaruh Musim Terhadap Penyewaan Sepeda')
if not seasonal_influence.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season_x', y='cnt_x', data=seasonal_influence, palette="Blues", ax=ax)
    ax.set_title('Pengaruh Musim Terhadap Penyewaan Sepeda')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Penyewaan Sepeda')
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")

# Menampilkan pengaruh cuaca terhadap penyewaan sepeda
st.subheader('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
if not weather_influence.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit_x', y='cnt_x', data=weather_influence, palette="Oranges", ax=ax)
    ax.set_title('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
    ax.set_xlabel('Cuaca')
    ax.set_ylabel('Total Penyewaan Sepeda')
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")
