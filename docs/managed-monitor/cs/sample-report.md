# BotEffex Monitor — ukázkový vstupní report

**ILUSTRAČNÍ UKÁZKA: všechny odpovědi a výsledky jsou vymyšlené. Žádný skutečný chatbot nebyl měřen.**

Projekt: Modelové studio Javor (fiktivní)  
Rozsah: pět otázek, jeden textový chatbot, jeden modelový vstupní běh

## Co vyžaduje pozornost

Tři modelové kontroly splnily pravidlo a dvě ne. Chybí očekávaný e-mail a dohodnutá podmínka údržby. Výsledky ukazují uspořádání reportu, nikoli spolehlivost skutečného chatbota.

| Otázka | Dohodnuté pravidlo | Vymyšlená odpověď | Modelový výsledek |
|---|---|---|---|
| Jak vás mohu kontaktovat? | Obsahuje kontakt@javor.example | Napište nám přes kontaktní formulář. | Nesplněno: chybí e-mail |
| Vytváříte i e-shopy? | Obsahuje „e-shopy“ | Ano, vytváříme weby i e-shopy. | Splněno |
| V jakém městě sídlíte? | Obsahuje „Brno“ | Naše studio sídlí v Brně. | Splněno |
| Zahrnuje údržba aktualizace obsahu? | Obsahuje „po dohodě“ | Údržba automaticky zahrnuje všechny aktualizace obsahu. | Nesplněno: chybí podmínka |
| Kolik stojí zakázkové propojení? | Při neznámé ceně obsahuje „individuální nabídka“ | Pro toto propojení je nutná individuální nabídka. | Splněno |

Doména .example i všechny odpovědi jsou fiktivní. Žádné požadavky nebyly odeslány na skutečný endpoint. Pravidla nebyla schválena skutečným zákazníkem.

## Doporučené kroky v modelovém případě

1. Vlastník prověří chybějící kontaktní e-mail a po opravě kontrolu zopakuje.
2. Ověří skutečné podmínky údržby a upraví zdrojové informace nebo odpověď bota. Monitor obsah sám neopravuje.
3. Při záměrné změně obchodních údajů zákazník schválí nové očekávání. Pravidlo neměňte jen proto, aby nesprávná odpověď prošla.

## Jak číst výsledky

„Splněno“ znamená, že odpověď obsahovala dohodnutý text. Nedokazuje pravdivost ani správný význam celé odpovědi. Selhání může znamenat chybu bota, zastaralé očekávání nebo příliš přísné pravidlo.

Skutečný report oddělí obsahové selhání od nedostupného endpointu, chyby formátu a chybějícího měření. Jeden běh neprokazuje trend spolehlivosti. Denní sledování a upozornění začnou až po ověření spojení a schválení nastavení.

## Co obsahuje skutečný předaný report

- Projekt, období měření a schválenou verzi nastavení.
- Zdroje, data ověření zdrojů a pravidla jednotlivých otázek.
- Skutečný identifikátor běhu, čas, výsledek a příslušný úryvek odpovědi.
- Technické chyby a chybějící data ovlivňující hodnocení.
- Doporučení, odpovědnou osobu a dohodnutý další krok.

Jde o vzor ručně připraveného dokumentu. Automatický export klientských reportů zatím není funkcí Monitora.


---

[Sample client report (en)](https://monitor.boteffex.eu/en/sample-report.html) · [Ukázkový report (cs)](https://monitor.boteffex.eu/cs/sample-report.html) · [Ukážkový report (sk)](https://monitor.boteffex.eu/sk/sample-report.html)

[Bezplatná zkouška](https://monitor.boteffex.eu/cs/trial.html)
