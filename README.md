# Slugger

Alat CLI Python 3.11 untuk mengganti nama berkas massal menjadi slug aman.
Hanya memakai pustaka standar, tanpa dependensi.

## Pemakaian

```
python slugger.py [folder] [--dry-run] [--pola GLOB]
```

- `folder` — folder berisi berkas (default: direktori saat ini).
- `--dry-run` — simulasi, tidak mengubah berkas.
- `--pola` — pola glob pemilihan berkas (default: `*`).

Contoh:

```
python slugger.py ./data --dry-run --pola "*.txt"
python slugger.py ./data --pola "*.jpg"
```

## Perilaku

- Nama diubah menjadi huruf kecil, karakter non-alfanumerik diganti tanda hubung.
- Ekstensi dipertahankan (huruf kecil).
- Berkas yang targetnya sudah ada akan ditolak (tidak menimpa).
- Konflik dan status dicetak ke keluaran standar dalam format ringkas yang mudah diparse.
- Galat folder/berkas tidak ada atau tidak bisa dibaca menghasilkan exit code 2
  dengan pesan jelas di stderr.

## Kode keluar

- `0` — sukses (termasuk simulasi).
- `1` — ada kegagalan saat mengganti nama.
- `2` — galat input (folder tidak ada / tidak bisa dibaca).

## Contoh keluaran

```
Folder    : data
Pola      : *.txt
Mode      : TERAPKAN
Ditemukan : 2 berkas
Rencana   : 1 perubahan
Konflik   : 0
OK        Halo Dunia!.txt -> halo-dunia.txt
Selesai   : 1 sukses, 0 gagal, 0 ditolak
```
