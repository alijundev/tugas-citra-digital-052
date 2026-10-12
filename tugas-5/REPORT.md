## 1. Mengapa median filter dapat memberikan hasil OCR yang lebih baik
pada citra yang mengandung salt-and-pepper noise?
Median filter merupakan jenis filter non-linear yang bekerja dengan cara
mengurutkan nilai intensitas piksel di dalam suatu kernel (jendela
ketetanggaan) dan mengganti nilai piksel pusat dengan nilai median (nilai
tengah) dari urutan tersebut. Salt-and-pepper noise sendiri
berkarakteristik sebagai anomali piksel ekstrem, yaitu piksel yang sangat
terang (putih/salt) atau sangat gelap (hitam/pepper) yang tersebar secara
acak.
Ketika median filter diaplikasikan, nilai-nilai ekstrem (noise) ini akan selalu
berada di ujung susunan urutan (terkecil atau terbesar), sehingga tidak
akan pernah terpilih sebagai nilai median. Hasilnya, noise berhasil
dihilangkan tanpa mengaburkan (blur) tepi atau batas objek secara
signifikan. Mempertahankan ketajaman tepi ini sangat krusial bagi
algoritma ekstraksi fitur pada mesin OCR agar dapat mengenali kontur dan
struktur karakter huruf atau angka dengan presisi yang tinggi. Sebaliknya,
metode seperti mean filter justru akan merata-ratakan nilai ekstrem
tersebut dengan piksel sekitar, yang pada akhirnya menyebarkan noise
dan mengaburkan bentuk asli teks.

## 2. Apakah citra yang paling bagus secara visual selalu menghasilkan
OCR dengan akurasi tertinggi? Jelaskan.
Tidak selalu. Citra yang tampak bagus secara visual bagi mata manusia
tidak secara absolut menjamin akurasi OCR yang tertinggi. Hal ini
dikarenakan sistem visual manusia dan algoritma komputer (seperti OCR)
memiliki mekanisme persepsi yang berbeda.
Manusia cenderung mendefinisikan citra yang "bagus" berdasarkan
tingginya kontras, ketajaman, dan estetika visual secara keseluruhan. Di
sisi lain, mesin OCR bekerja berdasarkan proses binarisasi (thresholding),
pengenalan pola batas tepi (edge detection), dan analisis topologi
karakter. Berdasarkan data pengujian di atas, hal ini terbukti pada
penerapan metode Sharpening. Secara visual, sharpening meningkatkan

ketajaman teks. Namun, sharpening juga cenderung memperkuat noise
frekuensi tinggi di latar belakang (background noise amplifications) dan
dapat memutus topologi karakter.
Akibatnya, pada citra 02_LowContrast, mesin OCR melakukan
misklasifikasi karakter angka "5" menjadi simbol "$" karena ketajaman
berlebih mengubah morfologi tepinya. Lebih fatal lagi, pada citra
04_HighNoise, penguatan noise oleh proses sharpening menyebabkan
algoritma OCR gagal melakukan segmentasi teks, yang berujung pada
hasil pembacaan kosong (akurasi 0%). Oleh karena itu, enhancement yang
ideal untuk OCR adalah yang mampu menghilangkan noise dan
menyeimbangkan intensitas tanpa mendistorsi morfologi karakter,
meskipun hasilnya mungkin terlihat agak halus atau buram bagi mata
manusia.