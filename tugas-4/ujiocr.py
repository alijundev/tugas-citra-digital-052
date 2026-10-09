import pytesseract

print("=== PENGUJIAN OCR TESSERACT ===")
# Konfigurasi Tesseract:
# --psm 7 (mengasumsikan gambar adalah satu baris teks)
# -c tessedit_char_whitelist=0123456789 (memaksa OCR hanya membaca angka)
custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

for img_path in image_paths:
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None: continue

    img_cropped = img[CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]
    img_contrast = cv2.normalize(img_cropped, None, 0, 255, cv2.NORM_MINMAX)

    # Proses OCR
    text_ori = pytesseract.image_to_string(img_cropped, config=custom_config).strip()
    text_enh = pytesseract.image_to_string(img_contrast, config=custom_config).strip()

    print(f"File: {os.path.basename(img_path)}")
    print(f"Hasil OCR Original           : '{text_ori}'")
    print(f"Hasil OCR Contrast Stretching: '{text_enh}'")
    print("-" * 60)