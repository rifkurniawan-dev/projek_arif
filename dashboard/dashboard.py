import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

day_df = "Dashboard/day.csv"

if os.path.exists(day_df):
    day_df = pd.read_csv(file_path)
    hour_df = day_df.copy()  
else:
    st.error(f"File {day_df} not found. Please check the file path.")
    raise FileNotFoundError(f"{day_df} not found.")

st.write(day_df.head())

st.write(day_df.info())
st.write("Missing values in day_df:")
st.write(day_df.isna().sum())

st.write(f"Jumlah duplikasi: {day_df.duplicated().sum()}")
st.write(day_df.describe())

day_df.drop_duplicates(inplace=True)
st.write(f"Jumlah duplikasi setelah dihapus: {day_df.duplicated().sum()}")

season_stats = day_df.groupby(by='season').agg({
    'instant': 'nunique',
    'temp': ['max', 'min', 'mean', 'std'],
    'hum': ['max', 'min', 'mean', 'std'],
    'windspeed': ['max', 'min', 'mean', 'std'],
    'cnt': ['max', 'min', 'mean', 'std']
})
st.write('\nStatistik Deskriptif Berdasarkan Season:')
st.write(season_stats)

# Group by 'mnth' and 'weathersit' to get unique instant counts
st.write(day_df.groupby(by="mnth").instant.nunique().sort_values(ascending=False))
st.write(day_df.groupby(by='weathersit').instant.nunique().sort_values(ascending=False))


hour_day_df = pd.merge(hour_df, day_df, how="left", on="season")


hour_day_df.groupby(by="temp_y").agg({
    'cnt_y': 'nunique',
    'casual_y': 'sum',
    'registered_y': 'sum'
})

hour_day_df.groupby(by="weathersit_x").agg({
    'cnt_y': 'nunique',
    'casual_y': 'sum',
    'registered_y': 'sum'
}).sort_values(by="registered_y", ascending=False)

hour_day_df['dteday_x'] = pd.to_datetime(hour_day_df['dteday_x'])

monthly_hour_df = hour_day_df.resample(rule='MS', on='dteday_x').agg({
    'instant_x': 'nunique',
    'cnt_x': 'sum'
})

monthly_hour_df.index = monthly_hour_df.index.strftime('%B')
monthly_hour_df = monthly_hour_df.reset_index()
monthly_hour_df.rename(columns={
    'instant_x': 'hour_count',
    'cnt_x': 'revenue'
}, inplace=True)

plt.figure(figsize=(12, 6))
plt.bar(monthly_hour_df["dteday_x"], monthly_hour_df["hour_count"], color="#72BCD4")
plt.title("Jumlah Penyewaan Sepeda per Bulan", loc="center", fontsize=20)
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=hour_df, errorbar='sd')
plt.title('Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit_x', y='cnt_x', data=hour_day_df, hue='weathersit_x', palette="Blues", dodge=False, legend=False)
plt.title("Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda", fontsize=20)
plt.xlabel("Kondisi Cuaca", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
plt.xticks(rotation=30, fontsize=10)
plt.yticks(fontsize=10)
plt.show()
