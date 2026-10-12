import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import os

# Ground Truth nomor ijazah (15 digit)
GROUND_TRUTH = "571012022000056"

def hitung_akurasi(pred, target=GROUND_TRUTH):
    benar = sum(1 for p, t in zip(pred, target) if p == t)
    akurasi = (benar / len(target)) * 100
    return benar, akurasi

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
        "Original": (img_gray, get_ocr_text(img_gray)),
        "Mean Filter": (mean_filtered, get_ocr_text(mean_filtered)),
        "Median Filter": (median_filtered, get_ocr_text(median_filtered)),
        "Gaussian Filter": (gaussian_filtered, get_ocr_text(gaussian_filtered)),
        "Sharpening": (sharpened, get_ocr_text(sharpened))
    }

    # 5. Tampilkan hasil di Terminal
    print(f"\n{'='*75}")
    print(f"Hasil Evaluasi OCR - {os.path.basename(image_path)}")
    print(f"{'='*75}")
    print(f"{'Metode':16} | {'Hasil OCR':18} | {'Karakter Benar':14} | {'Akurasi':8}")
    print("-" * 75)

    for method, (processed_img, text) in results.items():
        benar, akurasi = hitung_akurasi(text)
        print(f"{method:16} | {text:18} | {benar}/{len(GROUND_TRUTH)} ({benar} char)   | {akurasi:6.2f}%")

    # 6. Visualisasi plot
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    fig.suptitle(f'Hasil Enhancement - {os.path.basename(image_path)}', fontsize=14)
    axes = axes.ravel()

    for idx, (method, (processed_img, text)) in enumerate(results.items()):
        benar, akurasi = hitung_akurasi(text)
        axes[idx].imshow(processed_img, cmap='gray')
        axes[idx].set_title(f"{method}\nOCR: {text}\nAcc: {akurasi:.1f}%", fontsize=9)
        axes[idx].axis('off')

    axes[-1].axis('off')
    plt.tight_layout()

    # Simpan hasil visualisasi ke folder 'result'
    result_dir = os.path.join(os.path.dirname(__file__), 'result')
    os.makedirs(result_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    output_path = os.path.join(result_dir, f"plot_{filename.split('.')[0]}.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Hasil plot disimpan: {output_path}")

# --- KONFIGURASI ROI DAN DAFTAR FILE ---

# Koordinat ROI nomor ijazah: (x_awal, y_awal, lebar/width, tinggi/height)
roi_tetap = (550, 2240, (1020-550), (2340-2240))

# Folder yang memuat citra ijazah
folder_path = "./resources/ijazah"
if not os.path.exists(folder_path):
    folder_path = "../resources/ijazah"

# Ekstrak semua file gambar secara otomatis
if os.path.exists(folder_path):
    format_gambar = ('.png', '.jpg', '.jpeg', '.bmp')
    list_gambar = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                   if f.lower().endswith(format_gambar)]

    list_gambar.sort()

    print(f"Ditemukan {len(list_gambar)} gambar di dalam folder {folder_path}.\nMemulai proses...")

    for gambar in list_gambar:
        process_and_ocr_with_fixed_roi(gambar, roi_tetap)
else:
    print(f"Folder '{folder_path}' tidak ditemukan. Silakan periksa path folder.")