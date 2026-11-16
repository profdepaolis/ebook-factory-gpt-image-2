#!/usr/bin/env python3
"""Build reflowable KDP EPUB for Vol.1 — La valigia d'Italia."""
import re, sys, uuid
from pathlib import Path

import markdown
from ebooklib import epub

ROOT = Path(__file__).resolve().parent.parent / "saga-destinazione-italia" / "volume-1-mare-500-autostrada"
MD = ROOT / "MANOSCRITTO.md"
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "La_valigia_d_Italia_Vol1_Mare_500_e_autostrada.epub"

raw = MD.read_text(encoding="utf-8")

# --- split document -------------------------------------------------------
m_app = re.search(r"\n# Apparati\b", raw)
body, apparati = (raw[: m_app.start()], raw[m_app.start():]) if m_app else (raw, "")

# drop the top title block (everything before the first "## Capitolo")
m_first = re.search(r"\n## ", body)
body = body[m_first.start():] if m_first else body

chapter_blocks = re.split(r"\n(?=## )", body.strip())
chapters = []
for block in chapter_blocks:
    lines = block.strip().splitlines()
    title = lines[0].lstrip("# ").strip()
    text = "\n".join(lines[1:]).strip()
    chapters.append((title, text))

# image placement: map chapter number -> asset file (only images we have so far)
ILLUS = {
    1: "illus_02_breda.jpg",
    2: "illus_03_valigia.jpg",
    3: "illus_04_partenza.jpg",
    4: "illus_05_casello.jpg",
    5: "illus_06_autogrill.jpg",
}

md = markdown.Markdown(extensions=["tables", "smarty"])

book = epub.EpubBook()
book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
book.set_title("La valigia d'Italia — Vol. 1: Mare, 500 e autostrada")
book.set_language("it")
book.add_author("Il progetto La valigia d'Italia")
book.add_metadata("DC", "publisher", "La valigia d'Italia — collana di saga storica per ragazzi")
book.add_metadata("DC", "description", "Estate 1964. Marco Morelli, 10 anni, parte con la famiglia da Milano per Rimini in Fiat 500, sull'Autostrada del Sole appena completata. La prima estate di massa degli italiani, raccontata da un bambino. Primo volume della saga: la storia del turismo italiano dal Boom economico a oggi.")
book.add_metadata("DC", "subject", "ragazzi; storia; turismo; autostrada; Italia; 1964")

# --- CSS ------------------------------------------------------------------
css = """
@namespace epub "http://www.idpf.org/2007/ops";
body { font-family: Georgia, 'Times New Roman', serif; font-size: 1.05em; line-height: 1.5; margin: 5% 6%; color: #2b2118; }
h1 { font-size: 1.6em; color: #8a2b1d; border-bottom: 3px solid #d4a017; padding-bottom: .25em; page-break-before: always; }
h1.unnumbered { page-break-before: auto; }
h2 { font-size: 1.15em; color: #8a2b1d; }
table { border-collapse: collapse; width: 100%; font-size: .85em; margin: 1em 0; }
th, td { border: 1px solid #c9b48a; padding: .35em .5em; text-align: left; }
th { background: #f3e9d2; }
img { max-width: 100%; height: auto; }
.illustration { text-align: center; margin: 1em 0; page-break-inside: avoid; }
.illustration img { width: 100%; border-radius: 6px; }
.caption { font-size: .8em; color: #6b5b45; text-align: center; margin-top: .3em; font-style: italic; }
.frontmatter { text-align: center; }
.frontmatter .kicker { letter-spacing: .18em; text-transform: uppercase; color: #8a2b1d; font-size: .8em; }
.frontmatter .title { font-size: 2em; color: #8a2b1d; margin: .2em 0; }
.frontmatter .subtitle { font-size: 1.1em; color: #3b2d1f; }
.frontmatter .series { font-size: .9em; color: #6b5b45; margin-top: 2em; }
.colophon { font-size: .85em; color: #4a3f31; }
"""
book.add_item(epub.EpubItem(uid="css-main", file_name="style/main.css", media_type="text/css", content=css.encode()))

# --- register images -------------------------------------------------------
img_items = {}
for p in sorted(ASSETS.glob("illus_*.jpg")):
    if p.name == "illus_01_cover.jpg":
        continue  # gestita da set_cover()
    data = p.read_bytes()
    item = epub.EpubItem(uid=p.stem, file_name=f"images/{p.name}", media_type="image/jpeg", content=data)
    book.add_item(item)
    img_items[p.name] = item

