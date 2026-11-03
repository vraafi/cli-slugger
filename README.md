# slugger

Alat CLI Python 3.11 untuk mengganti nama berkas massal menjadi slug aman.

## Instalasi

Tidak perlu dependensi. Cukup Python 3.11+.

```bash
python slugger.py --help
```

## Penggunaan

```bash
python slugger.py [--dry-run] [--pola POLA] path [path ...]
```

- `path`: berkas atau direktori. Direktori diproses non-rekursif (hanya berkas langsung di dalamnya).
- `--dry-run`: tampilkan laporan sebelum/sesudah tanpa mengubah berkas.
- `--pola`: format nama baru. Default `{slug}{ext}`.
  Placeholder: `{slug}`, `{nama_asli}`, `{ext}`.

## Contoh

```bash
# Pratinjau perubahan
python slugger.py --dry-run "File Saya (1).txt"

# Ganti nama dengan slug
python slugger.py "File Saya (1).txt"

# Ganti nama semua berkas di folder dengan format khusus
python slugger.py --pola "{slug}-baru{ext}" folder/
```

## Keluaran

Keluaran dapat diparse baris per baris dengan prefiks:

- `SEBELUM: <path>`
- `SESUDAH: <path>`
- `AKSI: diubah` / `AKSI: dry-run (tidak diubah)`
- `LEWATI: <path>` (nama sudah sama)
- `ERROR: ...`
- `RINGKASAN: ...`

## Exit Code

- `0`: berhasil (termasuk dry-run).
- `1`: kesalahan umum (tidak dipakai saat ini).
- `2`: berkas tidak ada/tidak bisa dibaca, atau tujuan bentrok (menolak menimpa).

## Keamanan

- Menolak menimpa berkas yang sudah ada (exit code 2).
- `--help` tidak memiliki efek samping.
