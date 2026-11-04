# Kaufteile und 3D-Modelle

Stand 2026-11-04. Kaufteile liegen nur im IngeTrazo-Dokument (nicht im Generator). Die Bestellliste steht in `docs/HARDWARE.md`. Quelle der Komponentenauswahl: `CR10 Standalone Mod - Documentation.pdf` (alte Version: DIN EN 50022 2 × 300–350, Sunon 60er Lüfter, IEC-GS-1-100, Keystones, LRS-250/350-24 bzw. RS-15-5, Voron-DIN-Halter). Werte mit **(ungeprüft)** oder **(Annahme)** sind nicht aus Datenblatt oder Messung belegt.

## Mean Well LRS-350-24 (24 V, Hauptnetzteil)

- Gehäuse 215 × 115 × 30 (wie LRS-200). Das PDF nennt LRS-350-24 oder LRS-250-24; offizielles STEP ist LRS-350. Im Dokument Platzhalter `PSU LRS-200-24` (Layer `Electronics (Platzhalter)`, unsichtbar) und Vendor-Modell `PSU Mean Well LRS-350-24`.
- Pinbelegung (9 Pins, Raster 9,5, Pin 9 auf der Lüfterseite): 1 AC/L, 2 AC/N, 3 FG, 4–6 −V, 7–9 +V.
- Lage Welt (LRS X −373,75..−158,75 seit 2026-11-03, vorher −364..−149; Klemmen +X): Klemmblock X −175,85..−161,25, Y 498,5..585,5; Schrauben oben Z 48; Leitereintritt Z ca. 36.
- Kabelschuhe **(Annahme)**: isolierte Gabelkabelschuhe 0,5–1,5 mm² für M3,5 (Schraubengröße nicht geprüft), 18 mm ab Schraubenmitte; Schraubenmitte = Blockmitte X −168,55.

| Pin | Funktion | Welt-Y |
|---|---|---|
| 1 | AC/L | 580,75 |
| 2 | AC/N | 571,25 |
| 3 | FG (PE) | 561,75 |
| 4 | −V | 552,25 |
| 5 | −V | 542,75 |
| 6 | −V | 533,25 |
| 7 | +V | 523,75 |
| 8 | +V | 514,25 |
| 9 | +V | 504,75 |

## Mean Well RS-15-5 (5 V, Pi)

- Das PDF nennt RS-15-5 (nicht LRS-15). Vendor-Modell `PSU Mean Well RS-15-5`, Platzhalter `PSU LRS-15-5`.
- Pinbelegung (5 Pins, Raster 7,62, +V auf der ADJ/LED-Seite): 1 AC/L, 2 AC/N, 3 FG, 4 −V, 5 +V.
- Lage Welt seit 2026-11-04 (T-037, Nutzer: gegenüber T-033 um 90° gegen den Uhrzeigersinn gedreht): Klemmen −X wie im STEP, also die Ausrichtung vor T-033, verschoben um (−17,01 / −55,25) (`power_hub.rs_xy`). Gehäuse X −53,61..9,05, Y 475,5..526,6, Z 25..53; Klemmblock X −65,51..−53,61, Y 485,59..525,25, Z 30,59..43,75. Im Dokument Vendor-Modell und Platzhalter per X = 484,55 − y, Y = x + 517,55 aus der T-033-Lage gedreht.
- Kabelschuhe **(Annahme)**: isolierte Gabelkabelschuhe 0,5–1,5 mm² für M3 (Schraubengröße RS-15 nicht geprüft), 18 mm ab Schraubenmitte; Schraubenmitte = Blockmitte X −59,56.

| Pin | Funktion | Welt-Y | Welt-Y vor T-033 |
|---|---|---|---|
| 1 | AC/L | 520,75 | 576,0 |
| 2 | AC/N | 513,15 | 568,4 |
| 3 | FG (PE) | 505,55 | 560,8 |
| 4 | −V | 497,85 | 553,1 |
| 5 | +V | 490,25 | 545,5 |

AC/DC-Grenze: LRS-350 auf Y 557, RS-15-5 auf Y 501,7 (niedrige Trennwände in der LRS- und der RS-Box, `docs/DESIGN.md`).

## Adam Tech IEC-GS-1-100 (Netzeinbaustecker mit Schalter und Sicherung)

