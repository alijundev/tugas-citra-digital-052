# Instal Tesseract OCR di Fedora
!apt-get install tesseract tesseract-langpack-eng

# Instal library Python yang dibutuhkan
!pip install opencv-python pytesseract matplotlib numpy





import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import os

def process_and_ocr_with_fixed_roi(image_path, roi_coords):
    # Membaca citra berwarna
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Gambar {image_path} tidak ditemukan.")
        return

    # 1. Ekstrak koordinat ROI yang sudah ditetapkan
    x, y, w, h = roi_coords

    # 2. Crop gambar sesuai koordinat (slicing array numpy)
    cropped_img = img[y:y+h, x:x+w]

    # Konversi hasil crop ke grayscale untuk pemrosesan filter
    img_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    # 3. Terapkan Filter pada gambar yang sudah di-crop
    mean_filtered = cv2.blur(img_gray, (5, 5))
    median_filtered = cv2.medianBlur(img_gray, 5)
    gaussian_filtered = cv2.GaussianBlur(img_gray, (5, 5), 0)

    kernel_sharpening = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    sharpened = cv2.filter2D(img_gray, -1, kernel_sharpening)

    # 4. Fungsi pembantu untuk OCR
    def get_ocr_text(image):
        # config --psm 7 memaksa Tesseract membaca gambar sebagai 1 baris teks tunggal
        text = pytesseract.image_to_string(image, config='--psm 7').strip()
        return text

    # Dictionary hasil
    results = {
        "Original ROI": (img_gray, get_ocr_text(img_gray)),
        "Mean Filter": (mean_filtered, get_ocr_text(mean_filtered)),
        "Median Filter": (median_filtered, get_ocr_text(median_filtered)),
        "Gaussian Filter": (gaussian_filtered, get_ocr_text(gaussian_filtered)),
        "Sharpening": (sharpened, get_ocr_text(sharpened))
    }

    # 5. Tampilkan hasil di Terminal
    print(f"\n{'='*45}")
    print(f"Hasil Ekstraksi OCR - {os.path.basename(image_path)}")
    print(f"{'='*45}")

    for method, (processed_img, text) in results.items():
        print(f"{method:15} | Hasil OCR: {text}")

    # 6. Visualisasi plot
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    fig.suptitle(f'Hasil Enhancement - {os.path.basename(image_path)}', fontsize=14)
    axes = axes.ravel()

    for idx, (method, (processed_img, text)) in enumerate(results.items()):
        axes[idx].imshow(processed_img, cmap='gray')
        axes[idx].set_title(f"{method}\nOCR: {text}", fontsize=10)
        axes[idx].axis('off')

    axes[-1].axis('off')
    plt.tight_layout()
    plt.show()

# --- KONFIGURASI ROI DAN DAFTAR FILE ---

# GANTI ANGKA INI DENGAN KOORDINAT ROI YANG KAMU MILIKI
# Format: (x_awal, y_awal, lebar/width, tinggi/height)
roi_tetap = (550, 2252, (1020-550), (2330-2252))

# Laluan folder yang mengandungi 9 gambar anda
folder_path = "/content"

# Ekstrak semua fail gambar secara automatik
if os.path.exists(folder_path):
    # Dapatkan senarai fail dengan format gambar
    format_gambar = ('.png', '.jpg', '.jpeg', '.bmp')
    list_gambar = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                   if f.lower().endswith(format_gambar)]

    # Susun senarai fail supaya diproses mengikut urutan nama (pilihan)
    list_gambar.sort()

    print(f"Jumpa {len(list_gambar)} gambar di dalam folder {folder_path}.\nMemulakan proses...")

    # Jalankan proses untuk setiap gambar
    for gambar in list_gambar:
        process_and_ocr_with_fixed_roi(gambar, roi_tetap)
else:
    print(f"Folder '{folder_path}' tidak dijumpai. Sila pastikan folder tersebut wujud dan ejaannya betul.")