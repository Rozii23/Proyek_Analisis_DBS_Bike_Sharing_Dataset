import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Load Dataset ---
file_path = "Dashboard/day.csv"
day_df = pd.read_csv(file_path)

# --- Preprocessing ---
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mapping season agar lebih mudah dibaca
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_df['season_label'] = day_df['season'].map(season_mapping)

# --- Sidebar Navigation ---
st.sidebar.title("📊 Menu Analisis Data")
option = st.sidebar.selectbox("Pilih Analisis", [
    "Preview Dataset", "Distribusi Penyewaan Sepeda", "Tren Penyewaan Sepeda",
    "Barplot Musiman", "RFM Analysis", "Analisis Cuaca", "Pola Hari Kerja vs Akhir Pekan"
])

# --- Fitur Interaktif: Filter berdasarkan Tanggal ---
st.sidebar.subheader("📅 Filter Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", day_df['dteday'].max())

# Filter data berdasarkan tanggal
filtered_df = day_df[
    (day_df['dteday'] >= pd.Timestamp(start_date)) & 
    (day_df['dteday'] <= pd.Timestamp(end_date))
]

# --- Preview Dataset ---
if option == "Preview Dataset":
    st.title("📂 Dataset Bike Sharing")
    st.dataframe(filtered_df.head())

# --- Distribusi Penyewaan Sepeda Berdasarkan Musim ---
elif option == "Distribusi Penyewaan Sepeda":
    st.title("📊 Distribusi Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="season_label", y="cnt", data=filtered_df, estimator=np.mean, palette="viridis", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Tren Penyewaan Sepeda Sepanjang Tahun ---
elif option == "Tren Penyewaan Sepeda":
    st.title("📈 Tren Penyewaan Sepeda Sepanjang Tahun")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=filtered_df['dteday'], y=filtered_df['cnt'], color="blue", marker="o", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Tren Penyewaan Sepeda Sepanjang Tahun")
    plt.xticks(rotation=45)
    ax.grid(True, linestyle="--", alpha=0.7) # Tambahkan grid untuk memperjelas tren
    st.pyplot(fig)

# --- Barplot Penyewaan Sepeda Berdasarkan Musim ---
elif option == "Barplot Musiman":
    st.title("📊 Total Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="season_label", y="cnt", data=filtered_df, estimator=np.sum, palette="magma", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- RFM Analysis (Recency, Frequency, Monetary) ---
elif option == "RFM Analysis":
    st.title("📊 RFM Analysis untuk Pengguna Sepeda")

    # Simulasi RFM dengan UserID berdasarkan hari transaksi
    day_df['user_id'] = day_df.index % 1000  # Membuat dummy user_id
    rfm_df = day_df.groupby('user_id').agg(
        Recency=('dteday', lambda x: (day_df['dteday'].max() - x.max()).days),
        Frequency=('user_id', 'count'),
        Monetary=('cnt', 'sum')
    ).reset_index()
    
    st.subheader("Tabel RFM Analysis")
    st.dataframe(rfm_df.head(10))
    
    # Visualisasi RFM
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=rfm_df['Recency'], y=rfm_df['Monetary'], hue=rfm_df['Frequency'], palette='coolwarm', ax=ax)
    ax.set_xlabel("Recency (Hari sejak transaksi terakhir)")
    ax.set_ylabel("Total Penyewaan Sepeda (Monetary)")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Analisis Cuaca dan Penyewaan Sepeda ---
elif option == "Analisis Cuaca":
    st.title("☀️ Analisis Cuaca dan Penyewaan Sepeda")

    # Scatter plot hubungan temperatur dan penyewaan
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=filtered_df['temp'], y=filtered_df['cnt'], hue=filtered_df['season_label'], palette="coolwarm", alpha=0.6, ax=ax)
    ax.set_xlabel("Temperatur (Normalisasi)")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

    # Barplot hubungan kondisi cuaca dan jumlah penyewaan sepeda
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_df['weathersit'], y=filtered_df['cnt'], estimator=np.sum, palette="rocket", ax=ax)
    ax.set_xlabel("Kondisi Cuaca (1=Clear, 2=Cloudy, 3=Rain/Snow)")
    ax.set_ylabel("Total Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan ---
elif option == "Pola Hari Kerja vs Akhir Pekan":
    st.title("📅 Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")

    # Mapping Hari Kerja dan Akhir Pekan
    filtered_df["Kategori Hari"] = filtered_df["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})

    # Visualisasi dengan barplot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="Kategori Hari", y="cnt", data=filtered_df, estimator=np.mean, palette="coolwarm", ax=ax)
    ax.set_xlabel("Kategori Hari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Perbandingan Penyewaan Sepeda pada Hari Kerja vs. Akhir Pekan")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

st.sidebar.info("Pilih analisis di menu untuk melihat hasil visualisasi.")
