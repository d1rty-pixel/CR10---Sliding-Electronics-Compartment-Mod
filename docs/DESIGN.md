# Konstruktion

Stand 2026-11-04 (HANDOFF STAND 15). Alle Maße in mm, Weltkoordinaten des IngeTrazo-Dokuments (Dokument selbst in m). Codekonstanten gewinnen gegen Prosa. Kaufteile: `docs/COMPONENTS.md`.

## Koordinatensystem

- **x** entlang der Auszugsrichtung. Der Auszug fährt nach −x heraus. Frontplatte außen x −399 (innen −383), Rahmenrückfläche x 515–535, Außenfläche der Rückplatten x 534,7. Tray-Innenraum x −379..31.
- **y** quer. Rahmenbreite 258–658 (Außenkanten der Eckpfosten). Zellen Y 278–438 (`left`, Mitte 358) und Y 478–638 (`right`, Mitte 558), je 160 breit, Mittelpfosten Y 438–478. „Hohes Y“ = rechte Seite (Schalter, dünne Kette, Netzteile).
- **z** oben. Unterkante Füße −25, untere Schiene 5–25, **Zelle 25–105 (80 mm, Mitte ZC 65)**, obere Schiene 105–125. Vor dem Umbau war die Zelle 25–80. Tray-Boden (Oberkante) Z 5.
- Tray-/Kettenmaße gelten für den voll ausgefahrenen Auszug, sofern nicht anders genannt. Verfahrweg 396 (`TRAVEL`, abgeleitet, nicht bestätigt).

## Rahmen, Zellen, Profile

Profile sind Kaufteile (20×20 / 20×40, „Profil Typ B Nut 6“, Nut 6, M3-Nutensteine), nur im Dokument, benannt `<Typ> L=<mm> #n`. Zellenumbau auf 80 mm: oberer Aufbau (+25 Z), Eckpfosten und Seitenpaneele (Hex) per Instanz-Xform gestreckt, Frontgitter/Platten/Anschlüsse +12,5 Z, Zierrahmen Z 25–105 (Fenster Z 42,5–87,5; vorn seit T-025, hinten seit T-026 durch Hex-Paneele ersetzt). Alte Ringe `#45/#52/#37` nur ausgeblendet.

| Baugruppe (Top-Level) | Layer | Inhalt |
|---|---|---|
| `Stock Frame` (ex `Group#64`) | `Stock Frame` | Original-CR10-Rahmen, unverändert: 2040 L480 ×4, 2020 L400 ×4, 2040 L563 ×1, 2020 L320 ×1 |
| `Mod Frame Base` (ex `Gruppieren#11`) | `Mod Base` | fester Unterbau: 2040 L80 ×7, 2020 L400 ×1, 2020 L500 ×2 |
| `Mod Frame Drawer` (ex `Gruppieren#36`) | `Mod Drawer` | Auszug/Tray: 2020 L334 ×1, 2020 L80 ×2, 2040 L80 ×1, 2020 L400 ×2, 2040 L410 ×1, 2020 L410 ×1; Wannenplatte `Gruppieren#15` (Material unbekannt) |
| `Stock Foot` (ex `Gruppieren#2`, 1–4) | `Stock Feet` | Original-Füße, später am Mod-Rahmen anschrauben |

Alte Layer `Mod Frame`/`CR10 - Frame` bleiben unberührt und unsichtbar. Die weißen Kabelkanäle im Drawer (25×25, `Gruppieren#30` ×3, `#33`, `#26`, `#25`, `#7`) wurden gelöscht. Schrauben und Nutensteine sind nicht im Modell. Stückliste: `docs/BOM.md`.

Wichtige Profile am Tray (Welt): `2040 L=410 #1` (X −379..31, Y 290–330, Z 5–25, Spur der breiten Kette); `Mod Frame Drawer/14: 2020 L=410 #1` (X −379..31, Y 605–625, Z 5–25, Spur der dünnen Kette, Mitte Y 615); Querholm `2020 L=334 #1` (X 31–51, Y 291–625, Z 5–25); hinten unten `2020 L=400 #1` (X 515–535, Y 258–658, Z 5–25) und oben `Stock Frame/5: 2020 L=400 #2` (X 515–535, Z 105–125). Acrylplatte Z 102–105 (von unten in die Profile geschraubt) bis Y 638; darüber `2040 L=480 #4` (Y 618–658, Schrauben von oben nur bei Y < 618) und Quer-2020 X 425–445.

## Auszugsschienen (Kaufteil, nur im Dokument)

Dreiteilige Vollauszug-Schubladenschienen, je 450 lang, je Seite eine. **Nicht im Generator.** Layer `Schienen (gen)` ist nicht generiert, der Import fasst ihn nicht an. Nicht verwechseln mit MGN12 (`Group#65/#68`, Layer `Mechanics`, gehören nicht zum Modell).

