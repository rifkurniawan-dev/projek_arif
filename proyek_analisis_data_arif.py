import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


day_df = pd.read_csv("day.csv")
day_df.head()

hour_df = pd.read_csv("hour.csv")
hour_df.head()

day_df.info()

day_df.isna().sum()

print("Jumlah duplikasi: ", day_df.duplicated().sum())

day_df.describe()

hour_df.info()

hour_df.isna().sum()

print("Jumlah duplikasi: ", hour_df.duplicated().sum())

hour_df.describe()


day_df.duplicated().sum()

day_df.drop_duplicates(inplace=True)

print("Jumlah duplikasi: ", day_df.duplicated().sum())


hour_df.duplicated().sum()

hour_df.drop_duplicates(inplace=True)

print("jumlah duplikasi: ", hour_df.duplicated().sum())


day_df.sample(5)

day_df.describe(include="all")

day_df.instant.is_unique

season_stats = day_df.groupby(by='season').agg({
    'instant': 'nunique',
    'temp': ['max', 'min', 'mean', 'std'],
    'hum': ['max', 'min', 'mean', 'std'],
    'windspeed': ['max', 'min', 'mean', 'std'],
    'cnt': ['max', 'min', 'mean', 'std']
})

print('\nStatistik Deskriptif Berdasarkan Season:')
print(season_stats)

#Jumlah Unik 'instant' Berdasarkan 'mnth'
day_df.groupby(by="mnth").instant.nunique().sort_values(ascending=False)

# Jumlah Unik 'instant' Berdasarkan 'weathersit'
day_df.groupby(by='weathersit').instant.nunique().sort_values(ascending=False)

hour_df.sample(5)

hour_df.describe(include="all")

hour_df.head()

hour_df.groupby(by="instant")['cnt'].sum()

hour_day_df = pd.merge(
    left= hour_df,
    right=day_df,
    how="left",
    left_on="season",
    right_on="season"
)
hour_day_df.head()

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


hour_day_df.sample(5)

hour_df.head()

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
monthly_hour_df

plt.figure(figsize=(12, 6))
plt.bar(
    monthly_hour_df["dteday_x"],
    monthly_hour_df["hour_count"],
    color="#72BCD4"
)
plt.title("Jumlah Penyewaan Sepeda per Bulan", loc="center", fontsize=20)
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.show()

plt.figure(figsize=(10,6))
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
