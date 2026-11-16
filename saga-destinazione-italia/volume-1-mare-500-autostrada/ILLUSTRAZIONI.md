# Vol. 1 «Mare, 500 e autostrada» — Piano illustrazioni

**Formato:** ibrido (testo reale + illustrazioni AI). Pagine KDP 6×9" (2480×3368 px @300dpi).
**Stile unico della saga:** gouache + acquerello su carta ruvida, colori caldi, texture visibile, personaggi espressivi e tondeggianti, niente fotorealismo, niente testo nelle immagini (il testo è nel layout), full-bleed sulle scene chiave.

## Style anchor (identico in ogni prompt)
```
Gouache and watercolor children's book illustration, warm saturated palette
(cadmium yellow, coral red, teal, deep brown), visible paper texture,
confident brushstrokes, rounded expressive characters with big friendly eyes,
1960s Italy mood, soft natural light, full-page book illustration,
no text, no logos, no watermark, storybook quality
```

## Character sheet da generare PRIMA (GPT Image 2, riferimento)

1. **Marco** — 10 anni, capelli neri a spazzola, maglietta a righe bianche e blu navy, pantaloncini scuri, scarpe di tela bianche. 3/4 e profilo.
2. **Oreste** — 28 anni, operaio, baffi castani, camicia azzurra, gilet grigio, pettinato all'indietro. 3/4 e profilo.
3. **Lina** — 26 anni, capelli biondi raccolti in treccia, grembiule a fiori sopra gonna beige.
4. **Valigia di cuoio** — marrone tabacco, angoli ammaccati, fibbia di ottone, etichetta cartone "MORELLI — MILANO", cinghia di cuoio intrecciato. Multi-angolo.

## Le 12 illustrazioni

| # | Scena (capitolo) | Tipo | Spunto di prompt (oltre allo style anchor) |
|---|---|---|---|
| 1 | **Copertina** | full-bleed | Fiat 500 bianca in corsa sull'Autostrada del Sole vista dal davanti, valigia di cuoio sul tetto, sole enorme all'orizzonte, insegna "Rimini" in lontananza (testo SOLO titolo nel layout, non nell'immagine) |
| 2 | La Breda che chiude (cap. 1) | mezza pagina | Cancello di una grande fabbrica milanese aperto, operai in tuta blu che escono in bicicletta, sole d'agosto |
| 3 | Il mercato della valigia (cap. 2) | mezza pagina | Marco che indica una valigia di cuoio usata al mercato, bancarelle colorate |
| 4 | La partenza (cap. 3) | full-bleed | Cinquecento bianca vista da dietro, valigia e borse sul portapacchi, Corso Buenos Aires all'alba |
| 5 | Il casello (cap. 4) | mezza pagina | Casello autostradale 1964, sbarra bianco-rossa, un operaio fa segno di passare, sole alto |
| 6 | L'autogrill (cap. 5) | mezza pagina | Interno autogrill Pavesi, famiglie ai tavolini, bambini vedono gelati, giornali sul bancone |
| 7 | L'Emilia dal finestrino (cap. 6) | mezza pagina | Panorama Pianura Padana dall'auto in corsa: campi, pioppi, camion, treno in lontananza |
| 8 | L'arrivo a Rimini (cap. 7) | full-bleed | Spiaggia adriatica vista dall'alto, ombrelloni colorati, mare azzurro, la famiglia che scende dall'auto |
| 9 | Dieter e la foto (cap. 8) | mezza pagina | Marco e Dieter (bimbo biondo) seduti sulla sabbia con secchielli e torretta di sabbia, macchina fotografica Agfa al collo |
| 10 | La festa in spiaggia (cap. 9) | full-bleed | Serata di Ferragosto, rotonda illuminata, gente che balla, sole che tramonta sul mare |
| 11 | La cartolina (cap. 10) | mezza pagina | Primo piano: mani di Marco che scrive su una cartolina e la infila nella cassetta rossa |
| 12 | La radio del 4 ottobre (cap. 11–12) | mezza pagina | Oreste e Marco davanti alla radio in cucina, la mamma con le mani sul viso, luce calda |

**Mappe (2):** disegnare in vettoriale (non generare): (a) Milano→Rimini; (b) mappa saga Milano→Napoli.
**Spese stimate:** 12 immagini GPT Image 2 + 3 character sheet = 15 generazioni; ~3 prompt-iteration per immagine.

---

## Stato generazione (aggiornato 2026-11-16)

Generati (GPT Image 2, `assets/`):

- ✅ `ref_marco.jpg`, `ref_oreste.jpg`, `ref_lina.jpg`, `ref_valigia.jpg` — character/prop sheet approvati visivamente (coerenti tra loro).
- ✅ `illus_01_cover.jpg` — copertina (Fiat 500 al tramonto)
- ✅ `illus_02_breda.jpg` — cap. 1 Le città si svuotano
- ✅ `illus_03_valigia.jpg` — cap. 2 La valigia di cuoio
- ✅ `illus_04_partenza.jpg` — cap. 3 La partenza
- ✅ `illus_05_casello.jpg` — cap. 4 Il casello
- ✅ `illus_06_autogrill.jpg` — cap. 5 L'autogrill

⏳ Da generare al prossimo turno (limite turno: 10 immagini):

- `illus_07_pianura.jpg` — cap. 6 L'Italia si accorcia (Po valley dal finestrino)
- `illus_08_rimini.jpg` — cap. 7 Rimini, finalmente! (costa adriatica)
- `illus_09_dieter.jpg` — cap. 8 L'amico tedesco (Dieter e la foto Agfa)
- `illus_10_festa.jpg` — cap. 9 La rotonda sul mare (Ferragosto)
- `illus_11_cartolina.jpg` — cap. 10 La cartolina
- `illus_12_radio.jpg` — cap. 11–12 (la radio del 4 ottobre)

Note: le reference sheet (`ref_*.jpg`) non entrano nell'EPUB; servono solo come riferimento visivo per la coerenza delle scene.
