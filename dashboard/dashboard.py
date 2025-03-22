import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Fungsi Membaca Dataset
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df["dteday_x"] = pd.to_datetime(df["dteday_x"])
            return df
        except Exception as e:
            st.error(f"Kesalahan saat membaca file CSV: {e}")
            st.stop()
    else:
        st.error(f"File '{file_path}' tidak ditemukan.")
        st.stop()

# Fungsi untuk Mengelompokkan Data Berdasarkan Musim
def seasonal_influence(df):
    seasonal_df = df.groupby('season_x')[['cnt_x']].sum().sort_values(by='cnt_x', ascending=False).reset_index()
    seasonal_df.columns = ['Musim', 'Total Penyewaan Sepeda']
    musim_mapping = {
        1: 'Musim Dingin',
        2: 'Musim Semi',
        3: 'Musim Panas',
        4: 'Musim Gugur'
    }
    seasonal_df['Musim'] = seasonal_df['Musim'].map(musim_mapping)
    return seasonal_df

# Fungsi untuk Mengelompokkan Data Berdasarkan Cuaca
def weather_influence(df):
    weather_df = df.groupby('weathersit_x')[['temp_x', 'atemp_x', 'cnt_x']].mean().sort_values(by='cnt_x', ascending=False).reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Suhu', 'Rata-rata Suhu Terasa', 'Rata-rata Penyewaan Sepeda']
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_df['Kondisi Cuaca'] = weather_df['Kondisi Cuaca'].map(weather_mapping)
    return weather_df

# Load dataset
dashboard = "dashboard/hour_day.csv"
hour_day_df = load_data(dashboard)

# Mengurutkan Data Berdasarkan Tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Menampilkan Sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Berdasarkan Rentang Tanggal
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
].copy()

# Menampilkan Header
st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Metrik Total Penyewaan dan Pendapatan
col1, col2 = st.columns(2)
with col1:
    total_penyewa = main_df['cnt_x'].sum()
    st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
    st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_df = seasonal_influence(main_df)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='Musim',
    y='Total Penyewaan Sepeda',
    data=seasonal_df,
    palette="Blues",
    ax=ax
)
ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
main_df['Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df, palette="Oranges")
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Fungsi Membaca Dataset
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df["dteday_x"] = pd.to_datetime(df["dteday_x"])
            return df
        except Exception as e:
            st.error(f"Kesalahan saat membaca file CSV: {e}")
            st.stop()
    else:
        st.error(f"File '{file_path}' tidak ditemukan.")
        st.stop()

# Fungsi untuk Mengelompokkan Data Berdasarkan Musim
def seasonal_influence(df):
    seasonal_df = df.groupby('season_x')[['cnt_x']].sum().sort_values(by='cnt_x', ascending=False).reset_index()
    seasonal_df.columns = ['Musim', 'Total Penyewaan Sepeda']
    musim_mapping = {
        1: 'Musim Dingin',
        2: 'Musim Semi',
        3: 'Musim Panas',
        4: 'Musim Gugur'
    }
    seasonal_df['Musim'] = seasonal_df['Musim'].map(musim_mapping)
    return seasonal_df

# Fungsi untuk Mengelompokkan Data Berdasarkan Cuaca
def weather_influence(df):
    weather_df = df.groupby('weathersit_x')[['temp_x', 'atemp_x', 'cnt_x']].mean().sort_values(by='cnt_x', ascending=False).reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Suhu', 'Rata-rata Suhu Terasa', 'Rata-rata Penyewaan Sepeda']
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_df['Kondisi Cuaca'] = weather_df['Kondisi Cuaca'].map(weather_mapping)
    return weather_df

# Load dataset
dashboard = "dashboard/hour_day.csv"
hour_day_df = load_data(dashboard)

# Mengurutkan Data Berdasarkan Tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Menampilkan Sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Berdasarkan Rentang Tanggal
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
].copy()

