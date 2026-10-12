# Laporan Praktikum — Tugas Pertemuan 4
## Enhancement Nomor Ijazah & Pengujian OCR

**Mata Kuliah:** Pengolahan Citra Digital  
**Topik:** Peningkatan Kualitas Citra (*Image Enhancement*) dan Evaluasi Keterbacaan Karakter (OCR)  

---

## 1. Pendahuluan

Pada dokumen resmi seperti ijazah, kejelasan nomor ijazah sangat krusial untuk keperluan verifikasi identitas secara otomatis. Namun, proses digitalisasi (pemindaian atau pemotretan) seringkali menghasilkan degradasi citra seperti kontras rendah, pencahayaan redup, atau derau latar belakang.

Praktikum ini berfokus pada peningkatan kualitas citra (*image enhancement*) khusus pada area nomor ijazah (*Region of Interest* / ROI) menggunakan tiga metode:
1. **Brightness Adjustment** (penambahan nilai kecerahan konstan)
2. **Contrast Stretching** (normalisasi linier Min-Max ke rentang $[0, 255]$)
3. **Histogram Equalization** (perataan histogram non-linier berbasis CDF)

Setelah dilakukan perbaikan citra, hasilnya diuji menggunakan mesin OCR (*Optical Character Recognition*) Tesseract dengan konfigurasi `--oem 3 --psm 7` dan *whitelist* karakter angka `0-9` untuk mengetahui metode mana yang paling optimal dalam membantu pengenalan teks.

---

## 2. Hasil Pengujian & Komparasi OCR

Target nomor ijazah yang benar (*Ground Truth*) adalah: **`571012022000056`** (15 digit).

Berikut adalah ringkasan hasil pembacaan OCR pada ke-9 variasi citra ijazah setelah diterapkan masing-masing metode perbaikan:

| No | File Citra | Hasil OCR Original | Brightness Adj (+40) | Contrast Stretching | Histogram Equalization | Keterangan & Analisis |
|:--:|------------|--------------------|----------------------|---------------------|------------------------|-----------------------|
| 1 | `01_HighQuality_Enhanced.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Sempurna pada semua metode karena kualitas awal sudah tinggi. |
| 2 | `02_LowContrast.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Contrast stretching mempertegas batas angka yang tadinya pudar. |
| 3 | `03_Blurred.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Terbaca baik meski tepi karakter agak meluber. |
| 4 | `04_HighNoise.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `57101202200005` (gagal 1 digit) | Histogram Eq menaikkan bintik noise di sekitar angka terakhir. |
| 5 | `05_LowResolution_Upsampled.jpg`| `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Berhasil terbaca dengan baik. |
| 6 | `06_Faded_Underexposed.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Contrast stretching membuat latar kembali putih terang. |
| 7 | `07_ColorShift_WarmTint.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Konversi grayscale mengeliminasi efek warna hangat. |
| 8 | `08_JPEGCompression_Artifacts` | `571012022000056` | `571012022000056` | `571012022000056` | `571012022000056` | Terbaca stabil pada semua metode. |
| 9 | `09_CombinedDegradation.jpg` | `571012022000056` | `571012022000056` | `571012022000056` | `5710120220000` (gagal 2 digit) | Histogram Eq merusak kontur digit terakhir akibat akumulasi noise. |

---

## 3. Analisis dan Jawaban Pertanyaan

### 1. Mengapa peningkatan contrast dapat membantu OCR mengenali karakter nomor ijazah?

Mesin OCR (khususnya Tesseract) bekerja dengan cara melakukan segmentasi biner internal (*binarization/thresholding*) untuk memisahkan goresan karakter (*foreground*) dari latar belakang kertas (*background*). 

Pada citra yang memiliki kontras rendah (*low contrast*), selisih nilai intensitas piksel antara teks angka dan latar kertas sangat kecil (misal teks bernilai 120 dan latar bernilai 150). Kondisi ini menyulitkan algoritma binarisasi OCR dalam menentukan garis batas (*edge boundary*) pemisah karakter, sehingga huruf rawan putus atau melebur ke latar belakang.

Dengan melakukan **peningkatan kontras (*Contrast Stretching*)**:
- Rentang dinamis piksel direntangkan dari yang semula sempit menjadi skala penuh $[0, 255]$.
- Nilai piksel teks yang relatif gelap ditarik mendekati 0 (hitam pekat), sementara nilai piksel latar ditarik mendekati 255 (putih bersih).
- Hal ini mempertegas perbedaan intensitas (*gradient*) secara tajam, sehingga binarisasi pada tahap pra-pemrosesan OCR menjadi sangat mudah dan menghasilkan fitur kontur karakter yang tegas dan akurat.

---

### 2. Apakah histogram equalization selalu merupakan metode terbaik untuk meningkatkan kualitas nomor ijazah? Jelaskan berdasarkan hasil eksperimen.

**Tidak, Histogram Equalization bukan selalu metode terbaik.**

Berdasarkan hasil eksperimen di atas:
1. **Histogram Equalization Bersifat Agresif & Global:**  
   Metode ini bekerja dengan meratakan fungsi distribusi kumulatif (CDF) ke seluruh tingkat keabuan. Pada area nomor ijazah di mana mayoritas piksel adalah latar kertas putih, histogram equalization berusaha mendistribusikan piksel latar tersebut ke spektrum warna abu-abu hingga gelap.
2. **Memperkuat Derau Latar (*Amplifying Noise*):**  
   Pada citra dengan derau seperti `04_HighNoise.jpg` dan `09_CombinedDegradation.jpg`, bintik-bintik derau halus pada kertas yang seharusnya tidak terlihat justru diperjelas dan digelapkan. Akibatnya, timbul artefak bercak hitam di sekitar karakter angka. Mesin OCR mengenali bercak-bercak ini sebagai bagian dari karakter, yang menyebabkan salah baca atau karakter gagal terdeteksi (misal digit terakhir `56` hilang/terpotong).
3. **Contrast Stretching Lebih Unggul:**  
   Sebaliknya, *Contrast Stretching* melakukan transformasi linier proporsional tanpa memaksakan perataan frekuensi. Relasi spasial antar piksel tetap terjaga sehingga teks menjadi tajam tanpa membangkitkan derau baru.

---

## 4. Kesimpulan

- Metode **Contrast Stretching** terbukti sebagai metode perbaikan yang paling optimal, stabil, dan aman untuk pra-pemrosesan OCR nomor ijazah dengan tingkat keberhasilan pembacaan 100% di semua variasi citra degradasi.
- **Histogram Equalization** kurang direkomendasikan untuk dokumen teks yang memiliki noise karena dapat merusak kejelasan kontur karakter akibat pengangkatan derau latar belakang.
