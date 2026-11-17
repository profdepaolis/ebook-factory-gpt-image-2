#!/usr/bin/env python3
"""Build reflowable KDP EPUB for any volume of «La valigia d'Italia».

Uso: python tools/build_epub.py [vol1|vol2|vol3|vol4]
Senza argomenti: vol1. Le immagini devono essere in <volume>/assets/illus_*.jpg,
la copertina in <volume>/assets/illus_01_cover.jpg; quelle mancanti vengono saltate.
"""
import re, sys, uuid
from pathlib import Path

import markdown
from ebooklib import epub

BASE = Path(__file__).resolve().parent.parent / "saga-destinazione-italia"

VOLUMES = {
    "vol1": dict(
        folder="volume-1-mare-500-autostrada",
        epub="La_valigia_d_Italia_Vol1_Mare_500_e_autostrada.epub",
        title="La valigia d'Italia — Vol. 1: Mare, 500 e autostrada",
        title_html="<p class=\"kicker\">La valigia d'Italia</p><p class=\"title\">Mare, 500<br/>e autostrada</p><p class=\"subtitle\">La storia del turismo italiano raccontata<br/>dalla famiglia Morelli (vol. 1)</p><p class=\"series\">Estate 1964 · Marco, 10 anni · Milano → Rimini</p>",
        description="Estate 1964. Marco Morelli, 10 anni, parte con la famiglia da Milano per Rimini in Fiat 500, sull'Autostrada del Sole appena completata. La prima estate di massa degli italiani, raccontata da un bambino. Primo volume della saga: la storia del turismo italiano dal Boom economico a oggi.",
        subject="ragazzi; storia; turismo; autostrada; Italia; 1964",
        illus={1: "illus_02_breda.jpg", 2: "illus_03_valigia.jpg", 3: "illus_04_partenza.jpg",
               4: "illus_05_casello.jpg", 5: "illus_06_autogrill.jpg", 6: "illus_07_pianura.jpg",
               7: "illus_08_rimini.jpg", 8: "illus_09_dieter.jpg", 9: "illus_10_festa.jpg",
               10: "illus_11_cartolina.jpg", 11: "illus_12_radio.jpg"},
    ),
    "vol2": dict(
        folder="volume-2-tutto-compreso",
        epub="La_valigia_d_Italia_Vol2_Tutto_compreso.epub",
        title="La valigia d'Italia — Vol. 2: Tutto compreso!",
        title_html="<p class=\"kicker\">La valigia d'Italia</p><p class=\"title\">Tutto<br/>compreso!</p><p class=\"subtitle\">La storia del turismo italiano raccontata<br/>dalla famiglia Morelli (vol. 2)</p><p class=\"series\">Estate 1979 · Sara, 10 anni · Milano → Cilento</p>",
        description="Estate 1979. Sara Morelli, 10 anni, vince un concorso di nuoto e va con la famiglia in un villaggio turistico tutto compreso nel Cilento: bracciali colorati, mini-club, il walkman appena inventato e — da scoprire — la spiaggia dei pescatori. Secondo volume della saga: la storia del turismo italiano dal Boom economico a oggi.",
        subject="ragazzi; storia; turismo; villaggi turistici; Italia; 1979; crisi petrolifera",
        illus={1: "illus_02_nuoto.jpg", 2: "illus_03_pullman.jpg", 3: "illus_04_reception.jpg",
               4: "illus_05_miniclub.jpg", 5: "illus_06_walkman.jpg", 6: "illus_07_petrolio.jpg",
               7: "illus_08_palinuro.jpg", 8: "illus_09_paestum.jpg", 9: "illus_10_pescatori.jpg",
               10: "illus_11_festa.jpg", 11: "illus_12_assemblea.jpg"},
    ),
    "vol3": dict(
        folder="volume-3-agriturismo-giubileo",
        epub="La_valigia_d_Italia_Vol3_Agriturismo_e_Giubileo.epub",
        title="La valigia d'Italia — Vol. 3: Agriturismo e Giubileo",
        title_html="<p class=\"kicker\">La valigia d'Italia</p><p class=\"title\">Agriturismo<br/>e Giubileo</p><p class=\"subtitle\">La storia del turismo italiano raccontata<br/>dalla famiglia Morelli (vol. 3)</p><p class=\"series\">Estate 2000 · Niccolò, 10 anni · Mugello → Roma</p>",
        description="Estate 2000. Niccolò Morelli, 10 anni, va con la famiglia in un agriturismo del Mugello: mucche, forno a legna e la prima e-mail della sua vita. Con una deviazione: Roma per il Giubileo 2000, con venticinque milioni di pellegrini. Terzo volume della saga: la storia del turismo italiano dal Boom economico a oggi.",
        subject="ragazzi; storia; turismo; agriturismo; Giubileo; Italia; 2000",
        illus={1: "illus_02_busta.jpg", 2: "illus_03_stella.jpg", 3: "illus_04_forno.jpg",
               4: "illus_05_nonno.jpg", 5: "illus_06_internet.jpg", 6: "illus_07_legge.jpg",
               7: "illus_08_deviazione.jpg", 8: "illus_09_roma.jpg", 9: "illus_10_cartolina.jpg",
               10: "illus_11_scheda.jpg", 11: "illus_12_valigia.jpg"},
    ),
    "vol4": dict(
        folder="volume-4-selfie-a-venezia",
        epub="La_valigia_d_Italia_Vol4_Selfie_a_Venezia.epub",
        title="La valigia d'Italia — Vol. 4: Selfie a Venezia",
        title_html="<p class=\"kicker\">La valigia d'Italia</p><p class=\"title\">Selfie<br/>a Venezia</p><p class=\"subtitle\">La storia del turismo italiano raccontata<br/>dalla famiglia Morelli (vol. 4)</p><p class=\"series\">Estate 2026 · Lea, 11 anni · Milano → Venezia → Roma</p>",
        description="Estate 2026. Lea Morelli, 11 anni, va con la famiglia a Venezia con il contributo di accesso e poi a Roma, appena uscita dal Giubileo 2025. Overtourism, record di arrivi, tutorial per viaggiare senza rovinare ciò che amiamo. Quarto e ultimo volume della saga: la storia del turismo italiano dal Boom economico a oggi.",
        subject="ragazzi; storia; turismo; overtourism; Venezia; Italia; 2026",
        illus={1: "illus_02_arrivi.jpg", 2: "illus_03_frecciarossa.jpg", 3: "illus_04_contributo.jpg",
               4: "illus_05_vaporetto.jpg", 5: "illus_06_cannaregio.jpg", 6: "illus_07_sanmarco.jpg",
               7: "illus_08_airbnb.jpg", 8: "illus_09_roma.jpg", 9: "illus_10_colosseo.jpg",
               10: "illus_11_giubileo.jpg", 11: "illus_12_cartolina.jpg"},
    ),
}

