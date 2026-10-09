# Repositori Tugas Pengolahan Citra Digital

Repositori ini berisi kumpulan tugas praktikum dan proyek mata kuliah **Pengolahan Citra Digital** (Pertemuan 1 hingga Pertemuan 7). Fokus utama mencakup pemrosesan matriks citra dasar, representasi ruang warna, analisis histogram, teknik perbaikan citra (*image enhancement*), *spatial filtering*, *optical character recognition* (OCR), hingga *mini project* integrasi verifikasi dokumen ijazah otomatis.

---

## 📁 Struktur Direktori

```text
tugas-citra-digital-052/
├── README.md               # Dokumentasi utama proyek & panduan menjalankan seluruh tugas
├── pyproject.toml          # Konfigurasi dependensi proyek (uv / pip)
├── uv.lock                 # Lockfile dependensi proyek
│
├── resources/              # Dataset citra yang digunakan pada praktikum
│   └── ijazah/             # 9 variasi citra ijazah dengan skenario degradasi kualitas
│       ├── 01_HighQuality_Enhanced.jpg
│       ├── 02_LowContrast.jpg
│       ├── 03_Blurred.jpg
│       ├── 04_HighNoise.jpg
│       ├── 05_LowResolution_Upsampled.jpg
│       ├── 06_Faded_Underexposed.jpg
│       ├── 07_ColorShift_WarmTint.jpg
│       ├── 08_JPEGCompression_Artifacts.jpg
│       └── 09_CombinedDegradation.jpg
│
├── tugas-1/                # Pertemuan 1: Dasar representasi matriks citra 3D
│   ├── main.py
│   └── README.md
│
├── tugas-2/                # Pertemuan 2: Representasi ruang warna BGR vs RGB
│   └── README.md
│
├── tugas-3/                # Pertemuan 3: Analisis histogram intensitas piksel ijazah
│   ├── main.py
│   ├── README.md
│   ├── ijazah/             # Citra ijazah sampel praktikum 3
│   └── result/             # Plot grafik histogram hasil analisis
│
├── tugas-4/                # Pertemuan 4: Enhancement nomor ijazah & uji OCR
│   ├── main.py
│   ├── ujiocr.py
│   └── README.md
│
├── tugas-5/                # Pertemuan 5: Spatial Filtering (Mean, Median, Gaussian, Sharpening) + OCR
│   ├── main.py
│   └── README.md
│
├── tugas-6/                # Pertemuan 6: Segmentasi tanda tangan (Thresholding & Morfologi)
│   └── README.md
│
└── tugas-7/                # Pertemuan 7: Mini Project Integrasi (Pipeline Terpadu)
    ├── main.py
    └── README.md
```

---

## 🛠️ Prasyarat & Instalasi Lingkungan

### 1. Sistem Requirements
- **Python**: Versi $\ge$ 3.10 (proyek ini menggunakan Python 3.13)
- **Tesseract OCR Engine**: Diperlukan untuk modul OCR (Tugas 4, 5, dan 7).
  - **Linux (Fedora)**:
    ```bash
    sudo dnf install tesseract tesseract-langpack-eng
    ```
  - **Linux (Ubuntu/Debian)**:
    ```bash
    sudo apt-get install tesseract-ocr
    ```
  - **macOS (Homebrew)**:
    ```bash
    brew install tesseract
    ```
  - **Windows**: Unduh installer dari UB-Mannheim Tesseract OCR GitHub dan tambahkan ke PATH.

### 2. Instalasi Dependensi Python

#### Opsi A: Menggunakan `uv` (Direkomendasikan)
```bash
# Sinkronisasi dependensi otomatis dari pyproject.toml / uv.lock
uv sync
```

#### Opsi B: Menggunakan `pip` standar / virtualenv
```bash
# Buat dan aktifkan virtual environment (opsional)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Pasang pustaka yang diperlukan
pip install opencv-python numpy matplotlib pytesseract
```

---

## 🚀 Panduan Menjalankan Program (*How to Run*)

Setiap tugas dapat dijalankan langsung dari direktori root proyek menggunakan `uv run` maupun `python`:

