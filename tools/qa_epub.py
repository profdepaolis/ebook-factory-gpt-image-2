#!/usr/bin/env python3
"""QA strutturale leggero per gli EPUB della saga (senza Java/epubcheck).
Uso: .venv/bin/python tools/qa_epub.py <file.epub> ...
Controlla: mimetype, container.xml, well-formedness XML, riferimenti interni,
duplicati, spine/nav, metadati Dublin Core, immagini referenziate."""
import sys, zipfile, re, posixpath, posixpath as pp
import xml.etree.ElementTree as ET

NS = {
    'container': 'urn:oasis:names:tc:opendocument:xmlns:container',
    'opf': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'epub': 'http://www.idpf.org/2007/ops',
}

def qa(path):
    errs, warns = [], []
    print(f'=== {path} ===')
    try:
        z = zipfile.ZipFile(path)
    except Exception as e:
        return [f'zip non valido: {e}'], []

    names = z.namelist()
    # 1. mimetype primo e corretto
    if names[0] != 'mimetype':
        errs.append(f'mimetype non è la prima voce (trovato: {names[0]})')
    else:
        mt = z.read('mimetype').decode('utf-8', 'replace')
        if mt != 'application/epub+zip':
            errs.append(f'mimetype errato: {mt!r}')
    # 2. duplicati (case-insensitive, come richiesto dagli EPUB)
    from collections import Counter
    dup = {n: c for n, c in Counter(n.lower() for n in names).items() if c > 1}
    if dup:
        errs.append(f'file duplicati (ci): {list(dup)}')
    # 3. container.xml
    try:
        root = ET.fromstring(z.read('META-INF/container.xml'))
        rf = root.find('.//container:rootfile', NS)
        rootfile = rf.attrib['full-path']
    except Exception as e:
        errs.append(f'container.xml non valido: {e}')
        rootfile = None
    # 4. well-formedness di opf/xhtml/ncx
    xml_exts = ('.opf', '.xhtml', '.ncx', '.xml')
    for n in names:
        if n.lower().endswith(xml_exts):
            try:
                ET.fromstring(z.read(n))
            except Exception as e:
                errs.append(f'XML non valido in {n}: {e}')
    if not rootfile:
        print(f'  errori: {len(errs)}, avvisi: {len(warns)}')
        return errs, warns
    base = pp.dirname(rootfile)
    opf_root = ET.fromstring(z.read(rootfile))
    opf_dir = (base + '/') if base else ''
    # 5. spine + manifest
    manifest = {item.attrib['id']: item for item in opf_root.findall('.//opf:manifest/opf:item', NS)}
    spine = [itemref.attrib['idref'] for itemref in opf_root.findall('.//opf:spine/opf:itemref', NS)]
    missing_in_manifest = [idref for idref in spine if idref not in manifest]
    if missing_in_manifest:
        errs.append(f'spine referenzia id assenti dal manifest: {missing_in_manifest}')
    # file del manifest che non esistono nello zip
    for id_, item in manifest.items():
        href = item.attrib['href']
        target = pp.normpath(pp.join(opf_dir, href))
        if target not in names:
            errs.append(f'manifest: file mancante {target} (id={id_})')
    # 6. riferimenti interni negli xhtml (src/href relativi)
    href_re = re.compile(rb'(?:src|href)\s*=\s*["\']([^"\'#]+)["\']', re.I)
    for n in names:
        if n.lower().endswith('.xhtml'):
            for m in href_re.finditer(z.read(n)):
                ref = m.group(1).decode('utf-8', 'replace')
                if ref.startswith(('http://', 'https://', 'mailto:', 'data:', 'epub:')):
                    continue
                target = pp.normpath(pp.join(pp.dirname(n), ref))
                if target not in names:
                    errs.append(f'xhtml {n}: riferimento rotto → {ref}')
    # 7. metadati obbligatori
    metas = opf_root.findall('.//opf:metadata/*', NS)
    have_title = any(m.tag.endswith('title') and (m.text or '').strip() for m in metas)
    have_lang = any(m.tag.endswith('language') for m in metas)
    have_id = any(m.tag.endswith('identifier') for m in metas)
    for ok, label in [(have_title, 'dc:title'), (have_lang, 'dc:language'), (have_id, 'dc:identifier')]:
        if not ok:
            errs.append(f'metadato mancante: {label}')
    # 8. nav document (EPUB3)
    has_nav = any('nav' in (item.attrib.get('properties') or '') for item in manifest.values())
    if not has_nav:
        warns.append('nessun nav document (EPUB 3 richiede properties="nav")')
    # 9. immagini effettivamente referenziate
    imgs = [n for n in names if n.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg'))]
    referenced = set()
    for n in names:
        if n.lower().endswith('.xhtml'):
            for m in href_re.finditer(z.read(n)):
                ref = m.group(1).decode('utf-8', 'replace')
                if ref.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
                    referenced.add(pp.normpath(pp.join(pp.dirname(n), ref)))
    unref = [n for n in imgs if n not in referenced]
    if unref:
        warns.append(f'immagini non referenziate: {unref}')

    print(f'  voci: {len(names)} | spine: {len(spine)} | immagini: {len(imgs)} | errori: {len(errs)} | avvisi: {len(warns)}')
    for e in errs:
        print(f'  ✗ {e}')
    for w in warns:
        print(f'  ! {w}')
    return errs, warns

total_errs = 0
for p in sys.argv[1:]:
    e, _ = qa(p)
    total_errs += len(e)
print()
print('ESITO:', 'TUTTO OK' if total_errs == 0 else f'{total_errs} ERRORI TROVATI')
sys.exit(1 if total_errs else 0)
