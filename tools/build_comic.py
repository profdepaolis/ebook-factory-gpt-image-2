#!/usr/bin/env python3
"""Build the Vol.1 comic album PDF — bonellide 14×21 cm.

Usage:
    .venv/bin/python tools/build_comic.py [output.pdf]

Missing panel images are rendered as labelled placeholders (a warning is
printed), so the page layout can be QA'd before all AI art is generated.
Panels are centre-cropped to their frame aspect ratio, then framed with a
heavy black border. Balloons, captions and overlays are drawn as vectors —
never painted into the AI artwork.
"""
import math
import sys
from pathlib import Path

from PIL import Image
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
PANELS = ROOT / "saga-destinazione-italia/volume-1-mare-500-autostrada/fumetto/panels"
TMP = ROOT / "output/fumetto_tmp"
DEFAULT_OUT = (
    ROOT
    / "saga-destinazione-italia/volume-1-mare-500-autostrada/output"
    / "La_valigia_di_Cuoio_Fumetto_Vol1.pdf"
)

PW, PH = 140.0, 210.0
MX, MT, MB = 5.0, 6.0, 9.0
CW = PW - 2 * MX          # 130 mm usable width
GUT = 4.0                 # white gutter between panels
CONTENT_BOTTOM = PH - MB  # 201 mm

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

INK = (26, 26, 26)
CAPTION_BG = (252, 240, 200)
CAPTION_INK = (64, 44, 18)
FOOTER_GREY = (120, 120, 120)

MISSING: list[str] = []

# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

def panel_rects(template: str) -> dict[str, tuple[float, float, float, float]]:
    """Absolute panel rectangles (x, y, w, h) in mm."""
    if template == "top-wide":
        a = (MX, MT, CW, 66.0)
        y = MT + 66.0 + GUT                       # 76
        h = CONTENT_BOTTOM - y                    # 125
        bw = (CW - GUT) / 2                       # 63
        return {"A": a, "B": (MX, y, bw, h), "C": (MX + bw + GUT, y, bw, h)}
    if template == "finale":
        a = (MX, MT, CW, 54.0)                    #  6→ 60
        y_b = MT + 54.0 + GUT                     # 64
        b = (MX, y_b, CW, 44.0)                   # 64→108
        y_c = y_b + 44.0 + GUT                    # 112
        c = (MX, y_c, CW, CONTENT_BOTTOM - y_c)   # 112→201
        return {"A": a, "B": b, "C": c}
    if template == "duo":
        a = (MX, MT, CW, 66.0)                    #  6→ 72
        y_b = MT + 66.0 + GUT                     # 76
        return {"A": a, "B": (MX, y_b, CW, CONTENT_BOTTOM - y_b)}
    raise ValueError(f"unknown template {template}")


# per-panel vertical crop anchor (0 = top-anchored, 0.5 = centred, 1 = bottom)
ANCHOR_Y = {"p25_conto": 0.15, "p28_casa": 0.0}

def cropped(path: Path, w_mm: float, h_mm: float, key: str) -> Path:
    """Crop the panel to the target aspect ratio; cache on disk."""
    TMP.mkdir(parents=True, exist_ok=True)
    out = TMP / f"{key}.jpg"
    target_ar = w_mm / h_mm
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        ar = w / h
        if ar > target_ar:      # too wide → crop sides
            nw = int(h * target_ar)
            x0 = (w - nw) // 2
            im = im.crop((x0, 0, x0 + nw, h))
        elif ar < target_ar:    # too tall → crop top/bottom
            nh = int(w / target_ar)
            y0 = int((h - nh) * ANCHOR_Y.get(key, 0.5))
            im = im.crop((0, y0, w, y0 + nh))
        im.save(out, quality=92)
    return out


# --------------------------------------------------------------------------
# drawing primitives
# --------------------------------------------------------------------------

