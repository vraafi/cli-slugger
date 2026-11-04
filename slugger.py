#!/usr/bin/env python3
"""Alat CLI untuk mengganti nama berkas massal menjadi slug yang aman.

Fitur:
  - Mengubah nama berkas menjadi slug: huruf kecil, pemisah '-',
    hanya karakter [a-z0-9-], tanpa karakter berbahaya.
  - Mode --dry-run untuk melihat rencana tanpa mengubah apa pun.
  - Opsi --pola (glob) untuk memilih berkas yang diproses.
  - Menampilkan laporan sebelum/sesudah dalam format yang bisa diparse.
  - Menolak menimpa berkas yang sudah ada (exit code 3).

Keluaran menggunakan format `KUNCI: nilai` per baris agar mudah diparse.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

EXIT_OK = 0
EXIT_TIDAK_ADA = 2
EXIT_TABRAKAN = 3

_RENTANG_RE = re.compile(r"[^a-z0-9]+")


def buat_slug(teks: str) -> str:
    """Ubah teks menjadi slug aman.

    Langkah: normalisasi Unicode NFKD, buang tanda diakritik,
    lowercase, ganti non-[a-z0-9] dengan '-', rapikan '-', potong tepi.
    """
    dinorm = unicodedata.normalize("NFKD", teks)
    tanpa_diakritik = "".join(c for c in dinorm if not unicodedata.combining(c))
    slug = _RENTANG_RE.sub("-", tanpa_diakritik.lower()).strip("-")
    return slug


def slug_untuk_path(path: Path) -> str:
    """Hasilkan nama berkas ber-slug, mempertahankan ekstensi asli."""
    stem = path.stem
    suffix = path.suffix
    slug_stem = buat_slug(stem)
    if not slug_stem:
        slug_stem = "berkas"
    if suffix:
        slug_ext = buat_slug(suffix.lstrip("."))
        if slug_ext:
            return f"{slug_stem}.{slug_ext}"
    return slug_stem


def kumpulkan_berkas(folder: Path, pola: str) -> list[Path]:
    """Kumpulkan berkas yang cocok dengan pola di folder (non-rekursif)."""
    hasil: list[Path] = []
    for p in sorted(folder.glob(pola)):
        if p.is_file():
            hasil.append(p)
    return hasil


def periksa_dapat_dibaca(berkas: list[Path]) -> list[Path]:
    """Kembalikan daftar berkas yang tidak bisa dibaca."""
    gagal: list[Path] = []
    for p in berkas:
        try:
            with p.open("rb") as f:
                f.read(0)
        except OSError:
            gagal.append(p)
    return gagal


def rencanakan(berkas: list[Path]) -> list[tuple[Path, Path]]:
    """Buat rencana (asal, tujuan) unik; deteksi tabrakan internal."""
    rencana: list[tuple[Path, Path]] = []
    tujuan_terpakai: set[Path] = set()
    for p in berkas:
        nama_baru = slug_untuk_path(p)
        tujuan = p.with_name(nama_baru)
        if tujuan == p:
            continue
        if tujuan in tujuan_terpakai:
            raise FileExistsError(f"tabrakan-internal: {tujuan}")
        tujuan_terpakai.add(tujuan)
        rencana.append((p, tujuan))
    return rencana


def periksa_tabrakan(rencana: list[tuple[Path, Path]]) -> list[Path]:
    """Kembalikan tujuan yang sudah ada di disk atau dipakai ganda."""
    tabrakan: list[Path] = []
    for asal, tujuan in rencana:
        if tujuan.exists() and tujuan != asal:
            tabrakan.append(tujuan)
    return tabrakan


def tulis_laporan(rencana: list[tuple[Path, Path]], dry_run: bool) -> None:
    """Cetak laporan sebelum/sesudah yang bisa diparse."""
    print(f"MODE: {'dry-run' if dry_run else 'terapkan'}")
    print(f"JUMLAH_DIPROSES: {len(rencana)}")
    for asal, tujuan in rencana:
        print(f"SEBELUM: {asal.name}")
        print(f"SESUDAH: {tujuan.name}")
        print("STATUS: " + ("rencana" if dry_run else "diterapkan"))


def jalankan(args: argparse.Namespace) -> int:
    """Jalankan alur utama; kembalikan exit code."""
    folder = Path(args.folder)
    if not folder.exists():
        print(f"ERROR: folder-tidak-ada: {folder}", file=sys.stderr)
        return EXIT_TIDAK_ADA
    if not folder.is_dir():
        print(f"ERROR: bukan-folder: {folder}", file=sys.stderr)
        return EXIT_TIDAK_ADA

    berkas = kumpulkan_berkas(folder, args.pola)
    if not berkas:
        print(f"INFO: tidak-ada-berkas-cocok: {args.pola}")
        return EXIT_OK

    gagal = periksa_dapat_dibaca(berkas)
    if gagal:
        for p in gagal:
            print(f"ERROR: tidak-dapat-dibaca: {p}", file=sys.stderr)
        return EXIT_TIDAK_ADA

    try:
        rencana = rencanakan(berkas)
    except FileExistsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_TABRAKAN

    tabrakan = periksa_tabrakan(rencana)
    if tabrakan:
        for p in tabrakan:
            print(f"ERROR: akan-menimpa: {p}", file=sys.stderr)
        return EXIT_TABRAKAN

    if args.dry_run:
        tulis_laporan(rencana, dry_run=True)
        return EXIT_OK

    gagal_ganti: list[Path] = []
    for asal, tujuan in rencana:
        try:
            os.rename(asal, tujuan)
        except OSError:
            gagal_ganti.append(asal)
    if gagal_ganti:
        for p in gagal_ganti:
            print(f"ERROR: gagal-ganti-nama: {p}", file=sys.stderr)
        return EXIT_TIDAK_ADA

    tulis_laporan(rencana, dry_run=False)
    return EXIT_OK


def bangun_parser() -> argparse.ArgumentParser:
    """Bangun parser argparse dengan bantuan berbahasa Indonesia."""
    parser = argparse.ArgumentParser(
        prog="slugger",
        description="Ganti nama berkas massal menjadi slug aman.",
        epilog=(
            "Contoh: slugger --dry-run --pola '*.txt' ./data "
            "(lihat rencana tanpa mengubah berkas). "
            "Exit code: 0 sukses, 2 berkas/folder tidak ada atau tidak terbaca, "
            "3 tabrakan nama."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "folder",
        help="Folder tempat berkas akan diganti nama (non-rekursif).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Tampilkan laporan sebelum/sesudah tanpa mengubah berkas.",
    )
    parser.add_argument(
        "--pola",
        default="*",
        help="Pola glob untuk memilih berkas (default: *).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Titik masuk program."""
    parser = bangun_parser()
    args = parser.parse_args(argv)
    return jalankan(args)


if __name__ == "__main__":
    raise SystemExit(main())
