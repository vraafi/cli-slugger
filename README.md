# Slugger

Alat CLI Python 3.11 untuk mengubah nama berkas secara massal menjadi format *slug* yang aman (URL-safe).

## Fitur Utama

- **Tanpa Dependensi Eksternal**: Hanya menggunakan pustaka standar Python 3.11.
- **Simulasi Mode (`--dry-run`)**: Menampilkan laporan perubahan tanpa mengubah berkas asli.
- **Pencarian Pola (`--pola`)**: Mendukung pencarian berkas menggunakan pola glob.
- **Pencegahan Menimpa Berkas**: Menolak mengubah nama jika berkas tujuan sudah ada.
- **Format Laporan Ringkas**: Output berupa baris yang mudah diparse (TSV: Status, Asal, Tujuan).
- **Penanganan Kesalahan Jelas**: Mengembalikan *exit code* `2` untuk berkas tidak ada / tidak dapat dibaca.

## Penggunaan

### Mengubah Berkas Langsung
```bash
python3 slugger.py "Laporan Akhir (2023).pdf" "Foto Liburan 1.JPG"
```

### Menggunakan Pola Pencarian (Glob)
```bash
python3 slugger.py --pola "dokumen/*.txt"
```

### Mode Simulasi (Dry Run)
```bash
python3 slugger.py --pola "*.png" --dry-run
```

### Menampilkan Bantuan
```bash
python3 slugger.py --help
```

## Format Keluaran

Keluaran menggunakan format terpisah tab (TSV):

```
BERHASIL	dokumen/Laporan Akhir.txt	dokumen/laporan-akhir.txt
TETAP	dokumen/laporan-baru.txt	dokumen/laporan-baru.txt
SIMULASI	dokumen/Foto (1).jpg	dokumen/foto-1.jpg
```

## Kode Keluar (Exit Codes)

- `0`: Berhasil dieksekusi tanpa kendala.
- `1`: Terjadi kesalahan saat mengubah nama berkas.
- `2`: Berkas tidak ditemukan, tidak dapat dibaca, atau argumen tidak valid.
