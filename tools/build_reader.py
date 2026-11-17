#!/usr/bin/env python3
"""Genera reader/index.html — il lettore web completo dei 4 volumi.
Uso: .venv/bin/python tools/build_reader.py   (richiede il package markdown)
Immagini referenziate via path assoluti dal root del repo (/saga-destinazione-italia/...).
"""
import re, sys, ast
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Manca il package markdown: .venv/bin/pip install markdown")

import markdown as md_mod

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "saga-destinazione-italia"
OUT = BASE / "reader" / "index.html"

# --- estrae le mappe ILLUS da tools/build_epub.py (fonte unica) ---
src = (BASE / "tools" / "build_epub.py").read_text(encoding="utf-8")
ILLUS = {}
for vol, body in re.findall(r'"(vol\d)": dict\((.*?)\),', src, re.S):
    m = re.search(r'illus=(\{.*?\}),', body, re.S)
    if m:
        ILLUS[vol] = {int(k): v for k, v in ast.literal_eval(m.group(1)).items()}

VOLUMES = [
    ("vol1", "volume-1-mare-500-autostrada", "Vol. 1 · Mare 500 e autostrada", "1964 — Marco, 10 anni"),
    ("vol2", "volume-2-tutto-compreso", "Vol. 2 · Tutto compreso!", "1979 — Sara, 10 anni"),
    ("vol3", "volume-3-agriturismo-giubileo", "Vol. 3 · Agriturismo e Giubileo", "2000 — Niccolò, 10 anni"),
    ("vol4", "volume-4-selfie-a-venezia", "Vol. 4 · Selfie a Venezia", "2026 — Lea, 11 anni"),
]

def split_manuscript(text):
    """ritorna (front_matter, [(titolo_cap, corpo)], apparati)"""
    intro, rest = text.split("---\n", 1)[0], None
    m = re.split(r"\n## ", text)
    head = m[0]
    chapters, apparati = [], ""
    for part in m[1:]:
        part = part.rstrip("\n")
        if part.startswith("Apparati"):
            apparati = part
            continue
        title, _, body = part.partition("\n")
        chapters.append((title.strip(), body.strip()))
    return head, chapters, apparati

def md(t):
    return md_mod.markdown(t, extensions=["tables", "smarty"])

parts = []
nav_links = []
covers = {}
for vol, folder, name, sub in VOLUMES:
    text = (SRC / folder / "MANOSCRITTO.md").read_text(encoding="utf-8")
    _, chapters, apparati = split_manuscript(text)
    asset = f"/saga-destinazione-italia/{folder}/assets"
    covers[vol] = f"{asset}/illus_01_cover.jpg"
    ch_html = []
    for i, (title, body) in enumerate(chapters, start=1):
        illus = ILLUS.get(vol, {}).get(i)
        img = f'<figure class="plate"><img src="{asset}/{illus}" alt="Illustrazione — {title}" loading="lazy"></figure>' if illus else ""
        ch_html.append(f'<section class="chapter" id="{vol}-ch{i}"><h2>{title}</h2>{img}{md(body)}</section>')
    if apparati:
        ch_html.append(f'<section class="chapter apparati" id="{vol}-apparati"><h2>Apparati — «Lo sai che…?»</h2>{md(apparati)}</section>')
    body_html = "\n".join(ch_html)
    parts.append(f'''
<article class="volume" id="{vol}" data-vol="{vol}">
  <header class="vol-head">
    <img class="vol-cover" src="{covers[vol]}" alt="Copertina {name}" loading="lazy">
    <div><h1>{name}</h1><p class="vol-sub">{sub} · La valigia d'Italia</p></div>
  </header>
  {body_html}
</article>''')
    nav_links.append(f'<div class="nav-vol" data-vol="{vol}"><button class="nav-toggle">{name}</button><ul class="nav-chapters">'
                     + "".join(f'<li><a href="#" data-target="{vol}-ch{i}">{i}. {t}</a></li>' for i, (t, _) in enumerate(chapters, 1))
                     + f'<li><a href="#" data-target="{vol}-apparati">Apparati</a></li></ul></div>')

page = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>La valigia d'Italia — Lettore completo (saga in 4 volumi)</title>
<style>
:root {{
  --terra:#8a2b1d; --gold:#d4a017; --paper:#f7efe2; --ink:#2b2118; --card:#fffdf6;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Georgia,'Times New Roman',serif; color:var(--ink);
  background:var(--paper); display:flex; min-height:100vh; }}
aside#sidebar {{ width:290px; min-width:290px; background:#31231a; color:#f1e6d2; padding:18px 14px;
  position:sticky; top:0; height:100vh; overflow-y:auto; }}
#sidebar h1 {{ font-size:1.05em; letter-spacing:.04em; color:var(--gold); margin:.2em 0 .1em; }}
#sidebar .saga {{ font-size:.72em; color:#c9b48a; border-bottom:1px solid #4b3a2c; padding-bottom:.9em; margin-bottom:.8em; }}
.nav-vol {{ margin:.2em 0; }}
.nav-toggle {{ width:100%; text-align:left; background:none; border:1px solid #4b3a2c; border-radius:8px;
  color:#f1e6d2; padding:.45em .6em; font-family:inherit; font-size:.78em; cursor:pointer; }}
.nav-toggle:hover {{ background:#3d2f24; border-color:var(--gold); }}
.nav-vol.open .nav-toggle {{ border-color:var(--gold); color:var(--gold); }}
.nav-chapters {{ display:none; list-style:none; margin:.3em 0 .6em; padding:0 0 0 .4em; }}
.nav-vol.open .nav-chapters {{ display:block; }}
.nav-chapters a {{ display:block; color:#d8c9ae; text-decoration:none; font-size:.72em; padding:.18em .5em; border-radius:6px; }}
.nav-chapters a:hover {{ background:#4b3a2c; color:#fff; }}
main {{ flex:1; padding:26px 30px 90px; max-width:980px; }}
.volume {{ display:none; }}
.volume.active {{ display:block; animation:fade .4s ease; }}
@keyframes fade {{ from {{opacity:0; transform:translateY(8px);}} to {{opacity:1;}} }}
.vol-head {{ display:flex; gap:22px; align-items:center; background:var(--card); border:1px solid #e3d5bd;
  border-radius:14px; padding:18px; margin-bottom:26px; box-shadow:0 2px 10px rgba(43,33,24,.08); }}
.vol-cover {{ width:150px; border-radius:10px; box-shadow:0 4px 14px rgba(43,33,24,.35); }}
.vol-head h1 {{ color:var(--terra); font-size:1.5em; margin:.1em 0; }}
.vol-sub {{ color:#6b5b45; font-size:.85em; margin:0; }}
.chapter {{ background:var(--card); border:1px solid #e3d5bd; border-radius:12px; padding:22px 26px; margin-bottom:22px;
  box-shadow:0 1px 6px rgba(43,33,24,.06); }}
.chapter h2 {{ color:var(--terra); font-size:1.35em; border-bottom:3px solid var(--gold); padding-bottom:.3em; }}
.chapter p {{ font-size:1.02em; line-height:1.72; }}
.chapter em {{ color:#4a3f31; }}
.plate {{ margin:1.2em 0; text-align:center; }}
.plate img {{ max-width:100%; border-radius:10px; box-shadow:0 3px 16px rgba(43,33,24,.28); }}
.apparati table {{ border-collapse:collapse; width:100%; font-size:.9em; }}
.apparati th,.apparati td {{ border:1px solid #c9b48a; padding:.35em .55em; text-align:left; }}
.apparati th {{ background:#f3e9d2; }}
.toolbar {{ position:fixed; bottom:0; left:290px; right:0; background:rgba(255,253,246,.92); backdrop-filter:blur(6px);
  border-top:1px solid #e3d5bd; padding:10px 26px; display:flex; gap:12px; align-items:center; }}
.toolbar button {{ background:var(--terra); color:#fffdf6; border:none; border-radius:8px; padding:.5em 1.1em;
  font-family:inherit; font-size:.85em; cursor:pointer; }}
.toolbar button:hover {{ background:#6f2318; }}
.toolbar span {{ font-size:.8em; color:#6b5b45; }}
@media (max-width:900px) {{
  body {{ flex-direction:column; }}
  aside#sidebar {{ width:100%; min-width:0; height:auto; position:relative; }}
  .toolbar {{ left:0; }}
  main {{ padding:18px 14px 90px; }}
}}
</style>
</head>
<body>
<aside id="sidebar">
  <h1>La valigia d'Italia</h1>
  <div class="saga">Saga storica per ragazzi 9–12 · i 4 volumi completi di illustrazioni<br>© Il progetto La valigia d'Italia</div>
  {"".join(nav_links)}
</aside>
<main id="reader">
  {"".join(parts)}
</main>
<div class="toolbar">
  <button id="prevCh">← Capitolo precedente</button>
  <button id="nextCh">Capitolo successivo →</button>
  <span id="progress">Vol. 1 · cap. 1</span>
</div>
<script>
const vols = [...document.querySelectorAll('.volume')];
const volArts = Object.fromEntries(vols.map(v => [v.id, v]));
let currentVol = 'vol1';
let sections = [];
let secIdx = 0;
function refreshSections() {{
  sections = [...document.querySelectorAll(`#${{currentVol}} .chapter`)];
  secIdx = 0;
  updateProgress();
}}
function showVolume(vol) {{
  currentVol = vol;
  vols.forEach(v => v.classList.toggle('active', v.id === vol));
  document.querySelectorAll('.nav-vol').forEach(n => n.classList.toggle('open', n.dataset.vol === vol));
  refreshSections();
  window.scrollTo(0, 0);
}}
function updateProgress() {{
  const total = sections.length;
  const s = sections[secIdx];
  document.getElementById('progress').textContent =
    `${{currentVol.replace('vol','Vol. ')}} · sezione ${{secIdx + 1}}/${{total}} — ${{s ? s.querySelector('h2').textContent.split('—')[0].trim() : ''}}`;
}}
function go(delta) {{
  const order = ['vol1','vol2','vol3','vol4'];
  let i = secIdx + delta;
  if (i < 0) {{
    const vi = order.indexOf(currentVol);
    if (vi > 0) {{ showVolume(order[vi-1]); sections = [...document.querySelectorAll(`#${{currentVol}} .chapter`)]; secIdx = sections.length - 1; sections[secIdx].scrollIntoView({{behavior:'smooth'}}); updateProgress(); }}
    return;
  }}
  if (i >= sections.length) {{
    const vi = order.indexOf(currentVol);
    if (vi < order.length - 1) {{ showVolume(order[vi+1]); sections[0].scrollIntoView({{behavior:'smooth'}}); updateProgress(); }}
    return;
  }}
  secIdx = i;
  sections[secIdx].scrollIntoView({{behavior:'smooth'}});
  updateProgress();
}}
document.querySelectorAll('.nav-vol').forEach(n => {{
  n.querySelector('.nav-toggle').addEventListener('click', () => showVolume(n.dataset.vol));
  n.querySelectorAll('.nav-chapters a').forEach(a => {{
    a.addEventListener('click', e => {{
      e.preventDefault();
      const t = document.getElementById(a.dataset.target);
      secIdx = sections.indexOf(t);
      t.scrollIntoView({{behavior:'smooth'}});
      updateProgress();
    }});
  }});
}});
document.getElementById('prevCh').addEventListener('click', () => go(-1));
document.getElementById('nextCh').addEventListener('click', () => go(1));
document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight') go(1);
  if (e.key === 'ArrowLeft') go(-1);
}});
new IntersectionObserver(entries => {{
  entries.forEach(en => {{ if (en.isIntersecting) {{ secIdx = sections.indexOf(en.target); updateProgress(); }} }});
}}, {{ rootMargin: '-40% 0px -55% 0px' }}).observe && sections.forEach(() => {{}});
const obs = new IntersectionObserver(entries => {{
  entries.forEach(en => {{ if (en.isIntersecting) {{ secIdx = sections.indexOf(en.target); updateProgress(); }} }});
}}, {{ rootMargin: '-40% 0px -55% 0px' }});
sections.forEach(s => obs.observe(s));
showVolume('vol1');
</script>
</body>
</html>
"""
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"written: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
