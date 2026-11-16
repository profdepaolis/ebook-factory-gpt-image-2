# 📚 La Valigia d'Italia
## La storia del turismo italiano dal Boom economico a oggi — raccontata da quattro generazioni di una famiglia

**Saga per ragazzi 9–12 anni · 4 volumi · italiano · ibrido testo + illustrazioni**

---

## 1. Il concept in una frase

Una sola famiglia, i **Morelli**, quattro generazioni, quattro estati in quattro Italie diverse: dalla Fiat 500 del 1964 all'overtourism di Venezia, per scoprire come gli italiani — e i turisti di tutto il mondo — hanno imparato a viaggiare.

**Sottotitolo della saga:** *La storia del turismo italiano raccontata dalla famiglia Morelli*

**Tagline:** «Quattro generazioni, una valigia, mille viaggi.»

---

## 2. Perché questa saga ha senso

- **Nessuna proposta in Italia** racconta ai ragazzi la storia del turismo: un tema quotidiano (tutti vanno in vacanza!) diventato racconto storico, sociale e umano.
- **Il turismo è una macchina del tempo perfetta per la scuola**: economia, geografia, storia, musica, pubblicità, tecnologia, sostenibilità — tutto passa dalle vacanze.
- Il formato **saga multigenerazionale** crea un legame emotivo forte: il nonno di un volume è il protagonista del primo. I ragazzi vedono i "grandi" da piccoli.
- **Strumento editoriale + scolastico**: i quattro volumi possono funzionare in autonomia, come saga, o come percorso di educazione civica/storia/geografia per la scuola primaria e secondaria di I grado.
- **Filo conduttore narrativo**: la *valigia di cuoio* del giovane Oreste, passata di mano in mano, con dentro il *diario di bordo* che ogni generazione firma. Alla fine Lea (volume 4) capisce una cosa semplice: viaggiare è un dono, e come tutti i doni va usato con cura.

---

## 3. Target, tono e livello di lettura

| Aspetto | Scelta |
|---|---|
| Età | 9–12 anni (4ª primaria – 1ª secondaria I grado) |
| Lunghezza per volume | 110–128 pagine · 6.000–7.500 parole · lettura 45–75 min |
| Tono | Avventura quotidiana, calda, ironica, mai didascalica |
| Struttura narrativa | Ogni volume = una "quest": la vacanza come missione |
| Difficoltà | Frasario semplice, ma lessico storico reale spiegato in box |
| Apparati in ogni volume | "Lo sai che…?", "Parole d'epoca", "La linea del tempo", "Mappa del viaggio", "La storia vera dietro la storia" (per genitori/insegnanti) |
| Pedagogia | Storia vera intrecciata alla finzione; fatti verificati con fonti (§9) |

**Regola d'oro:** i fatti storici sono veri; i personaggi sono inventati. Nessun personaggio reale appare in scena, ma ogni volume cita luoghi, leggi, oggetti e notizie reali e verificabili.

---

## 4. Decisione di formato (e perché)

**Scelta: formato ibrido — testo vero impaginato + illustrazioni AI, non "full-image".**

- Il repo `ebook-factory-gpt-image-2` produce libri in cui *ogni pagina è un'immagine* generata dall'AI. Quel formato è ideale per picture book (0–8 anni) e cookbook.
- Per ragazzi **9–12**, che leggono densità e continuità di testo, e per un tema storico con **tanti nomi, date e termini**, il full-image rende illeggibile il testo (limossi di OCR, errori tipografici, accessibilità) e non è cercabile/iperTestualizzabile.
- **Formato scelto:** KDP **6×9"**, testo reale (Georgia/Carattere chiaro con supporto didattico), illustrazioni **full-bleed in gouache/acquerello analogico-digitale** a piena pagina o mezza pagina, copertina lucida. Versione **ebook reflowable** + **print**.
- Le illustrazioni si generano con il pipeline del repo (GPT Image 2), con foglio di coerenza per i personaggi (§8). Il full-image resta proponibile per una futura **edizione deluxe ridotta** (32 pagine illustrate) di ciascun titolo.

