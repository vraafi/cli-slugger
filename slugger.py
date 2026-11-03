"""
Alat CLI untuk mengganti nama berkas massal menjadi slug yang aman.

Fitur:
- Menghasilkan slug dari nama berkas (huruf kecil, spasi/karakter khusus diganti '-',
  hanya huruf, angka, dan tanda hubung).
- Mode --dry-run untuk pratinjau perubahan tanpa menyentuh berkas.
- Pola penamaan --pola untuk mengatur format nama baru (misal: '{slug}{ext}').
  Placeholder yang didukung: {slug}, {nama_asli}, {ext}.
- Laporan sebelum/sesudah dalam format yang mudah diparse.
- Menolak menimpa berkas yang sudah ada (exit code 2).
- Menangani berkas tidak ada atau tidak bisa dibaca dengan pesan jelas (exit code 2).

Hanya menggunakan pustaka standar Python 3.11.
"""

import argparse
import os
import re
import sys
import unicodedata

__version__ = "1.0.0"

EXIT_OK = 0
EXIT_GAGAL = 1
EXIT_FILE_ERROR = 2

def buat_slug(teks: str) -> str:
    """Mengubah teks menjadi slug aman: huruf kecil, angka, dan tanda hubung."""
    teks = unicodedata.normalize("NFKD", teks)
    teks = teks.encode("ascii", "ignore").decode("ascii")
    teks = teks.lower()
    teks = re.sub(r"[^a-z0-9]+", "-", teks)
    teks = teks.strip("-")
    return teks or "berkas"

def pecah_nama(nama: str) -> tuple[str, str]:
    """Mengembalikan (nama_tanpa_ekstensi, ekstensi_termasuk_titik)."""
    akar, ext = os.path.splitext(nama)
    return akar, ext

def buat_nama_baru(nama_asli: str, pola: str) -> str:
    """Menghasilkan nama berkas baru berdasarkan pola."""
    akar, ext = pecah_nama(nama_asli)
    slug = buat_slug(akar)
    return pola.format(slug=slug, nama_asli=nama_asli, ext=ext)

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ganti nama berkas massal menjadi slug aman.",
        epilog="Contoh: slugger.py --dry-run --pola '{slug}{ext}' folder/",
    )
    parser.add_argument(
        "path",
        nargs="+",
        help="Berkas atau direktori yang akan diproses. Direktori diproses non-rekursif.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Tampilkan rencana perubahan tanpa mengganti nama berkas.",
    )
    parser.add_argument(
        "--pola",
        default="{slug}{ext}",
        help="Pola nama baru (default: '{slug}{ext}'). Placeholder: {slug}, {nama_asli}, {ext}.",
    )
    return parser.parse_args(argv)

def kumpulkan_berkas(paths: list[str]) -> tuple[list[str], list[str]]:
    """Mengumpulkan daftar berkas dari path yang diberikan.

    Mengembalikan (daftar_berkas, daftar_kesalahan).
    """
    berkas = []
    kesalahan = []
    for p in paths:
        if not os.path.exists(p):
            kesalahan.append(f"ERROR: tidak ditemukan: {p}")
            continue
        if os.path.isdir(p):
            try:
                for nama in sorted(os.listdir(p)):
                    full = os.path.join(p, nama)
                    if os.path.isfile(full):
                        berkas.append(full)
            except OSError as e:
                kesalahan.append(f"ERROR: tidak bisa membaca direktori {p}: {e}")
        elif os.path.isfile(p):
            berkas.append(p)
        else:
            kesalahan.append(f"ERROR: bukan berkas biasa: {p}")
    return berkas, kesalahan

def cek_akses_berkas(path: str) -> str | None:
    """Mengembalikan pesan error jika berkas tidak bisa dibaca, else None."""
    if not os.access(path, os.R_OK):
        return f"ERROR: tidak bisa membaca berkas: {path}"
    try:
        with open(path, "rb"):
            pass
    except OSError as e:
        return f"ERROR: gagal membuka berkas {path}: {e}"
    return None

def proses(berkas: list[str], pola: str, dry_run: bool) -> int:
    """Memproses penggantian nama. Mengembalikan exit code."""
    rencana = []
    gagal = False
    for lama in berkas:
        err = cek_akses_berkas(lama)
        if err:
            print(err)
            gagal = True
            continue
        direktori = os.path.dirname(lama) or "."
        nama_lama = os.path.basename(lama)
        nama_baru = buat_nama_baru(nama_lama, pola)
        if nama_baru == nama_lama:
            print(f"LEWATI: {lama}")
            continue
        tujuan = os.path.join(direktori, nama_baru)
        if os.path.exists(tujuan):
            print(f"ERROR: tujuan sudah ada, menolak menimpa: {tujuan}")
            gagal = True
            continue
        rencana.append((lama, tujuan, nama_lama, nama_baru))

    if not rencana:
        print("TIDAK ADA PERUBAHAN")
        return EXIT_FILE_ERROR if gagal else EXIT_OK

    for lama, tujuan, nama_lama, nama_baru in rencana:
        print(f"SEBELUM: {lama}")
        print(f"SESUDAH: {tujuan}")
        if dry_run:
            print("AKSI: dry-run (tidak diubah)")
        else:
            try:
                os.rename(lama, tujuan)
                print("AKSI: diubah")
            except OSError as e:
                print(f"ERROR: gagal mengganti nama {lama}: {e}")
                gagal = True

    if dry_run:
        print("RINGKASAN: mode dry-run, tidak ada berkas diubah")
    else:
        print(f"RINGKASAN: {len(rencana)} berkas diproses")
    return EXIT_FILE_ERROR if gagal else EXIT_OK

def main(argv=None) -> int:
    args = parse_args(argv)
    berkas, kesalahan = kumpulkan_berkas(args.path)
    for pesan in kesalahan:
        print(pesan)
    if not berkas:
        print("TIDAK ADA BERKAS YANG DIPROSES")
        return EXIT_FILE_ERROR
    return proses(berkas, args.pola, args.dry_run)

if __name__ == "__main__":
    sys.exit(main())
