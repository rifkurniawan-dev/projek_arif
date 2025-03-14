import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
# Penanganan Error untuk memastikan file ditemukan
def load_data(file_path):
    if os.path.exists(file_path):
        st.write(f"✅ File ditemukan: {file_path}")
        return pd.read_csv(file_path)
    else:
        st.error(f"❌ File tidak ditemukan: {file_path}. Pastikan file berada di folder 'data/' dan path sudah benar.")
        return None


# Memuat data
day_df = load_data("data/day.csv")
hour_df = load_data("data/hour.csv")

if day_df is not None and hour_df is not None:
    st.write("### Data Day")
    st.write(day_df.head())

    st.write("### Data Hour")
    st.write(hour_df.head())
# Bagian Visualisasi Streamlit
st.title("Dashboard Analisis Penyewaan Sepeda")

if day_df is not None and hour_df is not None:
    # Sidebar untuk memilih visualisasi
    st.sidebar.title("Pengaturan Visualisasi")
    option = st.sidebar.selectbox(
        "Pilih Visualisasi yang ingin ditampilkan:",
        ("Jumlah Penyewaan Sepeda per Bulan", "Rata-rata Penyewaan Berdasarkan Musim", "Pengaruh Cuaca terhadap Penyewaan")
    )

    if option == "Jumlah Penyewaan Sepeda per Bulan":
        st.subheader("Jumlah Penyewaan Sepeda per Bulan")
        
        # Konversi kolom tanggal menjadi datetime
        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
        
        # Pengelompokan data per bulan
        monthly_data = hour_df.resample('M', on='dteday')['cnt'].sum().reset_index()
        monthly_data['month'] = monthly_data['dteday'].dt.strftime('%B')

        # Plot Bar Chart
        plt.figure(figsize=(12, 6))
        sns.barplot(x='month', y='cnt', data=monthly_data, palette="viridis")
        plt.title('Jumlah Penyewaan Sepeda per Bulan')
        plt.xlabel('Bulan')
        plt.ylabel('Jumlah Penyewaan Sepeda')
        plt.xticks(rotation=45)
        
        st.pyplot(plt)
        plt.clf()

    elif option == "Rata-rata Penyewaan Berdasarkan Musim":
        st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")

        # Plot Rata-rata Penyewaan Berdasarkan Musim
        plt.figure(figsize=(10, 6))
        sns.barplot(x='season', y='cnt', data=day_df, errorbar='sd', palette="Set2")
        plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Rata-rata Penyewaan Sepeda')
        plt.xticks([0, 1, 2, 3], ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])

        st.pyplot(plt)
        plt.clf()

    elif option == "Pengaruh Cuaca terhadap Penyewaan":
        st.subheader("Pengaruh Cuaca Terhadap Penyewaan Sepeda")

        # Plot Pengaruh Cuaca
        plt.figure(figsize=(10, 6))
        sns.barplot(x='weathersit', y='cnt', data=hour_df, palette="Blues")
        plt.title('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Penyewaan Sepeda')
        plt.xticks([1, 2, 3], ['Cerah', 'Mendung', 'Hujan/Sangat Buruk'])

        st.pyplot(plt)
        plt.clf()
