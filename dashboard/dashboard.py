import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os


day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

if day_df is not None and hour_df is not None:
    st.write("### Data Day")
    st.write(day_df.head())

    st.write("### Data Hour")
    st.write(hour_df.head())

st.title("Dashboard Analisis Penyewaan Sepeda")

if day_df is not None and hour_df is not None:

    st.sidebar.title("Pengaturan Visualisasi")
    option = st.sidebar.selectbox(
        "Pilih Visualisasi yang ingin ditampilkan:",
        ("Jumlah Penyewaan Sepeda per Bulan", "Rata-rata Penyewaan Berdasarkan Musim", "Pengaruh Cuaca terhadap Penyewaan")
    )

    if option == "Jumlah Penyewaan Sepeda per Bulan":
        st.subheader("Jumlah Penyewaan Sepeda per Bulan")


        hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])


        monthly_data = hour_df.resample('M', on='dteday')['cnt'].sum().reset_index()
        monthly_data['month'] = monthly_data['dteday'].dt.strftime('%B')

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


        plt.figure(figsize=(10, 6))
        sns.barplot(x='weathersit', y='cnt', data=hour_df, palette="Blues")
        plt.title('Pengaruh Cuaca Terhadap Penyewaan Sepeda')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Penyewaan Sepeda')
        plt.xticks([0, 1, 2, 3], ['sangat Cerah','Cerah', 'Mendung', 'Hujan'])

        st.pyplot(plt)
        plt.clf()



