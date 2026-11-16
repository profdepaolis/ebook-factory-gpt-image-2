#!/usr/bin/env python3
"""Rewrite selected text panels so the family guide follows the official brand philosophy."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "salento-per-famiglie/pages"


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def replace_panel(filename: str, page_number: int, title: str, subtitle: str, body: str, *, final_page: bool = False) -> None:
    source = PAGES / filename
    work = PAGES / ".philosophy_work"
    work.mkdir(exist_ok=True)
    target = work / filename
    # All selected pages use a photo header and a cream editorial panel below it.
    panel_bottom = 2365 if final_page else 2585
    command = [
        "convert", str(source),
        "-fill", "#fffdf6", "-stroke", "#c89e4b", "-strokewidth", "2",
        "-draw", f"roundrectangle 110,1420 1690,{panel_bottom} 18,18",
        "-gravity", "North", "-font", "DejaVu-Serif", "-stroke", "none",
        "-fill", "#182b3f", "-pointsize", "48", "-annotate", "+0+1515", title,
        "-pointsize", "32", "-annotate", "+0+1600", subtitle,
        "-fill", "#263b35", "-font", "DejaVu-Sans", "-pointsize", "27",
        "-interline-spacing", "8", "-annotate", "+0+1730", body,
    ]
    # Keep the original page number already present outside the editorial panel.
    command += ["-strip", "-quality", "88", str(target)]
    run(*command)
    target.replace(source)


def main() -> None:
    replace_panel(
        "page_003_benvenuti_in_famiglia.jpg", 3,
        "BENVENUTI IN FAMIGLIA",
        "Orientarsi è il primo modo per sentirsi a casa",
        "Dare il benvenuto significa aiutarti a orientarti\ne farti venire voglia di conoscere il posto in cui sei.\nIn famiglia vuol dire trovare una spiaggia, una piazza\no un sentiero che faccia stare bene tutti.\n\nQuesta guida unisce idee pratiche e storie del territorio:\ncosta, paesi, sapori e persone.\nSeguite la curiosità, rispettate i luoghi\ne lasciate spazio alle pause.",
    )
    replace_panel(
        "page_011_borghi_da_esplorare.jpg", 11,
        "BORGHI DA ESPLORARE CON CALMA",
        "Anche un piccolo paese ha qualcosa da raccontare",
        "Cercate piazze, botteghe, feste e persone\nche tengono vivo il paese.\nInformatevi sulle iniziative locali e lasciate\nche siano i bambini a fare una domanda.\n\nIl Salento è anche entroterra: distribuire le visite\nsignifica conoscere più luoghi e rispettare\ni ritmi di chi li abita.",
    )
    replace_panel(
        "page_014_sapori_da_provare.jpg", 14,
        "SAPORI DA PROVARE",
        "Il territorio si conosce anche a tavola",
        "Dietro ogni piatto ci sono ingredienti, gesti\ne persone che custodiscono una tradizione.\n\nFRISELLA  Croccante e semplice da condire insieme.\nORECCHIETTE  Un formato da scoprire anche con gli occhi.\nPITTULE  Piccole frittelle da condividere.\nPASTICCIOTTO  Una merenda dolce da gustare con calma.\n\nIn caso di allergie, chiedete sempre gli ingredienti.",
    )
    replace_panel(
        "page_023_contatti_informazioni.jpg", 23,
        "CONTATTI E INFORMAZIONI UTILI",
        "Il sito per orientarsi prima e durante il viaggio",
        "Per sapere che cosa succede nei paesi vicini,\ncercare un'iniziativa o organizzare la giornata,\nconsulta le informazioni aggiornate sul sito.\n\nVerifica sempre orari, accessibilità, prenotazioni\ne condizioni del mare prima di partire.\n\nSITO UFFICIALE\nbenvenutiinsalento.it",
    )
    replace_panel(
        "page_024_a_presto_salento.jpg", 24,
        "A PRESTO, SALENTO",
        "Una guida per guardarsi intorno",
        "Che tu stia organizzando una vacanza\no cercando un'idea per il fine settimana,\nsperiamo di averti dato informazioni utili\ne una buona ragione per guardarti intorno.\n\nIl Salento vive tutto l'anno:\ncosta, piccoli paesi, iniziative,\nartigiani e storie di chi lo abita.\n\nAlla prossima avventura.",
        final_page=True,
    )
    work = PAGES / ".philosophy_work"
    work.rmdir()
    print("Updated five family-guide pages with the official Benvenuti in Salento philosophy.")


if __name__ == "__main__":
    main()
