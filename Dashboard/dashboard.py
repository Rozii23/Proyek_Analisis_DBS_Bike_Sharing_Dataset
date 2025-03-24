import streamlit as st
import pandas as pd
import gdown
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Mengunduh file jika tidak ditemukan ---
file_path = "day.csv"
file_id = "16w4Z3Wy6hlVU6RHLu2BxdpqD4QXwU_8d"

if not os.path.exists(file_path):
    st.write("File tidak ditemukan, mengunduh dari Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", file_path, quiet=False)

# --- Membaca dataset ---
day_df = pd.read_csv(file_path)

# --- Judul Dashboard ---
st.title("📊 Bike Sharing Data Analysis")

# --- Menampilkan Dataframe ---
st.subheader("Dataset Preview")
st.dataframe(day_df.head())

# --- Visualisasi 1: Distribusi Penyewaan Sepeda Berdasarkan Musim ---
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 6))
sns.violinplot(x=day_df['season'], y=day_df['cnt'], ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# --- Visualisasi 2: Tren Penyewaan Sepeda Sepanjang Tahun ---
st.subheader("Tren Penyewaan Sepeda Sepanjang Tahun")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=day_df['dteday'], y=day_df['cnt'], ax=ax)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Insight ---
st.subheader("📌 Insight")
st.markdown("1. **Musim panas** memiliki jumlah penyewaan sepeda tertinggi dibandingkan musim lainnya.")
st.markdown("2. Tren penyewaan sepeda menunjukkan **peningkatan bertahap sepanjang tahun** dengan beberapa fluktuasi.")
