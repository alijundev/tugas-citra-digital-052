## 1. Analisis Distribusi Intensitas dan Identifikasi Permasalahan Citra
Berdasarkan hasil konversi citra dari RGB ke Grayscale beserta plot histogramnya,
citra-citra tersebut dapat dikelompokkan ke dalam tiga permasalahan utama:
a. Kasus Citra dengan Kontras Rendah dan Agak Gelap (Citra 1.jpg dan 9.jpg)
- Analisis Distribusi: Histogram sangat menumpuk pada area tengah yang
sempit (berada di sekitar nilai intensitas 150-160 untuk citra 1, dan ~190
untuk citra 9). Rentang piksel yang digunakan sangat kecil dan tidak
menyebar ke arah nilai 0 (hitam pekat) maupun 255 (putih murni).
- Permasalahan: Citra memiliki kontras yang sangat rendah (low contrast).
Karena rentang dinamis yang sempit, batas antara teks ijazah dan latar
belakang kertas menjadi kurang tegas.
b. Kasus Citra Terlalu Terang / Overexposed (Citra 2.jpg, 4.jpg, 5.jpg, 6.jpg, 7.jpg,
dan 8.jpg)
- Analisis Distribusi: Histogram menunjukkan tumpukan data yang ekstrem di
sisi paling kanan (mendekati atau menyentuh nilai 255). Pada plot RGB,
terlihat ketidakseimbangan saluran di mana kurva Red dan Green
mendominasi tinggi, sementara kurva Blue tertinggal (menyebabkan gambar
terlihat kekuningan atau memiliki color cast pada citra aslinya).
- Permasalahan: Citra terlalu terang (overexposed). Puncak yang sangat tinggi
pada area putih (kanan) menyebabkan hilangnya rentang intensitas pada area
gelap, yang berisiko membuat tulisan atau garis tipis pada ijazah menjadi
pudar (washed out) atau menyatu dengan background.
c. Kasus Overexposed dengan Dominasi Warna Kuat (Citra 3.jpg)
- Analisis Distribusi: Memiliki puncak yang sangat tajam mendekati nilai
240-250 di histogram Grayscale. Pada citra aslinya, terlihat pergeseran

saluran warna (color cast) yang parah ke arah hijau/biru (cyan), ditandai
dengan saluran Red yang memuncak lebih awal secara terpisah.
- Permasalahan: Selain terlalu terang, keseimbangan warna awal sangat buruk.
Meski masalah warna hilang saat diubah ke Grayscale, intensitas latar
belakang tetap mengalahkan teks.
2. Rekomendasi Metode Enhancement
Metode peningkatkan kualitas citra harus disesuaikan dengan permasalahan yang
ada pada masing-masing kelompok gambar di atas:
a. Untuk Citra Kontras Rendah (1.jpg & 9.jpg)
Metode yang disarankan: CLAHE (Contrast Limited Adaptive Histogram
Equalization).
Alasan: Berbeda dengan Histogram Equalization global yang menaikkan kontras
seluruh gambar (yang dapat memperjelas bercak kotor pada kertas), CLAHE
membagi citra menjadi blok-blok kecil (tiles) dan meningkatkan kontras secara
lokal. Batas (clip limit) pada CLAHE mencegah noise pada latar belakang kertas
menjadi terlalu menonjol, namun tetap berhasil menajamkan teks ijazah.
b. Untuk Citra Terlalu Terang & Pudar (2.jpg hingga 8.jpg)
Metode yang disarankan: Gamma Correction (Transformasi Pangkat)
dilanjutkan dengan Adaptive Thresholding.
Alasan: Karena teks cenderung pudar, kita bisa menggunakan Gamma
Correction untuk "menarik" piksel-piksel terang menjadi lebih gelap, sehingga
memunculkan kembali detail teks. Setelah itu, Adaptive Thresholding digunakan
untuk mengubah citra menjadi biner (hitam-putih sempurna). Adaptive
thresholding sangat efektif pada dokumen karena menghitung ambang batas
secara lokal, sehingga bayangan atau pencahayaan yang tidak merata di
pinggiran kertas dapat diatasi tanpa menghilangkan teksnya.

3. Apakah citra dengan histogram yang lebih tersebar selalu memiliki kualitas
yang lebih baik?
Tidak selalu.

Secara teori umum, histogram yang merata menyebar dari 0 hingga 255 memang
menunjukkan citra dengan kontras yang baik dan kaya akan detail. Namun, aturan
ini tidak berlaku ideal untuk citra dokumen tertulis (seperti ijazah).

Citra dokumen memiliki karakteristik yang unik. Citra dokumen yang berkualitas
baik justru idealnya memiliki histogram bimodal, yaitu memiliki dua puncak
dominan:

Satu puncak kecil di area nilai rendah (gelap) yang mewakili tinta teks, tanda
tangan, atau logo.

Satu puncak besar di area nilai tinggi (terang) yang mewakili bidang kertas latar
belakang.

Jika kita memaksa histogram dokumen untuk tersebar merata (misalnya dengan
menggunakan Global Histogram Equalization), sistem akan memaksa tekstur mikro
pada kertas dan sedikit bayangan lipatan menjadi sangat kontras. Hasilnya, latar
belakang ijazah yang seharusnya terlihat bersih justru akan dipenuhi oleh
bintik-bintik noise yang sangat tebal, sehingga malah merusak dan mengganggu
tingkat keterbacaan teks utama.