# Menampilkan Header
st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Metrik Total Penyewaan dan Pendapatan
col1, col2 = st.columns(2)
with col1:
    total_penyewa = main_df['cnt_x'].sum()
    st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
    st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_df = seasonal_influence(main_df)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='Musim',
    y='Total Penyewaan Sepeda',
    data=seasonal_df,
    palette="Blues",
    ax=ax
)
ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
main_df['Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df, palette="Oranges")
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Fungsi Membaca Dataset
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df["dteday_x"] = pd.to_datetime(df["dteday_x"])
            return df
        except Exception as e:
            st.error(f"Kesalahan saat membaca file CSV: {e}")
            st.stop()
    else:
        st.error(f"File '{file_path}' tidak ditemukan.")
        st.stop()

# Fungsi untuk Mengelompokkan Data Berdasarkan Musim
def seasonal_influence(df):
    seasonal_df = df.groupby('season_x')[['cnt_x']].sum().sort_values(by='cnt_x', ascending=False).reset_index()
    seasonal_df.columns = ['Musim', 'Total Penyewaan Sepeda']
    musim_mapping = {
        1: 'Musim Dingin',
        2: 'Musim Semi',
        3: 'Musim Panas',
        4: 'Musim Gugur'
    }
    seasonal_df['Musim'] = seasonal_df['Musim'].map(musim_mapping)
    return seasonal_df

# Fungsi untuk Mengelompokkan Data Berdasarkan Cuaca
def weather_influence(df):
    weather_df = df.groupby('weathersit_x')[['temp_x', 'atemp_x', 'cnt_x']].mean().sort_values(by='cnt_x', ascending=False).reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Suhu', 'Rata-rata Suhu Terasa', 'Rata-rata Penyewaan Sepeda']
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_df['Kondisi Cuaca'] = weather_df['Kondisi Cuaca'].map(weather_mapping)
    return weather_df

# Load dataset
dashboard = "dashboard/hour_day.csv"
hour_day_df = load_data(dashboard)

# Mengurutkan Data Berdasarkan Tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Menampilkan Sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Berdasarkan Rentang Tanggal
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
].copy()

# Menampilkan Header
st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Metrik Total Penyewaan dan Pendapatan
col1, col2 = st.columns(2)
with col1:
    total_penyewa = main_df['cnt_x'].sum()
    st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
    st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_df = seasonal_influence(main_df)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='Musim',
    y='Total Penyewaan Sepeda',
    data=seasonal_df,
    palette="Blues",
    ax=ax
)
ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
main_df['Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df, palette="Oranges")
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Fungsi Membaca Dataset
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df["dteday_x"] = pd.to_datetime(df["dteday_x"])
            return df
        except Exception as e:
            st.error(f"Kesalahan saat membaca file CSV: {e}")
            st.stop()
    else:
        st.error(f"File '{file_path}' tidak ditemukan.")
        st.stop()

# Fungsi untuk Mengelompokkan Data Berdasarkan Musim
def seasonal_influence(df):
    seasonal_df = df.groupby('season_x')[['cnt_x']].sum().sort_values(by='cnt_x', ascending=False).reset_index()
    seasonal_df.columns = ['Musim', 'Total Penyewaan Sepeda']
    musim_mapping = {
        1: 'Musim Dingin',
        2: 'Musim Semi',
        3: 'Musim Panas',
        4: 'Musim Gugur'
    }
    seasonal_df['Musim'] = seasonal_df['Musim'].map(musim_mapping)
    return seasonal_df

# Fungsi untuk Mengelompokkan Data Berdasarkan Cuaca
def weather_influence(df):
    weather_df = df.groupby('weathersit_x')[['temp_x', 'atemp_x', 'cnt_x']].mean().sort_values(by='cnt_x', ascending=False).reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Suhu', 'Rata-rata Suhu Terasa', 'Rata-rata Penyewaan Sepeda']
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_df['Kondisi Cuaca'] = weather_df['Kondisi Cuaca'].map(weather_mapping)
    return weather_df

# Load dataset
dashboard = "dashboard/hour_day.csv"
hour_day_df = load_data(dashboard)

# Mengurutkan Data Berdasarkan Tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Menampilkan Sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Berdasarkan Rentang Tanggal
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
].copy()