- Nah (niedriges Y): Komponente `Auszugschiene` mit Gruppen-Xform (−91,859 / +179,472 / −18,734); Outer x 16,9..466,9, z −6,1..36,1, Rücken bei niedrigem Y am Rahmen. Mitglieder-Xformen Middle x −198, Inner x −396 (Auszug ausgefahren 396, Mitte halber Hub, geschätzt; eingefahren beide 0).
- Fern: drei normale Gruppen `Auszugschiene Fern Outer/Middle/Inner`, exakte Spiegelung von Nah (y′ = 915,6 − y, kein z-Versatz). Fern folgt bei Fahrt nur per Hand/Skript (gleiche x-Verschiebung). Ferne Schiene: Outer Y 627–638 (Z bis 36), Inner Y 627–633.
- Bestätigt (Nutzer): Nah und Fern sitzen richtig, Inner berührt den Auszug, Outer das äußere untere Rahmenprofil; wenige mm Luft zum unteren Profil bewusst; 6-mm-Versatz der alten `#49/#38` gewollt (Montagelöcher mittig).
- Schraublöcher Ø5,5 (M5, Nutenstein): Outer mittig (x 241,9, z 15, Y 277,8–279,8), Inner mittig (lokal x 333,8 = −154,1 bei Hub 396, z 15); Middle ohne Loch. Alle Kanten 2 Flächen.
- Alte Schienen `Gruppieren#49/#38` (Y 278–289 / 626–638) ausgeblendet. Sicherung der Schienen-Geometrie aus dem Dokument: `gen/data/auszugschiene_raw.json` (Komponente `Auszugschiene` mit Outer/Inner/Middle samt Xform und die drei Fern-Gruppen; Polygone lokal in mm, Xform spaltenweise in m; neu exportiert 2026-11-03, von keinem Code gelesen).

## Blenden, Plugs, Paneele (Generator `cr10mod.py`)

Lokales Druckkoordinatensystem: u, v quer, h von der Außenfläche nach innen; STL liegt mit der Außenfläche auf dem Bett, kein Support.

| Parameter | Wert |
|---|---|
| Rear Panel Switch | 159,5 × 79,5, `hex_panel()` wie Front Panel Hex; massives Pad 80 × 44 × 3 (`REAR_PAD` ±40/±22) um den IEC, Ausschnitt + Tasche auf 1,0; 4 × M3 versenkt (Ø3,4 / Kopf Ø6,6) bei u `IEC_U` ± 34, v ±12; 24,1 cm³ |
| Rear Panel Connector | 159,5 × 79,5, `hex_panel()`; massives Band u −66,3..63, v ±14 (`CON_BAND`), 2 dick wie das alte Deckblech, Rand 2 breit auf 3; GX16 + 4 Keystones wie bisher; 25,0 cm³ |
| IEC Housing | separates rotes Teil hinter dem IEC: innen 55 × 36 (`HS_IN`), Wand 2,5, Rückwand außen X 484 (`HS_BACK_X`); 31,0 cm³ |
| Keystone-Ausschnitt | 14,6 × 19,2, Raster 24 (`SEG`), 4 Plätze |
| GX16-4 | Loch Ø16,2 |
| Hex-Raster (Original `Gruppieren#46`) | Flat-Top, Schlüsselweite 17,32, Eckenradius 1,7, Raster 19,4 (Steg 2,1), `HEX_SHIFT` (4,0) gegen Splitter < 0,1 mm |
| Side Panel Hex | 199,5 × 79,5, Rahmen 5 mm (`PANEL_RIM`), Hexfeld 2 mm dick (`GRID_T`), gemeinsamer Code `hex_panel()` mit dem Frontpaneel; 4 Instanzen: `SIDE_X0` a 55 / b 295, Länge 200 |
| Side Panel Fan60 | nur STL: 60-mm-Lüfter Ø57, 4 × Ø3,4 auf 50 × 50; Hexe im Radius 48 entfallen; nirgends platziert (Lüfterposition offen) |
| Front Panel Hex | 159,5 × 79,5 (`FRONT_PANEL_W` = `CELL_W` − 0,5), sonst wie Side Panel Hex (Rahmen 5, Hexfeld 2, Dicke 3), Gitter mittig (`FRONT_HEX_SHIFT` (0, 0), splitterfrei), Laschen auf den Bezel-Lagen (±40); 2 Instanzen vorn links/rechts. Ersetzt Bezel Ring + Front Grille vorn (T-025), 15,4 cm³ je Teil |

**Rückwände** (`place_rear`, T-026): je Zelle ein Teil statt Bezel Ring + Plug, Laschen der Cover Mounts unverändert auf ±40 (Z 25/105, Check). `Rear Panel Switch` auf `CELL_YC["right"]` (Y 478,2–637,8, IEC-Mitte Y 553,4 = 558 − `IEC_U` 4,6, Z 65); `Rear Panel Connector` auf `"left"` (Y 278,2–437,8): GX16-4 (Y 308) plus 4 Keystones (RJ45, USB, USB, Blind; Y 341/365/389/413). Netzschalter auf der Seite der dünnen 230-V-Kette. Die übrige Fläche ist Hexfeld (Lufteinlass für die 4 Lüfter). Hexe, deren Hüllrechteck das Pad bzw. Band berührt, entfallen ganz (`hex_exclude`), damit kein Hex angeschnitten wird (Near-Vertex-Check). Vorher: rechts Ring 21,6 + Plug 30,2 cm³, links 21,6 + 17,3 cm³.

**Rear Panel Switch / IEC-GS-1-100** (Snap-in, keine Schrauben): Ausschnitt `IEC_CUT` 47 × 27,8 R2 (+2·FIT), `IEC_WALL` 1,0 (Pad in der Tasche auf 1,0 gedünnt), `IEC_RECESS` 53 × 34 (Haken ±15,3 + Federweg). Rastkraft auf gedrucktem 1,0-mm-Rand ungetestet.

