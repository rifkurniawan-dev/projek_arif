import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit
import os
sns.set(style='darink')
def create_seasonal_influence :
            seasonal_influence = df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
            seasonal_influence.head(10)
            return _seasonal_influence
def create_weather_influence :
            weather_influence = hour_day_df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
            weather_influence.head(10)
 return _seasonal_influence
dashboard = pd.read_csv("dashboard/hour_day.csv")
datetime_columns = ["dteday"]
hour_day_df.sort_values(by="dteday", inplace=True)
hour_day_df.reset_index(inplace=True)
for coloumn in datetime_columns:
  hour_day_df[coloumn] = pd.to_datetime(hour_day_df[coloumn])

# Filter data
min_date = hour_day_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_day_df[(hour_day_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
seasonal_influence = create_seasonal_influence(main_df)
weather_influence = reate_weather_influence(main_df)



# plot number of daily orders (2021)
st.header('Dicoding Collection Dashboard :sparkles:')
st.subheader('Daily Orders')

            daily_rentals_df = df.resample(rule='D', on='dteday_x').agg({
                'instant': 'nunique',
                'cnt_x': 'sum'
            }).reset_index()

            daily_rentals_df.rename(columns={
                'instant': 'rental_count',
                'cnt_x': 'revenue'
            }, inplace=True)

            return daily_rentals_df

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
