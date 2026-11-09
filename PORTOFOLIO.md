### Masalah
Nama berkas yang tidak standar mengganggu otomatisasi alur kerja dan berisiko menimpa data penting.

### Yang Dibangun
Kami membangun `slugger`, sebuah CLI untuk mengganti nama berkas massal menjadi slug yang aman secara cepat dan terprediksi.

### Keputusan Teknis
Kami mengimplementasikan opsi `--dry-run` untuk simulasi tanpa risiko dan `--pola` untuk penyesuaian format nama. Sistem menghasilkan laporan transparan sebelum dan sesudah eksekusi, serta menolak keras operasi yang menimpa berkas yang ada. Kode utama tersimpan dalam `slugger.py` (4183 B) dan didokumentasikan pada `README.md` (1543 B).

### Bukti
Pemeriksaan kualitas pada 1 lapis aktif (kode) selesai dalam 1,48 detik dengan 0 temuan dari total 6 berkas yang diperiksa (1 Python, 1 JSON, dan 4 berkas pendukung).

### Batasan
Perangkat ini beroperasi secara lokal melalui antarmuka baris perintah tanpa integrasi penyimpan awan bawaan.