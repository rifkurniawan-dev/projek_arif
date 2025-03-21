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
                'instant': 'nunique',
                'cnt_x': 'sum'
            }).reset_index()

            daily_rentals_df.rename(columns={
                'instant': 'rental_count',
                'cnt_x': 'revenue'
            }, inplace=True)

            return daily_rentals_df

        def create_byseason_df(df):
            byseason_df = df.groupby(by='season_x').instant.nunique().reset_index()
            byseason_df.rename(columns={'instant': 'rental_count'}, inplace=True)
            return byseason_df

        def create_byweather_df(df):
            byweather_df = df.groupby(by='weathersit_x').instant.nunique().reset_index()
            byweather_df.rename(columns={'instant': 'rental_count'}, inplace=True)
            return byweather_df

        daily_rentals_df = create_daily_rentals_df(filtered_data)
        byseason_df = create_byseason_df(filtered_data)
        byweather_df = create_byweather_df(filtered_data)

        st.header('Dashboard Analisis Penyewaan Sepeda :sparkles:')

        col1, col2 = st.columns(2)

        with col1:
            total_rentals = daily_rentals_df['rental_count'].sum()
            st.metric('Total Penyewaan', value=total_rentals)

        with col2:
            total_revenue = format_currency(daily_rentals_df['revenue'].sum(), 'USD', locale='en_US')
            st.metric('Total Pendapatan', value=total_revenue)

        # Grafik Penyewaan Harian
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='dteday_x', y='rental_count', data=daily_rentals_df, color='blue')
        plt.title('Jumlah Penyewaan Sepeda Harian (2011-2012)', fontsize=20)
        plt.xlabel('Tanggal', fontsize=12)
        plt.ylabel('Jumlah Penyewaan', fontsize=12)
        plt.xticks(rotation=45)
        st.pyplot(plt)

day_df = pd.read_csv("day.csv")
day_df.head()

hour_df = pd.read_csv("hour.csv")
hour_df.head()

"""### Assessing Data

Menilai day
"""

day_df.info()

day_df.isna().sum()

print("Jumlah duplikasi: ", day_df.duplicated().sum())

day_df.describe()

"""Menilai Hour"""

hour_df.info()

hour_df.isna().sum()

print("Jumlah duplikasi: ", hour_df.duplicated().sum())

hour_df.describe()

"""### Cleaning Data

Duplicat day
"""

day_df.info()

"""memperbaiki type data"""

datetime_columns = ["dteday"]
for coloumn in datetime_columns:
  day_df[coloumn] = pd.to_datetime(day_df[coloumn])

day_df.head()

"""Duplikat Hour"""

hour_df.info()

"""memperbaiki type data"""

datetime_columns = ["dteday"]
for coloumn in datetime_columns:
  hour_df[coloumn] = pd.to_datetime(hour_df[coloumn])

hour_df.info()

hour_df.head()

"""menggabungkan Hour & day"""

day_hour_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="outer",
    left_on="instant",
    right_on="instant"
)
day_hour_df.head()

day_hour_df.nunique()

day_hour_df.isna().sum()

"""## Exploratory Data Analysis (EDA)

### Explore ...
"""

day_df.sample(5)

day_df.describe(include="all")

day_df.instant.is_unique

day_df.groupby(by='dteday').agg({
    'instant': 'nunique',
    'cnt': ['max', 'min', 'mean', 'std']
})

day_df.groupby(by="season").instant.nunique().sort_values(ascending=False).reset_index()

day_df.groupby(by="mnth").instant.nunique().sort_values(ascending=False).reset_index()

"""eksplor Hour_df"""

hour_df.sample(5)

weather_data = hour_df.groupby(by="weathersit")['cnt'].sum().sort_values(ascending=False).reset_index()

hour_df.sample(5)

hour_df.describe(include="all")

day_df.weathersit.hist()

instant_in_orders_df =  hour_df.instant
day_df["status"] = day_df["instant"].apply(lambda x: "Active" if x in instant_in_orders_df else "Non Active") # Changed instant_in_hour_df to instant_in_orders_df
day_df.sample(5)

day_df.groupby(by="status").instant.count()

"""## Explore day_df & hour_df"""

hour_day_df = pd.merge(
      left=hour_df,
      right=day_df,
      how="left",
      left_on="instant",
      right_on="instant"
)
hour_day_df.head()

hour_day_df.groupby(by="season_x").instant.nunique().sort_values(ascending=False).head(10).reset_index()

hour_day_df.groupby(by="mnth_x").instant.nunique().sort_values(ascending=False).head(10).reset_index()

hour_day_df.groupby(by="dteday_x").instant.nunique().sort_values(ascending=False)

hour_day_df["weather_category"] = hour_day_df["weathersit_x"].apply(lambda x: "Clear/Good Weather" if x == 1 else ("Moderate Weather" if x == 2 else "Bad Weather"))

hour_day_df.groupby("weather_category").instant.nunique().sort_values(ascending=False).reset_index()

hour_day_df.to_csv("hour_day.csv", index=False)

"""Menghubungkan semua

## Visualization & Explanatory Analysis

Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda
"""

hour_day_df.sample(5)

day_df.head()

seasonal_influence = hour_day_df.groupby('season_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
seasonal_influence.head(10)

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
plt.show()

"""bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda"""

weather_influence = hour_day_df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
weather_influence.head(10)

weather_influence = hour_day_df.groupby('weathersit_x')['cnt_x'].sum().sort_values(ascending=False).reset_index()
weather_mapping = {
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
}
hour_df['weathersit'] = hour_df['weathersit'].map(weather_mapping)
plt.figure(figsize=(12, 6))
sns.boxplot(x='weathersit', y='cnt', data=hour_df)
plt.title('pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca (weathersit)')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.show()

"""# Conclusion

Conclusion Pertanyaan 1 : Berdasarkan data yang ada, dapat disimpulkan bahwa musim memiliki pengaruh yang signifikan terhadap jumlah penyewaan sepeda. Pada musim panas, jumlah penyewaan sepeda cenderung mencapai titik tertinggi, kemungkinan karena cuaca yang hangat dan kondisi yang ideal untuk bersepeda. Musim semi juga menunjukkan tingkat penyewaan yang tinggi, meskipun mungkin sedikit lebih rendah dibandingkan musim panas. Ketika memasuki musim gugur, jumlah penyewaan sepeda mulai menurun, mungkin karena cuaca yang semakin dingin dan hari yang lebih pendek. Pada musim dingin, jumlah penyewaan sepeda mencapai titik terendah, yang dapat dikaitkan dengan cuaca yang tidak mendukung dan kondisi jalan yang mungkin kurang aman untuk bersepeda. Secara keseluruhan, musim panas dan semi merupakan periode puncak untuk penyewaan sepeda, sementara musim dingin menunjukkan penurunan yang signifikan dalam aktivitas tersebut.

Conclusion Pertanyaan 2 : Cuaca memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda. Kondisi cuaca cerah atau sedikit berawan menunjukkan tingkat penyewaan tertinggi, sementara kondisi cuaca buruk seperti hujan atau salju mengakibatkan penurunan penyewaan secara drastis. Semakin ekstrem cuaca, semakin rendah minat masyarakat dalam menyewa sepeda.
"""

