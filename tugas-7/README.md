# Tugas Pertemuan 7 — Mini Project Integrasi Verifikasi Ijazah Digital

Repositori ini berisi implementasi **Mini Project Integrasi (Tugas 7)** untuk mata kuliah Pengolahan Citra Digital. Sistem ini merupakan sebuah prototype otomatis yang memverifikasi dokumen ijazah dengan membaca **Nomor Ijazah** menggunakan Optical Character Recognition (OCR) serta mendeteksi keberadaan **Tanda Tangan Kepala Sekolah/Dekan**.

---

## 1. Alur Pipeline Sistem

Pipeline pemrosesan citra digital yang diimplementasikan mengikuti diagram alur berikut:

```
                  Citra Ijazah (Input)
                           ↓
                   Konversi Grayscale
                           ↓
                    Image Enhancement
                           ↓
         ┌─────────────────┴──────────────────┐
         ↓                                    ↓
     Area Nomor                       Area Tanda Tangan
         ↓                                    ↓
  Enhancement ROI                     Thresholding (Otsu)
         ↓                                    ↓
   Tesseract OCR                     Morfologi (Open & Close)
         ↓                                    ↓
    Nomor Ijazah                     Signature Detection
         └─────────────────┬──────────────────┘
                           ↓
              Hasil Verifikasi Terpadu:
              - Nomor Ijazah : 571012022000056
              - Tanda Tangan : PRESENT / ABSENT
```

---

## 2. Penjelasan Metode yang Digunakan

### A. Preprocessing & Ekstraksi ROI
1. **Grayscale Conversion**: Mengubah citra RGB/BGR menjadi citra intensitas 1-kanal menggunakan rumus luminansi $Y = 0.299R + 0.587G + 0.114B$. Hal ini mereduksi dimensi data citra sekaligus menghilangkan pengaruh variasi warna/tint kertas.
2. **Adaptive ROI Cropping**: Memotong area nomor ijazah (kiri bawah) dan area tanda tangan (kanan bawah) menggunakan koordinat bounding box yang proporsional terhadap resolusi citra input.

---

### B. Cabang Nomor Ijazah: Enhancement & OCR
Pada area nomor ijazah, diterapkan beberapa metode peningkatan kualitas citra (Image Enhancement) untuk memaksimalkan akurasi pembacaan karakter:
1. **Contrast Stretching (Min-Max Normalization)**:
   $$\text{dst}(x,y) = \frac{\text{src}(x,y) - \min}{\max - \min} \times 255$$
   Merentangkan rentang dinamis piksel yang sempit ke rentang penuh $[0, 255]$. Sangat efektif untuk citra berpencahayaan rendah (*underexposed*) atau pudar (*faded*).
2. **Histogram Equalization**: Meratakan distribusi probabilitas intensitas kumulatif (CDF). Metode ini meningkatkan kontras global, namun dapat memperkuat noise latar belakang pada citra bersensitivitas tinggi.
3. **Sharpening Filter (High-Pass Convolution)**:
   Menggunakan kernel Laplacian:
   $$\begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}$$
   Mempertegas tepi batas (*edge*) antara karakter angka dengan latar belakang kertas.
4. **Gaussian Blur + Adaptive Binarization**: Mengeliminasi noise frekuensi tinggi lalu membinerkan piksel berdasarkan nilai lokal lingkungan tetangga.
5. **OCR Tesseract (`--psm 7`)**: Membaca citra baris tunggal secara spesifik untuk mengekstrak string nomor ijazah.

---

### C. Cabang Tanda Tangan: Thresholding & Morfologi
1. **Otsu Thresholding (Binary Inverted)**:
   - Menggunakan algoritma Otsu untuk mencari nilai ambang batas (*threshold*) optimal otomatis yang meminimalkan varians intra-kelas.
   - Menggunakan opsi `THRESH_BINARY_INV` agar goresan tinta pena menjadi nilai **255 (putih / foreground)** dan kertas menjadi **0 (hitam / background)**.
2. **Morphological Opening**:
   $$\text{Open}(A, B) = (A \ominus B) \oplus B$$
   Erosi diikuti dilasi dengan kernel persegi berukuran $3 \times 3$. Bertujuan menghapus bintik-bintik derau (*salt noise*) atau serat kertas yang terbinerkan.
3. **Morphological Closing**:
   $$\text{Close}(A, B) = (A \oplus B) \ominus B$$
   Dilasi diikuti erosi dengan kernel persegi berukuran $5 \times 5$. Berfungsi menyambung kembali goresan tinta pena tipis yang terputus-putus.
