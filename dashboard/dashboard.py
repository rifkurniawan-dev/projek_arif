import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Load data
dashboard = ("dashboard/hour_day.csv")
if os.path.exists(dashboard):
    hour_day_df = pd.read_csv(dashboard)
else:
    st.error(f"❌ File '{dashboard}' tidak ditemukan. Pastikan file ada di folder yang benar.")
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
st.subheader('Pengaruh Musim & Cuaca terhadap Penyewaan Sepeda')

# Menampilkan metrik
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_orders = main_df['cnt_x'].sum() 
        st.metric("Total Penyewaan", value=total_orders)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

with col2:
    if 'cnt_x' in main_df.columns:
        total_pendapatan = format_currency(main_df['cnt_x'].sum(), 'USD', locale='en_US')
        st.metric('Total Pendapatan', value=total_pendapatan)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

# Visualisasi pengaruh musim
st.subheader('Pengaruh Musim terhadap Penyewaan Sepeda')
if not seasonal_influence.empty:
    musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    seasonal_influence['Musim'] = seasonal_influence['season_x'].map(musim_mapping)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Musim', y='cnt_x', data=seasonal_influence, palette="Blues", ax=ax)
    ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
    ax.set_xlabel('Musim', fontsize=14)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")

# Visualisasi pengaruh cuaca
st.subheader('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
if not weather_influence.empty:
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_influence['Cuaca'] = weather_influence['weathersit_x'].map(weather_mapping)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Cuaca', y='cnt_x', data=weather_influence, palette="Oranges", ax=ax)
    ax.set_title('Pengaruh Cuaca Terhadap Penyewaan Sepeda', fontsize=16)
    ax.set_xlabel('Cuaca', fontsize=14)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Load data
dashboard = "hour_day.csv"
if os.path.exists(dashboard):
    hour_day_df = pd.read_csv(dashboard)
else:
    st.error(f"❌ File '{dashboard}' tidak ditemukan. Pastikan file ada di folder yang benar.")
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
st.subheader('Pengaruh Musim & Cuaca terhadap Penyewaan Sepeda')

# Menampilkan metrik
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_orders = main_df['cnt_x'].sum() 
        st.metric("Total Penyewaan", value=total_orders)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

with col2:
    if 'cnt_x' in main_df.columns:
        total_pendapatan = format_currency(main_df['cnt_x'].sum(), 'USD', locale='en_US')
        st.metric('Total Pendapatan', value=total_pendapatan)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

# Visualisasi pengaruh musim
st.subheader('Pengaruh Musim terhadap Penyewaan Sepeda')
if not seasonal_influence.empty:
    musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    seasonal_influence['Musim'] = seasonal_influence['season_x'].map(musim_mapping)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Musim', y='cnt_x', data=seasonal_influence, palette="Blues", ax=ax)
    ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
    ax.set_xlabel('Musim', fontsize=14)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")

# Visualisasi pengaruh cuaca
st.subheader('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
if not weather_influence.empty:
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_influence['Cuaca'] = weather_influence['weathersit_x'].map(weather_mapping)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Cuaca', y='cnt_x', data=weather_influence, palette="Oranges", ax=ax)
    ax.set_title('Pengaruh Cuaca Terhadap Penyewaan Sepeda', fontsize=16)
    ax.set_xlabel('Cuaca', fontsize=14)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Load data
dashboard = "hour_day.csv"
if os.path.exists(dashboard):
    hour_day_df = pd.read_csv(dashboard)
else:
    st.error(f"❌ File '{dashboard}' tidak ditemukan. Pastikan file ada di folder yang benar.")
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
st.subheader('Pengaruh Musim & Cuaca terhadap Penyewaan Sepeda')

# Menampilkan metrik
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_orders = main_df['cnt_x'].sum() 
        st.metric("Total Penyewaan", value=total_orders)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

with col2:
    if 'cnt_x' in main_df.columns:
        total_pendapatan = format_currency(main_df['cnt_x'].sum(), 'USD', locale='en_US')
        st.metric('Total Pendapatan', value=total_pendapatan)
    else:
        st.error("Kolom 'cnt_x' tidak ditemukan dalam main_df.")

# Visualisasi pengaruh musim
st.subheader('Pengaruh Musim terhadap Penyewaan Sepeda')
if not seasonal_influence.empty:
    musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    seasonal_influence['Musim'] = seasonal_influence['season_x'].map(musim_mapping)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Musim', y='cnt_x', data=seasonal_influence, palette="Blues", ax=ax)
    ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
    ax.set_xlabel('Musim', fontsize=14)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")

# Visualisasi pengaruh cuaca
st.subheader('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
if not weather_influence.empty:
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_influence['Cuaca'] = weather_influence['weathersit_x'].map(weather_mapping)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Cuaca', y='cnt_x', data=weather_influence, palette="Oranges", ax=ax)
    ax.set_title('Pengaruh Cuaca Terhadap Penyewaan Sepeda', fontsize=16)
    ax.set_xlabel('Cuaca', fontsize=14)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang ditemukan untuk ditampilkan.")
