# Stückliste

Stand 2026-11-05. Erzeugt mit `gen/bom_document.py` aus dem IngeTrazo-Dokument (Profile, Kaufteile) und `build/bom_parts.json` (Druckteile, aus `gen/cr10mod.py build`).
Längen sind Modellmaße ohne Sägezugabe. Außer dem CR10-Rahmen sind sie nicht am Teil gegengemessen. Schrauben, Nutensteine, Kabel und Kleinteile stehen in `docs/HARDWARE.md`.

## CR10 Frame

Original-CR10-Rahmen, bleibt unverändert, nichts zu kaufen

| Profil | Länge (mm) | Stück | Summe (mm) |
|---|---:|---:|---:|
| 2020 | 320 | 1 | 320 |
| 2020 | 400 | 4 | 1600 |
| 2040 | 480 | 4 | 1920 |
| 2040 | 563 | 1 | 563 |

## Mod Frame Base

fester Unterbau

| Profil | Länge (mm) | Stück | Summe (mm) |
|---|---:|---:|---:|
| 2020 | 400 | 1 | 400 |
| 2020 | 500 | 2 | 1000 |
| 2040 | 80 | 7 | 560 |

## Tray Frame

Auszug (Tray)

| Profil | Länge (mm) | Stück | Summe (mm) |
|---|---:|---:|---:|
| 2020 | 80 | 2 | 160 |
| 2020 | 334 | 1 | 334 |
| 2020 | 400 | 2 | 800 |
| 2020 | 410 | 1 | 410 |
| 2040 | 80 | 1 | 80 |
| 2040 | 410 | 1 | 410 |

## Zukauf Profile für den Umbau (Base + Drawer)

| Profil | Länge (mm) | Stück | Summe (mm) |
|---|---:|---:|---:|
| 2020 | 80 | 2 | 160 |
| 2020 | 334 | 1 | 334 |
| 2020 | 400 | 3 | 1200 |
| 2020 | 410 | 1 | 410 |
| 2020 | 500 | 2 | 1000 |
| 2040 | 80 | 8 | 640 |
| 2040 | 410 | 1 | 410 |

| Typ | Stück | Gesamtlänge (mm) |
|---|---:|---:|
| 2020 | 9 | 3104 |
| 2040 | 9 | 1050 |

## Kaufteile im Modell

Gezählt nach Gruppennamen im Dokument (sichtbare Gruppen; ausgeblendete Platzhalter zählen nicht).

| Teil | Stück | Hinweis |
|---|---:|---|
| Netzteil 24 V Mean Well LRS-350-24 | 1 |  |
| Netzteil 5 V Mean Well RS-15-5 | 1 |  |
| Mainboard BTT Octopus (Modell V1.0, Kauf V1.1) | 1 |  |
| Raspberry Pi 4 Model B | 1 |  |
| Netzeinbaustecker IEC-GS-1-100 | 1 |  |
| Lüfter San Ace 60L 9LG0624P4H001 | 4 |  |
| WAGO 221-413 (L, N) | 2 |  |
| WAGO 221-414 (PE) | 1 |  |
| Hutschiene EN 50022 35 × 7,5 | 3 | Längen 280 mm, 370 mm, 370 mm |
| Rundsteckverbinder GX16-4 (Einbauteil) | 1 |  |
| Keystone-Modul RJ45 | 1 |  |
| Keystone-Modul USB | 2 |  |
| Keystone-Blindmodul | 1 |  |
| Ringöse M5 (PE) | 2 |  |
| Auszugschiene dreiteilig, Vollauszug, 450 mm | 2 |  |
| Original-Fuß (`CR10 Foot`, vom CR10-Rahmen umsetzen) | 4 |  |

## Druckteile

Volumen = Volumen des Körpers (100 % gefüllt), nicht der Filamentverbrauch des Slicers.

### Mod Frame: Rück- und Seitenpaneele, IEC-Gehäuse (`Mod Frame Print Parts`)

| Teil | STL | Stück | Volumen je Stück (cm³) | Volumen gesamt (cm³) |
|---|---|---:|---:|---:|
| Rear Panel Switch | `Rear_Panel_Switch.stl` | 1 | 24,1 | 24,1 |
| Rear Panel Connector | `Rear_Panel_Connector.stl` | 1 | 25,0 | 25,0 |
| IEC Housing | `IEC_Housing.stl` | 1 | 31,0 | 31,0 |
| Side Panel Hex | `Side_Panel_Hex.stl` | 4 | 17,9 | 71,5 |
| Side Panel Fan60 | `Side_Panel_Fan60.stl` | 0 | 22,4 | 0,0 |
| **Summe** | | 7 | | **151,7** |

### Schleppketten, Halter, fester Kanal (`Drag Chains`)

