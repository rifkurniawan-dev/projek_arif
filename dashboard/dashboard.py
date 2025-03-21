import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit
import os
sns.set(style='darkgrid')

# Load Data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Cleaning Data - Konversi kolom tanggal
for df in [day_df, hour_df]:
    df["dteday"] = pd.to_datetime(df["dteday"])

# Menggabungkan Data
hour_day_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="left",
    on="instant"
)

# Menambahkan kategori cuaca yang lebih deskriptif
hour_day_df["weather_category"] = hour_day_df["weathersit_x"].apply(
    lambda x: "Cerah / Sedikit Berawan" if x == 1 else 
              "Berkabut / Berawan" if x == 2 else 
              "Gerimis / Hujan Ringan" if x == 3 else 
              "Hujan Lebat / Badai"
)

# Menambahkan kategori musim yang lebih deskriptif
musim_mapping = {
    1: 'Musim Dingin',
    2: 'Musim Semi',
    3: 'Musim Panas',
    4: 'Musim Gugur'
}
hour_day_df['Musim'] = hour_day_df['season_x'].map(musim_mapping)

# Mengekspor file yang sudah dibersihkan
hour_day_df.to_csv("hour_day.csv", index=False)

# Mengecek hasil penggabungan
hour_day_df.head()
