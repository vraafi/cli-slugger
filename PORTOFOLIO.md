## Masalah

Mengganti nama berkas massal secara manual rawan salah dan bisa menimpa berkas yang sudah ada. Tim butuh alat yang aman, dapat diuji tanpa risiko, dan memberi laporan jelas.

## Yang Dibangun

slugger, CLI untuk mengganti nama berkas menjadi slug aman. Fitur inti: `--dry-run` untuk pratinjau, `--pola` untuk aturan penggantian, laporan sebelum/sesudah, dan penolakan menimpa berkas yang sudah ada. Kode ditulis dalam satu berkas Python `slugger.py` (5264 B) dengan dokumentasi `README.md` (1338 B).

## Keputusan Teknis

Kami pisahkan pratinjau dari eksekusi. `--dry-run` menghasilkan laporan sebelum/sesudah tanpa menyentuh berkas. Penolakan menimpa berkas menjadi pengaman bawaan, bukan opsi. Pola penggantian dibuat eksplisit lewat `--pola` agar perilaku dapat diprediksi dan diuji.

## Bukti

QC lapis kode aktif dan lulus. Total temuan: 0. Waktu QC: 1,09 detik. Berkas kode: 1 Python, 0 JavaScript, 0 JSON, 0 Lua, 1 lain.

## Batasan

QC baru mencakup lapis kode. Lapis lain belum aktif. Alat ini berfokus pada penggantian nama berkas, bukan validasi isi berkas.