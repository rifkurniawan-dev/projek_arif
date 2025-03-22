# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
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
st.subheader('Pengaruh Musim terhadap Penyewaan Sepeda')

# Membuat dua kolom
col1, col2 = st.columns(2)

with col1:
    if 'cnt_x' in main_df.columns:
        total_orders = main_df['cnt_x'].sum() 
        st.metric("Total Penyewa", value=total_orders)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

with col2:
    if 'cnt_x' in main_df.columns:
        total_pendapatan = format_currency(main_df['cnt_x'].sum(), 'USD', locale='en_US')
        st.metric('Total Pendapatan', value=total_pendapatan)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")
   st.sidebar.title('Filter Data')
    selected_season = st.sidebar.selectbox('Pilih Musim', hour_day_df['season_x'].unique())
    selected_weather = st.sidebar.selectbox('Pilih Cuaca', hour_day_df['weathersit_x'].unique())

    # Filter data based on selection
    filtered_data = hour_day_df[
        (hour_day_df['season_x'] == selected_season) & 
        (hour_day_df['weathersit_x'] == selected_weather)
    ]

    # Visualization 1: Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda
    st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
    seasonal_influence = hour_day_df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
    musim_mapping = {
        1: 'Musim Dingin',
        2: 'Musim Semi',
        3: 'Musim Panas',
        4: 'Musim Gugur'
    }
    seasonal_influence['Musim'] = seasonal_influence['season_x'].map(musim_mapping)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Musim', y='cnt_x', data=seasonal_influence, hue='Musim', dodge=False, palette="Blues")
    plt.title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
    plt.xlabel('Musim', fontsize=14)
    plt.ylabel('Total Penyewaan Sepeda', fontsize=14)
    plt.legend([], [], frameon=False)
    st.pyplot(plt)

    # Visualization 2: Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda
    st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
    weather_influence = hour_day_df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    hour_day_df['weathersit_x'] = hour_day_df['weathersit_x'].map(weather_mapping)
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='weathersit_x', y='cnt_x', data=hour_day_df)
    plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca (weathersit)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(plt)

    # Display filtered data
    st.subheader('Data yang Difilter')
    st.write(filtered_data)