def chapter_doc(idx, title, html_body, illus_name=None):
    illus_html = ""
    if illus_name and illus_name in img_items:
        illus_html = f'<div class="illustration"><img src="images/{illus_name}" alt="Illustrazione per {title}"/></div>'
    html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
<head><title>{title}</title>
<link rel="stylesheet" type="text/css" href="style/main.css"/></head>
<body>
<h1 class="unnumbered">{title}</h1>
{illus_html}
{html_body}
</body></html>"""
    ch = epub.EpubHtml(title=title, file_name=f"chap_{idx:02d}.xhtml", lang="it")
    ch.content = html.encode("utf-8")
    return ch

# --- cover (set_cover crea immagine cover + pagina cover EPUB3) ------------
book.set_cover("images/cover.jpg", (ASSETS / "illus_01_cover.jpg").read_bytes())

# --- front matter ----------------------------------------------------------
title_html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
<head><title>La valigia d'Italia — Vol. 1</title>
<link rel="stylesheet" type="text/css" href="style/main.css"/></head>
<body class="frontmatter">
<p class="kicker">La valigia d'Italia</p>
<p class="title">Mare, 500<br/>e autostrada</p>
<p class="subtitle">La storia del turismo italiano raccontata<br/>dalla famiglia Morelli (vol. 1)</p>
<p class="series">Estate 1964 · Marco, 10 anni · Milano → Rimini</p>
</body></html>"""
title_pg = epub.EpubHtml(title="Frontespizio", file_name="frontespizio.xhtml", lang="it")
title_pg.content = title_html.encode("utf-8")

colophon_html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
<head><title>Colophon e note</title>
<link rel="stylesheet" type="text/css" href="style/main.css"/></head>
<body class="colophon">
<h1 class="unnumbered">Un progetto, una valigia, quattro estati</h1>
<p><strong>La valigia d'Italia</strong> è la saga che racconta come l'Italia è diventata il Paese dei vacanze: dal Boom economico a oggi. Si legge in ordine, o si comincia da qualsiasi volume.</p>
<p><strong>Fonti e dati</strong>: i fatti storici di questo volume sono veri; i personaggi sono inventati. Dati e date fanno riferimento a fonti pubbliche (Università di Torino, Istat, MiC, Censis, archivio RAI); il dossier completo è in <em>PROGETTO_SAGA.md</em>, §9.</p>
<p><strong>Illustrazioni</strong>: generate con AI (GPT Image 2), stile gouache e acquerello. Nessuna fotografia di repertorio è stata usata in questa edizione.</p>
<p><strong>Per la scuola</strong>: ogni volume contiene «Lo sai che…?», «Parole d'epoca», «Linea del tempo» e la scheda «La storia vera dietro la storia» per genitori e insegnanti.</p>
<p>© Il progetto La valigia d'Italia. Tutti i diritti riservati.</p>
</body></html>"""
colophon = epub.EpubHtml(title="Colophon e note", file_name="colophon.xhtml", lang="it")
colophon.content = colophon_html.encode("utf-8")

# --- chapters --------------------------------------------------------------
spine_items, toc_items = [title_pg, colophon], []
for i, (title, text) in enumerate(chapters, start=1):
    chap_num = i
    html_body = md.convert(text)
    doc = chapter_doc(chap_num, title, html_body, ILLUS.get(chap_num))
    book.add_item(doc)
    spine_items.append(doc)
    toc_items.append(epub.Link(doc.file_name, title, f"ch{chap_num}"))

# --- apparati ---------------------------------------------------------------
if apparati.strip():
    md = markdown.Markdown(extensions=["tables", "smarty"])
    app_html = md.convert(apparati.lstrip("\n"))
    doc = epub.EpubHtml(title="Apparati — Lo sai che?", file_name="apparati.xhtml", lang="it")
    doc.content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
<head><title>Apparati</title><link rel="stylesheet" type="text/css" href="style/main.css"/></head>
<body>{app_html}</body></html>""".encode("utf-8")
    book.add_item(doc)
    spine_items.append(doc)
    toc_items.append(epub.Link(doc.file_name, "Apparati — «Lo sai che…?»", "apparati"))

# --- nav, spine, write ------------------------------------------------------
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.toc = toc_items
book.spine = spine_items
epub.write_epub(str(OUT), book)
print(f"written: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