| Eigenschaft | Wert |
|---|---|
| Flansch | 50 × 30,5 |
| Ausschnitt | 47 × 27,8, R2 (Generator: +2·FIT) |
| Befestigung | Snap-in für 1,0 mm Wand, keine Schrauben laut Datenblatt |
| Tiefe | 19,5 + Flachsteckhülsen (QC) 4,8; im Dokument-Mesh enden die Flachstecker bei X 507,2 |
| Flachstecker im STEP | 3: Y 534,6 / Z 65, Y 544,7 / Z 72, Y 557,2 / Z 72,5; Belegung **(ungeprüft)**, Nutzer: „3 Pins, oder paar mehr“ (T-003) |
| Lage | liegend, Flanschrückseite auf der Außenfläche von `Rear Panel Switch` X 534,7, Mitte Y 553,4 / Z 65, Wippe bei +Y |
| Farben im Import | Körper schwarz, Kontakte zinnfarben (STEP hat nur eine Farbe) |

Quelle: Datenblatt PDF S. 1 / Digikey. Rastkraft auf gedrucktem Rand ungetestet.

## WAGO 221

| Typ | Verwendung | Maße | Status |
|---|---|---|---|
| 221-413 | L, N (3 Leiter) | 18,7 × 18,6 × 8,3 (Breite × Länge × Dicke) | aus Datenblatt übernommen |
| 221-414 | PE (4 Leiter, Nutzerentscheidung) | Breite 24,9 | **(Annahme)** |

Im Dokument WAGO-Modelle plus Hebelstreifen (ersetzen die frühere 221-415), seit 2026-11-04 liegend in der WAGO-Box: Hebel oben, Leitereinführung +Y, Y 551,1..569,7 (hinteres Ende 6 mm außerhalb der Box), Z 51,8..60,1, Oberseite 0,5 über dem Deckel (Lagen in `docs/DESIGN.md`).
Leitereinführungen für die Litzen in `wiring.py`: Stirnseite +Y (Y 569,7), Mitte der Dicke, gleichmäßig über die Breite verteilt **(Annahme, nicht gemessen)**. Lage der Prüföffnung (Messspitze) nicht geprüft **(Annahme: von oben bzw. von der Einführungsseite erreichbar)**.

## BTT Octopus (Mainboard)

- STEP V1.0 wird für V1.1 verwendet (es gibt kein V1.1-STEP). Platzhalter `BTT Octopus V1.1`, Vendor `BTT Octopus (V1.0 STEP)`. PCB-Unterseite im Quellmodell z −1,6 **(Annahme, nicht gemessen)**; PCB im STEP hell statt schwarz; 689 Kleinteile < 2 mm weggelassen.
- Lage (seit 2026-11-03 hinten auf R2, nahe den 4 Lüftern; vorher X −300..−140): X −200..−40, Y 352..452, PCB-Unterkante Z 22,5 (seit 2026-11-03, vorher 31; Bauteile reichen 3,1 unter die Platine); Schraubklemmen +X, Motorstecker −Y; Lochraster 150 × 90.
- Leistungsklemmblock (J67, 8-polig) am +X-Rand, im STEP gemessen (2026-11-03, X nach dem Tausch +100): Gehäusefront X −39,1, Y 367,0..443,4, Z 24,1..38,6 (nach dem Absenken um 8,5); Schraubenköpfe X −46,1, Z 34,9 (Oberseite); Raster 9,5; Klemmkammern Z 31,5..38,6, offen nach +X und oben. Kabeleintritt von +X; das STEP hat keine Drahtöffnungen, Eintrittshöhe ca. Z 32,5..35,5 **(Annahme)**.
- Belegung laut BTT-Pinout `Firmware/Klipper/Images/octopus_pinout.png` (Repo bigtreetech/BIGTREETECH-OCTOPUS-V1.0), auf die Einbaulage (180°) umgerechnet, nach steigendem Y: 371,9 MOTOR_POWER GND (−), 381,4 MOTOR_POWER VM (+), 390,9 POWER GND (−), 400,4 POWER 24V (+), 409,9 BED_POWER GND (−), 419,4 BED_POWER BED_P (+), 428,9 BED_OUT BED_P (+), 438,4 BED_OUT (−). Sicherungen: MOTOR_POWER F1 15 A, POWER F3, BED_POWER F2 15 A. Heizerklemmen HE0..HE3 (J64) an der +Y-Kante.
- Freiraum vor J67: bis zu den Lüftern (Auslass X 31,2) ca. 70 mm frei (seit dem Tausch mit dem Pi; vorher 13,4 mm zum Pi).

## Raspberry Pi 4 Model B

