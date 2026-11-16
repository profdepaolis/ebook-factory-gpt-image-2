#!/usr/bin/env python3
"""Build a fixed-layout EPUB from the generated full-page JPEGs."""
from __future__ import annotations

import argparse
import html
import json
import shutil
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

EPUB_NS = "http://www.idpf.org/2007/opf"
DC_NS = "http://purl.org/dc/elements/1.1/"
CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=Path, default=Path("pages"))
    parser.add_argument("--config", type=Path, default=Path("config/project_config.json"))
    parser.add_argument("--output", type=Path, default=Path("output/sapori_del_salento.epub"))
    return parser.parse_args()


def page_files(pages_dir: Path, expected_count: int | None = None) -> list[Path]:
    files = sorted(pages_dir.glob("page_*.jpg"))
    if expected_count is not None and len(files) != expected_count:
        raise SystemExit(f"Expected {expected_count} page JPEGs in {pages_dir}, found {len(files)}")
    for number, path in enumerate(files, 1):
        expected = f"page_{number:03d}_"
        if not path.name.startswith(expected):
            raise SystemExit(f"Page order/name mismatch: expected prefix {expected}, got {path.name}")
    return files


def xhtml_page(number: int, image_name: str, title: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
  <head>
    <title>{html.escape(title)}</title>
    <meta name="viewport" content="width=1800, height=2700" />
    <link rel="stylesheet" type="text/css" href="../css/book.css" />
  </head>
  <body>
    <img src="../images/{html.escape(image_name)}" alt="Pagina {number}: {html.escape(title)}" />
  </body>
</html>
'''


def build(args: argparse.Namespace) -> Path:
    config = json.loads(args.config.read_text(encoding="utf-8"))
    expected_count = config.get("total_pages")
    pages = page_files(args.pages, int(expected_count) if expected_count else None)
    output = args.output
    work = output.parent / "epub_build"
    if work.exists():
        shutil.rmtree(work)
    (work / "META-INF").mkdir(parents=True)
    (work / "OEBPS/images").mkdir(parents=True)
    (work / "OEBPS/pages").mkdir(parents=True)
    (work / "OEBPS/css").mkdir(parents=True)

    (work / "mimetype").write_text("application/epub+zip", encoding="ascii")
    (work / "META-INF/container.xml").write_text(
        '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
''', encoding="utf-8")
    (work / "OEBPS/css/book.css").write_text(
        """@page { margin: 0; size: 6in 9in; }
html, body { margin: 0; padding: 0; width: 1800px; height: 2700px; background: #fff; }
body { overflow: hidden; }
img { display: block; width: 1800px; height: 2700px; object-fit: fill; margin: 0; padding: 0; }
""", encoding="utf-8")

    titles = {item["page"]: item["title"] for item in config["page_plan"]}
    manifest_items = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
        '<item id="css" href="css/book.css" media-type="text/css" />',
    ]
    spine_items = []
    nav_items = []
    for number, image in enumerate(pages, 1):
        image_name = image.name
        image_target = work / "OEBPS/images" / image_name
        shutil.copy2(image, image_target)
        title = titles.get(number, f"Pagina {number}")
        page_name = f"page_{number:03d}.xhtml"
        (work / "OEBPS/pages" / page_name).write_text(
            xhtml_page(number, image_name, title), encoding="utf-8"
        )
        properties = ' properties="cover-image"' if number == 1 else ""
        manifest_items.append(
            f'<item id="image{number:03d}" href="images/{image_name}" media-type="image/jpeg"{properties} />'
        )
        manifest_items.append(
            f'<item id="page{number:03d}" href="pages/{page_name}" media-type="application/xhtml+xml" />'
        )
        spine_items.append(f'<itemref idref="page{number:03d}" />')
        nav_items.append(f'<li><a href="pages/{page_name}">{number}. {html.escape(title)}</a></li>')

    modified = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    identifier = f"urn:uuid:{uuid.uuid4()}"
    title = html.escape(config["title"])
    subtitle = html.escape(config.get("subtitle", ""))
    language = html.escape(config.get("language", "it"))
    rights = html.escape(config.get("rights", ""))
    rights_element = f"    <dc:rights>{rights}</dc:rights>\n" if rights else ""
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{identifier}</dc:identifier>
    <dc:title>{title}</dc:title>
    <dc:language>{language}</dc:language>
    <dc:description>{subtitle}</dc:description>
{rights_element}    <meta property="dcterms:modified">{modified}</meta>
    <meta property="rendition:layout">pre-paginated</meta>
    <meta property="rendition:orientation">portrait</meta>
    <meta property="rendition:spread">none</meta>
  </metadata>
  <manifest>
    {' '.join(manifest_items)}
  </manifest>
  <spine page-progression-direction="ltr">
    {' '.join(spine_items)}
  </spine>
</package>
'''
    (work / "OEBPS/content.opf").write_text(opf, encoding="utf-8")
    nav = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="it">
  <head><title>{title}</title></head>
  <body>
    <nav epub:type="toc" id="toc"><h1>{title}</h1><ol>{''.join(nav_items)}</ol></nav>
  </body>
</html>
'''
    (work / "OEBPS/nav.xhtml").write_text(nav, encoding="utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w") as archive:
        archive.write(work / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(work.rglob("*")):
            if path.is_file() and path.name != "mimetype":
                archive.write(path, path.relative_to(work).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
    return output


if __name__ == "__main__":
    result = build(parse_args())
    print(result)