class ComicPDF(FPDF):
    def __init__(self):
        super().__init__(format=(PW, PH), unit="mm")
        self.set_auto_page_break(False)
        self.set_margins(0, 0, 0)
        self.add_font("sans", "", F_SANS)
        self.add_font("sansb", "", F_SANS_B)
        self.add_font("serif", "", F_SERIF)
        self.add_font("serifb", "", F_SERIF_B)

    # -- text measuring ----------------------------------------------------
    def text_height(self, family, size, w, text):
        self.set_font(family, "", size)
        h = self.multi_cell(w, size * 0.42 + 1.1, text, dry_run=True, output="HEIGHT")
        return h

    # -- panel frame ---------------------------------------------------------
    def panel(self, rect, image: Path | None, label: str):
        x, y, w, h = rect
        if image is None:
            MISSING.append(label)
            self.set_fill_color(38, 50, 66)
            self.rect(x, y, w, h, style="F")
            self.set_text_color(255, 255, 255)
            self.set_font("sansb", "", 34)
            self.set_xy(x, y + h / 2 - 10)
            self.cell(w, 14, "?", align="C")
            self.set_font("sans", "", 6)
            self.set_xy(x + 2, y + h / 2 + 8)
            self.cell(w - 4, 4, label, align="C")
        else:
            img = cropped(image, w, h, label)
            self.image(str(img), x=x, y=y, w=w, h=h)
        self.set_draw_color(*INK)
        self.set_line_width(1.15)
        self.rect(x, y, w, h, style="D")
        self.set_line_width(0.2)

    # -- tail -----------------------------------------------------------------
    def tail(self, cx, cy, rx, ry, tx, ty, style="speech"):
        dx, dy = tx - cx, ty - cy
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            return
        ux, uy = dx / dist, dy / dist
        # ray → axis-aligned ellipse intersection
        t = 1.0 / math.sqrt((ux / rx) ** 2 + (uy / ry) ** 2)
        px, py = cx + ux * t, cy + uy * t
        # perpendicular (base of the tail)
        nx, ny = -uy, ux
        half = min(3.4, dist * 0.18)
        b1 = (px + nx * half, py + ny * half)
        b2 = (px - nx * half, py - ny * half)
        self.set_draw_color(*INK)
        self.set_fill_color(255, 255, 255)
        if style == "radio":
            # zig-zag lightning tail
            steps = 4
            pts = []
            for i in range(steps + 1):
                f = i / steps
                px_ = b1[0] + (tx - b1[0]) * f
                py_ = b1[1] + (ty - b1[1]) * f
                off = (3.4 if i % 2 == 0 else -3.4) * (1 - f)
                pts.append((px_ + nx * off, py_ + ny * off))
            pts.append((tx, ty))
            self.polygon(pts, style="F")
        else:
            self.polygon([b1, b2, (tx, ty)], style="FD")

    def balloon(self, rect, spec):
        x, y, w, h = rect
        cx = x + spec["cx"]; cy = y + spec["cy"]
        bw = spec.get("w", 46.0)
        size = spec.get("size", 9.0)
        family = spec.get("family", "sansb")
        style = spec.get("style", "speech")
        tx, ty = spec.get("tail", (spec["cx"], spec["cy"] + 30))
        tx, ty = x + tx, y + ty
        pad_h, pad_v = 6.0, 4.6
        inner_w = bw - 2 * pad_h
        th = self.text_height(family, size, inner_w, spec["text"])
        bh = max(spec.get("min_h", 11.0), th + 2 * pad_v)
        rx, ry = bw / 2, bh / 2
        # tail first (base hidden under the balloon)
        if style == "thought":
            # small trailing circles instead of a wedge
            for i, f in enumerate((0.35, 0.62, 0.85)):
                px_ = cx + (tx - cx) * f
                py_ = cy + (ty - cy) * f
                r = 2.6 - i * 0.9
                self.set_fill_color(255, 255, 255)
                self.set_draw_color(*INK)
                self.set_line_width(0.5)
                self.ellipse(px_ - r, py_ - r, 2 * r, 2 * r, style="FD")
        else:
            self.tail(cx, cy, rx, ry, tx, ty, style="radio" if style == "radio" else "speech")
        # balloon body
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*INK)
        self.set_line_width(1.0 if style == "shout" else 0.6)
        if style == "thought":
            self.set_dash_pattern(dash=2.6, gap=1.8)
        self.ellipse(cx - rx, cy - ry, bw, bh, style="FD")
        self.set_dash_pattern()
        # text
        self.set_text_color(*INK)
        self.set_font(family, "", size)
        self.set_xy(cx - inner_w / 2, cy - th / 2)
        self.multi_cell(inner_w, size * 0.42 + 1.1, spec["text"], align="C")

    def caption(self, rect, spec):
        x, y, w, h = rect
        cx = x + spec["x"]; cy = y + spec["y"]
        w_ = spec.get("w", w - 8)
        size = spec.get("size", 8.5)
        family = spec.get("family", "serifb")
        pad_h, pad_v = 5.0, 4.0
        inner_w = w_ - 2 * pad_h
        th = self.text_height(family, size, inner_w, spec["text"])
        bh = th + 2 * pad_v
        self.set_fill_color(*CAPTION_BG)
        self.set_draw_color(*INK)
        self.set_line_width(0.55)
        self.rect(cx, cy, w_, bh, style="FD")
        self.set_text_color(*CAPTION_INK)
        self.set_font(family, "", size)
        self.set_xy(cx + pad_h, cy + pad_v)
        self.multi_cell(inner_w, size * 0.42 + 1.1, spec["text"], align="L")

    def overlay(self, rect, spec):
        x, y, w, h = rect
        ox, oy = x + spec["x"], y + spec["y"]
        w_ = spec.get("w", w - 8)
        size = spec.get("size", 12)
        color = tuple(spec.get("color", (255, 255, 255)))
        align = spec.get("align", "C")
        style = spec.get("style", "plain")
        family = spec.get("family", "sansb")
        if style == "neon":
            # glow: dark halo strokes, hot core
            self.set_font(family, "", size)
            for dx, dy, col in [(-0.5, 0, (120, 18, 24)), (0.5, 0, (120, 18, 24)),
                                 (0, -0.5, (120, 18, 24)), (0, 0.5, (120, 18, 24))]:
                self.set_text_color(*col)
                self.set_xy(ox + dx, oy + dy)
                self.cell(w_, size * 0.5, spec["text"], align=align)
            self.set_text_color(*color)
            self.set_xy(ox, oy)
            self.cell(w_, size * 0.5, spec["text"], align=align)
        else:
            self.set_font(family, "", size)
            self.set_text_color(*color)
            self.set_xy(ox, oy)
            self.multi_cell(w_, size * 0.46 + 0.8, spec["text"], align=align)

    def scene_footer(self, page_no):
        self.set_draw_color(190, 190, 190)
        self.set_line_width(0.35)
        self.line(MX, PH - 5.6, PW - MX, PH - 5.6)
        self.set_font("sans", "", 6.2)
        self.set_text_color(*FOOTER_GREY)
        self.set_xy(MX, PH - 4.6)
        self.cell(80, 3.4, "La valigia d'Italia · n° 1", align="L")
        self.set_xy(PW - MX - 30, PH - 4.6)
        self.cell(30, 3.4, str(page_no), align="R")