- Platine X −335..−250 (seit 2026-11-03 vorn auf R2 und um 180° gedreht; vorher −300..−215 mit Ports +X, davor −125..−40), Y 374..430 (Lochmitte 402 über R2), Z 22,5 (Unterkante, seit 2026-11-03, vorher 31; Bauteile reichen 2,1 unter die Platine); Ports −X, USB-C +Y, GPIO −Y. Löcher 58 × 49 (M2,5). 5-V-Versorgung über GPIO.
- STEP-Quelle ohne bekannte Lizenz (siehe Tabelle); Alternative PixelBot-STEP hat nur 166 Flächen. Maße der Anschlusslagen nicht gegen Datenblatt geprüft **(ungeprüft)**.

## Kabel (Lapp ÖLFLEX FD 855 P 3G1,5)

| Eigenschaft | Wert | Status |
|---|---|---|
| Außendurchmesser | 7,3 | aus früherer Notiz |
| Ader-Außendurchmesser (1,5 mm²) | 3,0 | **Annahme** (Modell `wiring.py`, Biegeradius ≥ 4 × D = 12) |
| Mantelfarbe | grau | **Annahme** (nur Darstellung) |
| Biegeradius fest R_fest | 22 | Lapp-Datenblatt **ungeprüft** |
| Biegeradius dynamisch R_dyn | 36,5 | Lapp-Datenblatt **ungeprüft** |
| Kette breit R 24,75 / dünn R 27,0 (seit T-005, vorher 28,35) | beide < R_dyn, > R_fest | PLAN T-004 |

Faustregel (nicht geprüft): Cat6/USB dynamisch ca. 8–10 × D = 36..60 mm, nur schleppkettentaugliche Kabel. Kabelliste breite Kette, **Durchmesser geschätzt (Annahme)**: GX16-4 (CAN + 24 V zum Druckkopf) ca. 6; RJ45 Cat6 ca. 5,5; 2 × USB je ca. 4,5; 24/5-V-Versorgung ca. 5; Sensoren ca. 4; Summe 29,5 plus ca. 10 % Luft = ca. 32,5 gegen Innenbreite 27,4 (einlagig zu breit; Innenhöhe 12,5, zweilagig nur ≤ 5 je Lage). Option: Slim-Cat6 ca. 3,8, ein USB weglassen (PLAN T-015).

## Profile, Schienen, Kleinteile

| Teil | Daten |
|---|---|
| Alu-Profile | 20 × 20 / 20 × 40, „Profil Typ B Nut 6“, Nut 6, M3-Hammer-/Nutensteine; Längen siehe `docs/BOM.md` |
| Auszugschienen | Vollauszug-Schubladenschienen, dreiteilig, 450 lang, 2 Stück; M5 mit Nutensteinen, Loch Ø5,5 mittig in Outer und Inner; Hub 396 geschätzt |
| Hutschienen | EN 50022 35 × 7,5, Höhe 12,5 über Tray-Boden. Anzeigemodell (`gen/rail_model.py`, T-034) nach Phoenix Contact NS 35/ 7,5 PERF 2000MM (Art. 0801733, Stahl verzinkt, EN 60715; Nutzer: „irgendein Modell“, gekauftes Produkt unbekannt). Datenblatt (phoenixcontact.com/us/products/0801733, PDF vom 2024-05-18, S. 3): Breite 35, Tiefe 7,5, Blech 1, Steg außen 27, Langlöcher 6,2 × 15 mittig, Teilung 25; 330 g/m (660 g je 2 m, Modell 329 g/m bei 7,85 g/cm³). **Annahmen:** Biegeradien innen 1,0 / außen 2,0, Flanschenden gerade, Lochbild mittig auf der Schienenlänge (R1a/R1b je 15 Löcher, Reststeg 2,8 an den Enden; R2 11 Löcher, Reststeg 7,5); Flanschunterseite eben ab \|y\| 14,5 (Clip-Haken ab 16,2) |
| Lüfter | Sunon 60 mm (laut PDF), Ø57 Ausschnitt, 4 × Ø3,4 auf 50 × 50; eigene Lüfter für Pi/Octopus entfallen (2026-11-03 gelöscht, Kühlung über die 4 Lüfter am Querholm) |
| Lüfter Querholm | 4 × Sanyo Denki San Ace 60L 9LG0624P4H001 (24 V, 4-Draht PWM 25 kHz + Impulssensor, 60 × 60 × 25, 8 × Ø4,3 auf 50 × 50, Flansch 4, Litzen AWG26 300 mm rot +/schwarz −/gelb Sensor/braun Control; 35 dB(A) bei 100 %). Quelle: Katalog San Ace 60L S. 291/292. Maßzeichnung (Katalog C1137B001, S. 382): 60 ± 0,5, Tiefe 25 ± 0,5, Flansche 4 ± 0,3, 8 × Ø4,3 ± 0,3 auf 50 ± 0,3, 7 Flügel, Litzenaustritt seitlich am Auslassflansch, Referenzöffnung 59 mit Fase 62,7 (Diagonale), 4 × Ø4,5. Rahmen Aluminium, Laufrad Kunststoff UL 94V-1. Nicht bemaßt, im Anzeigemodell `gen/fan_model.py` angenommen: Bohrung Ø57, Nabe Ø32, 4 Speichen auf der Auslassseite, Eckradius 3; Lüfter um 90° gedreht eingebaut, Litzenaustritt unten (Nutzer 2026-11-03). Daten und Begründung in `docs/HARDWARE.md`; im Dokument `Luefter 60x60x25 #1..4` (Layer `Electronics (neu)`) |
| Alu-Eckverbinder, Original-Füße, Panelclips | Kaufteile bzw. Original, nicht modelliert |

