#!/usr/bin/env python3
"""Genera i 4 PDF 6×9″ della saga da MANOSCRITTO.md + assets/.
Uso: .venv/bin/python tools/build_pdf.py [vol1|vol2|vol3|vol4|all]
Output in <volume>/output/La_valigia_d_Italia_VolN_*.pdf (cartella gitignored).
Margini ≥ 11 mm (entro i minimi KDP per libri ≤150 pagine).
"""
import re, sys, ast
from pathlib import Path

try:
    import markdown
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    sys.exit("Manca fpdf2: .venv/bin/pip install fpdf2 markdown")

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "saga-destinazione-italia"

src = (BASE / "tools" / "build_epub.py").read_text(encoding="utf-8")
ILLUS = {}
for vol, body in re.findall(r'"(vol\d)": dict\((.*?)\),', src, re.S):
    m = re.search(r'illus=(\{.*?\}),', body, re.S)
    if m:
        ILLUS[vol] = {int(k): v for k, v in ast.literal_eval(m.group(1)).items()}

VOLUMES = [
    ("vol1", "volume-1-mare-500-autostrada", "La_valigia_d_Italia_Vol1_Mare_500_e_autostrada.pdf",
     "Mare 500\ne autostrada", "Vol. 1", "1964 · Marco, 10 anni · Milano → Rimini"),
    ("vol2", "volume-2-tutto-compreso", "La_valigia_d_Italia_Vol2_Tutto_compreso.pdf",
     "Tutto\ncompreso!", "Vol. 2", "1979 · Sara, 10 anni · Milano → Cilento"),
    ("vol3", "volume-3-agriturismo-giubileo", "La_valigia_d_Italia_Vol3_Agriturismo_e_Giubileo.pdf",
     "Agriturismo\ne Giubileo", "Vol. 3", "2000 · Niccolò, 10 anni · Mugello → Roma"),
    ("vol4", "volume-4-selfie-a-venezia", "La_valigia_d_Italia_Vol4_Selfie_a_Venezia.pdf",
     "Selfie\na Venezia", "Vol. 4", "2026 · Lea, 11 anni · Milano → Venezia → Roma"),
]

PW, PH = 152.4, 228.6  # 6×9 in
MARGIN = 11
TERRA = (138, 43, 29)
GOLD = (212, 160, 23)
INK = (43, 33, 24)
CREAM = (247, 239, 226)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

class SagaPDF(FPDF):
    vol_label = ""

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-11)
        self.set_font("DejaVu", "", 6.5)
        self.set_text_color(107, 91, 69)
        self.cell(PW - 2 * MARGIN, 6, f"La valigia d'Italia  ·  {self.vol_label}  ·  {self.page_no()}", align="C")

def strip_tags(t):
    return re.sub(r"<[^>]+>", "", t)

def html_body(md_text):
    html = markdown.markdown(md_text, extensions=["tables", "smarty"])
    # tabelle -> righe puntate
    def table_to_list(m):
        rows = re.findall(r"<tr>(.*?)</tr>", m.group(0), re.S)
        out = []
        for r in rows:
            cells = [strip_tags(c).strip() for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)]
            cells = [c for c in cells if c]
            if cells:
                out.append("<p>• " + " — ".join(cells) + "</p>")
        return "\n".join(out)
    html = re.sub(r"<table>.*?</table>", table_to_list, html, flags=re.S)
    for tag in ["thead", "tbody", "tr", "td", "th"]:
        html = re.sub(rf"</?{tag}[^>]*>", "", html)
    # enfasi -> grassetto (niente italic nel font regolare)
    html = re.sub(r"</?(em|i)\b[^>]*>", lambda m: "<b>" if m.group(0)[1] != "/" else "</b>", html)
    html = re.sub(r"</?(strong)\b[^>]*>", lambda m: "<b>" if m.group(0)[1] != "/" else "</b>", html)
    # rimuovi wrapper non supportati
    html = re.sub(r"</?(div|span|figure)[^>]*>", "", html)
    html = re.sub(r"<p>\s*</p>", "", html)
    return html

