import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# 1. Tentukan path folder tempat gambar di-upload
image_folder = '/content/ijazah/*'
image_paths = glob.glob(image_folder)

# PENTING: Sesuaikan koordinat crop area nomor ijazah di sini (y1, y2, x1, x2)
# Format slicing array: img[y1:y2, x1:x2]
# Jika ke-9 ijazah memiliki tata letak berbeda, kamu mungkin perlu menyesuaikan
# ini satu per satu, tapi jika formatnya sama, satu set koordinat cukup.
CROP_Y1, CROP_Y2 = 2240, 2340  # Ganti dengan koordinat Y atas dan bawah
CROP_X1, CROP_X2 = 550, 1020  # Ganti dengan koordinat X kiri dan kanan

if len(image_paths) == 0:
    print("Belum ada gambar di folder /content/ijazah. Silakan upload terlebih dahulu.")

for img_path in image_paths:
    # Baca citra dalam mode Grayscale (karena operasi histogram lebih optimal di grayscale)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        continue

    # Crop area nomor ijazah
    # Jika kamu belum tahu koordinatnya dan ingin mencoba full image dulu,
    # ubah img_cropped = img.copy()
    img_cropped = img[CROP_Y1:CROP_Y2, CROP_X1:CROP_X2]

    # --- METODE ENHANCEMENT ---

    # a. Brightness Adjustment (Menambah kecerahan, misal +40)
    # cv2.convertScaleAbs mencegah nilai piksel melebihi 255 atau kurang dari 0
    img_brightness = cv2.convertScaleAbs(img_cropped, alpha=1.0, beta=40)

    # b. Contrast Stretching (Min-Max Normalization ke rentang 0-255)
    img_contrast = cv2.normalize(img_cropped, None, 0, 255, cv2.NORM_MINMAX)

    # c. Histogram Equalization
    img_hist_eq = cv2.equalizeHist(img_cropped)

    # --- VISUALISASI HASIL ---
    images = [img_cropped, img_brightness, img_contrast, img_hist_eq]
    titles = ['1. Original (Cropped)', '2. Brightness Adj', '3. Contrast Stretch', '4. Histogram Eq']

    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    fig.suptitle(f'Hasil Enhancement: {os.path.basename(img_path)}', fontsize=16)

    for i in range(4):
        # Plot Citra
        axes[0, i].imshow(images[i], cmap='gray', vmin=0, vmax=255)
        axes[0, i].set_title(titles[i])
        axes[0, i].axis('off')

        # Plot Histogram
        # ravel() digunakan untuk meratakan array 2D menjadi 1D
        axes[1, i].hist(images[i].ravel(), bins=256, range=[0, 256], color='black')
        axes[1, i].set_title(f'Histogram {titles[i]}')
        axes[1, i].set_xlim([0, 256])
        axes[1, i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()
    print("-" * 100)