**IEC Housing** (`iec_housing()`, rot = 230 V, Berührschutz der Flachstecker): offen zum Panel, liegt auf dem Pad (X 531,7), Rückwand X 484..486,5. Innen u ±27,5 / v ±18 um `IEC_U`, damit IEC-Körper samt Haken und Flachsteckern (bis X 507,2) frei sind (Check); hinter den Steckerspitzen 20,7 mm für Flachsteckhülsen. 4 Ohren (8 × 9 × 9) mit Gewindeeinsatz M3 (Bohrung Ø4,0 × 7, **Annahme** Einsatz M3 × 5,7), verschraubt von außen durch das Panel (M3 Senkkopf), 45°-Stütze unter jedem Ohr. Rückwand: Kabeleinführung Ø8 für den 230-V-Mantel (7,3) bei Y 553,4 / Z 73 und 2 Kabelbinderschlitze 2 × 4,5 bei ±7,5 als Zugentlastung **(ungetestet)**. Boden: Ø4,5 für die PE-Litze bei Y 570 / X 519, senkrecht über der Rahmen-Öse. Montage: Mantel durch die Einführung, Hülsen auf den IEC, IEC von außen einrasten, Gehäuse aufsetzen und verschrauben. Gedruckt auf der Rückwand, ohne Support. Checks: IEC-Körper frei, Abstand zu den eingefahrenen Lüfterhaltern (X 457,2) 26,8 (≥ 3), Z 44,5..85,5.

**Cover Mount** (gemeinsame Komponente `cover_mount()`): exakte Kopie des Originalteils `Side Cover - Mount` (131 Eckpunkte, 963 mm³, Lasche 19,7 × 13 × 5, Senkung Ø7 × 1, Loch Ø4), Mesh und vier Lagen in `gen/data/side_cover_mount.json`. Rückwände und Frontpaneele übernehmen die Lagen der früheren Bezel-Ringe (±40), Seitenpaneele schieben sie 20 mm nach außen (±60, `MT_SIDE_SHIFT`). Wurzel 0,5 mm im Teil (`MT_OVERLAP`, damit es verschmilzt), `MT_ROOT_FIX` −0,3. Laschen liegen immer auf Z 25 bzw. 105 (Check). Die Originalclips sind Panelhalter (Kaufteil).

Nicht gedruckt (Kaufteile): Profile, Schienen, Hutschienen (Anzeigemodell aus `gen/rail_model.py`, Profil und Annahmen in `docs/COMPONENTS.md`), Alu-Eckverbinder (Druckguss), Original-Panelclips.

## Tray-Layout entlang x (hohe-Y-Seite, Tray innen X −379..31)

| Element | X | Y | Z | Anmerkung |
|---|---|---|---|---|
| LRS-350-24 (Vendor/Platzhalter) | −373,75..−158,75 | 475..590 | 25..55,9 | Klemmen +X; 5,05 mm zum Auszugrahmen (X −378,8); DIN-Wiegen bei X −348,75/−183,75 (20 breit) |
| Power-Hub (Basis) | −158,25..10 | 475..604 | 5..58 | rot (230 V) X −158,25..10 auf Y 557,1..604 plus Tasche X −15,75..10 ab Y 538,36; DC X −158,25..−42,55 auf Y 475..556,9 plus Tasche X −42,55..−15,95 ab Y 538,36 (seit T-033) |
| RS-15-5 | −42,05..9,05 | Gehäuse 475,5..538,16, Klemmblock bis 550,06 | 25..53 | um 90° im Uhrzeigersinn gedreht (T-033, Nutzer 2026-11-04): Klemmen +Y in die Hub-Taschen, Pins entlang X (+V −27,3, −V −19,7, FG −12,0, N −4,4, L 3,2); 2 Wiegen X −41..−27 / −11..3 nur auf R1a; 1,15 mm bis zur +24-V-Spur (X 10,2) |
| 4 × Lüfter 60 × 60 × 25 (Kaufteil, Dokument, San Ace 9LG0624P4H001) | 31,2..56,2 | Mitten 367 / 433,5 / 500 / 566,5 (je ±30) | 25..85 | stehen auf dem Querholm, Achse X, blasen −X ins Tray; Modelle `Luefter 60x60x25 #1..4` (Layer `Electronics (neu)`, Mesh aus `gen/fan_model.py`, Litzenaustritt unten, alle um 90° gedreht, Nutzer 2026-11-03); die alten `… Nabe`-Gruppen liegen auf `Electronics (Platzhalter)` |
| `Fan Holder 1..4` (gen, `tray.fan_holder()`) | 51,2..61,2 | je 62 breit, 336,0..597,5 (Raster 66,5) | 7..85 | siehe „Lüfterhalter“ |
| BTT Octopus | −200..−40 | 352..452 | PCB-Unterkante 22,5 (`tray.BOARD_Z`) | hinten, direkt im Luftstrom der Lüfter 1/2 (Motortreiber); Einspeisung/Heizer +X oben, USB-C +X unten, Motor/Sensor unten (ungefähr, ungeprüft); DIN-Halter X −195/−45 (`tray.OCTO_X0`) |
| Raspberry Pi 4 | −335..−250 (Ports bis ca. −338) | 374..430 (Lochmitte 402 = R2) | PCB-Unterkante 22,5 | vorn, um 180° gedreht (2026-11-03): Ports −X zum Auszugrahmen (−378,8, ca. 41 mm für Stecker), USB-C +Y, GPIO −Y; 50 mm bis zum Octopus; Halter X −315..−250 unter dem Lochende (`tray.PI_X0`, `PI_HOLDER_X0`) |
| DC-Kanal | −300..−45 | Mitte 463 (453..473) | 5..30 | 20 breit, 25 hoch (`DUCT_H`, wie alle Kanäle, Deckel bis 31,6, Nutzer 2026-11-03), beide Enden offen, Deckel über volle Länge, Fingerschlitze (Raster 10); +Y-Wand unter der Rutsche der gelben Box ausgespart (X −140,2..−71,8 ab Z 15,7), Deckel dort ohne +Y-Lippe (T-032) |
| `Fan DC Duct` (T-032, +24 V/GND) | −54,8..20,5 | Stich 453..473, Spur X 10,2..20,5 auf Y 350,3..604 | 5..30 | T-Stück: Stich vom hinteren DC-Kanalende (Steckzunge 10 lang hinein) mit Ausrundungen R 6 in die Spur vor den Lüftern; −Y-Ende als Bogen um den PWM-Bogen (konzentrisch, R 11,8 um X 8,7 / Y 362, tangential in die +X-Wand, 0,2 Fuge), +Y-Ende geschlossen bei 604 (seit T-033); siehe „Lüfterkanäle“ |
| `Fan Data Duct` (T-032, PWM/Tacho) | −44,8..31,0 | Arm 330,5..350, Spur X 20,7..31,0 auf Y 330,5..604 | 5..30 | L-Stück: Arm vom hinteren Datenkanalende (Steckzunge) mit 90°-Bogen (außen R 13, innen R 12) in die Spur am Querholm, +Y-Ende geschlossen bei 604 (seit T-033) |
| Datenkanal | −300..−35 | Mitte 340 (330..350) | 5..30 | vom Austritt der breiten Kette (X −56..−38, Y 330) nach vorn zum Pi; offenes Vorderende; Deckelfenster X −58..−37 über dem Austritt der breiten Kette (offen von −Y, 4-mm-Steg an +Y) |
| Hutschiene R1a (Power A, 370 mm) | −361,5..9 | Mitte 510 (492,5..527,5) | 5..12,5 | LRS-350, DC-Hub-Box, RS-15-5 (`tray.RAIL_A`); seit T-033 von 527 nach 510 verschoben, damit das Riegelende (536,7) unter dem RS-Gehäuse bleibt und nicht unter den Hub-Taschen (ab 538,36) |
| Hutschiene R1b (Power B, 370 mm) | −361,5..9 | Mitte 577 (559,5..594,5) | 5..12,5 | LRS-350, rote Hub-Box (`tray.RAIL_B`). B ist durch die rote Box festgelegt (Haken und Riegel innerhalb Y 557,1..604). Schwerpunkt LRS 532,5 liegt zwischen den Schienen; das RS-15-5 steht nur auf A |
| Hutschiene R2 (Logik, 280 mm) | −320..−40 | Mitte 402 (384,5..419,5) = Octopus-Mitte | 5..12,5 | unter Pi (vorn) und Octopus (hinten), beide mittig darüber |
| PE-Öse Tray | −74..−50 | 615 (auf 2020) | ca. 26 | siehe PE-Erdung |
| PE-Öse Rahmen | 525 | 570 | – | siehe PE-Erdung |