# --------------------------------------------------------------------------
# album content
# --------------------------------------------------------------------------

def img(name):
    p = PANELS / name
    return p if p.exists() else None


PAGES = [
    # ---------------- Page 1 — Le città si svuotano
    dict(template="top-wide", title="Le città si svuotano", panels={
        "A": (img("p01_breda.jpg"), "p01_breda"),
        "B": (img("p02_cucina.jpg"), "p02_cucina"),
        "C": (img("p03_euforia.jpg"), "p03_euforia"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=100, text="1 agosto 1964. La Breda chiude per tre settimane.", size=8.5),
    ], balloons=[
        dict(panel="B", cx=22, cy=22, w=43, tail=(15, 52), size=9,
             text="Marco, quest'anno andiamo al mare."),
        dict(panel="B", cx=42, cy=76, w=39, tail=(41, 110), size=10, text="…Davvero?"),
        dict(panel="C", cx=31.5, cy=28, w=50, tail=(31.5, 55), size=12.5, style="shout", min_h=17,
             text="IL MARE! IL MARE PER DAVVERO!"),
    ], overlays=[]),
    # ---------------- Page 2 — La valigia di cuoio
    dict(template="top-wide", title="La valigia di cuoio", panels={
        "A": (img("p04_mercato.jpg"), "p04_mercato"),
        "B": (img("p05_valigia.jpg"), "p05_valigia"),
        "C": (img("p07_cucina2.jpg"), "p07_cucina2"),
    }, captions=[
        dict(panel="C", x=5, y=104, w=53, text="La valigia di cuoio: dal 1938 al 1964, e avanti.", size=7.6),
    ], balloons=[
        dict(panel="A", cx=88, cy=15, w=48, tail=(42, 32), size=10,
             text="Papà! QUELLA. Proprio quella."),
        dict(panel="B", cx=31.5, cy=20, w=49, tail=(28, 56), size=8.5,
             text="Duemiladuecento. Ultima offerta."),
        dict(panel="B", cx=32, cy=86, w=47, tail=(38, 112), size=9,
             text="…E che sia l'ultima davvero."),
        dict(panel="C", cx=22, cy=24, w=40, tail=(18, 58), size=10.5, text="Ma è USATA!"),
        dict(panel="C", cx=43, cy=72, w=43, tail=(45, 104), size=10.5, text="È VIS-SUTA, Lina."),
    ], overlays=[]),
    # ---------------- Page 3 — La partenza
    dict(template="top-wide", title="La partenza", panels={
        "A": (img("p06_500top.jpg"), "p06_500top"),
        "B": (img("p09_casello.jpg"), "p09_casello"),
        "C": (img("p10_marco500.jpg"), "p10_marco500"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=95, text="Un lunedì, alle sei del mattino.", size=8.5),
    ], balloons=[
        dict(panel="B", cx=32, cy=20, w=46, tail=(46, 54), size=9.5,
             text="Buon viaggio e… attenti al sole!"),
        dict(panel="C", cx=31.5, cy=30, w=48, tail=(28, 62), size=9.5,
             text="Papà… perché si chiama Autostrada del SOLE?"),
        dict(panel="C", cx=31.5, cy=88, w=50, tail=(53, 47), size=9.5,
             text="Perché unisce l'Italia da Milano a Napoli."),
    ], overlays=[]),
    # ---------------- Page 4 — L'autogrill
    dict(template="top-wide", title="L'autogrill", panels={
        "A": (img("p11_autogrill.jpg"), "p11_autogrill"),
        "B": (img("p12_gelato.jpg"), "p12_gelato"),
        "C": (img("p13_giornale.jpg"), "p13_giornale"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=95, text="Fiorenzuola d'Arda, prima sosta.", size=8.5),
    ], balloons=[
        dict(panel="B", cx=31, cy=22, w=43, tail=(27, 58), size=12, text="50 lire di pistacchio!"),
        dict(panel="C", cx=27, cy=24, w=44, tail=(18, 56), size=7,
             text="«IN ARRIVO L'AUTOSTRADA COMPLETA…»"),
        dict(panel="C", cx=41, cy=86, w=48, tail=(47, 114), size=8.5,
             text="Il 4 ottobre, Marco. Ricordatene."),
    ], overlays=[]),
    # ---------------- Page 5 — Rimini, finalmente!
    dict(template="top-wide", title="Rimini, finalmente!", panels={
        "A": (img("p14_rimini.jpg"), "p14_rimini"),
        "B": (img("p15_argia.jpg"), "p15_argia"),
        "C": (img("p16_letto.jpg"), "p16_letto"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=40, text="Il traguardo.", size=8.5),
        dict(panel="C", x=6, y=100, w=51, text="Il mare respira sotto di lui.", size=8.5),
    ], balloons=[
        dict(panel="B", cx=31.5, cy=22, w=52, tail=(30, 58), size=9.5,
             text="Qui i prezzi sono onesti. E il mare è basso!"),
    ], overlays=[
        dict(panel="A", x=96, y=29.5, w=27, text="LA SIRENA", size=10, style="neon", color=(255, 96, 76)),
    ]),
    # ---------------- Page 6 — L'amico tedesco
    dict(template="top-wide", title="L'amico tedesco", panels={
        "A": (img("p17_tufo.jpg"), "p17_tufo"),
        "B": (img("p18_dieter.jpg"), "p18_dieter"),
        "C": (img("p19_agfa.jpg"), "p19_agfa"),
    }, captions=[], balloons=[
        dict(panel="A", cx=40, cy=14, w=40, tail=(35, 48), size=13, style="shout", min_h=15,
             text="CE L'HO FATTA!"),
        dict(panel="A", cx=103, cy=40, w=45, tail=(70, 58), size=9.5,
             text="…Non sei l'Oceanico!"),
        dict(panel="B", cx=31.5, cy=17, w=52, tail=(30, 54), size=8,
             text="Ciao! Vengo da Monaco. Mio nonno dice che qui tutto è «un po' in ritardo e un po' più buono»!"),
        dict(panel="C", cx=34, cy=22, w=34, tail=(49, 46), size=11, text="Te la mando."),
    ], overlays=[]),
    # ---------------- Page 7 — La rotonda sul mare
    dict(template="top-wide", title="La rotonda sul mare", panels={
        "A": (img("p20_banda.jpg"), "p20_banda"),
        "B": (img("p21_festa.jpg"), "p21_festa"),
        "C": (img("p22_diario.jpg"), "p22_diario"),
    }, captions=[], balloons=[
        dict(panel="A", cx=82, cy=16, w=58, tail=(95, 42), size=9, style="shout", min_h=17,
             text="SABATO 15 AGOSTO, GRANDE FESTA DI FERRAGOSTO!"),
        dict(panel="B", cx=27, cy=20, w=43, tail=(23, 56), size=9.5,
             text="ORE-STE! Non si balla…!"),
        dict(panel="B", cx=40, cy=85, w=44, tail=(45, 114), size=12, style="shout",
             text="ECCOME SE BALLO!"),
        dict(panel="C", cx=31.5, cy=24, w=50, tail=(25, 62), size=9.5, style="thought",
             text="Io oggi ho visto mio papà ballare."),
    ], overlays=[]),
    # ---------------- Page 8 — La cartolina
    dict(template="duo", title="La cartolina", panels={
        "A": (img("p23_cartolina.jpg"), "p23_cartolina"),
        "B": (img("p24_francobollo.jpg"), "p24_francobollo"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=70, text="Giovedì, giorno di pioggia.", size=8.5),
        dict(panel="B", x=8, y=102, w=90, text="Buon viaggio, cartolina.", size=9),
    ], balloons=[
        dict(panel="A", cx=32, cy=28, w=48, tail=(30, 62), size=8.5,
             text="Cara Nonna Rosa, sono a Rimini e non voglio tornare."),
        dict(panel="B", cx=65, cy=22, w=42, tail=(64, 58), size=12, text="Cinque lire. Corri!"),
    ], overlays=[]),
    # ---------------- Page 9 — Il 4 ottobre
    dict(template="top-wide", title="Il 4 ottobre", panels={
        "A": (img("p25_conto.jpg"), "p25_conto"),
        "B": (img("p26_radio.jpg"), "p26_radio"),
        "C": (img("p27_ripostiglio.jpg"), "p27_ripostiglio"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=110, text="Ottomila lire per tutta la settimana.", size=8.5),
    ], balloons=[
        dict(panel="B", cx=31.5, cy=24, w=52, tail=(40, 60), size=8.5, style="radio",
             text="…il 4 ottobre l'Autostrada del Sole sarà completata. 760 km."),
        dict(panel="C", cx=31.5, cy=24, w=50, tail=(30, 62), size=9.5,
             text="La teniamo. Giuro. Questa valigia non resterà ferma."),
    ], overlays=[]),
    # ---------------- Page 10 — L'ultima pagina del diario
    dict(template="finale", title="L'ultima pagina del diario", panels={
        "A": (img("p28_casa.jpg"), "p28_casa"),
        "B": (img("p29_diario.jpg"), "p29_diario"),
        "C": (img("p30_finestra.jpg"), "p30_finestra"),
    }, captions=[
        dict(panel="A", x=4, y=4, w=110, text="Milano, di nuovo. Ma qualcosa è cambiato.", size=8.5),
        dict(panel="C", x=10, y=70, w=110, text="Il viaggio, in Italia, era appena cominciato.",
             size=10, family="serifb"),
    ], balloons=[], overlays=[
        dict(panel="B", x=27, y=17, w=34,
             text="«Questa valigia non si butta. Questa valigia va avanti.»",
             size=9, family="serif", color=(84, 55, 22), style="plain", align="L"),
        dict(panel="C", x=10, y=20, w=110, text="FINE",
             size=19, family="serifb", color=(246, 232, 198), style="plain", align="C"),
    ]),
]