## Quellen der 3D-Modelle

STEP-Dateien liegen nicht im Projekt (nur im Scratchpad geladen); für Neukonvertierung neu herunterladen. Konverter: `gen/step_to_mesh.py` in separatem venv mit `cadquery-ocp`. Layer im Dokument: `Electronics (vendor)`.

| Modell | Quelle (URL) | JSON | Konverter-Parameter | Platzierung in `vendor_import.py` (`rot`, Bezug) |
|---|---|---|---|---|
| LRS-350-24 | https://www.meanwell.com/upload/pdf/LRS-350/LRS-350-3D.zip (offiziell) | `build/vendor/lrs350.json` | `--defl 0.5 --ang 1.0 --min-solid 1.5` | `rot=((0,-1),(1,-1),(2,1))` = 180° um Z (Klemmen +X); mittig in X/Y auf Platzhalter `PSU LRS-200-24`, Unterkante auf Platzhalter-Unterkante (`z_ref=None`) |
| RS-15-5 | https://www.meanwell.com/upload/pdf/RS-15/RS-15-3D.zip (offiziell) | `build/vendor/rs15.json` | `--defl 0.5 --ang 1.0 --min-solid 1.5` | `rot=((0,1),(1,1),(2,1))` = unverändert (Klemmen −X wie in der Quelle; seit T-037 wieder wie vor T-033); mittig auf Platzhalter `PSU LRS-15-5` (mitgedreht), Unterkante bündig. Ungetestet, weil `build/vendor/` lokal fehlt |
| Raspberry Pi 4 Model B | https://code.c-base.org (wercc/monorail-pcb) `Libraries/Raspberry-Pi-4-library-for-kicad-master/Raspberry Pi 4 Model B.STEP`; Lizenz unbekannt | `build/vendor/pi4.json` | `--defl 0.5 --ang 1.0 --min-solid 1.5` | `rot=((0,-1),(2,1),(1,1))` Y-up → Z-up (Ports −X, GPIO −Y); `z_ref=-0.8` (PCB y −0,8..0,8) auf Platzhalter `Raspberry Pi 4` |
| BTT Octopus V1.0 (für V1.1) | github bigtreetech/BIGTREETECH-OCTOPUS-V1.0 `3D/BIGTREETECH Octopus V1.0.stp` | `build/vendor/octopus.json` | `--defl 1 --ang 1.5 --min-solid 2` | `rot=((0,-1),(1,-1),(2,1))` = 180° (Schraubklemmen +X, Motorstecker −Y); `z_ref=-1.6` auf Platzhalter `BTT Octopus V1.1` |
| IEC-GS-1-100 | https://app.adam-tech.com/products/download/model/203611/iec-gs-1-100-model.step (Datenblatt `.../data_sheet/203611/iec-gs-1-100-data-sheet.pdf`) | `build/vendor/iec_gs_1_100.json` | nicht dokumentiert **(ungeprüft)** | `rot=((2,1),(1,-1),(0,1))`, `at=(537.7, 553.4, 65.0)` (Quellursprung = Flansch-Vorderseite, +z aus der Platte; Flanschrückseite auf x 534,7), kein Platzhalter; Farbe per `paint` (Kontakte zinnfarben z < −21, Körper schwarz) |

Alle Modelle: Platzhalter auf Layer `Electronics (Platzhalter)` (unsichtbar, nicht gelöscht), Vendor-Gruppen werden bei jedem Lauf von `vendor_import.py` ersetzt. Der Konverter schreibt Millimeter, Farben aus dem STEP, planare Flächen als Polygone mit Löchern, den Rest als Dreiecke. gmsh wurde verworfen (zu langsam). Platzhaltergrößen: LRS X −364..−149; RS X −59,48..3,02, Y 475,55..526,55 (seit T-037).
