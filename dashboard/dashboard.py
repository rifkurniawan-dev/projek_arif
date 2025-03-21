import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency
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

        weather_mapping = {
            1: 'Cerah/Sedikit Berawan',
            2: 'Berkabut/Berawan',
            3: 'Hujan Ringan/Snow Ringan',
            4: 'Hujan Deras/Snow Lebat'
        }
        filtered_data['weathersit_x'] = filtered_data['weathersit_x'].map(weather_mapping)

        st.header('Dashboard Analisis Penyewaan Sepeda :sparkles:')

        # Pengaruh Cuaca terhadap Penyewaan
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='weathersit_x', y='cnt_x', data=filtered_data)
        plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Jumlah Penyewaan Sepeda')
        st.pyplot(plt)

    except Exception as e:
        st.error(f'Terjadi kesalahan dalam pemrosesan data: {e}')

else:
    st.error('Data gagal dimuat. Pastikan file day.csv dan hour.csv tersedia di folder data.')

