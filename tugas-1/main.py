import numpy as np
def main():
    print("--- PROGRAM PERKALIAN MATRIKS 3D ---")

    # Input dimensi dari user
    batch = int(input("Masukkan jumlah batch (depth): "))
    baris = int(input("Masukkan jumlah baris: "))
    kolom_a = int(input("Masukkan jumlah kolom Matriks A: "))
    kolom_b = int(input("Masukkan jumlah kolom Matriks B: "))

    # Mengisi matriks dengan angka acak (1-9)
    matriks_a = np.random.randint(1, 10, size=(batch, baris, kolom_a))
    matriks_b = np.random.randint(1, 10, size=(batch, kolom_a, kolom_b))

    print("\n--- Matriks A ---")
    print(matriks_a)

    print("\n--- Matriks B ---")
    print(matriks_b)

    # Perkalian matriks 3D menggunakan operator @ (matmul)
    hasil = matriks_a @ matriks_b

    print("\n--- Hasil Perkalian Matriks 3D ---")
    print(hasil)
    print(f"Bentuk (Shape) Hasil: {hasil.shape}")


if __name__ == "__main__":
    main()