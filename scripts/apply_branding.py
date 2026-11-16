#!/usr/bin/env python3
"""Apply the supplied Benvenuti in Salento logo and copyright footer to every page."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=Path, default=Path("pages"))
    parser.add_argument("--logo", type=Path, default=Path("assets_benvenutiinsalento_logo.png"))
    parser.add_argument("--brand-name", default="Benvenuti in Salento")
    parser.add_argument("--website", default="benvenutiinsalento.it")
    args = parser.parse_args()

    pages = sorted(args.pages.glob("page_*.jpg"))
    if len(pages) != 30:
        raise SystemExit(f"Expected 30 pages, found {len(pages)}")
    if not args.logo.exists():
        raise SystemExit(f"Logo not found: {args.logo}")

    work = args.pages / ".branding_work"
    work.mkdir(exist_ok=True)
    logo_circle = work / "logo_circle.png"
    logo_small = work / "logo_160.png"
    credits = work / "copyright_footer.png"
    # Keep the artwork inside the supplied circular border and make the outside transparent.
    run(
        "convert", str(args.logo), "-alpha", "on",
        "(", "-size", "512x512", "xc:none", "-fill", "white",
        "-draw", "circle 256,256 256,18", ")",
        "-compose", "CopyOpacity", "-composite", "-strip", str(logo_circle),
    )
    run("convert", str(logo_circle), "-resize", "160x160!", "-strip", str(logo_small))

    line_one = f"Opera editoriale esclusiva per {args.brand_name}"
    line_two = f"© 2026 {args.brand_name} · {args.website} · Riproduzione vietata"
    # A cream, bordered footer keeps the credit readable over the photographic page.
    run(
        "convert", "-size", "1420x150", "xc:#fffdf6",
        "-fill", "#c89e4b", "-stroke", "#c89e4b", "-strokewidth", "3",
        "-draw", "roundrectangle 2,2 1418,148 16,16",
        "-fill", "#15283f", "-stroke", "none", "-font", "DejaVu-Sans",
        "-gravity", "center", "-pointsize", "24", "-annotate", "+0-25", line_one,
        "-pointsize", "18", "-annotate", "+0+25", line_two,
        "-strip", str(credits),
    )

    for number, page in enumerate(pages, 1):
        tmp = work / page.name
        # Pages with recipe/content panels get the logo in the photographic header;
        # cover and final page keep it in the bottom margin. This avoids text entirely.
        logo_geometry = "+70+2470" if number in (1, 30) else "+70+70"
        command = [
            "convert", str(page), str(logo_small), "-geometry", logo_geometry, "-composite",
        ]
        if number == 30:
            command.extend([str(credits), "-geometry", "+320+2390", "-composite"])
        command.extend(["-strip", "-quality", "88", str(tmp)])
        run(*command)
        tmp.replace(page)

    # Keep the source logo and brand metadata in the repository; do not retain scratch files.
    for scratch in (logo_circle, logo_small, credits):
        scratch.unlink(missing_ok=True)
    work.rmdir()
    print(f"Applied {args.brand_name} logo to {len(pages)} pages; copyright footer added to page 30.")


if __name__ == "__main__":
    main()