# Menampilkan Header
st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Metrik Total Penyewaan dan Pendapatan
col1, col2 = st.columns(2)
with col1:
    total_penyewa = main_df['cnt_x'].sum()
    st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
    st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_df = seasonal_influence(main_df)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='Musim',
    y='Total Penyewaan Sepeda',
    data=seasonal_df,
    palette="Blues",
    ax=ax
)
ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
main_df['Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df, palette="Oranges")
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Fungsi Membaca Dataset
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df["dteday_x"] = pd.to_datetime(df["dteday_x"])
            return df
        except Exception as e:
            st.error(f"Kesalahan saat membaca file CSV: {e}")
            st.stop()
    else:
        st.error(f"File '{file_path}' tidak ditemukan.")
        st.stop()

# Fungsi untuk Mengelompokkan Data Berdasarkan Musim
def seasonal_influence(df):
    seasonal_df = df.groupby('season_x')[['cnt_x']].sum().sort_values(by='cnt_x', ascending=False).reset_index()
    seasonal_df.columns = ['Musim', 'Total Penyewaan Sepeda']
    musim_mapping = {
        1: 'Musim Dingin',
        2: 'Musim Semi',
        3: 'Musim Panas',
        4: 'Musim Gugur'
    }
    seasonal_df['Musim'] = seasonal_df['Musim'].map(musim_mapping)
    return seasonal_df

# Fungsi untuk Mengelompokkan Data Berdasarkan Cuaca
def weather_influence(df):
    weather_df = df.groupby('weathersit_x')[['temp_x', 'atemp_x', 'cnt_x']].mean().sort_values(by='cnt_x', ascending=False).reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Suhu', 'Rata-rata Suhu Terasa', 'Rata-rata Penyewaan Sepeda']
    weather_mapping = {
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Hujan Ringan/Snow Ringan',
        4: 'Hujan Deras/Snow Lebat'
    }
    weather_df['Kondisi Cuaca'] = weather_df['Kondisi Cuaca'].map(weather_mapping)
    return weather_df

# Load dataset
dashboard = "dashboard/hour_day.csv"
hour_day_df = load_data(dashboard)

# Mengurutkan Data Berdasarkan Tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Menampilkan Sidebar
min_date = hour_day_df["dteday_x"].min()
max_date = hour_day_df["dteday_x"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=150)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data Berdasarkan Rentang Tanggal
main_df = hour_day_df[
    (hour_day_df["dteday_x"] >= pd.to_datetime(start_date)) & 
    (hour_day_df["dteday_x"] <= pd.to_datetime(end_date))
].copy()

# Menampilkan Header
st.header('Dashboard Analisis Penyewaan Sepeda 🚲✨')

# Metrik Total Penyewaan dan Pendapatan
col1, col2 = st.columns(2)
with col1:
    total_penyewa = main_df['cnt_x'].sum()
    st.metric("Total Penyewa", value=int(total_penyewa))
with col2:
    total_pendapatan = format_currency(float(total_penyewa), 'USD', locale='en_US')
    st.metric('Total Pendapatan', value=total_pendapatan)

# Grafik Pengaruh Musim Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda')
seasonal_df = seasonal_influence(main_df)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='Musim',
    y='Total Penyewaan Sepeda',
    data=seasonal_df,
    palette="Blues",
    ax=ax
)
ax.set_title('Pengaruh Musim Terhadap Jumlah Penyewaan Sepeda', fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Total Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Grafik Pengaruh Cuaca Terhadap Penyewaan Sepeda
st.subheader('Pengaruh Cuaca Terhadap Jumlah Penyewaan Sepeda')
main_df['Cuaca'] = main_df['weathersit_x'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Snow Ringan',
    4: 'Hujan Deras/Snow Lebat'
})

plt.figure(figsize=(12, 6))
sns.boxplot(x='Cuaca', y='cnt_x', data=main_df, palette="Oranges")
plt.title('Pengaruh Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(plt)
plt.clf()
