# Hardware-Stückliste (Kaufteile)

Stand 2026-11-03. Von Hand gepflegt. Profile und Druckteile stehen in `docs/BOM.md`, das `gen/bom_document.py` erzeugt. Daten und Pinlagen stehen in `docs/COMPONENTS.md`. Mengen kommen aus dem Modell oder dem Generator-Code. **(offen)** heißt: noch nicht festgelegt, nicht geprüft oder nicht gezählt.

## Elektronik und Netz

| Teil | Typ | Stück | Quelle / Status |
|---|---|---:|---|
| Netzteil 24 V | Mean Well LRS-350-24 | 1 | PDF nennt LRS-350-24 oder LRS-250-24; modelliert LRS-350 |
| Netzteil 5 V (Pi) | Mean Well RS-15-5 | 1 | PDF |
| Mainboard | BTT Octopus V1.1 | 1 | PDF |
| Einplatinenrechner | Raspberry Pi 4 Model B | 1 | PDF |
| Netzeinbaustecker mit Schalter und Sicherung | Adam Tech IEC-GS-1-100 (Snap-in, 1,0 mm Wand) | 1 | Datenblatt; Sicherungswert **(offen)** |
| Klemmen L/N | WAGO 221-413 | **(offen)** | Typ laut `docs/COMPONENTS.md`; Stückzahl aus dem Modell noch nicht gezählt |
| Klemme PE | WAGO 221-414 | **(offen)** | Nutzerentscheidung; Stückzahl noch nicht gezählt |
| Netzleitung Kette | Lapp ÖLFLEX FD 855 P 3G1,5 | Länge **(offen)** | Biegeradien ungeprüft (T-004) |
| Rundstecker Druckkopf | GX16-4 (Einbau Ø16,2) | 1 Paar | PDF |
| Keystone-Module | RJ45, USB, USB, Blind | 4 | `connector_panel()` |
| Ringöse PE Rahmen | M5 | 1 | `docs/DESIGN.md`, PE; Tray-Öse Größe **(offen)** |

## Lüfter

| Teil | Typ | Stück | Quelle / Status |
|---|---|---:|---|
| Lüfter Querholm | Sanyo Denki San Ace 60L **9LG0624P4H001** | 4 | Katalog „San Ace 60L“ S. 291/292 (Datei `2003014.pdf`, Farnell/Mercateo) |

Datenblattwerte 9LG0624P4H001: 24 V (21,6–26,4 V). Bei 100 % PWM: 0,08 A, 1,92 W, 6150 min⁻¹, 0,78 m³/min (27,5 CFM), 97 Pa, 35 dB(A). Bei 20 % PWM: 0,02 A, 1300 min⁻¹, 14 dB(A). Bei 0 % steht der Lüfter. PWM-Frequenz 25 kHz, Impulssensor. Gehäuse aus Aluminium, 60 × 60 × 25, 100 g. Lebensdauer 180 000 h bei 60 °C (L10). 8 × Ø4,3 auf 50 × 50, Flansch 4 mm. Litzen AWG26, 300 mm: rot +, schwarz −, gelb Sensor, braun Control. Bezug zum Beispiel DigiKey 9LG0624P4H001 oder RS 793-2415. Stecker sind keine dran, nur offene Litzen.

Gewählt, weil: Die 24-V-PWM-Varianten der 9LG-Reihe sind S (53 dB(A)), J (47), H (35) und M (24). H ist ein Kompromiss aus Luftmenge und Geräusch. Alle 4 zusammen ziehen bei 100 % 0,32 A aus dem LRS-350-24.

Ansteuerung **(offen, T-022)**: Die PWM- und Tacho-Leitungen brauchen Pins am Octopus. Die Pegel des PWM-Eingangs stehen nicht im Katalog, dafür das Einzeldatenblatt holen.

Weitere Lüfter: `Side Panel Fan60` (Lochbild 50 × 50, Ø3,4) ist nirgends platziert. Die Lüftersätze für Pi und Octopus baut der Nutzer selbst, die Typen sind **(offen)**.

## Mechanik

| Teil | Typ | Stück | Quelle / Status |
|---|---|---:|---|
| Auszugschienen | Vollauszug, dreiteilig, 450 mm | 2 | Modell; je Seite 1 |
| Hutschienen | EN 50022 35 × 7,5 | 3 | R1a, R1b je 370 mm, R2 (X −305..−40, 265 mm) |
| Aluprofile | 20 × 20 / 20 × 40, Nut 6 | siehe `docs/BOM.md` | erzeugt |
| Alu-Eckverbinder, Panelclips | Original | – | nicht modelliert |

## Schrauben und Nutensteine (nur bereits festgelegte)

| Wo | Schraube | Stück | Quelle |
|---|---|---:|---|
| Lüfter an Halter | M4 × 35 + Mutter + Scheibe (durch Platte und beide Lüfterflansche) | 16 | `tray.fan_holder()` |
| Lüfterhalter an Querholm, obere Nut | M5 + Nutenstein | 8 | `tray.fan_holder()` |
| Lüfterhalter an Querholm, hintere Nut | M5 + Nutenstein | 8 | `tray.fan_holder()` |
| Auszugschienen | M5 + Nutenstein | **(offen)** | je 1 Loch mittig in Outer und Inner |
| Kanal dünne Kette | M3 | 5 | `cable_thin.CH_SCREWS` |
| Pi auf Halter | M2,5 | 4 | Lochbild 58 × 49 |
| IEC Housing an Rear Panel Switch | M3 × 8 Senkkopf (ISO 10642) + Gewindeeinsatz M3 × 5,7 | je 4 | `iec_housing()`; Länge und Einsatztyp **(Annahme)** |
| Zugentlastung 230-V-Mantel am IEC Housing | Kabelbinder ≤ 4,5 breit | 1 | `TIE_SLOT` |
| Übrige (Kettenhalter, Hub-Deckel, Kanäle, Octopus) | M3 | **(offen)** | noch nicht gezählt |

Die Nutgröße des Querholms ist „Nut 6“. In `docs/COMPONENTS.md` stehen M3-Nutensteine, Schienen und Lüfterhalter verwenden aber M5. Vor der Bestellung die passenden Nutensteine prüfen **(offen)**.
