# Aufgabenliste

Stand 2026-11-03. Erledigte Aufgaben wandern nach `docs/done/<YYYY-MM>.md` (Datum, Ergebnis).

Legende: ID `T-nnn` fortlaufend, nie wiederverwendet. Tabellen: **In Arbeit** (aktiv bearbeitet), **Offen** (bereit, nicht begonnen), **Blockiert / Entscheidung Nutzer** (braucht Entscheidung oder Vorarbeit).

**Regel:** `.claude/HANDOFF.md` verweist auf genau die Aufgaben der Tabelle „In Arbeit“, keine mehr, keine weniger. Ablauf: `CLAUDE.md`, Abschnitt „Handoff-Hygiene“.

## In Arbeit

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-001 | Kabelrouten als modellierte Litzen (`gen/wiring.py`) | Neues Modul, Rohre entlang geglätteter Pfade (Parallel-Transport, 12 Segmente, Kappen, Manifold), Layer `Kabel (gen)`, nicht als STL, nicht im Kollisionstest der Druckteile, aber eigener Check Litzen vs Druckteile (Wände/Deckel nicht durchstoßen). Routen und Farben siehe HANDOFF. Biegeradien >= 4 × D. Akzeptanz: `build --check` ok, Import ok, Sichtprüfung, keine Durchstoßung. **Stand 2026-11-03:** 230 V fertig (Mantel + 10 Adern, Checks grün, Import ok; Knick an LRS FG, RS FG, RS N nach Nutzerentscheidung; `PE_SLOT` nach X −80..−74 verschoben). Offen: DC-Routen | Octopus-Klemmenlage ungeprüft (T-003), Abnahme durch Nutzer (Schleifen einiger Adern, T-021) |

## Offen

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-002 | Lüfterhalter Pi/Octopus und Lüfterposition | Halterfüße (Z 30..33) schweben nach dem Verschieben (Octopus-Lüfter X −312..−302 / Y 382..422, Pi-Lüfter X −102..−62 / Y 432..442, mit dem Pi +22 Y verschoben); ggf. als Generator-Teil auf DIN neu. Danach Lüfterposition festlegen, `Side Panel Fan60` platzieren; Kollisionsprüfung Halterfüße gegen Wanne | – |
| T-003 | Anschlusslagen verifizieren | Octopus-Klemmen (X ca. −145, Y 370..445), PCB-Unterseite z −1,6, Pi-Anschlüsse gegen Datenblatt/STEP prüfen | vor Abnahme T-001 |
| T-004 | Biegeradien gegen Lapp-Datenblatt prüfen | R_fest 22 / R_dyn 36,5 aus Notiz; Kette breit R 29, dünn R 28,35, Viertelkurven R 24 in den Haltern. Ergebnis in `docs/COMPONENTS.md`; falls R_dyn gilt: Radius/Pivot/Kabelwahl neu | – |
| T-005 | Bogenfront dünne Kette zur Frontplatte | eingefahren −379,0 in Tray-Koordinaten gegen Frontplatte −383 (ca. 4 mm, Check >= −380); prüfen, ob Reserve reicht, sonst `X_SHIFT` anpassen | – |
| T-006 | Fahrsimulation Schienen/Tray, Kollision gegen Dokument | Fern-Schienen folgen Nah per Skript; Kollision Tray-Teile gegen Dokument bisher nur per Bbox | – |
| T-007 | Auszug-Seitenwände und Schienen prüfen | Passung Seitenwände zu Inner Nah/Fern (6,1 mm z-Versatz), Kollision Schienen gegen Auszug-/Rahmenteile | T-006 |
| T-008 | `Group#4/#19/#1` nachführen | hängen unter der oberen Schiene (X 472–514, Y 392–463) nach dem +25-Anheben zu hoch | – |
| T-009 | Befestigung Kanäle in die Wannenplatte | DC-/Datenkanal: M3 in `Gruppieren#15` (Material unbekannt), Bohrungen nötig; Hub-Boxen sitzen auf den Hutschienen R1a/R1b (erledigt) | Material klären |
| T-010 | Probedrucke und Tests | Breite Kette: Klammer-Rastkräfte, Zapfen, Brücke/Überhänge; dünne Kette: Schnappgelenk, Klammer (3,2–3,5 breit, Haken 0,6), Überhänge Anschlagecken, Austritt Z 29..39; Durchhang freies Obertrum (breit ca. 217 mm, evtl. Rampe am Tray-Querprofil X 31–51); Hub-/Kanaldeckel (Rastwulst), DIN-Clips mit Federschieber (Print-in-Place: Spalte 0,4/0,5 lösen sich?, Federweg 1,5, Dehnung der Stege 0,6, Rastkraft, Lösen per Schraubendreher, Passung EN 50022; Hub-Boxen werden stehend gedruckt, Wiegen liegend), IEC-Snap-in auf 1,0-mm-Rand | Druckteile vorhanden |
| T-011 | BOM aktualisieren | `gen/bom_document.py` kennt Ketten, Kanäle, Tray-Teile, Elektronik nicht; erweitern, `docs/BOM.md` neu erzeugen (Schrauben/Nutensteine nicht im Modell) | – |
| T-012 | Skizzenlayer `Kabelweg (Skizze)` löschen | ausgeblendet, veraltet, keine Geometriequelle | nach T-001 |
| T-020 | Tray-PE-Öse im Dokument an die Litze anpassen | Litze endet bei X −63, Y 615, Z 26,6 (Hülse des Kabelschuhs), Öse bisher X −74..−50; Kaufteil im Dokument verschieben/drehen | – |
| T-021 | 230-V-Routen glätten, Router ins Repo | Stützpunkte stammen aus einer Offline-Strafkostensuche (Scratch-Skript, nicht im Repo); mehrere Adern machen große Schleifen (u. a. PE Kette, PE Tray, PE RS, L LRS), weil R ≥ 12 im Hub eng ist. Router als `gen/tools/` übernehmen und Routen von Hand/mit Längengewicht nachziehen | Abnahme T-001 |

