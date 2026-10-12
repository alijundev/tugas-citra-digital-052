import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def process_signature(image_path, roi_coords):
    # 1. Baca Citra
    img = cv2.imread(image_path)
    if img is None:
        print(f"Gagal membaca citra: {image_path}")
        return None

    # 1. Crop area tanda tangan (x, y, w, h)
    x, y, w, h = roi_coords
    roi_img = img[y:y+h, x:x+w]

    # 2. Konversi ke Grayscale
    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)

    # 3. Terapkan Minimal 2 Metode Thresholding
    # Menggunakan THRESH_BINARY_INV agar tinta (gelap) menjadi putih (255) / foreground
    _, thresh_global = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    _, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 4. Morphological Operation (Kita gunakan hasil Otsu karena biasanya lebih tahan noise)
    kernel = np.ones((3, 3), np.uint8)
    # Opening: Menghapus noise titik-titik putih kecil (salt noise) di luar tanda tangan
    opening = cv2.morphologyEx(thresh_otsu, cv2.MORPH_OPEN, kernel)
    # Closing: Menutup lubang hitam kecil (pepper noise) di dalam goresan tanda tangan
    morph_final = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    # 5. Hitung Karakteristik Area (Jumlah Piksel Foreground)
    foreground_pixels = cv2.countNonZero(morph_final)

    # 6. Aturan Sederhana (Rule-based)
    # Sesuaikan MIN_PIXELS dengan resolusi gambar ROI kamu
    MIN_PIXELS = 5000 
    
    if foreground_pixels >= MIN_PIXELS:
        status = "SIGNATURE PRESENT"
    else:
        status = "SIGNATURE ABSENT"

    return {
        "status": status,
        "pixels": foreground_pixels,
        "roi_gray": gray,
        "thresh_global": thresh_global,
        "thresh_otsu": thresh_otsu,
        "morph_final": morph_final
    }

def main():
    # Folder tempat menyimpan gambar uji
    input_folder = os.path.join(os.path.dirname(__file__), "..", "resources", "ijazah")
    
    # Kordinat ROI (x, y, width, height) - Sesuaikan dengan area TTD kepala sekolah di ijazahmu
    ROI_COORDS = (465, 1750, (1400-465), (2030-1750)) 
    
    image_files = glob.glob(os.path.join(input_folder, "*.jpg")) + glob.glob(os.path.join(input_folder, "*.png"))
    
    if not image_files:
        print("Tidak ada gambar ditemukan")
        return

    print(f"{'Nama File':<20} | {'Jumlah Piksel':<15} | {'Status'}")
    print("-" * 60)

    for file_path in image_files:
        filename = os.path.basename(file_path)
        result = process_signature(file_path, ROI_COORDS)
        
        if result:
            print(f"{filename:<20} | {result['pixels']:<15} | {result['status']}")
            
            # --- Visualisasi Komparasi (Bandingkan Hasilnya) ---
            plt.figure(figsize=(12, 3))
            
            plt.subplot(1, 4, 1)
            plt.title("Grayscale ROI")
            plt.imshow(result['roi_gray'], cmap='gray')
            plt.axis('off')
            
            plt.subplot(1, 4, 2)
            plt.title("Global Threshold")
            plt.imshow(result['thresh_global'], cmap='gray')
            plt.axis('off')
            
            plt.subplot(1, 4, 3)
            plt.title("Otsu Threshold")
            plt.imshow(result['thresh_otsu'], cmap='gray')
            plt.axis('off')

            plt.subplot(1, 4, 4)
            plt.title(f"Morph (Final)\n{result['status']}")
            plt.imshow(result['morph_final'], cmap='gray')
            plt.axis('off')
            
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main()