4. **Analisis Karakteristik Area & Aturan Keputusan**:
   - Menghitung total piksel foreground ($\text{fg\_pixels}$) dan rasio kepadatan tanda tangan ($\text{density} = \frac{\text{fg\_pixels}}{\text{area}} \times 100\%$).
   - **Aturan**:
     - Jika $\text{fg\_pixels} \ge 3000$ dan $\text{density} \ge 0.8\%$, maka **`SIGNATURE PRESENT`**.
     - Jika tidak memenuhi batas tersebut, maka **`SIGNATURE ABSENT`**.

---

## 3. Evaluasi Efektivitas Enhancement Berdasarkan CER (Character Error Rate)

### Definisi CER
Character Error Rate dihitung menggunakan metrik Levenshtein Distance (jarak edit minimum):
$$\text{CER} = \frac{S + D + I}{N}$$
Di mana:
- $S$: Jumlah karakter yang disubstitusi (diganti).
- $D$: Jumlah karakter yang dideplesi (dihapus).
- $I$: Jumlah karakter yang diinsersi (ditambahkan).
- $N$: Jumlah total karakter pada teks referensi (*Ground Truth*).

Semakin kecil nilai CER (mendekati $0.0$), semakin akurat metode enhancement tersebut.

### Hasil Uji Komparasi pada Dataset Ijazah

Pengujian dilakukan pada seluruh 9 skenario degradasi citra di `resources/ijazah/` dengan Ground Truth: **`571012022000056`** ($N = 15$).

| No | Kondisi Citra Ijazah | Original (CER) | Contrast Stretch (CER) | Hist. Equalization (CER) | Sharpening (CER) |
|---|-------------------------------------|:--------------:|:----------------------:|:------------------------:|:----------------:|
| 1 | 01_HighQuality_Enhanced.jpg        | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 2 | 02_LowContrast.jpg                  | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 3 | 03_Blurred.jpg                      | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 4 | 04_HighNoise.jpg                    | 0.0000         | **0.0000**             | 0.0667                   | 0.0000           |
| 5 | 05_LowResolution_Upsampled.jpg      | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 6 | 06_Faded_Underexposed.jpg           | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 7 | 07_ColorShift_WarmTint.jpg          | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 8 | 08_JPEGCompression_Artifacts.jpg    | 0.0000         | **0.0000**             | 0.0000                   | 0.0000           |
| 9 | 09_CombinedDegradation.jpg          | 0.0000         | **0.0000**             | 0.1333                   | 0.0000           |
| **-** | **Rata-rata CER Keseluruhan**    | **0.0000**     | **0.0000**             | **0.0222**               | **0.0000**       |

### Analisis Metode yang Paling Efektif
1. **Metode Paling Efektif**: **Contrast Stretching** dan **Sharpening** terbukti paling stabil dan efektif dengan rata-rata **CER = 0.0000 (Akurasi 100%)**.
2. **Kelemahan Histogram Equalization**: Histogram Equalization mengalami degradasi performa pada citra `HighNoise` dan `CombinedDegradation` (CER naik hingga $0.1333$). Hal ini terjadi karena Histogram Equalization meratakan intensitas secara agresif ke seluruh skala abu-abu, sehingga derau latar belakang (*background grain/artifacts*) ikut diperkuat menyerupai goresan karakter, yang membingungkan engine Tesseract OCR.
3. **Kesimpulan**: *Contrast Stretching* adalah pilihan terbaik untuk tahap pra-OCR karena memaksimalkan kontras tepi teks secara proporsional tanpa menghasilkan artefak noise berlebih.

---

## 4. Panduan Menjalankan Program (*How to Run*)

### Prasyarat
- Tesseract OCR terpasang di sistem (`tesseract --version`)
- Dependensi: `opencv-python`, `numpy`, `pytesseract`

### Cara Menjalankan
Jalankan script langsung dari terminal:
```bash
python tugas-7/main.py
```
atau menggunakan `uv`:
```bash
uv run python tugas-7/main.py
```

---

## 5. Contoh Output Program

```text
=============================================
Input        : 01_HighQuality_Enhanced.jpg
Nomor Ijazah : 571012022000056
Tanda Tangan : PRESENT
---------------------------------------------
Evaluasi CER : Original = 0.0000 | Contrast Stretch = 0.0000
=============================================
```