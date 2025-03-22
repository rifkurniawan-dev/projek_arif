# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Data Cleaning
datetime_columns = ["dteday"]
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

# Merge data
day_hour_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="outer",
    left_on="instant",
    right_on="instant"
)

# Streamlit App
st.title('Proyek Analisis Data: E-Commerce Public Dataset')
st.write('**Nama:** Arif Kurniawan')
st.write('**Email:** m299d5y1908@student.devacaademy.id')
st.write('**ID Dicoding:** MC299D5Y1908')

# Sidebar
st.sidebar.title('Filter Data')
selected_season = st.sidebar.selectbox('Pilih Musim', day_hour_df['season_x'].unique())
selected_weather = st.sidebar.selectbox('Pilih Cuaca', day_hour_df['weathersit_x'].unique())

# Filter data based on selection
filtered_data = day_hour_df[(day_hour_df['season_x'] == selected_season) & (day_hour_df['weathersit_x'] == selected_weather)]

# Visualization 1: Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_influence = day_hour_df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
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
weather_influence = day_hour_df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
weather_mapping = {
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
}
day_hour_df['weathersit_x'] = day_hour_df['weathersit_x'].map(weather_mapping)
plt.figure(figsize=(12, 6))
sns.boxplot(x='weathersit_x', y='cnt_x', data=day_hour_df)
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca (weathersit)')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(plt)

# Display filtered data
st.subheader('Data yang Difilter')
st.write(filtered_data)

# Save filtered data to CSV
if st.button('Simpan Data yang Difilter ke CSV'):
    filtered_data.to_csv('filtered_data.csv', index=False)
    st.success('Data berhasil disimpan sebagai filtered_data.csv')