**Lüfterhalter** (`tray.fan_holder(yc)`, 4 gleiche Teile, eins pro Lüfter, 15,5 cm³, vorher 24,5; T-028): Die Lüfter stehen auf dem Querholm `2020 L=334 #1` (X 31,2..51,2, Z 5..25): Auslassfläche bündig mit der Holmvorderseite (X 31,2), Lüfter X 31,2..56,2, Z 25..85. Grund: Der Schrittmotor `Stock Frame/Group#4` (X 472..514, Y 392..463, ab Z 77,9) bleibt, wo er ist (Nutzer). Eingefahren (Hub 396) enden Lüfter, Halteroberteil und M4-Muttern bei X 461,4, also vor dem Motor (Check < 472). Der Halter ist nur an der Rückseite des Holms verschraubt, mit 2 × M5 in der hinteren Nut (Z 15, Y ±18 um die Lüftermitte). Unten verschrauben geht nicht, der Holm liegt auf der Wannenplatte `Gruppieren#15` (Z 0..5). Aufbau (ein Schnitt in X/Z, 62 breit in Y): Distanzblock hinter dem Holm (X 51,2..56,2, Z 7..25), der auch die 5 mm Lüfter hinter dem Holm trägt; Platte an der Ansaugseite (X 56,2..61,2, Z 7..85) mit achteckiger Öffnung (Innenkreis Ø57 = Lüfterbohrung **(Annahme)**, flache Oberkante für den Druck) und 4 × Ø4,5 auf 50 × 50. Keine Kabelablage (Nutzer), der Halter endet hinten an der Platte (X 61,2). Lüfter: 4 × M4 × 35 von der Auslassseite durch beide Flansche und die Platte, Mutter + Scheibe hinten auf der Platte. Seit T-033 steht vor den Lüftern kein Netzteil mehr (RS-15-5 endet X 9,05, rote Box X 10). Die Lüfter sind um 90° gedreht (Nutzer 2026-11-03), die Litzen kommen unten aus der Kerbe des Auslassflansches (Lüftermitte, Z ca. 25) und gehen vorn über die Holmkante in die Lüfterkanäle (siehe unten, alle 4 über eine Einführung); die 4,5-mm-Spalte zwischen den Haltern werden dafür nicht mehr gebraucht. Die M5-Köpfe (Z 10,75..19,25) sitzen hinten auf der Platte, frei zugänglich. Gedruckt flach auf der Plattenrückseite (78 × 62 × 10, Block oben), Löcher senkrecht, ohne Support. Grenzen: Die Kettenspuren Y 290..330 (Obertrum ab Z 80,7) und 603..627 bleiben frei. Oberkante Z 85; der ortsfeste Kanal der dünnen Kette (Z 86,5, Y ab 573,4) liegt beim Fahren über Lüfter 4 und Halter 4: **nur 1,5 mm Luft**. Die Checks prüfen Lüfterkörper gegen alle Druckteile, Halter in Y 330,4..603 bei Z ≤ 85 und die eingefahrene Lage gegen den Motor.

