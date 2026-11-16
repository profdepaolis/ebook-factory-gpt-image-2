#!/usr/bin/env python3
"""Brand the 24-page family guide without placing the logo over visible text."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=Path, default=Path("salento-per-famiglie/pages"))
    parser.add_argument("--logo", type=Path, default=Path("assets_benvenutiinsalento_logo.png"))
    args = parser.parse_args()

    pages = sorted(args.pages.glob("page_*.jpg"))
    if len(pages) != 24:
        raise SystemExit(f"Expected 24 pages, found {len(pages)}")
    work = args.pages / ".branding_work"
    work.mkdir(exist_ok=True)
    circle = work / "logo_circle.png"
    small = work / "logo_160.png"
    footer = work / "copyright_footer.png"

    run(
        "convert", str(args.logo), "-alpha", "on",
        "(", "-size", "512x512", "xc:none", "-fill", "white",
        "-draw", "circle 256,256 256,18", ")",
        "-compose", "CopyOpacity", "-composite", "-strip", str(circle),
    )
    run("convert", str(circle), "-resize", "160x160!", "-strip", str(small))
    run(
        "convert", "-size", "1420x150", "xc:#fffdf6",
        "-fill", "#c89e4b", "-stroke", "#c89e4b", "-strokewidth", "3",
        "-draw", "roundrectangle 2,2 1418,148 16,16",
        "-fill", "#15283f", "-stroke", "none", "-font", "DejaVu-Sans",
        "-gravity", "center", "-pointsize", "24", "-annotate", "+0-25",
        "Opera editoriale esclusiva per Benvenuti in Salento",
        "-pointsize", "18", "-annotate", "+0+25",
        "© 2026 Benvenuti in Salento · benvenutiinsalento.it · Riproduzione vietata",
        "-strip", str(footer),
    )

    # Prototypes on pages 1, 2 and 5 already contain the approved logo.
    for number, page in enumerate(pages, 1):
        if number in (1, 2, 5):
            continue
        tmp = work / page.name
        geometry = "+70+2470" if number == 24 else "+70+70"
        command = ["convert", str(page), str(small), "-geometry", geometry, "-composite"]
        if number == 24:
            command.extend([str(footer), "-geometry", "+320+2390", "-composite"])
        command.extend(["-strip", "-quality", "88", str(tmp)])
        run(*command)
        tmp.replace(page)

    for scratch in (circle, small, footer):
        scratch.unlink(missing_ok=True)
    work.rmdir()
    print("Applied transparent circular logo and copyright footer to the family guide.")


if __name__ == "__main__":
    main()
