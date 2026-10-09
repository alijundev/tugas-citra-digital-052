# Laporan Praktikum & Analisis — Tugas Pertemuan 7
## Mini Project Integrasi: Sistem Verifikasi Ijazah Digital

---

## 1. Pendahuluan & Gambaran Masalah
Sistem verifikasi dokumen ijazah digital dirancang untuk mengotomatisasi validasi dua elemen krusial:
1. **Nomor Ijazah**: Membaca deretan kode/nomor seri dokumen menggunakan *Optical Character Recognition* (OCR).
2. **Tanda Tangan Kepala Sekolah/Dekan**: Mendeteksi keberadaan tanda tangan basah yang telah disahkan (*Signature Presence Detection*).

Tantangan utama dalam pemrosesan citra ijazah di dunia nyata adalah adanya degradasi kualitas citra seperti kontras rendah, blur (*out of focus*), derau (*high noise*), pemudaran warna (*faded/underexposed*), dan artefak kompresi JPEG. Oleh karena itu, diperlukan pipeline pengolahan citra digital terpadu untuk memastikan akurasi ekstraksi informasi.

---

## 2. Penjelasan Metode yang Digunakan

Struktur pipeline pemrosesan citra digital yang diimplementasikan:

```
                  Citra Ijazah (Input)
                           ↓
                   Konversi Grayscale
                           ↓
         ┌─────────────────┴──────────────────┐
         ↓                                    ↓
     Area Nomor                       Area Tanda Tangan
         ↓                                    ↓
  Image Enhancement                   Otsu Thresholding
         ↓                                    ↓
   Tesseract OCR                     Morfologi (Open & Close)
         ↓                                    ↓
    Nomor Ijazah                     Signature Detection
         └─────────────────┬──────────────────┘
                           ↓
                 Hasil Verifikasi Terpadu
```

### A. Preprocessing & Ekstraksi ROI
1. **Konversi ke Grayscale**:
   Citra berwarna (RGB/BGR) diubah menjadi citra intensitas satu kanal menggunakan persamaan luminansi standar ITU-R BT.601:
   $$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$
   Tujuan: Mereduksi kompleksitas komputasi serta mengeliminasi ketergantungan model terhadap perubahan warna latar (*color tint*) atau distorsi krominansi.
2. **Adaptive Cropping (Region of Interest / ROI)**:
   - **Area Nomor Ijazah**: Dipotong pada bagian kiri bawah dokumen ($y \in [2240, 2340], x \in [550, 1020]$ pada resolusi $3506 \times 2481$).
   - **Area Tanda Tangan**: Dipotong pada bagian kanan bawah dokumen ($y \in [1850, 2250], x \in [2150, 2950]$).

---

### B. Cabang Nomor Ijazah: Image Enhancement & OCR
Kualitas teks pada area nomor ditingkatkan sebelum dialirkan ke OCR Tesseract:
1. **Contrast Stretching (Min-Max Normalization)**:
   Merentangkan jangkauan nilai piksel dari rentang dinamis sempit $[\min, \max]$ ke rentang penuh $[0, 255]$:
   $$I_{\text{out}}(x, y) = \frac{I_{\text{in}}(x, y) - I_{\min}}{I_{\max} - I_{\min}} \times 255$$
   Metode ini mempertegas perbedaan antara tinta teks angka dan kertas putih tanpa merusak geometri karakter.
2. **Histogram Equalization**:
   Mentransformasikan fungsi distribusi kumulatif (CDF) intensitas piksel agar terdistribusi merata di seluruh rentang skala abu-abu.
3. **Sharpening Filter (High-pass Laplacian Convolution)**:
   Menggunakan kernel penajaman $3 \times 3$:
   $$K = \begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}$$
   Metode ini menonjolkan gradien perubahan intensitas pada garis batas tepi karakter.
4. **Optical Character Recognition (OCR Tesseract)**:
   Menggunakan engine Tesseract dengan konfigurasi `--oem 3 --psm 7` (*Page Segmentation Mode 7: Treat the image as a single text line*). Konfigurasi ini sangat optimal untuk pembacaan nomor serial baris tunggal.

---

### C. Cabang Tanda Tangan: Thresholding, Morfologi & Deteksi
1. **Otsu Thresholding (Binary Inverted)**:
   Algoritma Otsu secara otomatis menentukan nilai ambang pemisah $T^*$ yang meminimalkan varians intra-kelas (atau memaksimalkan varians antar-kelas):
   $$\sigma_B^2(T) = \omega_0(T) \omega_1(T) [\mu_0(T) - \mu_1(T)]^2$$
   Dengan inversi biner (`THRESH_BINARY_INV`), goresan tinta tanda tangan bernilai $255$ (putih / *foreground*), sedangkan kertas dokumen bernilai $0$ (hitam / *background*).
