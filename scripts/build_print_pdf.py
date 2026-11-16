#!/usr/bin/env python3
"""Create a simple 6x9 inch image-only print PDF from the book JPEG pages."""
from __future__ import annotations

import argparse
from pathlib import Path

PAGE_WIDTH_PT = 432  # 6 inches at 72 points/inch
PAGE_HEIGHT_PT = 648  # 9 inches at 72 points/inch
IMAGE_WIDTH = 1800
IMAGE_HEIGHT = 2700


def pdf_object(number: int, body: bytes) -> bytes:
    return f"{number} 0 obj\n".encode() + body + b"\nendobj\n"


def stream_object(dictionary: str, data: bytes) -> bytes:
    return dictionary.encode() + f"\nstream\n".encode() + data + b"\nendstream"


def build(pages_dir: Path, output: Path) -> Path:
    pages = sorted(pages_dir.glob("page_*.jpg"))
    if len(pages) != 30:
        raise SystemExit(f"Expected 30 JPEG pages, found {len(pages)}")

    objects: dict[int, bytes] = {}
    # Object 1: catalog; object 2: pages tree.
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R /PageMode /UseOutlines >>"

    kids: list[int] = []
    next_object = 3
    for index, page in enumerate(pages, 1):
        image_obj = next_object
        content_obj = next_object + 1
        page_obj = next_object + 2
        next_object += 3
        kids.append(page_obj)

        image_data = page.read_bytes()
        image_dict = (
            f"<< /Type /XObject /Subtype /Image /Width {IMAGE_WIDTH} "
            f"/Height {IMAGE_HEIGHT} /ColorSpace /DeviceRGB /BitsPerComponent 8 "
            f"/Filter /DCTDecode /Length {len(image_data)} >>"
        )
        objects[image_obj] = stream_object(image_dict, image_data)
        content = f"q\n{PAGE_WIDTH_PT} 0 0 {PAGE_HEIGHT_PT} 0 0 cm\n/Im{index:03d} Do\nQ\n".encode()
        objects[content_obj] = stream_object(f"<< /Length {len(content)} >>", content)
        objects[page_obj] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH_PT} {PAGE_HEIGHT_PT}] "
            f"/Resources << /XObject << /Im{index:03d} {image_obj} 0 R >> >> "
            f"/Contents {content_obj} 0 R >>"
        ).encode()

    kids_ref = " ".join(f"{number} 0 R" for number in kids)
    objects[2] = f"<< /Type /Pages /Count {len(kids)} /Kids [ {kids_ref} ] >>".encode()

    max_object = max(objects)
    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * (max_object + 1)
    for number in range(1, max_object + 1):
        offsets[number] = len(result)
        result.extend(pdf_object(number, objects[number]))
    xref_offset = len(result)
    result.extend(f"xref\n0 {max_object + 1}\n".encode())
    result.extend(b"0000000000 65535 f \n")
    for number in range(1, max_object + 1):
        result.extend(f"{offsets[number]:010d} 00000 n \n".encode())
    result.extend(
        f"trailer\n<< /Size {max_object + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode()
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(result)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=Path, default=Path("pages"))
    parser.add_argument("--output", type=Path, default=Path("output/sapori_del_salento_print.pdf"))
    args = parser.parse_args()
    print(build(args.pages, args.output))


if __name__ == "__main__":
    main()