**Lüfterkanäle** (`tray.fan_dc_duct()` / `fan_data_duct()` mit Deckeln, T-032): zwei schmale Spuren in Y vor dem Querholm, je 10,3 breit (innen 7,1), Wand 1,6, Boden Z 5..7, Wandoberkante Z 30 (`FD_ZT` = Höhe aller Kanäle), Deckel 1,6 bis Z 31,6. PWM/Tacho X 20,7..31,0 direkt am Holm (0,2 Luft), +24 V/GND X 10,2..20,5 davor, 0,2 Spalt. Die +24-V-Spur beginnt mit einem Bogen konzentrisch zur Innenrundung des PWM-Bogens (`FD_BEND_RI` 12, Radius 12 − Fuge 0,2 = 11,8, tangential zur +X-Wand, trifft die −X-Wand bei Y 350,3), damit auch die Wechselöffnung von Lüfter 1 (Y 367) in ihrer geraden Wand liegt (Check). Beide laufen seit T-033 (RS-15-5 gedreht) bis Y 604 (`FD_Y_END`, 0,8 vor der 2020 des Trays ab 604,8) und sind dort geschlossen; vorher endeten sie offen bei Y 528 vor dem RS. X-Grenzen Hutschienen-Ende X 9,0, rote Hub-Box X 10,0 (0,2 Fuge), RS-Gehäuse X 9,05; Y-Grenze 2040 der breiten Kette (bis 330,4). Lüfterlitzen: alle 4 Lüfter bei Y = Lüftermitte (367 / 433,5 / 500 / 566,5) durch eine Einführung 6 breit mit runder Sohle (Z 20) in der +X-Wand der PWM-Spur, Deckel dort ausgespart. Rot/schwarz wechseln durch fluchtende Schlitze 5 breit (Tiefe 9) in den beiden Innenwänden (Y wie die Einführungen) in die +24-V-Spur. M4-Köpfe der unteren Lüfterschrauben (Y Lüftermitte ± 25, Kopf Ø7 × 4 **(Annahme)**, X 27,2..31,2, Z 26,5..33,5): Aussparungen in +X-Wand und Deckel ab X 27, Y ± 4,5, ab Z 26 (Check). Anschluss an die alten Kanäle: U-Steckzunge (Wand 1,2, 0,2 Spiel, bis Z 24,5 unter die Deckellippen) 10 tief in das offene hintere Ende des DC- bzw. Datenkanals, 0,2 Fuge an den Stirnflächen. Je 4 M3-Bodenschrauben (+24 V: (−20 | 463), (15,35 | 400 / 515 / 585); PWM: (−15 | 340), (25,85 | 400 / 515 / 585)). Deckel mit Lippen und Rastwulst wie die anderen Kanäle (Wulst ohne Rampe, nur eine 0,25-Stufe). Gedruckt auf dem Boden, ohne Support; Fußabdruck 75 × 254 bzw. 76 × 274. Bestehende Überlappung (nicht neu): Datenkanal Y 330 gegen die 2040 bis Y 330,4 laut Bbox-Scan.

**Boards tief** (Nutzer 2026-11-03, statt höherer Kanäle, die die Lüfterauslässe verdecken würden): Octopus und Pi mit PCB-Unterkante Z 22,5 (`BOARD_Z`, vorher 31), Oberkante der Octopus-Stege und der Pi-Platte Z 18 (`HOLDER_TOP`); Luft zu den Bauteilen unter der Platine (Dokument): Octopus 1,4, Pi 2,4. Dome Z 17..22,5, Vorbohrungen 6 bzw. 5,5 tief. Die Fingerschlitze der Kanäle (Z 21..30) liegen damit auf Board-Höhe, J67-Klemmkammern Z 31,5..38,6.

DIN-Teile (`tray.py`, Clips für EN 50022 35 × 7,5, Rail-Oberkante Z 12,5): `DIN PSU24 Cradle 1/2` (20 breit), `DIN PSU5 Cradle 1/2` (14 breit, X −41..−27 und −11..3, nur auf R1a, Anschlag −Y; +Y hält die Taschenwand des Hubs, 0,2 Spiel), `DIN Octopus Holder 1/2` (Balken unter einer Lochspalte, Lochraster 150 × 90), `DIN Pi Holder` (Löcher 58 × 49, M2,5). Clips (`tray._clip_cs`, alle aus einem Code): feste Nase −Y, gefederter Schieber +Y, **alle Riegel zeigen nach +Y**, damit sich benachbarte Halter nicht gegenseitig blockieren. Schieber (Print-in-Place, ein Körper): Nase 1,3 unter dem Flansch, Rampe zum Aufrasten, Mäanderfeder aus 3 Stegen 0,6 (Spalt 0,5) an einem Pfosten des Clips, Schieber 0,4 unter der Clipbasis; Riegelseite bis +26,7 ab Schienenmitte (`LATCH_END`). Lösen: Schlitz von oben (`RELEASE` +18,8..+22,6 ab Schienenmitte, 5 lang in X), Schraubendreher in die Kerbe, Schieber 1,5 nach +Y hebeln; ein Stift ≤ 1,4 in den entstehenden Spalt (Schlitzkante −Y / Kerbwand) hält ihn offen, so lassen sich Halter mit 2 Clips nacheinander entriegeln. LRS-Wiegen je 2 Clips (A + B), RS-Wiegen 1 Clip (A). Lösen der Wiegen erst nach Abnahme des Netzteils (Schlitze A unter dem Gerät; Schlitz B der LRS-Wiegen bei Y 595,8..599,6 frei). Pi-Halter: Clips 14 breit, Schlitze X −305 / −260 (neben den Domen). Hub: rote Box auf R1b, gelbe auf R1a, je 2 Clips, keine Bodenschrauben. Eigene Lüfter für Pi und Octopus gibt es nicht mehr (2026-11-03 gelöscht).