| Direktori | Topik Tugas | Perintah Menjalankan |
|---|---|---|
| **`tugas-1`** | Perkalian Matriks Citra 3D | `uv run tugas-1/main.py` atau `python tugas-1/main.py` |
| **`tugas-2`** | Teori Ruang Warna BGR | Baca analisis pada [tugas-2/README.md](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-2/README.md) |
| **`tugas-3`** | Analisis Histogram Citra Ijazah | `uv run tugas-3/main.py` atau `python tugas-3/main.py` |
| **`tugas-4`** | Peningkatan Kontras & OCR Nomor | `uv run tugas-4/main.py` atau `python tugas-4/main.py` |
| **`tugas-5`** | Spatial Filtering & Akurasi OCR | `uv run tugas-5/main.py` atau `python tugas-5/main.py` |
| **`tugas-6`** | Segmentasi Tanda Tangan Kepala Sekolah | Baca teori & analisis pada [tugas-6/README.md](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-6/README.md) |
| **`tugas-7`** | **Mini Project Integrasi (End-to-End)** | `uv run tugas-7/main.py` atau `python tugas-7/main.py` |

---

## 📖 Ringkasan Singkat Setiap Tugas

### 🔹 [Tugas 1 — Perkalian Matriks Citra 3D](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-1/README.md)
- **Fokus**: Memahami citra digital sebagai tensor/matriks berdimensi tiga (batch/channel, baris/tinggi, kolom/lebar).
- **Implementasi**: Perkalian matriks multidimensi menggunakan NumPy (`@` operator).

### 🔹 [Tugas 2 — Teori Warna BGR pada Citra Digital](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-2/README.md)
- **Fokus**: Menjawab alasan historis OpenCV menggunakan urutan kanal BGR (Blue-Green-Red) serta alternatif representasi warna seperti RGB, Grayscale, HSV, dan CIELAB.

### 🔹 [Tugas 3 — Analisis Histogram Citra Ijazah](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-3/README.md)
- **Fokus**: Konversi citra ke Grayscale dan menganalisis sebaran intensitas piksel melalui visualisasi histogram.
- **Output**: Plot histogram citra asli vs grayscale yang disimpan di folder `tugas-3/result/`.

### 🔹 [Tugas 4 — Enhancement Area Nomor Ijazah](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-4/README.md)
- **Fokus**: Memotong (*cropping*) Region of Interest (ROI) nomor ijazah dan menguji metode *Brightness Adjustment*, *Contrast Stretching*, serta *Histogram Equalization* sebelum diproses Tesseract OCR.

### 🔹 [Tugas 5 — Filtering, Noise Reduction & OCR](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-5/README.md)
- **Fokus**: Menerapkan spatial filtering (*Mean*, *Median*, *Gaussian*, dan *Laplacian Sharpening*) untuk mereduksi derau dan meningkatkan keterbacaan teks nomor ijazah pada OCR.

### 🔹 [Tugas 6 — Deteksi Tanda Tangan Kepala Sekolah](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-6/README.md)
- **Fokus**: Segmentasi area tanda tangan dengan metode *Otsu Thresholding*, operasi morfologi (*Opening* untuk hapus noise, *Closing* untuk menyambung goresan pena), dan penghitungan piksel *foreground*.

### 🔹 [Tugas 7 — Mini Project Integrasi (Verifikasi Ijazah Digital)](file:///home/alijundev/projects/collage/tugas-citra-digital-052/tugas-7/README.md)
- **Fokus**: Mengintegrasikan seluruh pipeline ke dalam satu sistem otomatis:
  1. Input Citra Ijazah $\rightarrow$ Konversi Grayscale.
  2. **Cabang Nomor**: Crop ROI $\rightarrow$ Enhancement (Contrast Stretching) $\rightarrow$ OCR Tesseract $\rightarrow$ Ekstraksi Nomor Ijazah.
  3. **Cabang Tanda Tangan**: Crop ROI $\rightarrow$ Otsu Thresholding $\rightarrow$ Morfologi $\rightarrow$ Klasifikasi status (`PRESENT` / `ABSENT`).
  4. **Evaluasi**: Pengukuran akurasi menggunakan metrik **Character Error Rate (CER)**.
- **Output Program**:
  ```text
  Input        : 01_HighQuality_Enhanced.jpg
  Nomor Ijazah : 571012022000056
  Tanda Tangan : PRESENT
  Evaluasi CER : Original = 0.0000 | Contrast Stretch = 0.0000
  ```

---

## 📌 Catatan Tambahan
Dokumentasi spesifik, pembahasan analitis, dan laporan detail masing-masing pertemuan dapat dilihat langsung pada berkas `README.md` di dalam setiap folder tugas.