**Conclusione pratica:** cambia il "motore di assemblaggio" (testo + immagini invece di sole immagini), non cambia il motore creativo (GPT Image 2 per le illustrazioni).

---

## 5. I personaggi della famiglia Morelli

### Scheda multigenerazionale (costante per tutta la saga)

| Personaggio | Ruolo | Volumi | Biografia |
|---|---|---|---|
| **Oreste Morelli** | Operaio alla Breda di Sesto San Giovanni, poi pensionato | V1 (28 anni), V3 (64), V4 (90) | Sogna Rimini dall'infanzia. Compra la valigia di cuoio nel 1964; la porterà con sé per 60 anni. |
| **Lina** | Moglie di Oreste, sarta | V1 (26) | Organizza l'economia domestica; prepara il pranzo al sacco "per due giorni". |
| **Marco** | Figlio di Oreste e Lina | V1 (10), V2 (25), V3 (46), V4 (—) | Protagonista del V1. Adulto nel V2 fa il ragioniere. Appassionato di macchine e musica. |
| **Piera** | Moglie di Marco | V2 | Insegnante elementare; organizza le vacanze "intelligenti". |
| **Sara** | Figlia di Marco e Piera | V2 (10), V3 (31) | Protagonista del V2. Nel V3 ha Niccolò. |
| **Niccolò** | Figlio di Sara | V3 (10), V4 (36) | Protagonista del V3. In V4 accompagna sua figlia Lea. |
| **Viola** | Moglie di Niccolò | V4 | Bibliotecaria; cerca "la vacanza giusta" che non consumi i luoghi. |
| **Lea** | Figlia di Niccolò e Viola | V4 (11) | Protagonista del V4. Cresce con Google, Airbnb e la coscienza ambientale. |

### L'oggetto-filo rosso: la valigia di cuoio

- **V1:** Oreste la compra usata al mercato di Porta Venezia con la prima mensilità intera: costa 2.400 lire (lo spiega in un box). La riempie di panini, thermos e un paio di scarpe di ricambio.
- **V2:** Marco la eredita: dentro c'è ancora il biglietto del pedaggio del primo viaggio. Sara ci infila una mini-radio.
- **V3:** Sara la passa a Niccolò; dentro ci sono tre cartoline: Rimini 1964, Palinuro 1979, e una mai spedita.
- **V4:** Niccolò la passa a Lea; dentro, tutte le cartoline + il diario di bordo che ospiterà **la sua** pagina. Chiude la saga con la scritta: *"La valigia più bella non è quella che pesa di più. È quella che torna a casa piena di storie."*

---

## 6. Il piano editoriale dei 4 volumi

### VOLUME 1 — «Mare, 500 e autostrada»
**Anno:** estate 1964 · **Protagonista:** Marco (10) · **Luogo:** Milano → Rimini (prima vacanza al mare in assoluto della famiglia) · **Mappa:** Milano → Parma → Bologna → riviera romagnola

**Trama:** Le città si svuotano per ferie, la Breda chiude per tre settimane e la famiglia Morelli carica la Fiat 500 (comprata con un anno di rate) e la valigia di cuoio. Marco, che non ha mai visto il mare, scopre le code in autostrada, il primo Autogrill della storia, Rimini, i tedeschi in vacanza in Italia, la rotonda di "Una rotonda sul mare" (Fred Bongusto, estate 1964), le grida dei venditori di sdraio. Torna a Milano con il diario: *«Mamma dice che l'Italia è lunga. Io dico che è corta, se la percorri in 500».*

