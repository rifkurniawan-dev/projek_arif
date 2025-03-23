import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


sns.set(style='dark')

def create_seasonal_influence(df):
    seasonal_influence = df.groupby("season_x")["cnt_x"].sum().reset_index()
    seasonal_influence.rename(columns={
        "cnt_x": "Total Penyewaan Sepeda",
        "season_x": "Musim"
    }, inplace=True)
    
    musim_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    seasonal_influence['Musim'] = seasonal_influence['Musim'].map(musim_mapping)
    seasonal_influence['Musim'] = pd.Categorical(
        seasonal_influence['Musim'],
        categories=["Musim Dingin", "Musim Semi", "Musim Panas", "Musim Gugur"],
        ordered=True
    )
    return seasonal_influence


def create_weather_influence(df):
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    
    df['weathersit_description'] = df['weathersit_x'].map(weather_mapping)
    
    weather_influence = df.groupby('weathersit_description')[['temp_x', 'atemp_x', 'cnt_x']].mean().sort_values(by=['cnt_x'], ascending=False).reset_index()
    weather_influence.columns = ['Kondisi Cuaca', 'Rata-rata Suhu', 'Rata-rata Suhu Terasa', 'Rata-rata Penyewaan Sepeda']
    
    return weather_influence


# Load data
hour_day_df = pd.read_csv("dashboard/hour_day.csv")


# Mengonversi kolom tanggal menjadi tipe datetime
hour_day_df['dteday_x'] = pd.to_datetime(hour_day_df['dteday_x'])

# Mengurutkan dan mengatur ulang indeks data
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Rentang waktu data
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

# Sidebar dengan rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    
    # Menggunakan widget date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        key='rentang_waktu'
    )
    
# Filter data berdasarkan rentang waktu yang dipilih
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
]

# Analisis Musim dan Cuaca
seasonal_influence = create_seasonal_influence(main_df)
weather_influence = create_weather_influence(main_df)


# Menampilkan Header
st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Metrik Total Penyewaan dan Pendapatan
col1, col2 = st.columns(2)
with col1:
    total_penyewa = main_df['cnt_x'].sum()
    st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
    st.metric('Total Pendapatan', value=total_pendapatan)


# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="Musim",
    y="Total Penyewaan Sepeda",
    data=seasonal_influence.sort_values(by="Musim"),
    palette=colors_,
    ax=ax
)

ax.set_title("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda", fontsize=15)
ax.set_ylabel("Total Penyewaan Sepeda", fontsize=12)
ax.set_xlabel("Musim", fontsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)


# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
col1, col2, col3 = st.columns(3)

with col1:
    avg_temp = round(main_df['temp_x'].mean(), 2)
    st.metric("Rata-rata Suhu (°C)", value=f"{avg_temp} °C")

with col2:
    avg_atemp = round(main_df['atemp_x'].mean(), 2)
    st.metric("Rata-rata Suhu Terasa (°C)", value=f"{avg_atemp} °C")

with col3:
    avg_cnt = round(main_df['cnt_x'].mean(), 0)
    st.metric("Rata-rata Penyewaan Sepeda", value=int(avg_cnt))
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(
    x='weathersit_description',
    y='cnt_x',
    data=main_df,
    palette='Oranges',
    ax=ax
)

ax.set_title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
ax.set_xlabel('Kondisi Cuaca', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)
