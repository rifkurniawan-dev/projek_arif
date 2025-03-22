# -*- coding: utf-8 -*-
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Path file CSV
dashboard = "dashboard/hour_day.csv"

# Fungsi untuk mengecek keberadaan file
def check_file(path):
    if os.path.exists(path):
        st.write(f"📁 Direktori saat ini: {os.getcwd()}")
        st.write(f"📂 Isi folder 'dashboard': {os.listdir('dashboard')}")
        return True
    else:
        return False

# Mengecek apakah file CSV ada atau tidak
if check_file(dashboard):
    try:
        # Membaca file CSV
        hour_day_df = pd.read_csv(dashboard)
        st.success(f"✅ File '{dashboard}' berhasil dibaca!")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat membaca file CSV: {e}")
        st.stop()
else:
    st.error(f"❌ File '{dashboard}' tidak ditemukan. Pastikan file ada di folder 'dashboard'.")
    st.stop()

# Konversi kolom tanggal ke tipe datetime
if 'dteday_x' in hour_day_df.columns:
    try:
        hour_day_df["dteday_x"] = pd.to_datetime(hour_day_df["dteday_x"])
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat mengonversi kolom 'dteday_x' menjadi datetime: {e}")
        st.stop()
else:
    st.error("❌ Kolom 'dteday_x' tidak ditemukan di dalam file CSV.")
    st.stop()

# Mengurutkan dan mereset index berdasarkan tanggal
hour_day_df.sort_values(by="dteday_x", inplace=True)
hour_day_df.reset_index(drop=True, inplace=True)

# Tampilkan preview dari data yang berhasil dibaca
st.write("📋 **Preview Data:**")
st.dataframe(hour_day_df.head())
