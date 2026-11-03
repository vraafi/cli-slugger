#!/usr/bin/env python3
"""Slugger: alat CLI untuk mengganti nama berkas massal menjadi slug aman.

Fitur:
- Mengubah nama berkas menjadi slug aman (huruf kecil, tanpa karakter khusus).
- Mode simulasi dengan --dry-run untuk melihat perubahan tanpa menyentuh berkas.
- Filter berkas dengan --pola (glob).
- Menampilkan laporan sebelum/sesudah.
- Menolak menimpa berkas yang sudah ada.
- Hanya menggunakan pustaka standar Python.

Contoh:
    slugger.py ./data
    slugger.py ./data --dry-run --pola "*.txt"
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


def slugify(nama: str) -> str:
    """Ubah nama berkas menjadi slug aman.

    Contoh: "Halo Dunia!.txt" -> "halo-dunia.txt"
    """
    path = Path(nama)
    stem = path.stem
    suffix = path.suffix.lower()

    teks = unicodedata.normalize("NFKD", stem)
    teks = teks.encode("ascii", "ignore").decode("ascii")
    teks = teks.lower()
    teks = re.sub(r"[^a-z0-9]+", "-", teks)
    teks = teks.strip("-")

    if not teks:
        teks = "berkas"

    return teks + suffix


def kumpulkan_berkas(folder: Path, pola: str) -> list[Path]:
    """Kumpulkan berkas yang cocok dengan pola di folder."""
    hasil = []
    for path in sorted(folder.glob(pola)):
        if path.is_file():
            hasil.append(path)
    return hasil


def buat_rencana(berkas: list[Path]) -> tuple[list[tuple[Path, Path]], list[tuple[Path, str]]]:
    """Buat rencana penggantian nama.

    Kembalikan (rencana, konflik) di mana rencana adalah daftar (lama, baru)
    dan konflik adalah daftar (berkas, alasan) yang tidak bisa diproses.
    """
    rencana: list[tuple[Path, Path]] = []
    konflik: list[tuple[Path, str]] = []
    target_terpakai: set[Path] = set()

    for path in berkas:
        baru = path.with_name(slugify(path.name))

        if baru == path:
            continue

        if baru in target_terpakai or baru.exists():
            konflik.append((path, f"target sudah ada: {baru.name}"))
            continue

        if not path.name.isascii():
            pass

        target_terpakai.add(baru)
        rencana.append((path, baru))

    return rencana, konflik


def jalankan(rencana: list[tuple[Path, Path]], dry_run: bool) -> tuple[int, int]:
    """Jalankan penggantian nama. Kembalikan (sukses, gagal)."""
    sukses = 0
    gagal = 0

    for lama, baru in rencana:
        if dry_run:
            print(f"SIMULASI  {lama.name} -> {baru.name}")
            sukses += 1
            continue
        try:
            lama.rename(baru)
        except OSError as exc:
            print(f"GAGAL     {lama.name}: {exc}", file=sys.stderr)
            gagal += 1
            continue
        print(f"OK        {lama.name} -> {baru.name}")
        sukses += 1

    return sukses, gagal


def buat_parser() -> argparse.ArgumentParser:
    """Bangun parser argparse dengan --help berbahasa Indonesia."""
    parser = argparse.ArgumentParser(
        prog="slugger.py",
        description="Ganti nama berkas massal menjadi slug aman.",
        epilog="Contoh: slugger.py ./data --dry-run --pola '*.txt'",
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder yang berisi berkas (default: direktori saat ini).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Tampilkan rencana perubahan tanpa mengubah berkas.",
    )
    parser.add_argument(
        "--pola",
        default="*",
        help="Pola glob untuk memilih berkas (default: '*').",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Titik masuk utama CLI."""
    parser = buat_parser()
    args = parser.parse_args(argv)

    folder = Path(args.folder)
    if not folder.exists():
        print(f"ERROR: folder tidak ditemukan: {folder}", file=sys.stderr)
        return 2
    if not folder.is_dir():
        print(f"ERROR: bukan folder: {folder}", file=sys.stderr)
        return 2
    try:
        list(folder.iterdir())
    except PermissionError:
        print(f"ERROR: tidak bisa membaca folder: {folder}", file=sys.stderr)
        return 2

    try:
        berkas = kumpulkan_berkas(folder, args.pola)
    except OSError as exc:
        print(f"ERROR: gagal membaca folder: {exc}", file=sys.stderr)
        return 2

    rencana, konflik = buat_rencana(berkas)

    print(f"Folder    : {folder}")
    print(f"Pola      : {args.pola}")
    print(f"Mode      : {'SIMULASI' if args.dry_run else 'TERAPKAN'}")
    print(f"Ditemukan : {len(berkas)} berkas")
    print(f"Rencana   : {len(rencana)} perubahan")
    print(f"Konflik   : {len(konflik)}")

    for path, alasan in konflik:
        print(f"TOLAK     {path.name}: {alasan}")

    if not rencana:
        print("TIDAK ADA perubahan yang perlu dilakukan.")
        return 0

    sukses, gagal = jalankan(rencana, args.dry_run)

    print(f"Selesai   : {sukses} sukses, {gagal} gagal, {len(konflik)} ditolak")
    return 0 if gagal == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
