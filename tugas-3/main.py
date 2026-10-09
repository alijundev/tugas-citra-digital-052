import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def analyze_and_plot(image_path):
    # 1. Baca citra dan konversi ke RGB & Grayscale
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print(f"Gagal memuat: {image_path}")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 2. Hitung Histogram
    # Histogram RGB (Pisahkan channel R, G, B)
    color = ('r', 'g', 'b')

    # Setup plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    filename = os.path.basename(image_path)
    fig.suptitle(f'Analisis Citra: {filename}', fontsize=16)

    # Plot Citra RGB Asli
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title('Citra Asli (RGB)')
    axes[0, 0].axis('off')

    # Plot Histogram RGB
    for i, col in enumerate(color):
        hist_rgb = cv2.calcHist([img_rgb], [i], None, [256], [0, 256])
        axes[0, 1].plot(hist_rgb, color=col)
    axes[0, 1].set_title('Histogram RGB')
    axes[0, 1].set_xlim([0, 256])

    # Plot Citra Grayscale
    axes[1, 0].imshow(img_gray, cmap='gray')
    axes[1, 0].set_title('Citra Grayscale')
    axes[1, 0].axis('off')

    # Plot Histogram Grayscale
    hist_gray = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
    axes[1, 1].plot(hist_gray, color='black')
    axes[1, 1].set_title('Histogram Grayscale')
    axes[1, 1].set_xlim([0, 256])

    plt.tight_layout()
    
    output_filename = f"plot_{filename.split('.')[0]}.png"
    output_path = os.path.join(os.path.dirname(__file__), 'result', output_filename)
    
    # Simpan grafik ke folder 'result'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Berhasil menyimpan: {output_path}")
    
    plt.close(fig)

# Eksekusi untuk semua citra di folder
image_files = glob.glob('./resources/ijazah/*.jpg')
print(image_files)
for file in image_files:
    print("H")
    analyze_and_plot(file)