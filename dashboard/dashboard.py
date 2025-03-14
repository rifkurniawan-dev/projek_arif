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
day_df = load_data("../data/day.csv")
hour_df = load_data("../data/hour.csv")

if day_df is not None and hour_df is not None:
    st.write("### Data Day")
    st.write(day_df.head())

    st.write("### Data Hour")
    st.write(hour_df.head())
