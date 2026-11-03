# Aufgabenliste

Stand 2026-11-03. Erledigte Aufgaben wandern nach `docs/done/<YYYY-MM>.md` (Datum, Ergebnis).

Legende: ID `T-nnn` fortlaufend, nie wiederverwendet. Tabellen: **In Arbeit** (aktiv bearbeitet), **Offen** (bereit, nicht begonnen), **Blockiert / Entscheidung Nutzer** (braucht Entscheidung oder Vorarbeit).

**Regel:** `.claude/HANDOFF.md` verweist auf genau die Aufgaben der Tabelle „In Arbeit“, keine mehr, keine weniger. Ablauf: `CLAUDE.md`, Abschnitt „Handoff-Hygiene“.

## In Arbeit

_keine_

## Offen

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-002 | Lüfterhalter Pi/Octopus und Lüfterposition | Halterfüße (Z 30..33) schweben nach dem Verschieben (Octopus-Lüfter X −312..−302 / Y 382..422, Pi-Lüfter X −102..−62 / Y 432..442, mit dem Pi +22 Y verschoben); ggf. als Generator-Teil auf DIN neu. Danach Lüfterposition festlegen, `Side Panel Fan60` platzieren; Kollisionsprüfung Halterfüße gegen Wanne | – |
| T-003 | Anschlusslagen verifizieren | Octopus-Leistungsklemmen J67 erledigt (2026-11-03, Lage + Belegung in `docs/COMPONENTS.md`). Offen: PCB-Unterseite z −1,6, Pi-GPIO (5 V Pin 2/4, GND Pin 6) im STEP lokalisieren | vor T-022 |
| T-004 | Biegeradien gegen Lapp-Datenblatt prüfen | R_fest 22 / R_dyn 36,5 aus Notiz; Kette breit R 24,75 (seit T-016, vorher 29), dünn R 28,35, Viertelkurven R 24 in den Haltern. Ergebnis in `docs/COMPONENTS.md`; falls R_dyn gilt: Radius/Pivot/Kabelwahl neu | – |
| T-005 | Bogenfront dünne Kette zur Frontplatte | eingefahren −379,0 in Tray-Koordinaten gegen Frontplatte −383 (ca. 4 mm, Check >= −380); prüfen, ob Reserve reicht, sonst `X_SHIFT` anpassen | – |
| T-006 | Fahrsimulation Schienen/Tray, Kollision gegen Dokument | Fern-Schienen folgen Nah per Skript; Kollision Tray-Teile gegen Dokument bisher nur per Bbox | – |
| T-007 | Auszug-Seitenwände und Schienen prüfen | Passung Seitenwände zu Inner Nah/Fern (6,1 mm z-Versatz), Kollision Schienen gegen Auszug-/Rahmenteile | T-006 |
| T-008 | `Group#4/#19/#1` nachführen | hängen unter der oberen Schiene (X 472–514, Y 392–463) nach dem +25-Anheben zu hoch. Neu (T-027): sie reichen bis Z 77,9 und kollidieren bei eingefahrenem Tray (X 427..480) mit Lüfterhalter/Lüfter 2 (Oberkante Z 83, Y 400,5..466,5); beim Nachführen Z ≥ 84 sicherstellen | – |
| T-009 | Befestigung Kanäle in die Wannenplatte | DC-/Datenkanal: M3 in `Gruppieren#15` (Material unbekannt), Bohrungen nötig; Hub-Boxen sitzen auf den Hutschienen R1a/R1b (erledigt) | Material klären |
| T-010 | Probedrucke und Tests | Nutzer will je Kette 3 Glieder + 3 Klammern drucken (Gelenk, Anschlag, Klammer). Breite Kette (seit T-016 gleicher Mechanismus): Schnappgelenk, Klammer (Bogen 2,0, Arme 1,5, Haken 0,8), Anschlagecken; dünne Kette: Schnappgelenk, Klammer (3,2–3,5 breit, Haken 0,6), Überhänge Anschlagecken, Austritt Z 29..39; Durchhang freies Obertrum (breit ca. 217 mm, evtl. Rampe am Tray-Querprofil X 31–51); Hub-/Kanaldeckel (Rastwulst), DIN-Clips mit Federschieber (Print-in-Place: Spalte 0,4/0,5 lösen sich?, Federweg 1,5, Dehnung der Stege 0,6, Rastkraft, Lösen per Schraubendreher, Passung EN 50022; Hub-Boxen werden stehend gedruckt, Wiegen liegend), IEC-Snap-in auf 1,0-mm-Rand | Druckteile vorhanden |
| T-011 | BOM aktualisieren | `gen/bom_document.py` kennt Ketten, Kanäle, Tray-Teile, Elektronik nicht; erweitern, `docs/BOM.md` neu erzeugen (Schrauben/Nutensteine nicht im Modell) | – |
| T-012 | Skizzenlayer `Kabelweg (Skizze)` löschen | ausgeblendet, veraltet, keine Geometriequelle | nach T-022 |
| T-022 | Kabelläufe als Litzen neu (`gen/wiring.py`) | Vom Nutzer vertagt (2026-11-03). Alle Routen neu, auch 230 V: die Litzen wurden gelöscht, weil Netzteile und Hub-Boxen verschoben sind (Stützpunkt-Skripte in `.claude/router/` passen nicht mehr). 230 V: Kette -> WAGO -> LRS/RS, PE zur Tray-Öse (Öse im Dokument X −74..−50, Y 615 an die Litze anpassen). DC: LRS 3 Paare (−V Y 552,25/542,75/533,25, +V 523,75/514,25/504,75) -> Octopus J67 MOTOR_POWER/POWER/BED_POWER (Lage und Belegung in `docs/COMPONENTS.md`); RS-Paar (−V 553,1, +V 545,5) -> Pi GPIO 5 V; 4 Lüfter am Querholm (je 4 Litzen AWG26 300 mm, +24 V/GND, PWM 25 kHz und Tacho an Octopus-Pins; Pegel des PWM-Eingangs aus dem Einzeldatenblatt 9LG0624P4H001 holen; Kabelkanal im Halter offen an beiden Enden); durch `DUCT_WIN` (X −140..−72, Z 17,5..25) in den DC-Kanal (Y 453..473). Problem: nur 13,4 mm zwischen J67-Front (X −139,1) und Pi (X −125,7); Optionen: 90°-Bogen R ≈ 12 nach ±Y, Pi nach +X verschieben (dann T-002), oder R < 12 am Klemmenknick erlauben. Gleiche Checks wie zuvor | Nutzerentscheidung Platz vor J67; T-003 (Pi-GPIO) |
| T-026 | Hintere Mod-Frame-Druckteile neu | Nutzer (todo.md): die beiden hinteren Druckteile neu entwerfen, weniger Filament, stabiler (230 V: alles stabil), Schalter rot einhausen, Halterungen (Cover Mounts) beibehalten. Offen: welche Teile genau (vermutlich Switch Plug + Connector Plug samt Bezel Ring), welcher Schalter (IEC-Kombistecker?) | – |

