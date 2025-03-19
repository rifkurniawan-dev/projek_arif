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

data = load_data()

if data is not None:
    try:
        data['dteday_x'] = pd.to_datetime(data['dteday_x'], errors='coerce')
        data = data.dropna(subset=['dteday_x'])
        data['hr'] = data['hr'].fillna(0).astype(int)
        data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')

        min_date = data['dteday_x'].min().date()
        max_date = data['dteday_x'].max().date()

        with st.sidebar:
            st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
            start_date, end_date = st.date_input(
                'Rentang Waktu',
                min_value=min_date,
                max_value=max_date,
                value=[min_date, max_date]
            )

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_data = data[(data['dteday_x'] >= start_date) & (data['dteday_x'] <= end_date)]

        def create_daily_rentals_df(df):
            daily_rentals_df = df.resample(rule='D', on='dteday_x').agg({
                "instant": "nunique",
                "cnt_x": "sum"
            }).reset_index()

            daily_rentals_df.rename(columns={
                "instant": "rental_count",
                "cnt_x": "revenue"
            }, inplace=True)

            return daily_rentals_df

        def create_byseason_df(df):
            byseason_df = df.groupby(by="season_x").instant.nunique().reset_index()
            byseason_df.rename(columns={"instant": "rental_count"}, inplace=True)
            return byseason_df

        def create_byweather_df(df):
            byweather_df = df.groupby(by="weathersit_x").instant.nunique().reset_index()
            byweather_df.rename(columns={"instant": "rental_count"}, inplace=True)
            return byweather_df

        daily_rentals_df = create_daily_rentals_df(filtered_data)
        byseason_df = create_byseason_df(filtered_data)
        byweather_df = create_byweather_df(filtered_data)

        st.header('Dashboard Analisis Penyewaan Sepeda :sparkles:')

        col1, col2 = st.columns(2)

        with col1:
            total_rentals = daily_rentals_df['rental_count'].sum()
            st.metric("Total Penyewaan", value=total_rentals)

        with col2:
            total_revenue = format_currency(daily_rentals_df['revenue'].sum(), "USD", locale='en_US')
            st.metric("Total Pendapatan", value=total_revenue)

        # Grafik Penyewaan Harian
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='dteday_x', y='rental_count', data=daily_rentals_df, color="blue")
        plt.title(""Jumlah Penyewaan Sepeda Harian (2011-2012)", fontsize=20)
        plt.xlabel("Tanggal", fontsize=12)
        plt.ylabel("Jumlah Penyewaan", fontsize=12)
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Grafik Penyewaan Berdasarkan Musim
        plt.figure(figsize=(10, 6))
        sns.barplot(x='season_x', y='rental_count', data=byseason_df, palette="Blues")
        plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
        plt.xlabel('Musim', fontsize=14)
        plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
        plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])
        st.pyplot(plt)

        # Grafik Pengaruh Cuaca terhadap Penyewaan
        plt.figure(figsize=(10, 6))
        sns.barplot(x='weathersit_x', y='rental_count', data=byweather_df, palette="Blues")
        plt.title('Pengaruh Cuaca Terhadap Penyewaan Sepeda', fontsize=16)
        plt.xlabel('Cuaca', fontsize=14)
        plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
        plt.xticks([0, 1, 2, 3], ['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat'])
        st.pyplot(plt)

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam pemrosesan data: {e}")

else:
    st.error("Data gagal dimuat. Pastikan file day.csv dan hour.csv tersedia di folder data.")