## Blockiert / Entscheidung Nutzer

| ID | Aufgabe | Details / Akzeptanz | Abhängigkeit / Entscheidung |
|---|---|---|---|
| T-013 | Fester Halter breit aufweiten und Datenkanal unter der Platte bauen | Trichter 27 → 16 zu eng für das Bündel, auf ca. 27 aufweiten; Datenkanal X ca. 159..440 auf Y 290..330 unter der Acrylplatte (Schrauben nur +y-Flansch Y > 298, nicht X 425..445); Wege zum Connector Plug (GX16 Y 308, Keystones Y 341/365/389/413, Z 65, Auffächern über ca. 105 mm in Y, statisch R >= 22) | T-015, T-014 |
| T-014 | Kanalende hinten (fest, X 445..528, ohne Acrylplatte) | Daten von der breiten Kette zum Connector Plug: geschlossenes Rohr mit S-Abstieg + Lasche am Plug / offene fallende Rinne + Lasche / frei. 230 V: dünner Kanal endet offen bei Y 573,4, Kabel frei (STAND 14c), Bestätigung offen. Nutzer: „weiß noch nicht“ | Nutzerentscheidung |
| T-015 | Kabelliste breite Kette bestätigen | Durchmesser geschätzt, Summe ca. 32,5 > 27,4 Innenbreite (einlagig zu breit); Optionen: ein USB weglassen, Slim-Cat6 ca. 3,8, zweilagig mit Trennboden (Höhe 12 reicht nur für 2 × ≤ 5) | Nutzerentscheidung |
| T-016 | Breite Kette wie die dünne umbauen? | volle Anschläge statt 2,7, Klammer bündig in Nut statt Basis unter dem Glied; dann Pivot-Höhen/Radius neu, `hinge_sweep`-Check ergänzen | Nutzerentscheidung, T-004 |