## Blockiert / Entscheidung Nutzer

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-013 | Fester Halter breit aufweiten und Datenkanal unter der Platte bauen | Trichter 27 → 16 zu eng für das Bündel, auf ca. 27 aufweiten; Datenkanal X ca. 159..440 auf Y 290..330 unter der Acrylplatte (Schrauben nur +y-Flansch Y > 298, nicht X 425..445); Wege zum Connector Plug (GX16 Y 308, Keystones Y 341/365/389/413, Z 65, Auffächern über ca. 105 mm in Y, statisch R >= 22) | T-015, T-014 |
| T-014 | Kanalende hinten (fest, X 445..528, ohne Acrylplatte) | Daten von der breiten Kette zum Connector Plug: geschlossenes Rohr mit S-Abstieg + Lasche am Plug / offene fallende Rinne + Lasche / frei. 230 V: dünner Kanal endet offen bei Y 573,4, Kabel frei (STAND 14c), Bestätigung offen. Nutzer: „weiß noch nicht“ | Nutzerentscheidung |
| T-015 | Kabelliste breite Kette bestätigen | Durchmesser geschätzt, Summe ca. 32,5 > 27,4 Innenbreite (einlagig zu breit); Optionen: ein USB weglassen, Slim-Cat6 ca. 3,8, zweilagig mit Trennboden (Höhe 12 reicht nur für 2 × ≤ 5) | Nutzerentscheidung |
