# 🚴 Bike Sharing Data Analysis Dashboard
## 📌 Deskripsi Proyek
Dashboard ini dibuat menggunakan Streamlit untuk menganalisis dataset Bike Sharing. Dashboard ini menyajikan berbagai visualisasi interaktif untuk memahami pola penggunaan sepeda berdasarkan musim, cuaca, tren tahunan, serta analisis lanjutan seperti RFM Analysis.
## 🚀 Fitur Dashboard
1. Dataset Preview: Menampilkan data awal dari Bike Sharing Dataset.
2. Distribusi Penyewaan Sepeda Berdasarkan Musim: Visualisasi menggunakan Violin Plot.
3. Tren Penyewaan Sepeda Sepanjang Tahun: Grafik Line Chart untuk melihat pola penggunaan sepeda.
4. Analisis RFM:
 - Recency: Kapan terakhir kali pelanggan menyewa sepeda.
 - Frequency: Berapa kali pelanggan menyewa sepeda.
 - Monetary: Total biaya sewa yang dikeluarkan pelanggan.
5. Analisis Cuaca & Suhu: Menghubungkan faktor lingkungan dengan jumlah penyewaan sepeda.
6. Menu Interaktif: Memungkinkan pengguna memilih visualisasi yang ingin ditampilkan.
# 📥 Instalasi dan Penggunaan
## 1️⃣ Clone Repository
```
git clone https://github.com/Rozii23/Proyek_Analisis_DBS_Bike_Sharing_Dataset.git
cd Proyek_Analisis_DBS_Bike_Sharing_Dataset/Dashboard
```
## 2️⃣ Install Dependensi
```
pip install -r requirements.txt
```
## 3️⃣ Jalankan Dashboard
```
streamlit run dashboard.py
```
## 🌐 Live Dashboard
🚀 Coba di sini 👉 [Bike Sharing Dashboard](https://rozii23-proyek-analisis-dbs-bike-shar-dashboarddashboard-pbwxbi.streamlit.app/)

## 🛠 Teknologi yang Digunakan
- Python: Bahasa pemrograman utama
- Streamlit: Framework untuk membuat dashboard interaktif
- Pandas: Analisis dan manipulasi data
- Matplotlib & Seaborn: Visualisasi data
- NumPy: Operasi numerik
## 💡 Insight & Kesimpulan
- Penyewaan sepeda meningkat selama musim panas, sedangkan musim dingin memiliki jumlah penyewaan terendah.
- Tren tahunan menunjukkan peningkatan signifikan dalam penggunaan sepeda dari waktu ke waktu.
- Cuaca dan suhu berpengaruh besar terhadap jumlah penyewaan sepeda.
- Dengan RFM Analysis, pelanggan dapat dikategorikan untuk strategi pemasaran yang lebih baik.
