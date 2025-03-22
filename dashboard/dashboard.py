import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Path file CSV
dashboard = "dashboard/hour_day.csv"

# Mengecek apakah file CSV ada atau tidak
if os.path.exists(dashboard):
    try:
        # Membaca file CSV
        hour_day_df = pd.read_csv(dashboard)
    except Exception as e:
        st.error(f" Terjadi kesalahan saat membaca file CSV: {e}")
        st.stop()
else:
    st.error(f" File '{dashboard}' tidak ditemukan. Pastikan file ada di folder 'dashboard'.")
    st.stop()

# Konversi kolom tanggal ke tipe datetime
if 'dteday_x' in hour_day_df.columns:
    try:
        hour_day_df["dteday_x"] = pd.to_datetime(hour_day_df["dteday_x"])
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengonversi kolom 'dteday_x' menjadi datetime: {e}")
        st.stop()
else:
    st.error("Kolom 'dteday_x' tidak ditemukan di dalam file CSV.")
    st.stop()

# Mengurutkan dan mereset index berdasarkan tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Mapping musim
musim_mapping = {
    1: 'Musim Dingin',
    2: 'Musim Semi',
    3: 'Musim Panas',
    4: 'Musim Gugur'
}
seasonal_influence['Musim'] = seasonal_influence['Musim'].map(musim_mapping)


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
].copy()

# Menambahkan kolom Cuaca
main_df.loc[:, 'Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Menampilkan metrik total penyewaan dan pendapatan
col1, col2 = st.columns(2)
with col1:
    if 'cnt_x' in main_df.columns:
        total_penyewa = main_df['cnt_x'].sum()
        st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    if 'cnt_x' in main_df.columns:
        try:
            total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
        except:
            total_pendapatan = "Tidak Tersedia"
        st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')

# Kelompokkan data berdasarkan musim
seasonal_influence = hour_day_df.groupby('season_x')[['cnt_x']].sum().sort_values(by='cnt_x', ascending=False).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(
    x='Musim',
    y='Total Penyewaan Sepeda',
    data=seasonal_influence,
    errorbar=None 
)
plt.title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
plt.xlabel('Musim', fontsize=14)
plt.ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf() 

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df, palette="Oranges")
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()