Farbe der Druckteile = Filament (Nutzer 2026-11-03): anthrazit für alle Innenteile (Kanäle, DC-Box, DIN- und Lüfterhalter, `tray.COL_ANTHRACITE`), Themenfarbe orange außen (Paneele, Ketten; `cr10mod.COL`, `CHAIN_COL`), rot nur für 230 V (Netz-Box, `IEC Housing`). Vorher rot/gelb/grün/dunkelgrau, Ketten blau.

## Kabelschleppketten

Zwei Ketten, Obertrum fest an der Acrylplatte (Z 102), Untertrum am Tray, 180-Grad-Bogen vorn (−x). Platz Z 25..102 = 77. Kabel: Lapp ÖLFLEX FD 855 P 3G1,5 (siehe COMPONENTS). Bogenradius der Ketten (breit 24,75, dünn 28,35) liegt unter R_dyn 36,5 des Kabels (Datenblatt ungeprüft, PLAN T-004).

| Parameter | Breit (`cable.py`) | Dünn (`cable_thin.py`) |
|---|---|---|
| Aufgabe | CAN, 24/5 V, Sensoren, USB, Netzwerk | 230 V |
| Spur | Y 290..330, Mitte 310 (2040) | Mitte Y 615 (2020, Spur 605..627), Kette Y 606,1..623,9 |
| Glieder / Teilung | 11 / 29,5 | 12 / 26 |
| Plattenradius (Höhe) | 9 (18) | 7,5 (15) |
| Plattendicke / Spalt Inner-Outer | 3,0 / 0,3 | 1,8 / 0,3 |
| Innenmaß | 27,4 × 12,5 (Balken Z −9..−6,5, Klammersteg ab Z 6) | 10 × 10 |
| Außenbreite | 40 (\|y\| 20) | 17,8 |
| Pivothöhe oben / unten | 87,25 / 37,75 (Bogenradius 24,75; gesucht: Glieder Z 25,2..101,8 in allen Lagen, gerade Trume 96,25 / 28,75) | 91,4 / 34,7 (Bogenradius 28,35) |
| `X_MOVING_EXT` (bewegtes Ende, ausgefahren) | −83,5 | −128,5 (`X_SHIFT` 45) |
| `X_FIXED` (festes Ende, Hubmitte) | 114,5 | 69,5 |
| Anschlag (`STOP_H`) | = R (voll, eckig) | = R (voll, eckig) |
| Gelenk | Zapfen Ø4 hinten, Loch Ø4,4 + Schlitz 3,6 zur Deckelseite; Steg X 14,5..17,5, Balken 2,5 | Steg X 12,5..15,5, Balken Z −7,5..−5,5 |
| Glied | gemeinsamer Code `chain_link.Link` (Schema von `Chain Link (new)`, `chain_link_user.json`), Parametersatz breit | `chain_link.Link`, Parametersatz dünn |
| Klammer (`lid()`) | Bogen 2,0 bündig in Kerbe der Innenplatten (X 9,8..14,2), Arme 1,5, Haken 0,8 in Nut Z 1,5..4,0; ganz in der Gliedhülle | Bogen 1,8 bündig in Nut der Innenplatten (Kerbe X 8,3..12,2), ganz in der Gliedhülle |
| Scharnier-Check | `hinge_sweep`: 0..78° frei (Bogen braucht 73,2), Anschlag bei −1,5° | `hinge_sweep`: 0..60° frei (Bogen braucht 54,6), Anschlag bei −1,5° |
| Druck | Glieder stehend auf dem Balken (Platten senkrecht), Klammer mit dem Bogen auf dem Bett, ohne Support | wie breit |

**X_SHIFT** der dünnen Kette (45 mm nach vorn): ihr Kabelaustritt landet auf dem Power-Hub (Eingang X −109..−94). Bogenfront eingefahren in Tray-Koordinaten −379,0 (Frontplatte −383, nur ca. 4 mm; Check verlangt >= −380 bzw. `DRAWER_FRONT_IN` + 3).

**Endhalter** (Layer `Schlepp (gen)`):
- breit fest: Gabel (`Link.fork`) um Pivot X 114,5 / Z 87,25, Körper ab X +12 (Gegenstück zum Innenplatten-Anschlag), 2 M3 durch die Acrylplatte in Mutterntaschen, Trichter ab Z 83,25, 27 → 16 mm in den (noch nicht gebauten) festen Kanal; für das Kabelbündel zu eng (PLAN T-013). Breit beweglich: Zapfenzunge (`Link.tongue`) auf dem 2040, Körper ab X +9,2 (Gegenstück zur Außen-Anschlagecke), 2 M3 in Hammermuttern (Y 300/320), Kabel in Viertelkurve (Mittellinie R 24 > R_fest 22, Nut 18 breit, Boden Z 31,25 = Balkenoberkante) durch die +y-Fläche in den Datenkanal (X −60..−35), Austritt Z 31,25..46,75.
- dünn fest: Gabel um Pivot X 69,5 / Z 91,4, 2 M3 von oben bei Y 607 (< 618), Tunnel 10 breit. Dünn beweglich: Zunge + Körper auf dem 2020, 2 M3 in Hammermuttern Y 615, Viertelkreis-Nut R 24 / 9,6 breit nach −y; Kabelaustritt X −108..−96, Z 29..39 (zum Hub-Eingang).

## Fester Kanal der dünnen Kette (`Thin Channel`)