2. **Operasi Morfologi**:
   - **Opening ($3 \times 3$)**: Erosi dilanjutkan dengan Dilasi.
     $$\text{Open}(A, B) = (A \ominus B) \oplus B$$
     Fungsi: Menghilangkan derau bintik-bintik putih (*salt noise*) dan kotoran latar belakang yang lebih kecil dari ukuran kernel.
   - **Closing ($3 \times 3$)**: Dilasi dilanjutkan dengan Erosi.
     $$\text{Close}(A, B) = (A \oplus B) \ominus B$$
     Fungsi: Menjembatani putusnya garis guratan tanda tangan akibat goresan tinta pena yang tipis atau putus-putus.
3. **Aturan Deteksi Tanda Tangan (*Decision Rule*)**:
   Menghitung total piksel *foreground* ($N_{\text{fg}}$) pada area ROI:
   $$N_{\text{fg}} = \sum_{x, y} [I_{\text{morph}}(x, y) == 255]$$
   - Jika $N_{\text{fg}} > 3000$ piksel, maka tanda tangan diklasifikasikan sebagai **`SIGNATURE PRESENT`**.
   - Jika $N_{\text{fg}} \le 3000$ piksel, maka tanda tangan diklasifikasikan sebagai **`SIGNATURE ABSENT`**.

---

## 3. Analisis Nilai CER (Character Error Rate)

### Formula CER
Character Error Rate diukur menggunakan jarak Levenshtein (*Edit Distance*) antara teks referensi (*Ground Truth*) $R$ dan teks hipotesis OCR $H$:
$$\text{CER} = \frac{S + D + I}{N}$$
Di mana:
- $S$: Jumlah substitusi karakter
- $D$: Jumlah karakter yang terhapus (delesi)
- $I$: Jumlah karakter yang tersisip (insersi)
- $N$: Jumlah panjang karakter referensi ($N = 15$ untuk ground truth `"571012022000056"`)

### Tabel Hasil Pengujian CER pada 9 Kondisi Citra

| No | Kondisi Citra Ijazah | Original | Contrast Stretching | Histogram Equalization | Sharpening |
|:--:|--------------------------------------|:--------:|:-------------------:|:----------------------:|:----------:|
| 1  | `01_HighQuality_Enhanced.jpg`        |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 2  | `02_LowContrast.jpg`                 |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 3  | `03_Blurred.jpg`                     |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 4  | `04_HighNoise.jpg`                   |  0.0000  |     **0.0000**      |         0.0667         |   0.0000   |
| 5  | `05_LowResolution_Upsampled.jpg`     |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 6  | `06_Faded_Underexposed.jpg`          |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 7  | `07_ColorShift_WarmTint.jpg`         |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 8  | `08_JPEGCompression_Artifacts.jpg`   |  0.0000  |     **0.0000**      |         0.0000         |   0.0000   |
| 9  | `09_CombinedDegradation.jpg`         |  0.0000  |     **0.0000**      |         0.1333         |   0.0000   |
| **-** | **Rata-rata CER**                | **0.0000** |   **0.0000**        |       **0.0222**       | **0.0000** |

---

### Metode Enhancement Mana yang Paling Efektif?

Berdasarkan hasil eksperimen di atas:
1. **Metode Paling Efektif**: **Contrast Stretching** (serta **Sharpening**) merupakan metode yang paling konsisten dan efektif dengan **rata-rata $\text{CER} = 0.0000$ (Akurasi 100%)** pada seluruh variasi citra degradasi.
2. **Alasan Efektivitas Contrast Stretching**:
   - *Contrast Stretching* melakukan normalisasi linear yang melebarkan kontras dinamis antara karakter dan latar kertas secara proporsional.
   - Tidak mengubah relasi intensitas lokal sehingga tidak memunculkan artefak baru.
3. **Mengapa Histogram Equalization Kurang Efektif?**:
   - Pada citra `04_HighNoise` dan `09_CombinedDegradation`, nilai CER mengalami penurunan akurasi (CER naik menjadi $0.0667$ dan $0.1333$).
   - Histogram Equalization memaksa perataan histogram secara agresif ke seluruh skala intensitas. Akibatnya, derau latar belakang (*background noise* dan bintik-bintik kompresi) ikut terangkat menjadi gelap menyerupai guratan karakter, yang menyebabkan salah baca pada Tesseract OCR.

---

## 4. Kesimpulan
1. Integrasi alur pemrosesan citra digital dengan pemisahan cabang ROI terbukti sangat efektif:
   - Cabang nomor ijazah dioptimalkan dengan **Contrast Stretching + OCR Tesseract**.
   - Cabang tanda tangan dioptimalkan dengan **Otsu Thresholding + Operasi Morfologi (Open & Close)**.
2. Sistem berhasil menghasilkan output verifikasi terpadu yang akurat:
   - Membaca nomor ijazah secara tepat (`571012022000056`).
   - Mengklasifikasikan keberadaan tanda tangan kepala sekolah secara konsisten (`PRESENT`).

