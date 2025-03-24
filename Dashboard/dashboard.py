import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Dataset ---
file_path = "Dashboard/day.csv"
day_df = pd.read_csv(file_path)

# --- Preprocessing ---
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# --- Sidebar Navigation ---
st.sidebar.title("📊 Menu Analisis Data")
option = st.sidebar.selectbox("Pilih Analisis", [
    "Preview Dataset", "Distribusi Penyewaan Sepeda", "Tren Penyewaan Sepeda", "Barplot Musiman", "RFM Analysis"
])

# --- Preview Dataset ---
if option == "Preview Dataset":
    st.title("📂 Dataset Bike Sharing")
    st.dataframe(day_df.head())

# --- Distribusi Penyewaan Sepeda Berdasarkan Musim ---
elif option == "Distribusi Penyewaan Sepeda":
    st.title("📊 Distribusi Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=day_df['season'], y=day_df['cnt'], ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

# --- Tren Penyewaan Sepeda Sepanjang Tahun ---
elif option == "Tren Penyewaan Sepeda":
    st.title("📈 Tren Penyewaan Sepeda Sepanjang Tahun")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=day_df['dteday'], y=day_df['cnt'], ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Barplot Penyewaan Sepeda Berdasarkan Musim ---
elif option == "Barplot Musiman":
    st.title("📊 Barplot Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=day_df['season'], y=day_df['cnt'], estimator=sum, ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan Sepeda")
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
    st.pyplot(fig)

st.sidebar.info("Pilih analisis di menu untuk melihat hasil visualisasi.")
