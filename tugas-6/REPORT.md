# Laporan Analisis: Deteksi Tanda Tangan Kepala Sekolah

**Mata Kuliah:** Citra Digital  
**Dosen:** Muhammad Riansyah Tohamba S.T., M.Kom  

---

## Analisis Metode

Dalam proses mendeteksi keberadaan tanda tangan kepala sekolah pada citra ijazah, terdapat beberapa tahapan penting seperti *cropping* ROI (Region of Interest), konversi ke grayscale, *thresholding*, hingga operasi morfologi. Berikut adalah analisis dari penerapan metode tersebut:

### 1. Mengapa thresholding diperlukan sebelum melakukan analisis keberadaan tanda tangan?

Thresholding sangat diperlukan karena berfungsi memisahkan objek utama (tanda tangan) dari background (kertas ijazah) dengan cara mengubah citra *grayscale* (yang memiliki 256 tingkat kecerahan) menjadi citra biner (hanya bernilai 0 dan 255 / hitam dan putih). 

Proses ini sangat krusial karena menyederhanakan struktur data matriks citra, sehingga sistem komputer bisa secara matematis membedakan mana yang merupakan "tinta" dan mana yang "kertas". Tanpa adanya proses thresholding, sistem tidak akan bisa menghitung jumlah piksel *foreground* secara akurat karena akan terganggu oleh gradasi warna, tekstur kertas, bayangan lipatan, atau noise pencahayaan pada saat dokumen di-scan atau difoto.

### 2. Apa masalah yang terjadi jika threshold terlalu tinggi atau terlalu rendah?

Pemilihan nilai threshold yang kurang tepat akan sangat mempengaruhi akurasi deteksi:

*   **Jika Threshold Terlalu Tinggi:** 
    Sistem akan menjadi terlalu sensitif dan menganggap area abu-abu terang di dokumen (seperti noise kertas, bayangan lipatan, kotoran, atau stempel tipis yang bertumpuk) sebagai bagian dari tanda tangan (*foreground*). Hal ini menyebabkan **False Positive**, di mana sistem mendeteksi `SIGNATURE PRESENT` (tanda tangan ada) padahal sebenarnya kosong.
    
*   **Jika Threshold Terlalu Rendah:** 
    Sistem akan menjadi kurang sensitif dan cenderung mengabaikan goresan tinta yang kurang pekat, tipis, atau pudar. Piksel-piksel pembentuk tanda tangan akan ikut terhapus karena dianggap sebagai *background*. Hal ini menyebabkan **False Negative**, di mana sistem mengeluarkan status `SIGNATURE ABSENT` padahal sebenarnya terdapat tanda tangan di area tersebut. 

Oleh karena itu, pada *mini-project* ini dilakukan komparasi antara *Global Thresholding* dan *Otsu Thresholding*. Metode Otsu seringkali memberikan hasil yang lebih adaptif karena secara otomatis mencari nilai ambang batas (*threshold*) yang paling optimal untuk memisahkan kedua kelas (background dan foreground) berdasarkan histogram citra.