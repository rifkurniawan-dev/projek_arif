import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

# Memuat data dari file CSV
def load_data():
    day_df = pd.read_csv('data/day.csv')
    hour_df = pd.read_csv('data/hour.csv')

    if day_df is not None and hour_df is not None:
        st.write("### Data Day")
        st.write(day_df.head())

        st.write("### Data Hour")
        st.write(hour_df.head())

        # Menggabungkan kedua dataframe
        merged_df = pd.merge(hour_df, day_df, how="outer", on="instant")
        return merged_df

# Memuat data
data = load_data()

# Membuat kolom datetime dari dteday_x dan hr
data['datetime'] = pd.to_datetime(data['dteday_x']) + pd.to_timedelta(data['hr'], unit='h')

# Pastikan kolom 'dteday_x' dalam format dateti