def build(vol, folder, pdf_name, title, vol_label, series_line):
    ASSETS = SRC / folder / "assets"
    OUT_DIR = SRC / folder / "output"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf = SagaPDF(orientation="P", unit="mm", format=(PW, PH))
    pdf.vol_label = vol_label
    pdf.set_margins(MARGIN, 12, MARGIN)
    pdf.set_auto_page_break(True, margin=13)
    pdf.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSerif.ttf"))
    pdf.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSerif-Bold.ttf"))
    pdf.set_text_color(*INK)

    # --- copertina ---
    pdf.add_page()
    pdf.set_fill_color(*TERRA)
    pdf.rect(0, 0, PW, PH, style="F")
    cover = ASSETS / "illus_01_cover.jpg"
    if cover.exists():
        img_w = PW - 2 * 8
        img_h = img_w * 9 / 16
        pdf.image(str(cover), x=8, y=(PH - img_h) / 2 - 14, w=img_w)
        pdf.set_xy(8, (PH + img_h) / 2 - 6)
        pdf.set_font("DejaVu", "B", 13)
        pdf.set_text_color(*GOLD)
        pdf.cell(PW - 16, 8, "LA VALIGIA D'ITALIA", align="C")
        pdf.set_xy(8, (PH + img_h) / 2 + 3)
        pdf.set_font("DejaVu", "", 8)
        pdf.set_text_color(*CREAM)
        pdf.cell(PW - 16, 6, series_line, align="C")

    # --- frontespizio ---
    pdf.add_page()
    pdf.set_text_color(*TERRA)
    pdf.ln(24)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(107, 91, 69)
    pdf.cell(PW - 2 * MARGIN, 6, "L A   V A L I G I A   D ' I T A L I A", align="C")
    pdf.ln(16)
    pdf.set_font("DejaVu", "B", 26)
    pdf.set_text_color(*TERRA)
    for line in title.split("\n"):
        pdf.multi_cell(PW - 2 * MARGIN, 13, line, align="C")
    pdf.ln(6)
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.8)
    x = (PW - 46) / 2
    pdf.line(x, pdf.get_y(), x + 46, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(PW - 2 * MARGIN, 7, series_line, align="C")
    pdf.ln(30)
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(107, 91, 69)
    pdf.multi_cell(PW - 2 * MARGIN, 5, "Saga storica per ragazzi 9–12 anni\nTesto: italiano · Formato ibrido (testo + illustrazioni)\nKDP 6×9\" · © Il progetto La valigia d'Italia", align="C")

    # --- corpo ---
    text = (SRC / folder / "MANOSCRITTO.md").read_text(encoding="utf-8")
    sections = re.split(r"(?=\n## )", text)
    # sezioni: tutto ciò che inizia con ## in ordine
    for sec in sections:
        m = re.match(r"\n?## (.*?)\n", sec)
        if not m:
            continue  # intestazione del volume (frontespizio gestito sopra)
        heading = m.group(1).strip()
        body = sec[m.end():].strip()
        is_apparati_head = heading.lower().startswith("apparati")
        chap_match = re.match(r"Capitolo\s+(\d+)", heading)
        ch_num = int(chap_match.group(1)) if chap_match else None

        pdf.add_page()
        pdf.set_font("DejaVu", "B", 16)
        pdf.set_text_color(*TERRA)
        pdf.multi_cell(PW - 2 * MARGIN, 9, heading, align="L")
        pdf.ln(1)
        pdf.set_draw_color(*GOLD)
        pdf.set_line_width(0.6)
        y = pdf.get_y()
        pdf.line(MARGIN, y, MARGIN + 34, y)
        pdf.ln(4)

        if ch_num and ILLUS.get(vol, {}).get(ch_num):
            img = ASSETS / ILLUS[vol][ch_num]
            if img.exists():
                pdf.image(str(img), x=MARGIN + 4, w=PW - 2 * (MARGIN + 4))
                pdf.ln(4)

        pdf.set_text_color(*INK)
        pdf.set_font("DejaVu", "", 10.5)
        pdf.write_html(html_body(body))
        pdf.ln(2)

    OUT = OUT_DIR / pdf_name
    pdf.output(str(OUT))
    print(f"written: {OUT} ({OUT.stat().st_size/1024:.0f} KB, {pdf.page_no()} pagine)")

which = sys.argv[1] if len(sys.argv) > 1 else "all"
for cfg in VOLUMES:
    if which in ("all", cfg[0]):
        build(*cfg)
