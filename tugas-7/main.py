import cv2
import numpy as np
import pytesseract
import glob
import os

# 1. Konfigurasi Ground Truth & Koordinat Crop (Format resolusi ijazah: ~3506x2481)
GROUND_TRUTH = "571012022000056"

# Koordinat Area Nomor Ijazah [y1:y2, x1:x2]
NOMOR_Y1, NOMOR_Y2 = 2240, 2340
NOMOR_X1, NOMOR_X2 = 550, 1020

# Koordinat Area Tanda Tangan Kepala Sekolah [y1:y2, x1:x2]
TTD_Y1, TTD_Y2 = 1850, 2250
TTD_X1, TTD_X2 = 2150, 2950

def hitung_cer(ref, hyp):
    """Menghitung Character Error Rate (CER) sederhana berbasis Levenshtein."""
    r, h = ref.strip(), hyp.strip()
    if not r: return 0.0 if not h else 1.0
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1): dp[i][0] = i
    for j in range(len(h) + 1): dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[len(r)][len(h)] / len(r)

def proses_ijazah(image_path):
    # 1. Baca Citra & Konversi ke Grayscale
    img = cv2.imread(image_path)
    if img is None:
        print(f"Gagal memuat: {image_path}")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. CABANG AREA NOMOR IJAZAH
    crop_nomor = gray[NOMOR_Y1:NOMOR_Y2, NOMOR_X1:NOMOR_X2]

    # Penerapan Image Enhancement
    # a. Contrast Stretching
    nomor_contrast = cv2.normalize(crop_nomor, None, 0, 255, cv2.NORM_MINMAX)
    # b. Histogram Equalization
    nomor_histeq = cv2.equalizeHist(crop_nomor)

    # OCR menggunakan Tesseract (--psm 7: satu baris teks)
    config_ocr = r'--oem 3 --psm 7'
    text_ori = pytesseract.image_to_string(crop_nomor, config=config_ocr).strip()
    text_enh = pytesseract.image_to_string(nomor_contrast, config=config_ocr).strip()

    # Hitung CER untuk membandingkan metode
    cer_ori = hitung_cer(GROUND_TRUTH, text_ori)
    cer_enh = hitung_cer(GROUND_TRUTH, text_enh)

    # 3. CABANG AREA TANDA TANGAN
    crop_ttd = gray[TTD_Y1:TTD_Y2, TTD_X1:TTD_X2]

    # a. Thresholding (Otsu Inverted: tinta tanda tangan jadi putih/255)
    _, thresh_ttd = cv2.threshold(crop_ttd, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # b. Morphology: Opening (hapus noise) & Closing (sambung goresan tinta)
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh_ttd, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    # c. Signature Detection: Hitung jumlah piksel putih (foreground)
    fg_pixels = np.sum(closed == 255)
    tanda_tangan = "PRESENT" if fg_pixels > 3000 else "ABSENT"

    # 4. TAMPILKAN HASIL VERIFIKASI
    print("=" * 45)
    print(f"Input        : {os.path.basename(image_path)}")
    print(f"Nomor Ijazah : {text_enh if text_enh else text_ori}")
    print(f"Tanda Tangan : {tanda_tangan}")
    print("-" * 45)
    print(f"Evaluasi CER : Original = {cer_ori:.4f} | Contrast Stretch = {cer_enh:.4f}")
    print("=" * 45 + "\n")

if __name__ == "__main__":
    # Path folder dataset ijazah
    folder_path = os.path.join(os.path.dirname(__file__), "..", "resources", "ijazah")
    image_paths = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))

    if not image_paths:
        print("Citra tidak ditemukan di folder resources/ijazah.")
    else:
        print(f"Memproses {len(image_paths)} citra ijazah...\n")
        for img_path in image_paths:
            proses_ijazah(img_path)
