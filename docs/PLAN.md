# Aufgabenliste

Stand 2026-11-03. Erledigte Aufgaben wandern nach `docs/done/<YYYY-MM>.md` (Datum, Ergebnis).

Legende: ID `T-nnn` fortlaufend, nie wiederverwendet. Tabellen: **In Arbeit** (aktiv bearbeitet), **Offen** (bereit, nicht begonnen), **Blockiert / Entscheidung Nutzer** (braucht Entscheidung oder Vorarbeit).

**Regel:** `.claude/HANDOFF.md` verweist auf genau die Aufgaben der Tabelle „In Arbeit“, keine mehr, keine weniger. Ablauf: `CLAUDE.md`, Abschnitt „Handoff-Hygiene“.

## In Arbeit

_keine_

## Offen

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-003 | Anschlusslagen verifizieren | Octopus-Leistungsklemmen J67 erledigt (2026-11-03, Lage + Belegung in `docs/COMPONENTS.md`). Offen: Anzahl und Belegung der IEC-Flachstecker (STEP zeigt 3, Nutzer: „oder paar mehr“; `IEC Housing` umschließt den ganzen Körper), PCB-Unterseite z −1,6, Pi-GPIO (5 V Pin 2/4, GND Pin 6) im STEP lokalisieren (Pi jetzt X −300..−215) | vor T-022 |
| T-004 | Biegeradien gegen Lapp-Datenblatt prüfen | R_fest 22 / R_dyn 36,5 aus Notiz; Kette breit R 24,75 (seit T-016, vorher 29), dünn R 28,35, Viertelkurven R 24 in den Haltern. Ergebnis in `docs/COMPONENTS.md`; falls R_dyn gilt: Radius/Pivot/Kabelwahl neu | – |
| T-005 | Bogenfront dünne Kette zur Frontplatte | eingefahren −379,0 in Tray-Koordinaten gegen Frontplatte −383 (ca. 4 mm, Check >= −380); prüfen, ob Reserve reicht, sonst `X_SHIFT` anpassen | – |
| T-006 | Fahrsimulation Schienen/Tray, Kollision gegen Dokument | Fern-Schienen folgen Nah per Skript; Kollision Tray-Teile gegen Dokument bisher nur per Bbox | – |
| T-007 | Auszug-Seitenwände und Schienen prüfen | Passung Seitenwände zu Inner Nah/Fern (6,1 mm z-Versatz), Kollision Schienen gegen Auszug-/Rahmenteile | T-006 |
| T-009 | Befestigung Kanäle in die Wannenplatte | DC-/Datenkanal: M3 in `Gruppieren#15` (Material unbekannt), Bohrungen nötig; Hub-Boxen sitzen auf den Hutschienen R1a/R1b (erledigt) | Material klären |
| T-010 | Probedrucke und Tests | Nutzer will je Kette 3 Glieder + 3 Klammern drucken (Gelenk, Anschlag, Klammer). Breite Kette (seit T-016 gleicher Mechanismus): Schnappgelenk, Klammer (Bogen 2,0, Arme 1,5, Haken 0,8), Anschlagecken; dünne Kette: Schnappgelenk, Klammer (3,2–3,5 breit, Haken 0,6), Überhänge Anschlagecken, Austritt Z 29..39; Durchhang freies Obertrum (breit ca. 217 mm, evtl. Rampe am Tray-Querprofil X 31–51); Hub-/Kanaldeckel (Rastwulst), DIN-Clips mit Federschieber (Print-in-Place: Spalte 0,4/0,5 lösen sich?, Federweg 1,5, Dehnung der Stege 0,6, Rastkraft, Lösen per Schraubendreher, Passung EN 50022; Hub-Boxen werden stehend gedruckt, Wiegen liegend), IEC-Snap-in auf 1,0-mm-Rand; `IEC Housing` (Gewindeeinsätze in den Ohren, 45°-Stützen, Zugentlastung per Kabelbinder, Platz der Flachsteckhülsen), Rückwände (Steifigkeit Hexfeld, Keystone-Rast im 2-mm-Band); `Fan Holder` (T-028: Steifigkeit nur mit 2 × M5 hinten, Passung auf dem Holm, Litzen durch die 4,5-mm-Spalte; Luft 1,5 mm unter dem Kanal der dünnen Kette beim Fahren prüfen) | Druckteile vorhanden |
| T-011 | BOM aktualisieren | `gen/bom_document.py` kennt Ketten, Kanäle, Tray-Teile, Elektronik nicht; erweitern, `docs/BOM.md` neu erzeugen (Schrauben/Nutensteine nicht im Modell) | – |
| T-012 | Skizzenlayer `Kabelweg (Skizze)` löschen | ausgeblendet, veraltet, keine Geometriequelle | nach T-022 |
| T-022 | Kabelläufe als Litzen neu (`gen/wiring.py`) | Vom Nutzer vertagt (2026-11-03). Alle Routen neu, auch 230 V: die Litzen wurden gelöscht, weil Netzteile und Hub-Boxen verschoben sind (Stützpunkt-Skripte in `.claude/router/` passen nicht mehr). 230 V: Kette -> WAGO -> LRS/RS, PE zur Tray-Öse (Öse im Dokument X −74..−50, Y 615 an die Litze anpassen). DC: LRS 3 Paare (−V Y 552,25/542,75/533,25, +V 523,75/514,25/504,75) -> Octopus J67 MOTOR_POWER/POWER/BED_POWER (Lage und Belegung in `docs/COMPONENTS.md`); RS-Paar (−V 553,1, +V 545,5) -> Pi GPIO 5 V; 4 Lüfter am Querholm (je 4 Litzen AWG26 300 mm, +24 V/GND, PWM 25 kHz und Tacho an Octopus-Pins; Pegel des PWM-Eingangs aus dem Einzeldatenblatt 9LG0624P4H001 holen; Kabelkanal im Halter offen an beiden Enden); durch `DUCT_WIN` (X −140..−72, Z 17,5..25) in den DC-Kanal (Y 453..473). Seit dem Tausch Pi/Octopus (2026-11-03): J67-Front bei X −39,1, davor ca. 70 mm frei bis zu den Lüftern (Platzproblem vor J67 erledigt); der DC-Kanal endet bei X −45 geschlossen direkt neben J67, das offene Vorderende (X −300) liegt jetzt beim Pi; Kanalenden und Datenkanal (führt nach vorn zum Pi) beim Neurouten prüfen. Gleiche Checks wie zuvor | T-003 (Pi-GPIO) |

