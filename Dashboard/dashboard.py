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
    "Preview Dataset", "Distribusi Penyewaan Sepeda", "Tren Penyewaan Sepeda", 
    "Barplot Musiman", "RFM Analysis", "Analisis Cuaca"
])

# --- Fitur Interaktif: Filter berdasarkan Tanggal ---
st.sidebar.subheader("📅 Filter Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", day_df['dteday'].max())

# --- Fitur Interaktif Tambahan ---
st.sidebar.subheader("🔍 Filter Tambahan")
# Dropdown untuk memilih musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season = st.sidebar.selectbox("Pilih Musim", ["Semua"] + list(season_mapping.values()))

# Slider untuk memilih jumlah minimum penyewaan sepeda
min_rentals = st.sidebar.slider("Jumlah Minimum Penyewaan Sepeda", 0, int(day_df["cnt"].max()), 0)

# Filter data berdasarkan tanggal, musim, dan jumlah penyewaan sepeda
filtered_df = day_df[
    (day_df['dteday'] >= pd.Timestamp(start_date)) & 
    (day_df['dteday'] <= pd.Timestamp(end_date)) & 
    (day_df['cnt'] >= min_rentals)
]

# Jika pengguna memilih musim tertentu, filter juga berdasarkan musim
if selected_season != "Semua":
    season_num = list(season_mapping.keys())[list(season_mapping.values()).index(selected_season)]
    filtered_df = filtered_df[filtered_df['season'] == season_num]

# Checkbox untuk menampilkan data mentah
if st.sidebar.checkbox("Tampilkan Data Mentah", False):
    st.subheader("📋 Data Mentah Setelah Filter")
    st.dataframe(filtered_df.head())

# --- Preview Dataset ---
if option == "Preview Dataset":
    st.title("📂 Dataset Bike Sharing")
    st.dataframe(filtered_df.head())

# --- Distribusi Penyewaan Sepeda Berdasarkan Musim ---
elif option == "Distribusi Penyewaan Sepeda":
    st.title("📊 Distribusi Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_df['season'], y=filtered_df['cnt'], ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

# --- Tren Penyewaan Sepeda Sepanjang Tahun ---
elif option == "Tren Penyewaan Sepeda":
    st.title("📈 Tren Penyewaan Sepeda Sepanjang Tahun")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=filtered_df['dteday'], y=filtered_df['cnt'], ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Barplot Penyewaan Sepeda Berdasarkan Musim ---
elif option == "Barplot Musiman":
    st.title("📊 Barplot Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_df['season'], y=filtered_df['cnt'], estimator=sum, ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan Sepeda")
    st.pyplot(fig)

# --- RFM Analysis (Recency, Frequency, Monetary) ---
elif option == "RFM Analysis":
    st.title("📊 RFM Analysis untuk Pengguna Sepeda")
    
    # Simulasi RFM dengan UserID berdasarkan hari transaksi
    filtered_df['user_id'] = filtered_df.index % 1000  # Membuat dummy user_id
    rfm_df = filtered_df.groupby('user_id').agg(
        Recency=('dteday', lambda x: (filtered_df['dteday'].max() - x.max()).days),
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

# --- Analisis Cuaca dan Penyewaan Sepeda ---
elif option == "Analisis Cuaca":
    st.title("☀️ Analisis Cuaca dan Penyewaan Sepeda")
    
    # Scatter plot hubungan temperatur dan penyewaan
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=filtered_df['temp'], y=filtered_df['cnt'], alpha=0.6, ax=ax)
    ax.set_xlabel("Temperatur (Normalisasi)")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

    # Barplot hubungan kondisi cuaca dan jumlah penyewaan sepeda
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_df['weathersit'], y=filtered_df['cnt'], estimator=sum, ax=ax)
    ax.set_xlabel("Kondisi Cuaca (1=Clear, 2=Cloudy, 3=Rain/Snow)")
    ax.set_ylabel("Total Penyewaan Sepeda")
    st.pyplot(fig)

st.sidebar.info("Pilih analisis di menu untuk melihat hasil visualisasi.")
