# Deteksi Tanda Tangan Kepala Sekolah (Signature Detection)

Mini project ini adalah tugas mata kuliah Citra Digital. Sistem ini bertujuan untuk memproses citra dokumen ijazah, mengekstraksi area Region of Interest (ROI), dan mendeteksi apakah dokumen tersebut telah ditandatangani oleh kepala sekolah atau belum menggunakan metode Image Processing dasar.

## Alur Pemrosesan
1. **Cropping:** Mengambil koordinat tertentu (ROI) tempat tanda tangan berada.
2. **Grayscale:** Mengubah citra RGB menjadi keabuan.
3. **Thresholding:** Mengkomparasi **Global Thresholding** dan **Otsu Thresholding** untuk segmentasi citra menjadi *binary image*.
4. **Morphological Operations:** Menggunakan kombinasi *Opening* dan *Closing* untuk mereduksi noise (bintik-bintik hasil *scan*) dan menyambung garis putus.
5. **Karakteristik Piksel:** Menghitung total piksel bernilai *True* / Putih (foreground).
6. **Decision Rule:** Mengeluarkan hasil `SIGNATURE PRESENT` atau `SIGNATURE ABSENT` berdasarkan *threshold* jumlah piksel.

## Prasyarat (Requirements)
Project ini menggunakan [uv](https://github.com/astral-sh/uv) sebagai Python package manager (pengganti pip/venv). Pastikan `uv` versi terbaru sudah terpasang di sistem operasi Anda.

Library yang digunakan:
- OpenCV (`opencv-python`)
- NumPy (`numpy`)
- Matplotlib (`matplotlib`)

## Struktur Folder
```text
/
├── dataset/                # Simpan ke-9 gambar ijazah (format .jpg atau .png) di dalam folder ini
│   ├── ijazah_1.jpg
│   ├── ijazah_2.jpgV
│   └── ...
├── main.py                 # Source code utama
└── README.md
```

## Cara running program
- Clone repo
```bash
git clone https://github.com/alijundev/tugas-6-citra-digital-052.git
cd tugas-6-citra-digital-052
```

- siapan environtment
```bash
uv sync
```
- masukkan gambar ijazah ke fodler `dataset`
- Buka file `main.py` menggunakan Text Editor dan pastikan kordinat `ROI_COORDS = (x, y, width, height)` sudah disesuaikan dengan posisi tanda tangan di gambar ijazah Anda.
- jalankan code
```bash
uv run main.py
```
- Terminal akan menampilkan tabel hasil klasifikasi jumlah piksel foreground beserta status kehadirannya. Jendela Matplotlib akan muncul bergantian menampilkan visualisasi komparasi (`Grayscale` vs `Global` vs `Otsu` vs `Morph Final`).

# Penjelasan/jawaban dari pertanyaan ada apda file `REPORT.md`