**Cap. per cap.:**
1. Le città si svuotano (l'esodo, la chiusura delle fabbriche ad agosto)
2. La valigia di cuoio (mercato di Porta Venezia, il prezzo, il carico)
3. La partenza (valige sul portapacchi, panini, nessun bambino nel sedile anteriore)
4. Il casello (la prima volta che Marco vede l'Autostrada del Sole)
5. L'autogrill (il primo Autogrill Pavesi del 1959; il papà paga col portafoglio Gonzo)
6. L'Italia si accorcia (i km, i paesi che sfilano, la radio: "manca un ultimo tratto…")
7. **Rimini, finalmente!** (pensione "La Sirena", ombrellone, sdraio, primo bagno)
8. L'amico tedesco (un ragazzo di Monaco con la macchina fotografica "Agfa")
9. La rotonda sul mare (la radio all'UNA e mezza, la canzone dell'estate)
10. La cartolina (Marco scrive e sbaglia francobollo; la mamma ride)
11. Ritorno (la radio annuncia: il 4 ottobre 1964 l'Autostrada del Sole sarà completata)
12. L'ultima pagina del diario (la valigia torna sul ripostiglio)

**Apparati:** Sai che…? ×6 · Parole d'epoca: villeggiatura · casello · autogrill · sdraio · ombrellone · suddetto · Autostrada del Sole · linea del tempo 1955–1965 · scheda storica per adulti.

**Illustr.:** 12 (copertina + 11 scene chiave) — vedi `volume-1-mare-500-autostrada/ILLUSTRAZIONI.md`.

---

### VOLUME 2 — «Tutto compreso!»
**Anno:** estate 1979 · **Protagonista:** Sara (10) · **Luogo:** Milano → villaggio turistico "La Baia del Sole", Costa del Cilento (vicino a Palinuro) · **Mappa:** Milano → Firenze → Roma → Cilento (SS 18 Tirrenica)

**Trama:** Sara ha vinto un concorso di nuoto e in premio la famiglia va nel villaggio "tutto compreso": pensione, pasti, animazione, mini-club. Marco (il papà del V1, qui adulto e ragioniere) non sopporta l'animatore. Il walkman (Sony TPS-L2, 1979) fa furore tra gli adolescenti. Il papà spiega a Sara la crisi petrolifera: la benzina costa, si viaggia "con la testa", i treni sono pieni. Sara capisce che il villaggio è bello ma la "vera vacanza" è il Cilento fuori dal cancello: Palinuro, i templi di Paestum, il pescatore. C'è un momento di conflitto: il villaggio sta comprando la spiaggia accanto dove i pescatori tirano su le reti. Sara trova un compromesso: la famiglia conosce i pescatori, Sara disegna sulla valigia di cuoio la baia e scrive sul diario: *«La vacanza perfetta è quella che rispetta chi ci abita»*.

**Cap. per cap.:**
1. Il concorso di nuoto e il biglietto in premio
2. Il pullman del villaggio (maxi-bagagli, bambini in pigiama)
3. La reception e i bracciali colorati (tutto compreso: la parola magica)
4. Il mini-club e l'animatore Vito (balli, giochi, trucchi di magia)
5. Il walkman (Sony TPS-L2, 1979)
6. La crisi del petrolio (la benzina sale; cosa succede al mondo)
7. Palinuro fuori dal villaggio (la Punta, le grotte, il pescatore Salvatore)
8. Paestum (i templi; Sara immagina i Greci in vacanza)
9. La spiaggia dei pescatori (il conflitto: il villaggio vuole allargarsi)
10. La festa del villaggio e la serenata (Carosello è finito nel 1977: la pubblicità è in TV libera)
11. Il compromesso (firma simbolica; la famiglia saluta i pescatori)
12. La cartolina numero due (la valigia si apre: dentro, una cartolina del 1964)

**Apparati:** Sai che…? ×6 (crisi petrolifera '73 e '79 · Carosello 1957–1977 · Valtur 1964 e Cefalù 1957 · walkman 1979 · mini-club Club Med 1967 · TV libere 1976) · Parole d'epoca: villaggio · animatore · tutto compreso · walkman · jeans a zampa · prefisso (prefisso telefonico!) · linea del tempo 1964–1985.

**Illustr.:** 12.

---

### VOLUME 3 — «Agriturismo e Giubileo»
**Anno:** estate 2000 · **Protagonista:** Niccolò (10) · **Luogo:** Milano → agriturismo "La Quercia", Mugello (Toscana) → Roma (Giubileo) · **Mappa:** Milano → Firenze → Mugello → Roma

**Trama:** Seconda estate della famiglia in agriturismo. La Legge 730/1985 (agriturismo, 5 dicembre 1985) ha cambiato la campagna italiana: contadini che ospitano turisti. Niccolò conosce le mucche, la ricotta, il pane del forno. Il nonno Oreste (64) racconta la sua prima vacanza in 500. A metà vacanza il nonno vuole vedere Roma per il **Giubileo 2000**: 25 milioni di pellegrini, secondo le stime. La famiglia prende il treno; Roma è piena, cori, giubileo, cantieri, mostre. Niccolò compra una cartolina speciale con il 2000 e pensa agli euro che arriveranno (la moneta unica entra nel 2002). Alla fine regala alla valigia la **terza cartolina**: Roma 2000.

**Cap. per cap.:**
1. La busta con le foto nuove (l'agriturismo: la casa del contadino-ospite)
2. La mucca Stella e il giro in aia
3. Il forno a legna e la ricotta (la mamma Sara impara)
4. Il nonno Oreste racconta (viaggio 1964, la valigia, la Breda)
5. Computer e posta Internet (il bar "La Quercia" ha un PC con Internet: Niccolò scrive alla nonna)
6. Il panino con la merenda del contadino (nonno spiega le tasse agricole e perché l'agriturismo salva le campagne)
7. Deviazione per Roma (il nonno vuole vedere il Giubileo)
8. Roma piena (25 milioni di pellegrini: file ai musei, preghiera in piazza San Pietro)
9. La cartolina speciale (la freccia di San Pietro; il 2000)
10. Telefonare dall'agriturismo (la scheda telefonica; il call center non c'era)
11. Ritorno alla Quercia (le mucche; il diario; la terza cartolina)
12. Le lire che vanno via (nonno spiega: arriverà l'euro, 2002)

**Apparati:** Sai che…? ×6 (L. 730/1985 agriturismo · L. 217/1983 turismo · Giubileo 2000 25 mln pellegrini · Italia '90 Mondiali · Internet in Italia, Booking 1996, TripAdvisor 2000 · lire→euro 1/1/2002) · Parole d'epoca: call center · poster · cartolina · euro · "navigare" in Internet · agriturismo · linea del tempo 1985–2002.

**Illustr.:** 12.

---

### VOLUME 4 — «Selfie a Venezia»
**Anno:** estate 2026 · **Protagonista:** Lea (11) · **Luogo:** Milano → Venezia (con contributo di accesso) → Roma (dopo il Giubileo 2025) · **Mappa:** Milano → Venezia → Firenze → Roma

**Trama:** Il mondo è pieno di turisti: l'Italia nel 2024 ha toccato **139,6 milioni di arrivi** e **466,2 milioni di presenze** (Istat), secondo Paese in Ue dopo la Spagna. Lea prenota con un'app: Frecciarossa, Airbnb vicino a Piazzale Roma, biglietto del **contributo di accesso a Venezia** (in vigore dal 2024: 5 € se prenoti in tempo, 10 € se aspetti). Venezia è bellissima e piena, piena, piena: selfie-stick, gondolas finte in cartone, steward, il "turismo mordi e fuggi". Lea intervista un veneziano (l'affittacamere Lorenzo) che le mostra la Venezia dei veneziani: il caffè di Cannaregio, i gatti sui tetti. Poi Lea e la famiglia scendono a Roma, da poco uscita dal Giubileo 2025: i cantieri delle mura, la basilica San Pietro, il Colosseo con tetto giornaliero. A casa, Lea scrive sul diario della valigia l'ultima pagina: *«Il turismo non è male. Il turismo è un dono. I doni vanno aperti con delicatezza.»* La valigia si chiude; nonno Oreste (90) la guarda e dice: "È tornata".

**Cap. per cap.:**
1. 139 milioni di arrivi (una cifra che non ci sta nella testa)
2. Il treno Frecciarossa (Milano–Venezia in 2h24)
3. L'app e il contributo di accesso (5 € o 10 €: la città si prenota)
4. Venezia mordi e fuggi (selfie-stick, maschere a 1 euro, coda ai vaporetti)
5. La Venezia dei veneziani (Cannaregio; Lorenzo affittacamere; i gatti)
6. La basilica e il silenzio (San Marco; il significato del turismo rispettoso)
7. Airbnb e chi ci abita (le case che diventano hotel; cosa ne pensano i residenti)
8. Treno per Roma (Frecciarossa; due Italie che si guardano dal finestrino)
9. Il Colosseo con tetto giornaliero (la febbre dei numeri: come gestire l'overtourism)
10. Giubileo 2025 appena finito (cantieri; la città che si rifa il trucco)
11. L'ultima cartolina (Lea scrive il suo nome nella valigia)
12. La valigia torna (nonno Oreste sorride; la saga si chiude)

**Apparati:** Sai che…? ×6 (Istat 2024: 139,6M arrivi / 466,2M presenze · Italia 2ª in UE, superata solo dalla Spagna · Venezia 2024 prima al mondo con il contributo di accesso; 54 giornate nel 2025 · Frecciarossa 2008 · Booking 1996 · Airbnb 2008 · COVID-19 2020–22: turismo fermo, poi record) · Parole d'epoca: overtourism · contributo di accesso · selfie · Airbnb · sostenibilità · lavoro agile/workation · linea del tempo 2002–2026.

**Illustr.:** 12.

---

## 7. Apparati fissi in ogni volume (la "scuola nella valigia")

1. **"Lo sai che…?"** — 6 box storici verificati (vedi §9 fonti).
2. **"Parole d'epoca"** — 6-8 termini: significato + frase del libro.
3. **"Linea del tempo"** — 6-8 date chiave dell'epoca.
4. **"Mappa del viaggio"** — disegnata a tratto, con le tappe numerate.
5. **"La storia vera dietro la storia"** (per genitori/insegnanti) — 1 pagina: fonti, contesto, spunti per il dibattito in classe (es. *"Il turismo di massa è sempre positivo?"*).
6. **"L'ultima pagina del diario"** — il testo che il protagonista scrive sulla valigia (leggibile con grafia infantile nell'illustrazione o con font corsivo nel testo reale).

**Spunti di lavoro per la scuola (appendice comune):** interviste ai nonni ("Come viaggiavi?"), raccolta di cartoline vere, linea del tempo personale, dibattito: *turismo = ricchezza o stress?*, geografia: le 10 mete più visitate d'Italia, matematica: 139,6 milioni di arrivi divisi per 60 milioni di italiani = quanti viaggi a testa?

---

## 8. Illustrator brief (per GPT Image 2)

**Stile unico della saga:** gouache + acquerello su carta ruvida, colori caldi e saturi, campiture decise, texture visibile, personaggi tondeggianti e espressivi (naso largo, occhi grandi), niente fotorealismo. Coerente con libri KDP 6×9".

**Personaggi da fissare PRIMA della produzione (character sheet):**
- Marco (V1): capelli neri a spazzola, maglietta a righe bianca-blu, pantaloncini scuri, scarpe di tela.
- Oreste (V1 giovane / V3 adulto / V4 vecchio): operaio, baffi, camicia chiara; V3: occhiali da lettura argentati; V4: cappello di paglia, giacca marrone.
- Lina: treccia bionda, grembiule; Piera: capelli corti castani, foulard; Sara (V2): due codini, maglietta gialla; (V3 adulta): capelli lunghi, zaino di tela; Niccolò (V3): occhiali, capelli ricci; (V4 adulto): barba corta, maglione verde; Lea (V4): coda di cavallo castana, zaino con pins.
- La **valigia di cuoio**: marrone tabacco, etichetta di cartone "Morelli – Milano", angoli ammaccati, cinghia nera con fibbia di ottone. RICORRENTE in ogni volume.

**Processo:** character sheet per ciascun protagonista + valigia → 2-3 pagine test (copertina + 1 scena) → approvazione → 10-11 illustrazioni per volume → impaginazione → EPUB/PDF.

**Diritti:** solo immagini AI originali + mappe disegnate vettorialmente. Nessuna fotografia di repertorio di terzi senza licenza esplicita; eventuali foto d'epoca solo da fonti in pubblico dominio (es. archivi nazionali) con didascalia "Fonte: …, pubblico dominio".

---

## 9. Fonti storiche verificate (per gli apparati e le schede)

1. **Esodo estivo / vacanze di massa** — Università di Torino, *«Quando agosto era di tutti: l'Italia che chiudeva per ferie»* (interv. a E. Locci): 1959 solo il 13% degli italiani andava in vacanza; inizio anni '60 21%; anni '80 ≈43% (Istat). https://www.otto.unito.it/it/articoli/quando-agosto-era-di-tutti-litalia-che-chiudeva-ferie
2. **Triplicano le presenze 1956–1965** — @UniTE, *L'Italia del boom* (PDF IUSO): tra 1956 e 1965 triplicano le presenze turistiche legate alle vacanze; 1958: 1 famiglia su 10 ha la TV, 1965: 1 su 2; Modugno, "Nel blu dipinto di blu" 1958. https://www.unite.it/UniTE/Engine/RAServeFile.php/f/File_Prof/IUSO_592/sospirato_trauma_della_modernita__prima_parte.pdf
3. **Architetture del turismo di massa** — Atlante Architettura Contemporanea (MiC): turismo balneare come industria della Riviera romagnola; 100+ opere moderniste 1948–1970. https://atlantearchitetturacontemporanea.cultura.gov.it/en/category/l-italia-va-in-vacanza/
4. **Autostrada del Sole (A1)** — posa prima pietra 19/5/1956; Milano–Parma 8/12/1958; Bologna–Firenze 3/12/1960; Roma–Napoli 22/9/1962; **completata 4/10/1964** (Aldo Moro); ~760 km, 6 regioni, 15M giornate lavorative; Milano–Napoli ≈ 2 giorni prima del 1964 → 7-8h dopo. https://www.benzina24.it/approfondimenti/autostrada-a1-l-autostrada-del-sole-storia-costruzione-e-impatto-sull-italia-del/ (cronologia confermata anche da ANAS e Ministero Infrastrutture)
5. **Costa Smeralda** — Consorzio Costa Smeralda fondato il 14/3/1962 dall'Aga Khan; Porto Cervo; Alisarda→Meridiana 1963; aeroporto Olbia 1969. https://www.consorziocostasmeralda.com/anniversario-consorzio-costa-smeralda-compie-59-anni/
6. **Club Med in Italia** — Club Med fondato 1950 da Blitz e Trigano; primo villaggio italiano Cefalù (1957); Mini Club 1967 a Donoratico; Palinuro inaugurato 1963; anni '70–'80 età d'oro; 1974 crisi e ingresso di Gianni Agnelli. https://scripomuseum.com/club-mediterranee ; https://www.villamirella.it/cilento/club-med-a-palinuro-storica-destinazione-vacanze-in-italia
7. **Valtur** — fondata a Roma nel 1964 (iniziativa privata; Ostuni e Capo Rizzuto primi villaggi). https://to-news.it/images/stories/ton55/valtur-winter25-con-intro.pdf
8. **Agriturismo** — primo riconoscimento normativo: Trentino 1973; L. 217/1983 art. 27 (legge-quadro turismo) prima citazione statale; **L. 5/12/1985 n. 730** prima legge-quadro agriturismo; L. 96/2006 l'abroga/rinnova. https://it.wikipedia.org/wiki/Turismo_rurale ; https://www.ilcittadinoonline.it/quicoldiretti/la-nascita-dellagriturismo-una-storia-lunga-mezzo-secolo/
9. **Giubileo 2000** — circa **25 milioni di pellegrini** a Roma (Censis). https://roma.repubblica.it/cronaca/2015/07/21/news/giubileo_roma_punta_su_car_sharing_elettrico_2500_auto-119522889/
10. **Italia 2024 (record)** — Istat, *I flussi turistici – Anno 2024*: **139,6M arrivi (+4,5%), 466,2M presenze (+4,2%)**, dato più alto mai rilevato; Italia **2ª in UE dopo la Spagna** e davanti alla Francia; presenze straniere al 54,5%; comuni marittimi 38% delle presenze; Roma, Milano e Venezia ai primi posti. https://www.istat.it/comunicato-stampa/i-flussi-turistici-anno-2024/
11. **Venezia e l'overtourism** — record 2024: 5,88M arrivi, **13,29M presenze** (supera il 2019); **contributo di accesso** dal 25/4/2024 (29 giornate 2024 → **54 giornate 2025**, 5 € in anticipo / 10 € in ritardo), prima città al mondo; 2026 terza edizione (fino al 26 luglio). https://www.ultimaoralive.it/2025/attualita/turismo-a-venezia-nel-2025-le-giornate-con-contributo-daccesso-salgono-a-54-ecco-quali-sono-e-quanto-si-paghera/ ; https://www.geopop.it/lingresso-a-venezia-torna-a-pagamento-come-funziona-il-contributo-di-accesso-e-chi-e-esente/
12. **COVID-19** — 2020–2022: crollo del turismo globale; 2023 record; 2024 oltre i livelli pre-pandemia (Istat).

*Nota editoriale:* per ogni "Lo sai che…?" del testo definitivo va allegato il riferimento bibliografico esatto in coda al volume (per la scuola). Dove un dato è uno stimato (es. 25 mln pellegrini), scriverlo con "secondo le stime".

---

## 10. Numeri di partenza e strategia (senza inventare dati di mercato)

- **Stampa KDP 6×9"**, copertina lucida, 110–128 pp, PB; **ebook reflowable** (Georgia 16pt, interlinea 1.5) + `print-ready PDF`.
- **Uscita scaglionata**: V1 in primavera, V2-V4 a distanza di 6–12 mesi (mantiene vivo il passaparola della saga).
- **Serie "Scuola nella valigia"**: spedito 1 copia V1 alle biblioteche scolastiche pilota; QR code sulla copertina → dossier fonti PDF gratuito (lead magnet per la newsletter dei docenti).
- **Prezzo indicativo**: €9,99–12,99 ebook/print (benchmark KDP ragazzi ITA: €6–15). Royalty KDP 60% ebook, ~40–50% print.
- **Distribuzione scolastica**: kit "Valigia in classe" (cartellina con mappa poster + linea del tempo + 20 schede didattiche) — licenza per classi, non per singola copia.
- **Nessun dato vendite è garantito**; la leva è la qualità narrativa + la coerenza educativa + il passaparola famiglie/scuole.

---

## 11. Titoli definitivi dei volumi

1. **La valigia d'Italia — 1. Mare, 500 e autostrada** (1964)
2. **La valigia d'Italia — 2. Tutto compreso!** (1979)
3. **La valigia d'Italia — 3. Agriturismo e Giubileo** (2000)
4. **La valigia d'Italia — 4. Selfie a Venezia** (2026)

---

## 12. Prossimi passi (roadmap di produzione)

1. ✅ **Scelta della saga e piano editoriale** — questo documento.
2. ✅ **Outline dei 4 volumi** — §6.
3. ✅ **Manoscritto completo Vol. 1** — `volume-1-mare-500-autostrada/MANOSCRITTO.md` (~4.700 parole + apparati; illustrazioni 12/12; EPUB reflowable generato).
4. ✅ **Manoscritto Vol. 2** — `volume-2-tutto-compreso/MANOSCRITTO.md` (~2.500 parole, prima stesura completa).
5. ✅ **Manoscritto Vol. 3** — `volume-3-agriturismo-giubileo/MANOSCRITTO.md` (~2.500 parole, prima stesura completa).
6. ✅ **Manoscritto Vol. 4** — `volume-4-selfie-a-venezia/MANOSCRITTO.md` (~2.100 parole, prima stesura completa).
7. ⏳ **Illustrazioni Vol. 2–4** (12 per volume) — al prossimo turno (limite 10 immagini/turno).
8. ⏳ **Editing finale tutti i volumi** (espansione a 4.500–7.000 parole, lettura di un adulto/esperto storico, normalizzazione grafica).
9. ⏳ **EPUB + PDF KDP dei Vol. 2–4** — una volta generate le illustrazioni.
10. ⏳ **Schede didattiche** (4 set × 20 schede) + dossier fonti PDF.

**Costo/tempo indicativo totale:** ~4 settimane per i 4 volumi (manoscritto + illustrazioni + KDP), con 1 voce umana di editing finale prima della pubblicazione (contenuti storici vanno rivisti da un medialab/insegnante).