Offen oben, unter der Acrylplatte (Boden `CH_ZB` Z 86,5, Oberkante 102), Flansch ±13,5. Pfad: gerade bei Y 615 bis X 380, eine L-Kurve R 30 (`L_R`, Mitte 380/585), Schenkel `X_LEG` 410 nach −Y bis zum offenen Ende `Y_END` 573,4 (= Schalter-Y + 20) mit Bodenrampe; hinterste Wand X 417 (`CH_END_X`). Geteilt bei `CH_SPLIT` 262 (0,2 Spalt): Front 147,9 / Rear 161,4 lang (Bett 300). 5 Schrauben M3 (`CH_SCREWS`): (145 | 235 | 290 | 350, 605,5) und (400,5, 579,4), alle Y < 618 und X < 425. Ab dem offenen Ende läuft das 230-V-Kabel frei (Bogen nach +X, R >= 22, Abstieg zur Kabeleinführung des `IEC Housing` X 484 / Y 553,4 / Z 73). Der Kanal der breiten Kette (Datenkanal unter der Platte bis zum Rear Panel Connector) ist nicht gebaut.

## Power-Hub (`power_hub.py`)

Das LRS-350 hat die AC/DC-Klemmengrenze auf **Y 557** (`Y_DIV`). Das RS-15-5 ist seit T-033 um 90° im Uhrzeigersinn gedreht (Klemmen +Y, Pins entlang X); seine Grenze liegt zwischen FG (X −12,0) und −V (X −19,7) auf **X −15,85** (`XD`). Die Trennwand ist deshalb ein L: Y 557 vom LRS bis X −15,85, dann entlang X bis zur Klemmenseite des RS (`Y_P` 538,36 = RS-Gehäuse 538,16 + 0,2). Zwei getrennte Boxen (rot Netz, DC anthrazit), jede mit eigener Wand auf der Grenze: Doppelwand, 0,2 Spalt (DC Y 555,3..556,9 / X −17,55..−15,95; rot Y 557,1..558,7 / X −15,75..−14,15). Jede Box sitzt auf ihrer eigenen Hutschiene (rot R1b, DC R1a) mit 2 vollen Clips (`tray.hub_clip_x`: rot X −152,25..−138,25 und −10..4, DC −152,25..−138,25 und −62,55..−48,55) und hat eigene Deckelschrauben; keine Verbindung nötig. Lösen: Deckel ab, Schraubendreher durch die Bodenschlitze (rot X −143,75..−138,75 und −9,5..−4,5 auf Y 595,8..599,6; DC X −143,75..−138,75 und −62,05..−57,05 auf Y 528,8..532,6). LRS-Lage per `LRS_DX` −9,75 gegen die STEP-Lage (binär exakt, −9,8 erzeugte in IngeTrazo Kanten der Länge 0 an den Deckeln). Boden Z 15,9..17,5 auf den Clips, Wände bis Z 58 (`Z_TOP`), Boden/Wand 1,6 (`T`).

Der RS-Klemmblock (X −31,96..7,7, Y 538,16..550,06, Z 30,59..43,75) ragt durch die Taschenwand und die L-Trennwand: Ausschnitt X −32,46..8,2, bis Y 550,56, ab Z 30 (`BLK_Z`, 0,59 unter dem Block). Die Deckel schließen ihn mit Schürzen bis 0,5 über den Block (Z 44,25). In den Taschen gibt es keine Dome (Block und Leiter füllen sie); die Taschenecken sind scharf (ein Bogen dort lag < 0,1 mm am Ausschnitt).

| Teil | Wert |
|---|---|
| Mains Hub Base/Lid (rot) | X −158,25..10 (`X1R`; +24-V-Spur ab 10,2) auf Y 557,1..604 (`Y_RED`; 2020 des Trays ab 604,8), Tasche über den AC-Klemmen des RS X −15,75..10 ab Y 538,36; 168 × 47 plus Tasche, vorher 109 × 47 |
| DC Hub Base/Lid | X −158,25..−42,55 (`XR0`, 0,5 zum RS-Gehäuse) auf Y 475..556,9 (`Y_DC`; DC-Kanal bis 473), Tasche über den DC-Klemmen des RS X −42,55..−15,95 ab Y 538,36 |
| WAGO-Taschen (`wago_slots()`) | stehend an der roten Wand (Y 557), mittig auf X −158,25..−15,85, je eigene Rippen, 10 mm Abstand (`W_GAP`, Nutzer 2026-11-04: an der Wand lassen); Y 558,9..567,2, Z 17,5..36,1, Einführung oben, Hebel +Y; L X −130,8..−112,1; N −99,5..−80,8; PE −68,2..−43,3; freie Rippen (1,2) mit Fußlippen und Rastnasen |
| WAGO-Breiten (`WAGOS`) | L/N 221-413: 18,7 (Tiefe 18,6, Dicke 8,3); PE 221-414: 24,9 (angenommen) |
| Eingang 230 V Kette (`ENTRY`) | +Y-Wand X −109..−94 ab Z 27, Kabelbinder-Zugentlastung innen |
| PE-Schlitz (`PE_SLOT`) | X −80..−74 (Z 22) zur Tray-Öse; 2026-11-03 von X −86..−78 verschoben, weil dort nur 2,8 mm bis zum beweglichen Kettenbügel (`Thin Bracket Moving` bis X −80,8, ab Y 605) frei waren (Ader Ø 3) |
| DC-Fenster (`DUCT_WIN`) | −Y-Wand X −140..−72, Z 17,5..29 (ab Hub-Bodenoberkante bis 1 unter den Kanaldeckel) |
| Rutsche (`spout()`, T-032) | formschlüssiger Anschluss an den DC-Kanal unter dem Fenster, X −140..−72: Boden läuft als Viertelrundung R 4 (Mitte Y 473,5 / Z 13,5) über die ausgesparte Kanalwand (Oberkante Z 15,7, Brücke ab Z 15,9) nach innen; Haken Y 469,5..471,2 hinter der Wandinnenfläche (471,4) bis Z 11,8 (3,9 tief, Spitze 45°), Schürze Y 473,2..476,6 vor der Außenfläche (473) bis Z 6 (Druckbett). Spiel 0,2 rundum; sperrt Y in beide Richtungen und X über die Aussparungsenden. Montage: Kanal verschrauben, Box von oben aufclipsen (Haken taucht ein), Deckel zuletzt |
| Lüftungsschlitze (`vent_slots()`) | senkrechte Streifen 2,5 breit, Raster 5, Z 19,5..54 (unter der Deckellippe), unter den LRS-Klemmen-Ausschnitten nur bis `wire_z` − 2; 1,5 Steg zu Ausschnitten, Eck-Bögen, Domen und Grenzwand. Rot: −X-Wand 6, +X-Wand 9 (Y 549,2..589,2, Lüfter 4 bläst darauf); DC: −X-Wand 13 (die +X-Wand liegt am RS-Gehäuse). Wirkung nicht berechnet oder gemessen |
| Deckel | 1,6, Port-Haube über den LRS-Klemmblock (bis X −177,75), Schürzen auf das LRS-Gehäuse, je Deckel eigene Grenzschürze auf `RW` bzw. `YW` bis Z 49; Schürzen über dem RS-Block (Taschenwand und Trennwand); Blitz graviert (rot) |
| Befestigung | je Deckel 3 M3 mit vollen Bohrungen, alle Dome im eigenen Teil: 2 Eck-Dome (r 4, konzentrisch zum Eck-Radius `R_BASE` 6, voll mit den Außenwänden verbunden; rot an der +Y-Wand X −152,25 / 4, DC an der −Y-Wand X −152,25 / −48,55) + 1 Wand-Dom (`wall_boss`, r 3,5, X −74,5; rot Y 560,7 in der Lücke N/PE, DC Y 553,3); keine Bodenschrauben |
| Klemmblock LRS (Code) | X −175,85..−161,25, Y 498,5..585,5; Oberkante Gehäuse 55,9; `wire_z` 30 = Oberkante der abgesenkten Hub-Wand vor den Klemmen (Leitereintritt Z ca. 36) |
| RS-15-5 (Code, `RS_BODY`/`RS_BLOCK`/`RS_PINS`) | aus der alten STEP-Lage per `rs_xy` (x' = y − 572,8, y' = 501,56 − x): Gehäuse X −42,05..9,05, Y 475,5..538,16, Z 25..53; Block siehe oben; Leitereintritt von +Y, Z ca. 33..37 |

