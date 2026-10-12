import cv2
import glob
import os
import pytesseract

# Konfigurasi ROI nomor ijazah (sama dengan main.py)
CROP_Y1, CROP_Y2 = 2240, 2340
CROP_X1, CROP_X2 = 550, 1020

# Ambil daftar gambar
image_paths = sorted(glob.glob('./resources/ijazah/*.jpg'))
if not image_paths:
    image_paths = sorted(glob.glob('../resources/ijazah/*.jpg'))

print("=== PENGUJIAN OCR TESSERACT ===")
# Konfigurasi Tesseract:
# --psm 7 (mengasumsikan gambar adalah satu baris teks)
# -c tessedit_char_whitelist=0123456789 (memaksa OCR hanya membaca angka)
custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

for img_path in image_paths:
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    img_cropped = img[CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]

    # Penerapan 3 metode enhancement sesuai tugas:
    # 1. Brightness Adjustment (+40)
    img_brightness = cv2.convertScaleAbs(img_cropped, alpha=1.0, beta=40)

    # 2. Contrast Stretching (Min-Max Normalization 0-255)
    img_contrast = cv2.normalize(img_cropped, None, 0, 255, cv2.NORM_MINMAX)

    # 3. Histogram Equalization
    img_hist_eq = cv2.equalizeHist(img_cropped)

    # Proses OCR untuk setiap metode
    text_ori = pytesseract.image_to_string(img_cropped, config=custom_config).strip()
    text_bright = pytesseract.image_to_string(img_brightness, config=custom_config).strip()
    text_contrast = pytesseract.image_to_string(img_contrast, config=custom_config).strip()
    text_hist_eq = pytesseract.image_to_string(img_hist_eq, config=custom_config).strip()

    print(f"File: {os.path.basename(img_path)}")
    print(f"  Hasil OCR Original             : '{text_ori}'")
    print(f"  Hasil OCR Brightness Adj (+40) : '{text_bright}'")
    print(f"  Hasil OCR Contrast Stretching  : '{text_contrast}'")
    print(f"  Hasil OCR Histogram Eq         : '{text_hist_eq}'")
    print("-" * 60)