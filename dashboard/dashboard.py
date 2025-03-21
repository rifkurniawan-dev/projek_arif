import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit
import os
sns.set(style='drink')
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