Pin-Positionen für die Verdrahtung: `docs/COMPONENTS.md`.

## Verdrahtung (`wiring.py`)

Die modellierten 230-V-Litzen wurden am 2026-11-03 gelöscht (Nutzer): Netzteile und Hub-Boxen haben sich verschoben, die Stützpunkte passen nicht mehr. Neue Routen werden vorerst nicht erzeugt (T-022). `wiring.py` behält Rohr- und Bogen-Code (`fillet_path`, `tube`) und die Checks in `cr10mod.py`; `ROUTES` ist leer, der Layer `Kabel (gen)` bleibt leer.

## PE-Erdung

- **Rahmen-Öse:** M5 im oberen Schlitz der hinteren Base-2020 bei X 525, **Y 570** (Ringöse Y 564..576), zwischen den Mounts der rechten Rückwand (Y 527..588); die PE-Litze kommt senkrecht aus dem Boden des `IEC Housing` (Y 570, X 519). Die frühere Lage Y 594..606 saß im unteren Mount der rechten Rückwand (damals `Bezel Rear Right`, Y 588..604, Z 25..30) und wurde verworfen (Regel unten).
- **Tray-Öse:** X −74..−50, Y 615 auf der 2020 L=410 (Z ca. 26); PE-Leiter vom PE-WAGO durch den PE-Schlitz im Hub.
- PE vom IEC-Einbaustecker zur Rahmen-Öse. PE-WAGO ist 221-414 mit 4 Leitern (Nutzerentscheidung).

## Konstruktionsregeln (aus der Praxis)

- Alle Halterungen entstehen aus **einem** Code und sind identisch. Generierte Halter/Brackets nie anschneiden oder verändern; Kaufteile (Ösen, Kabel) wandern, nie ein Halter. Nichts darf generierte Halterungen schneiden.
- Geometrie nur im Generator ändern, nicht in IngeTrazo. Kaufteile nur im Dokument.
- `build --check` prüft: jedes Teil manifold und ein Körper, keine Eckpunkte < 0,1 mm Abstand (IngeTrazo verschmilzt sie), keine Kollision zwischen allen zusammengebauten Teilen (exaktes Boolean-Volumen), Lagen/Fensterchecks. Gegen das Dokument nur per Bbox/Koordinatenscan.
- Berührende Körper bleiben bei manifold3d getrennt: 0,05 überlappen. Exakte Bögen (`_rounded()`) statt `offset()`-Rundung und Kreisen an Wänden; Grundkörper als ein Block minus Hohlraum; Deckelaussparungen in 2D; Extrusion aus einem 2D-Schnitt statt Vereinigung koplanarer Flächen (Splitter-Vertices).
- Nutzerkomponenten (`Chain Link (new)`, 2 Instanzen im Dokument) bleiben unberührt; der Import überspringt Namen mit „(new)“.
- Der Kettenanschlag sperrt nur Biegen nach außen (Hochbiegen), nicht das Durchhängen; Durchhang des freien Obertrums (breit ca. 217 mm) nicht auf voller Länge getestet; 3 gedruckte Glieder hängen nicht durch, Nutzer verzichtet auf den Test (2026-11-04).
- Hersteller-Modelle sind Referenzgeometrie; Kollisionen zwischen ihnen und Druckteilen wurden vom Nutzer bewusst ignoriert (STAND 14).