## Blockiert / Entscheidung Nutzer

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-013 | Fester Halter breit aufweiten und Datenkanal unter der Platte bauen | Trichter 27 → 16 zu eng für das Bündel, auf ca. 27 aufweiten; Datenkanal X ca. 159..440 auf Y 290..330 unter der Acrylplatte (Schrauben nur +y-Flansch Y > 298, nicht X 425..445); Wege zum Rear Panel Connector (GX16 Y 308, Keystones Y 341/365/389/413, Z 65, Auffächern über ca. 105 mm in Y, statisch R >= 22) | T-015, T-014 |
| T-014 | Kanalende hinten (fest, X 445..528, ohne Acrylplatte) | Daten von der breiten Kette zum Rear Panel Connector: geschlossenes Rohr mit S-Abstieg + Lasche am Plug / offene fallende Rinne + Lasche / frei. 230 V: dünner Kanal endet offen bei Y 573,4, Kabel frei (STAND 14c), Bestätigung offen. Nutzer: „weiß noch nicht“ | Nutzerentscheidung |
| T-015 | Kabelliste breite Kette bestätigen | Durchmesser geschätzt, Summe ca. 32,5 > 27,4 Innenbreite (einlagig zu breit); Optionen: ein USB weglassen, Slim-Cat6 ca. 3,8, zweilagig mit Trennboden (Höhe 12 reicht nur für 2 × ≤ 5) | Nutzerentscheidung |
