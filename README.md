# Mental Health & Digital Usage Analytics Dashboard

Dashboard interaktif ini memvisualisasikan hubungan antara penggunaan teknologi digital dan kesehatan mental. Dibangun menggunakan Python dan Streamlit, aplikasi ini mengambil data langsung dari database Supabase.

## Fitur Utama
- **Visualisasi Data**: Grafik interaktif untuk menganalisis tren stres, kecemasan, dan penggunaan perangkat.
- **Filter Dinamis**: Filter data berdasarkan Gender dan Wilayah.
- **Koneksi Database Langsung**: Menggunakan SQLAlchemy untuk mengambil data real-time dari Supabase.

## Prasyarat
Pastikan Anda telah menginstal:
- Python 3.9 atau lebih baru
- pip (Python package installer)

## Instalasi

1.  **Clone Repository** (jika menggunakan git) atau ekstrak folder proyek.
2.  **Buat Virtual Environment** (disarankan):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
3.  **Instal Dependensi**:
    ```bash
    pip install -r requirements.txt
    ```

## Konfigurasi

Pastikan file `.env` telah dibuat di root direktori proyek dengan isi sebagai berikut:

```env
DATABASE_URL="postgresql://[user]:[password]@[host]:[port]/[database]"
```

*Catatan: Kredensial database sudah dikonfigurasi di lingkungan Anda.*

## Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:

```bash
streamlit run main.py
```

Aplikasi akan terbuka otomatis di browser default Anda di alamat `http://localhost:8501`.

## Struktur Proyek
- `main.py`: File utama aplikasi Streamlit.
- `config.py`: Konfigurasi koneksi database dan query data.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.
- `laporan_analisis.md`: Laporan hasil analisis data.
