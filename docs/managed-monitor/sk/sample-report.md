# BotEffex Monitor — vstupný report

**ILUSTRAČNÁ UKÁŽKA · nejde o meranie skutočného chatbota ani zákaznícku referenciu**

Projekt: Modelové štúdio Javor (fiktívne)  
Rozsah ukážky: 5 otázok pre jeden textový chatbot  
Obdobie: jeden modelový vstupný beh  
Spracoval: Miloš Brisuda · BotEffex Monitor

## Čo si vyžaduje pozornosť

V tomto vymyslenom príklade tri kontroly splnili pravidlo a dve ho nesplnili. Chýba očakávaný kontakt a údaj o rozsahu služby. Nejde o hodnotenie celého chatbota. Výsledky iba ukazujú, ako bude report usporiadaný.

| Otázka | Dohodnuté pravidlo | Ukážka odpovede | Modelový výsledok |
|---|---|---|---|
| Ako vás môžem kontaktovať? | Musí obsahovať kontakt@javor.example | „Napíšte nám cez kontaktný formulár.“ | Nesplnené: chýba e-mail |
| Vytvárate aj e-shopy? | Musí obsahovať „e-shopy“ | „Áno, vytvárame weby aj e-shopy.“ | Splnené |
| V akom meste sídlite? | Musí obsahovať „Brno“ | „Naše štúdio sídli v meste Brno.“ | Splnené |
| Zahŕňa údržba aktualizácie obsahu? | Musí obsahovať „po dohode“ | „Údržba automaticky zahŕňa všetky aktualizácie obsahu.“ | Nesplnené: chýba dohodnutá podmienka |
| Akú cenu má zákazkové prepojenie? | Pri neznámej cene musí obsahovať „individuálna ponuka“ | „Pri tomto prepojení je potrebná individuálna ponuka.“ | Splnené |

Doména .example a všetky odpovede v tabuľke sú fiktívne. Žiadne požiadavky sa neposielali na reálny endpoint.

## Zdroj očakávaní a schválenie

V skutočnom reporte bude pri každom pravidle konkrétny zdroj, dátum kontroly zdroja a verzia nastavenia schválená zákazníkom. V tejto ukážke sú pravidlá vytvorené iba na ilustráciu. Schválenie skutočným zákazníkom neprebehlo.

## Odporúčané kroky v tomto modelovom prípade

1. Vlastník chatbota preverí, prečo odpoveď na kontakt neobsahuje schválený e-mail. Po oprave sa zopakuje kontrola podľa pravidiel Monitora.
2. Vlastník overí skutočné podmienky údržby a upraví zdrojové informácie alebo odpoveď bota. Monitor sám tento obsah neopravuje.
3. Ak sa obchodné údaje zmenili zámerne, zákazník schváli nové očakávanie. Pravidlo sa nemá meniť iba preto, aby nesprávna odpoveď prešla.

## Ako čítať výsledok

„Splnené“ znamená, že odpoveď obsahovala dohodnutý text. Nedokazuje to všeobecnú pravdivosť alebo správny význam celej odpovede. „Nesplnené“ znamená, že pravidlo neprešlo; môže ísť o chybu bota, zastarané očakávanie alebo príliš prísne pravidlo.

V skutočnom reporte oddelíme obsahové zlyhanie od nedostupného endpointu, chyby formátu či chýbajúceho merania. Z jedného behu neurčíme trend spoľahlivosti. Denné sledovanie a upozornenia začnú až po overení spojenia a schválení nastavenia.

## Čo bude obsahovať skutočný odovzdaný report

- Projekt, obdobie, schválená verzia a skutočný rozsah merania.
- Zdroje očakávaní a pravidlá ku každej otázke.
- Identifikátor a čas behu, výsledok a relevantný úryvok odpovede.
- Technické chyby alebo chýbajúce dáta, ktoré ovplyvnili hodnotenie.
- Konkrétne odporúčania, zodpovedná osoba a dohodnutý ďalší krok.

Tento report je vzor ručne pripraveného dokumentu. Automatický export klientskych reportov zatiaľ nie je funkciou Monitora.


---

[Sample client report (en)](https://monitor.boteffex.eu/en/sample-report.html) · [Ukázkový report (cs)](https://monitor.boteffex.eu/cs/sample-report.html) · [Ukážkový report (sk)](https://monitor.boteffex.eu/sk/sample-report.html)

[Bezplatná skúška](https://monitor.boteffex.eu/sk/trial.html)