vol = sys.argv[1] if len(sys.argv) > 1 else "vol1"
if vol not in VOLUMES:
    sys.exit(f"Volume sconosciuto: {vol}. Usa uno tra: {', '.join(VOLUMES)}")
cfg = VOLUMES[vol]
ROOT = BASE / cfg["folder"]
MD = ROOT / "MANOSCRITTO.md"
ASSETS = ROOT / "assets"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / cfg["epub"]

raw = MD.read_text(encoding="utf-8")
m_app = re.search(r"\n# Apparati\b", raw)
body, apparati = (raw[: m_app.start()], raw[m_app.start():]) if m_app else (raw, "")
m_first = re.search(r"\n## ", body)
body = body[m_first.start():] if m_first else body

chapters = []
for block in re.split(r"\n(?=## )", body.strip()):
    lines = block.strip().splitlines()
    chapters.append((lines[0].lstrip("# ").strip(), "\n".join(lines[1:]).strip()))

ILLUS = cfg["illus"]
md = markdown.Markdown(extensions=["tables", "smarty"])

book = epub.EpubBook()
book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
book.set_title(cfg["title"])
book.set_language("it")
book.add_author("Il progetto La valigia d'Italia")
book.add_metadata("DC", "publisher", "La valigia d'Italia — collana di saga storica per ragazzi")
book.add_metadata("DC", "description", cfg["description"])
book.add_metadata("DC", "subject", cfg["subject"])

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
.frontmatter { text-align: center; }
.frontmatter .kicker { letter-spacing: .18em; text-transform: uppercase; color: #8a2b1d; font-size: .8em; }
.frontmatter .title { font-size: 2em; color: #8a2b1d; margin: .2em 0; }
.frontmatter .subtitle { font-size: 1.1em; color: #3b2d1f; }
.frontmatter .series { font-size: .9em; color: #6b5b45; margin-top: 2em; }
.colophon { font-size: .85em; color: #4a3f31; }
"""
book.add_item(epub.EpubItem(uid="css-main", file_name="style/main.css", media_type="text/css", content=css.encode()))

img_items = {}
for p in sorted(ASSETS.glob("illus_*.jpg")):
    if p.name == "illus_01_cover.jpg":
        continue  # gestita da set_cover()
    item = epub.EpubItem(uid=p.stem, file_name=f"images/{p.name}", media_type="image/jpeg", content=p.read_bytes())
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
    doc = epub.EpubHtml(title=title, file_name=f"chap_{idx:02d}.xhtml", lang="it")
    doc.content = html.encode("utf-8")
    return doc

cover_path = ASSETS / "illus_01_cover.jpg"
if cover_path.exists():
    book.set_cover("images/cover.jpg", cover_path.read_bytes())

title_pg = epub.EpubHtml(uid="frontespizio", title="Frontespizio", file_name="frontespizio.xhtml", lang="it")
title_pg.content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
<head><title>{cfg['title']}</title>
<link rel="stylesheet" type="text/css" href="style/main.css"/></head>
<body class="frontmatter">{cfg['title_html']}</body></html>""".encode("utf-8")

colophon = epub.EpubHtml(uid="colophon", title="Colophon e note", file_name="colophon.xhtml", lang="it")
colophon.content = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="it">
<head><title>Colophon e note</title>
<link rel="stylesheet" type="text/css" href="style/main.css"/></head>
<body class="colophon">
<h1 class="unnumbered">Un progetto, una valigia, quattro estati</h1>
<p><strong>La valigia d'Italia</strong> è la saga che racconta come l'Italia è diventata il Paese delle vacanze: dal Boom economico a oggi. Si legge in ordine, o si comincia da qualsiasi volume.</p>
<p><strong>Fonti e dati</strong>: i fatti storici di questo volume sono veri; i personaggi sono inventati. Dati e date fanno riferimento a fonti pubbliche (Università di Torino, Istat, MiC, Censis, archivio RAI); il dossier completo è in <em>PROGETTO_SAGA.md</em>, §9.</p>
<p><strong>Illustrazioni</strong>: generate con AI (GPT Image 2), stile gouache e acquerello. Nessuna fotografia di repertorio è stata usata in questa edizione.</p>
<p><strong>Per la scuola</strong>: ogni volume contiene «Lo sai che…?», «Parole d'epoca», «Linea del tempo» e la scheda «La storia vera dietro la storia» per genitori e insegnanti.</p>
<p>© Il progetto La valigia d'Italia. Tutti i diritti riservati.</p>
</body></html>""".encode("utf-8")

book.add_item(title_pg)
book.add_item(colophon)
spine_items, toc_items = [title_pg, colophon], []
for i, (title, text) in enumerate(chapters, start=1):
    doc = chapter_doc(i, title, md.convert(text), ILLUS.get(i))
    book.add_item(doc)
    spine_items.append(doc)
    toc_items.append(epub.Link(doc.file_name, title, f"ch{i}"))

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

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.toc = toc_items
book.spine = spine_items
epub.write_epub(str(OUT), book)
print(f"written: {OUT} ({OUT.stat().st_size/1024:.0f} KB, {len(img_items)} scene image(s))")