| Teil | STL | Stück | Volumen je Stück (cm³) | Volumen gesamt (cm³) |
|---|---|---:|---:|---:|
| Chain Link | `Chain_Link.stl` | 11 | 6,3 | 69,2 |
| Chain Lid | `Chain_Lid.stl` | 11 | 0,5 | 5,3 |
| Chain Bracket Fixed | `Chain_Bracket_Fixed.stl` | 1 | 21,9 | 21,9 |
| Chain Bracket Moving | `Chain_Bracket_Moving.stl` | 1 | 22,1 | 22,1 |
| Thin Link | `Thin_Link.stl` | 12 | 2,6 | 31,3 |
| Thin Lid | `Thin_Lid.stl` | 12 | 0,2 | 2,3 |
| Thin Bracket Fixed | `Thin_Bracket_Fixed.stl` | 1 | 9,9 | 9,9 |
| Thin Bracket Moving | `Thin_Bracket_Moving.stl` | 1 | 11,5 | 11,5 |
| Thin Channel Front | `Thin_Channel_Front.stl` | 1 | 16,7 | 16,7 |
| Thin Channel Rear | `Thin_Channel_Rear.stl` | 1 | 19,7 | 19,7 |
| **Summe** | | 52 | | **209,7** |

### Tray: Frontpaneele, Power-Hub, Kanäle, DIN-Halter, Lüfterhalter (`Tray Print Parts`)

| Teil | STL | Stück | Volumen je Stück (cm³) | Volumen gesamt (cm³) |
|---|---|---:|---:|---:|
| Front Panel Hex | `Front_Panel_Hex.stl` | 2 | 15,4 | 30,8 |
| WAGO Box | `WAGO_Box.stl` | 1 | 44,8 | 44,8 |
| WAGO Box Lid | `WAGO_Box_Lid.stl` | 1 | 7,2 | 7,2 |
| LRS Box | `LRS_Box.stl` | 1 | 36,2 | 36,2 |
| LRS Box Lid | `LRS_Box_Lid.stl` | 1 | 10,5 | 10,5 |
| RS Box | `RS_Box.stl` | 1 | 27,9 | 27,9 |
| RS Box Lid | `RS_Box_Lid.stl` | 1 | 5,2 | 5,2 |
| AC Duct | `AC_Duct.stl` | 1 | 9,4 | 9,4 |
| AC Duct Lid | `AC_Duct_Lid.stl` | 1 | 2,7 | 2,7 |
| DC Duct | `DC_Duct.stl` | 1 | 25,6 | 25,6 |
| DC Duct Lid | `DC_Duct_Lid.stl` | 1 | 11,3 | 11,3 |
| Data Duct | `Data_Duct.stl` | 1 | 27,3 | 27,3 |
| Data Duct Lid | `Data_Duct_Lid.stl` | 1 | 11,4 | 11,4 |
| Fan DC Duct | `Fan_DC_Duct.stl` | 1 | 28,9 | 28,9 |
| Fan DC Duct Lid | `Fan_DC_Duct_Lid.stl` | 1 | 10,0 | 10,0 |
| Fan Data Duct | `Fan_Data_Duct.stl` | 1 | 29,8 | 29,8 |
| Fan Data Duct Lid | `Fan_Data_Duct_Lid.stl` | 1 | 9,5 | 9,5 |
| DIN PSU24 Cradle 1 | `DIN_PSU24_Cradle_1.stl` | 1 | 25,6 | 25,6 |
| DIN PSU24 Cradle 2 | `DIN_PSU24_Cradle_2.stl` | 1 | 25,6 | 25,6 |
| DIN PSU5 Cradle 1 | `DIN_PSU5_Cradle_1.stl` | 1 | 8,8 | 8,8 |
| DIN PSU5 Cradle 2 | `DIN_PSU5_Cradle_2.stl` | 1 | 8,8 | 8,8 |
| DIN Octopus Holder 1 | `DIN_Octopus_Holder_1.stl` | 1 | 4,8 | 4,8 |
| DIN Octopus Holder 2 | `DIN_Octopus_Holder_2.stl` | 1 | 4,8 | 4,8 |
| DIN Pi Holder | `DIN_Pi_Holder.stl` | 1 | 11,6 | 11,6 |
| Fan Holder 1 | `Fan_Holder_1.stl` | 1 | 15,5 | 15,5 |
| Fan Holder 2 | `Fan_Holder_2.stl` | 1 | 15,5 | 15,5 |
| Fan Holder 3 | `Fan_Holder_3.stl` | 1 | 15,5 | 15,5 |
| Fan Holder 4 | `Fan_Holder_4.stl` | 1 | 15,5 | 15,5 |
| **Summe** | | 29 | | **480,4** |

Alle platzierten Druckteile zusammen: **841,8 cm³**.

Nicht platziert (nur STL, nicht in der Summe): `Side Panel Fan60`.
