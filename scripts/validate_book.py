#!/usr/bin/env python3
"""Validate the image-based Salento cookbook outputs."""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

EXPECTED = (1800, 2700)


def jpeg_size(data: bytes) -> tuple[int, int]:
    index = 2
    sof_markers = set(range(0xC0, 0xC4)) | set(range(0xC5, 0xC8)) | set(range(0xC9, 0xCC)) | set(range(0xCD, 0xD0))
    while index < len(data) - 9:
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in (0xD8, 0xD9):
            continue
        length = int.from_bytes(data[index:index + 2], "big")
        if marker in sof_markers:
            height = int.from_bytes(data[index + 3:index + 5], "big")
            width = int.from_bytes(data[index + 5:index + 7], "big")
            return width, height
        index += length
    raise ValueError("JPEG dimensions not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=Path, default=Path("pages"))
    parser.add_argument("--epub", type=Path, default=Path("output/sapori_del_salento.epub"))
    parser.add_argument("--pdf", type=Path, default=Path("output/sapori_del_salento_print.pdf"))
    args = parser.parse_args()

    pages = sorted(args.pages.glob("page_*.jpg"))
    assert len(pages) == 30, f"Expected 30 pages, found {len(pages)}"
    for number, page in enumerate(pages, 1):
        assert page.name.startswith(f"page_{number:03d}_"), f"Wrong page order: {page.name}"
        assert jpeg_size(page.read_bytes()) == EXPECTED, f"Wrong dimensions: {page}"
        assert page.stat().st_size > 20_000, f"Suspiciously small/blank page: {page}"

    with zipfile.ZipFile(args.epub) as epub:
        assert epub.testzip() is None, "EPUB contains a corrupt member"
        assert epub.read("mimetype") == b"application/epub+zip"
        assert len([n for n in epub.namelist() if n.startswith("OEBPS/images/")]) == 30
        assert len([n for n in epub.namelist() if n.startswith("OEBPS/pages/")]) == 30
        opf = epub.read("OEBPS/content.opf")
        assert b"pre-paginated" in opf

    pdf_data = args.pdf.read_bytes()
    assert pdf_data.startswith(b"%PDF-"), "PDF header missing"
    assert pdf_data.count(b"/Type /Page /Parent") == 30, "PDF page count mismatch"
    print("PASS: 30 JPEG pages, fixed-layout EPUB, and 30-page PDF validated")


if __name__ == "__main__":
    main()
