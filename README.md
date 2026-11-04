# slugger

Alat CLI Python 3.11 untuk mengganti nama berkas massal menjadi slug yang aman.
Hanya menggunakan pustaka standar, tanpa dependensi.

## Fitur

- Mengubah nama berkas menjadi slug: huruf kecil, pemisah `-`, hanya `[a-z0-9-]`.
- `--dry-run` untuk melihat rencana tanpa mengubah berkas.
- `--pola` untuk memilih berkas dengan glob (default `*`).
- Laporan `SEBELUM` / `SESUDAH` yang bisa diparse.
- Menolak menimpa berkas yang sudah ada (exit code 3).

## Pemakaian

```sh
python slugger.py --help
python slugger.py --dry-run --pola '*.txt' ./data
python slugger.py --pola '*.jpg' ./gambar
```

## Keluaran

Baris `KUNCI: nilai`, misalnya:

```
MODE: dry-run
JUMLAH_DIPROSES: 2
SEBELUM: Laporan Tahunan!.pdf
SESUDAH: laporan-tahunan.pdf
STATUS: rencana
```

## Exit code

- `0` sukses (termasuk dry-run).
- `2` folder/berkas tidak ada atau tidak dapat dibaca.
- `3` tabrakan nama atau akan menimpa berkas.

## Catatan

Operasi hanya pada satu folder (non-rekursif). Nama yang sudah cocok slug
tidak diubah. Jika dua berkas menghasilkan slug sama, proses dibatalkan.
