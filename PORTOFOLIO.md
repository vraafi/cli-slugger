## Masalah
Penggantian nama berkas massal sering menghasilkan nama tidak aman: spasi, karakter non-ASCII, dan huruf besar. Risiko lain: menimpa berkas yang sudah ada. Tim butuh alat yang dapat diprediksi dan aman.

## Yang Dibangun
Slugger, CLI untuk mengubah nama berkas menjadi slug aman. Fitur: --dry-run, --pola, laporan sebelum/sesudah, dan penolakan menimpa berkas. Berkas hasil: README.md (1118 B) dan slugger.py (6431 B).

## Keputusan Teknis
Kode Python dipilih agar mudah diaudit dan dijalankan di lingkungan mana pun. Mode --dry-run memungkinkan pratinjau tanpa perubahan. Pola kustom memberi kendali. Penolakan menimpa mencegah kehilangan data.

## Bukti (angka QC)
QC lapis kode lulus dalam 0,41 detik. Temuan: 0. Berkas kode: 1 Python, 1 JSON, 4 lain. Lapis aktif: kode.

## Batasan
QC hanya mencakup lapis kode. Belum ada uji lapis integrasi atau antarmuka. Alat ini tidak menangani konflik nama secara otomatis; pengguna harus menentukan pola atau menghapus berkas yang bentrok.