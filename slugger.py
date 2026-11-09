#!/usr/bin/env python3
"""CLI untuk mengubah nama berkas secara massal menjadi format slug yang aman.

Modul ini menyediakan fungsi CLI untuk mengganti nama berkas menjadi format slug
URL-safe tanpa merusak ekstensi berkas.
"""

import argparse
import glob
import os
import re
import sys
import unicodedata
from pathlib import Path


def slugify(filename: str) -> str:
    """Mengubah nama berkas menjadi format slug aman."""
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix.lower()

    # Normalisasi unicode (hilangkan aksen/diakritik)
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii")
    # Ubah ke huruf kecil
    stem = stem.lower()
    # Ganti karakter non-alfanumerik dengan strip
    stem = re.sub(r"[^\w\s-]", "", stem)
    stem = re.sub(r"[-\s]+", "-", stem).strip("-")

    if not stem:
        stem = "berkas"

    return f"{stem}{suffix}"


def parse_args() -> argparse.Namespace:
    """Membuat dan mengonfigurasi argumen CLI."""
    parser = argparse.ArgumentParser(
        prog="slugger",
        description="Ubah nama berkas secara massal menjadi format slug aman (URL-safe).",
        epilog="Contoh: slugger -p '*.jpg' --dry-run",
    )
    parser.add_argument(
        "berkas",
        nargs="*",
        help="Daftar berkas atau direktori yang akan diproses.",
    )
    parser.add_argument(
        "-p",
        "--pola",
        type=str,
        metavar="POLA",
        help="Pola pencarian berkas (glob pattern), contoh: '*.jpg' atau 'dokumen/*.pdf'.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Simulasi perubahan nama tanpa mengubah berkas secara aktual.",
    )
    return parser.parse_args()


def main() -> None:
    """Fungsi utama eksekusi CLI slugger."""
    args = parse_args()

    target_files: list[str] = []

    if args.pola:
        matched = glob.glob(args.pola, recursive=True)
        target_files.extend(matched)

    if args.berkas:
        for item in args.berkas:
            if os.path.isdir(item):
                target_files.extend([str(p) for p in Path(item).rglob("*") if p.is_file()])
            else:
                target_files.append(item)

    if not target_files:
        print("KESALAHAN: Tidak ada berkas atau pola masukan yang ditentukan.", file=sys.stderr)
        sys.exit(2)

    # Hilangkan duplikat sambil menjaga urutan
    seen = set()
    unique_files: list[str] = []
    for f in target_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    # Verifikasi keberadaan dan hak akses membaca berkas
    for fpath in unique_files:
        path = Path(fpath)
        if not path.exists():
            print(f"KESALAHAN: Berkas '{fpath}' tidak ditemukan.", file=sys.stderr)
            sys.exit(2)
        if not os.access(fpath, os.R_OK):
            print(f"KESALAHAN: Berkas '{fpath}' tidak dapat dibaca.", file=sys.stderr)
            sys.exit(2)

    # Eksekusi penggantian nama
    has_error = False

    for fpath in unique_files:
        path = Path(fpath)
        if not path.is_file():
            continue

        parent = path.parent
        old_name = path.name
        new_name = slugify(old_name)

        if old_name == new_name:
            print(f"TETAP\t{fpath}\t{fpath}")
            continue

        target_path = parent / new_name

        # Tolak menimpa berkas yang sudah ada
        if target_path.exists():
            print(f"LEWATI\t{fpath}\t{target_path}\t(Target sudah ada)", file=sys.stderr)
            continue

        status = "SIMULASI" if args.dry_run else "BERHASIL"

        if not args.dry_run:
            try:
                path.rename(target_path)
            except Exception as e:
                print(f"GAGAL\t{fpath}\t{target_path}\t({e})", file=sys.stderr)
                has_error = True
                continue

        print(f"{status}\t{fpath}\t{target_path}")

    if has_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
