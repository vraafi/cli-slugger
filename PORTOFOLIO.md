## Masalah
Mengganti nama berkas massal secara manual rawan salah dan berisiko menimpa berkas yang sudah ada. Tim butuh alat kecil yang aman, dapat diperiksa dulu, dan tidak menghapus data tanpa persetujuan.

## Yang Dibangun
`slugger` adalah CLI Python yang mengubah nama berkas menjadi slug aman. Fitur inti: `--dry-run`, `--pola` untuk aturan penggantian, laporan sebelum/sesudah, dan penolakan menimpa berkas. Repositori berisi `README.md` 1394 B dan `slugger.py` 5665 B.

## Keputusan Teknis
Semua logika ditempatkan di satu berkas Python (`slugger.py`) agar mudah diaudit dan dipasang. Mode `--dry-run` menjadi jalur default pemeriksaan: pengguna melihat rencana perubahan sebelum eksekusi. Penolakan menimpa berkas dijalankan sebelum penulisan, bukan setelah. Pola kustom dipisahkan dari logika slug dasar.

## Bukti
QC lapis kode aktif dan lulus. Waktu QC 0,58 detik dengan 0 temuan. Komposisi kode: 1 berkas Python, 1 berkas lain; tanpa JS, JSON, atau Lua.

## Batasan
QC baru mencakup lapis kode, belum lapis integrasi atau uji beban. Alat ini menangani berkas lokal, bukan sistem terdistribusi. Kami belum menguji di direktori besar atau nama berkas non-ASCII ekstrem.