def build_cover(pdf: ComicPDF):
    pdf.add_page()
    cover = PANELS / "p00_cover.jpg"
    if cover.exists():
        img_c = cropped(cover, PW, PH, "cover_full")
        pdf.image(str(img_c), x=0, y=0, w=PW, h=PH)
    else:
        MISSING.append("p00_cover")
        pdf.set_fill_color(24, 46, 56)
        pdf.rect(0, 0, PW, PH, style="F")
    # masthead band
    pdf.set_fill_color(14, 44, 55)
    pdf.rect(0, 0, PW, 34, style="F")
    pdf.set_fill_color(232, 178, 92)   # ochre rule
    pdf.rect(0, 34, PW, 2.2, style="F")
    pdf.set_text_color(246, 240, 224)
    pdf.set_font("serifb", "", 24)
    pdf.set_xy(0, 6.5)
    pdf.cell(PW, 11, "LA VALIGIA DI CUOIO", align="C")
    pdf.set_font("serifb", "", 12.5)
    pdf.set_text_color(232, 178, 92)
    pdf.set_xy(0, 18.5)
    pdf.cell(PW, 6, "IL VIAGGIO DI MARCO", align="C")
    pdf.set_font("sans", "", 7.5)
    pdf.set_text_color(246, 240, 224)
    pdf.set_xy(0, 27.5)
    pdf.cell(PW, 4, "LA VALIGIA D'ITALIA  ·  N° 1", align="C")
    # colophon strip
    pdf.set_fill_color(14, 44, 55)
    pdf.rect(0, PH - 12, PW, 12, style="F")
    pdf.set_font("serif", "", 7.5)
    pdf.set_text_color(246, 240, 224)
    pdf.set_xy(0, PH - 9.5)
    pdf.cell(PW, 5, "Raccontata da La valigia d'Italia  ·  per ragazzi da 9 a 12 anni", align="C")


def build(out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf = ComicPDF()
    pdf.set_title("La valigia di cuoio — il viaggio di Marco · La valigia d'Italia n° 1")
    pdf.set_author("La valigia d'Italia")
    pdf.set_creator("tools/build_comic.py")
    build_cover(pdf)
    page_no = 2
    for page in PAGES:
        pdf.add_page()
        rects = panel_rects(page["template"])
        for key, (image, label) in page["panels"].items():
            pdf.panel(rects[key], image, label)
        for cap in page["captions"]:
            pdf.caption(rects[cap["panel"]], cap)
        for ov in page["overlays"]:
            pdf.overlay(rects[ov["panel"]], ov)
        for bal in page["balloons"]:
            pdf.balloon(rects[bal["panel"]], bal)
        pdf.scene_footer(page_no)
        page_no += 1
    pdf.output(str(out))
    if MISSING:
        print("WARNING — panels still missing: " + ", ".join(sorted(set(MISSING))), file=sys.stderr)
    print(f"OK → {out}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    build(target)
