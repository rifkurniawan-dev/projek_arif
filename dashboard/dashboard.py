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
st.subheader("Tren Penyewaan Harian")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="dteday_x", y="rental_count", data=daily_rentals_df, marker='o', color="#90CAF9", ax=ax)
ax.set_title("Tren Penyewaan Harian", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.grid(True, which='both', linestyle='--', linewidth=0.7)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Pengaruh Musim dan Cuaca")
col1, col2 = st.columns(2)

with col1:
    if not byseason_df.empty:
        # Pemetaan nama musim
        season_mapping = {
            1: "Musim Dingin", 
            2: "Musim Semi", 
            3: "Musim Panas", 
            4: "Musim Gugur"
        }
        
        # Menambahkan kolom label musim
        byseason_df["season_label"] = byseason_df["season_x"].map(season_mapping)
        
        # Membuat empat diagram perbandingan untuk setiap musim
        fig, ax = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=20)

        # Diagram 1: Musim Dingin
        sns.barplot(x='season_label', y='rental_count', data=byseason_df[byseason_df['season_x'] == 1], ax=ax[0, 0], color="#90CAF9")
        ax[0, 0].set_title('Musim Dingin')
        ax[0, 0].set_xlabel('Musim')
        ax[0, 0].set_ylabel('Jumlah Penyewaan')
        ax[0, 0].set_xticklabels(['Musim Dingin'], rotation=45)

        # Diagram 2: Musim Semi
        sns.barplot(x='season_label', y='rental_count', data=byseason_df[byseason_df['season_x'] == 2], ax=ax[0, 1], color="#FFEB3B")
        ax[0, 1].set_title('Musim Semi')
        ax[0, 1].set_xlabel('Musim')
        ax[0, 1].set_ylabel('Jumlah Penyewaan')
        ax[0, 1].set_xticklabels(['Musim Semi'], rotation=45)

        # Diagram 3: Musim Panas
        sns.barplot(x='season_label', y='rental_count', data=byseason_df[byseason_df['season_x'] == 3], ax=ax[1, 0], color="#F44336")
        ax[1, 0].set_title('Musim Panas')
        ax[1, 0].set_xlabel('Musim')
        ax[1, 0].set_ylabel('Jumlah Penyewaan')
        ax[1, 0].set_xticklabels(['Musim Panas'], rotation=45)

        # Diagram 4: Musim Gugur
        sns.barplot(x='season_label', y='rental_count', data=byseason_df[byseason_df['season_x'] == 4], ax=ax[1, 1], color="#8BC34A")
        ax[1, 1].set_title('Musim Gugur')
        ax[1, 1].set_xlabel('Musim')
        ax[1, 1].set_ylabel('Jumlah Penyewaan')
        ax[1, 1].set_xticklabels(['Musim Gugur'], rotation=45)

        st.pyplot(fig)  # Menampilkan plot dengan empat perbandingan
    else:
        st.warning("Data untuk penyewaan berdasarkan musim tidak tersedia.")

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="weathersit_x", y="rental_count", data=byweather_df, palette="Blues", ax=ax)
    ax.set_title("Jumlah Penyewaan Berdasarkan Cuaca", fontsize=16)
    ax.set_xlabel("Cuaca", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)
