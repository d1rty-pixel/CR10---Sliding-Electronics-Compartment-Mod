# Konstruktion

Stand 2026-11-03 (HANDOFF STAND 15). Alle Maße in mm, Weltkoordinaten des IngeTrazo-Dokuments (Dokument selbst in m). Codekonstanten gewinnen gegen Prosa. Kaufteile: `docs/COMPONENTS.md`.

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

Nicht gedruckt (Kaufteile): Profile, Schienen, Hutschienen, Alu-Eckverbinder (Druckguss), Original-Panelclips.

## Tray-Layout entlang x (hohe-Y-Seite, Tray innen X −379..31)

| Element | X | Y | Z | Anmerkung |
|---|---|---|---|---|
| LRS-350-24 (Vendor/Platzhalter) | −373,75..−158,75 | 475..590 | 25..55,9 | Klemmen +X; 5,05 mm zum Auszugrahmen (X −378,8); DIN-Wiegen bei X −348,75/−183,75 (20 breit) |
| Power-Hub (Basis) | −158,25..−49 | 475..604 | 5..58 | rot Y 557..604, gelb Y 475..557 |
| RS-15-5 | −48,5..26,06 | 530,8..581,8 | 25..53 | Klemmen −X; 2 Wiegen X −35,5..−23,5 / −4..8 (zweite bleibt auf den Schienen, Ende X 9), Y 528,8..583,8; 5,14 mm bis Querholm (X 31,2) |
| 4 × Lüfter 60 × 60 × 25 (Kaufteil, Dokument, San Ace 9LG0624P4H001) | 31,2..56,2 | Mitten 367 / 433,5 / 500 / 566,5 (je ±30) | 25..85 | stehen auf dem Querholm, Achse X, blasen −X ins Tray; Modelle `Luefter 60x60x25 #1..4` (Layer `Electronics (neu)`, Mesh aus `gen/fan_model.py`, Litzenaustritt nach +Y); die alten `… Nabe`-Gruppen liegen auf `Electronics (Platzhalter)` |
| `Fan Holder 1..4` (gen, `tray.fan_holder()`) | 51,2..61,2 | je 62 breit, 336,0..597,5 (Raster 66,5) | 7..85 | siehe „Lüfterhalter“ |
| BTT Octopus | −200..−40 | 352..452 | PCB-Unterkante 31 | hinten, direkt im Luftstrom der Lüfter 1/2 (Motortreiber); Einspeisung/Heizer +X oben, USB-C +X unten, Motor/Sensor unten (ungefähr, ungeprüft); DIN-Halter X −195/−45 (`tray.OCTO_X0`) |
| Raspberry Pi 4 | −335..−250 (Ports bis ca. −338) | 374..430 (Lochmitte 402 = R2) | PCB-Unterkante 31 | vorn, um 180° gedreht (2026-11-03): Ports −X zum Auszugrahmen (−378,8, ca. 41 mm für Stecker), USB-C +Y, GPIO −Y; 50 mm bis zum Octopus; Halter X −315..−250 unter dem Lochende (`tray.PI_X0`, `PI_HOLDER_X0`) |
| DC-Kanal (gelb) | −300..−45 | Mitte 463 (453..473) | 5..25 | 20 × 20, Deckel über volle Länge, Fingerschlitze (Raster 10) |
| Datenkanal (grün) | −300..−35 | Mitte 340 (330..350) | 5..25 | vom Austritt der breiten Kette (X −56..−38, Y 330) nach vorn zum Pi; offenes Vorderende |
| Hutschiene R1a (Power A, 370 mm) | −361,5..9 | Mitte 527 (509,5..544,5) | 5..12,5 | LRS-350, gelbe Hub-Box, RS-15-5 (`tray.RAIL_A`) |
| Hutschiene R1b (Power B, 370 mm) | −361,5..9 | Mitte 577 (559,5..594,5) | 5..12,5 | LRS-350, rote Hub-Box, RS-15-5 (`tray.RAIL_B`). Abstand A/B 50: Riegelende A 553,7, Haken B ab 557,3. B ist durch die rote Box festgelegt (Haken und Riegel innerhalb Y 557,1..604). Schwerpunkte LRS 532,5 und RS 556,3 liegen zwischen den Schienen |
| Hutschiene R2 (Logik, 280 mm) | −320..−40 | Mitte 402 (384,5..419,5) = Octopus-Mitte | 5..12,5 | unter Pi (vorn) und Octopus (hinten), beide mittig darüber |
| PE-Öse Tray | −74..−50 | 615 (auf 2020) | ca. 26 | siehe PE-Erdung |
| PE-Öse Rahmen | 525 | 570 | – | siehe PE-Erdung |

**Lüfterhalter** (`tray.fan_holder(yc)`, 4 gleiche Teile, eins pro Lüfter, 15,5 cm³, vorher 24,5; T-028): Die Lüfter stehen auf dem Querholm `2020 L=334 #1` (X 31,2..51,2, Z 5..25): Auslassfläche bündig mit der Holmvorderseite (X 31,2), Lüfter X 31,2..56,2, Z 25..85. Grund: Der Schrittmotor `Stock Frame/Group#4` (X 472..514, Y 392..463, ab Z 77,9) bleibt, wo er ist (Nutzer). Eingefahren (Hub 396) enden Lüfter, Halteroberteil und M4-Muttern bei X 461,4, also vor dem Motor (Check < 472). Der Halter ist nur an der Rückseite des Holms verschraubt, mit 2 × M5 in der hinteren Nut (Z 15, Y ±18 um die Lüftermitte). Unten verschrauben geht nicht, der Holm liegt auf der Wannenplatte `Gruppieren#15` (Z 0..5). Aufbau (ein Schnitt in X/Z, 62 breit in Y): Distanzblock hinter dem Holm (X 51,2..56,2, Z 7..25), der auch die 5 mm Lüfter hinter dem Holm trägt; Platte an der Ansaugseite (X 56,2..61,2, Z 7..85) mit achteckiger Öffnung (Innenkreis Ø57 = Lüfterbohrung **(Annahme)**, flache Oberkante für den Druck) und 4 × Ø4,5 auf 50 × 50. Keine Kabelablage (Nutzer), der Halter endet hinten an der Platte (X 61,2). Lüfter: 4 × M4 × 35 von der Auslassseite durch beide Flansche und die Platte, Mutter + Scheibe hinten auf der Platte. Die Schraubenköpfe am Auslassflansch von Lüfter 4 haben ca. 2 mm zum RS-15-5 (endet X 26,06, Z 25..53). Die 4,5-mm-Spalte zwischen den Haltern nehmen die Lüfterlitzen auf (Austritt +Y), sie werden hinter der Platte frei verlegt. Die M5-Köpfe (Z 10,75..19,25) sitzen hinten auf der Platte, frei zugänglich. Gedruckt flach auf der Plattenrückseite (78 × 62 × 10, Block oben), Löcher senkrecht, ohne Support. Grenzen: Die Kettenspuren Y 290..330 (Obertrum ab Z 80,7) und 603..627 bleiben frei. Oberkante Z 85; der ortsfeste Kanal der dünnen Kette (Z 86,5, Y ab 573,4) liegt beim Fahren über Lüfter 4 und Halter 4: **nur 1,5 mm Luft**. Die Checks prüfen Lüfterkörper gegen alle Druckteile, Halter in Y 330,4..603 bei Z ≤ 85 und die eingefahrene Lage gegen den Motor.

DIN-Teile (`tray.py`, Clips für EN 50022 35 × 7,5, Rail-Oberkante Z 12,5): `DIN PSU24 Cradle 1/2` (20 breit), `DIN PSU5 Cradle 1/2` (12 breit, X −35,5..−23,5 und −4..8), `DIN Octopus Holder 1/2` (Balken unter einer Lochspalte, Lochraster 150 × 90), `DIN Pi Holder` (Löcher 58 × 49, M2,5). Clips (`tray._clip_cs`, alle aus einem Code): feste Nase −Y, gefederter Schieber +Y, **alle Riegel zeigen nach +Y**, damit sich benachbarte Halter nicht gegenseitig blockieren. Schieber (Print-in-Place, ein Körper): Nase 1,3 unter dem Flansch, Rampe zum Aufrasten, Mäanderfeder aus 3 Stegen 0,6 (Spalt 0,5) an einem Pfosten des Clips, Schieber 0,4 unter der Clipbasis; Riegelseite bis +26,7 ab Schienenmitte (`LATCH_END`). Lösen: Schlitz von oben (`RELEASE` +18,8..+22,6 ab Schienenmitte, 5 lang in X), Schraubendreher in die Kerbe, Schieber 1,5 nach +Y hebeln; ein Stift ≤ 1,4 in den entstehenden Spalt (Schlitzkante −Y / Kerbwand) hält ihn offen, so lassen sich Halter mit 2 Clips nacheinander entriegeln. LRS-Wiegen und RS-Wiege je 2 Clips (A + B). Lösen der Wiegen erst nach Abnahme des Netzteils (Schlitze A unter dem Gerät; Schlitz B der LRS-Wiegen bei Y 595,8..599,6 frei). Pi-Halter: Clips 14 breit, Schlitze X −305 / −260 (neben den Domen). Hub: rote Box auf R1b, gelbe auf R1a, je 2 Clips, keine Bodenschrauben. Eigene Lüfter für Pi und Octopus gibt es nicht mehr (2026-11-03 gelöscht).

Farbe der Druckteile = Filament: rot 230 V, gelb 24/5 V, grün Daten/Bus, dunkelgrau DIN-Halter; Ketten blau (`CHAIN_COL`), Paneele orange, `IEC Housing` rot.

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

Beide Netzteile haben die AC/DC-Klemmengrenze auf **Y 557** (`Y_DIV`). Zwei getrennte Boxen (rot Netz +Y, gelb DC −Y, je einfarbig), jede mit eigener Wand auf der Grenze: Doppelwand gelb Y 555,3..556,9 (`YW`), rot 557,1..558,7 (`RW`), 0,2 Spalt. Jede Box sitzt auf ihrer eigenen Hutschiene (rot R1b, gelb R1a) mit 2 vollen Clips (`tray.hub_base`, X −152,25..−138,25 und −69..−55, innerhalb der R-6-Eckbögen) und hat eigene Deckelschrauben; keine Verbindung nötig. Lösen: Deckel ab, Schraubendreher durch die Bodenschlitze (X −143,75..−138,75 und −68,5..−63,5; rot Y 595,8..599,6, gelb Y 545,8..549,6). Netzteillagen per `LRS_DX` −9,75 / `RS_DX` +14,5 gegen die STEP-Lage (Nutzer 2026-11-03: beide Netzteile ca. 5 mm an die Tray-Kante, damit die Boxen länger werden und die Verdrahtung einfacher; binär exakte Werte, −9,8/+14,6 erzeugten in IngeTrazo Kanten der Länge 0 an den Deckeln). Basis X −158,25..−49 (0,5 Spiel zum LRS-Gehäuseende −158,75 und zum RS-Block −48,5), Boden Z 15,9..17,5 auf den Clips, Wände bis Z 58 (`Z_TOP`), Boden/Wand 1,6 (`T`).

| Teil | Wert |
|---|---|
| Mains Hub Base/Lid (rot) | Y 557,1..604 (`Y_RED`; 2020 des Trays ab 605) |
| DC Hub Base/Lid (gelb) | Y 475..556,9 (`Y_DC`; DC-Kanal bis 473) |
| WAGO-Taschen (`wago_slots()`) | stehend an der roten Wand, Y 558,9..567,2, Z 17,5..36,1, Einführung oben, Hebel +Y; L X −140,775..−122,075; N −120,675..−101,975; PE −91,375..−66,475 (Lücke `SEAM_GAP` 8 für den Wand-Dom); freie Rippen (1,2) mit Fußlippen und Rastnasen |
| WAGO-Breiten (`WAGOS`) | L/N 221-413: 18,7 (Tiefe 18,6, Dicke 8,3); PE 221-414: 24,9 (angenommen) |
| Eingang 230 V Kette (`ENTRY`) | +Y-Wand X −109..−94 ab Z 27, Kabelbinder-Zugentlastung innen |
| PE-Schlitz (`PE_SLOT`) | X −80..−74 (Z 22) zur Tray-Öse; 2026-11-03 von X −86..−78 verschoben, weil dort nur 2,8 mm bis zum beweglichen Kettenbügel (`Thin Bracket Moving` bis X −80,8, ab Y 605) frei waren (Ader Ø 3) |
| DC-Fenster (`DUCT_WIN`) | −Y-Wand X −140..−72, Z 17,5..25 (ab Hub-Bodenoberkante), auf die Fingerschlitze des DC-Kanals (Z 16..25) |
| Lüftungsschlitze (`vent_slots()`) | senkrechte Streifen 2,5 breit, Raster 5, in beiden X-Wänden beider Boxen (rot 12, gelb 26); Z 19,5..54 (unter der Deckellippe), unter den Klemmen-Ausschnitten nur bis `wire_z` − 2; 1,5 Steg zu Ausschnitten, Eck-Domen und Grenzwand. Luftweg: Lüfter hinter dem RS-15-5 bläst −X, Eintritt durch die +X-Wände (frei neben dem RS: gelb Y 486..530, rot Y 582..592), Austritt durch die −X-Wände auf das LRS-350. Wirkung nicht berechnet oder gemessen |
| Deckel | 1,6, Port-Hauben über beide Klemmblöcke (LRS bis X −177,75, RS bis X −33,5), Schürzen auf die Gehäuse, je Deckel eigene Grenzschürze auf `RW` bzw. `YW` bis Z 49 (LRS) / 44,2 (RS); Blitz graviert |
| Befestigung | je Deckel 3 M3 mit vollen Bohrungen, alle Dome im eigenen Teil: 2 Eck-Dome (r 4, konzentrisch zum Eck-Radius `R_BASE` 6, voll mit den Außenwänden verbunden) + 1 Wand-Dom (`wall_boss`, r 3,5, X −96,675; rot Y 560,7 in der Lücke N/PE, gelb Y 553,3); keine Bodenschrauben |
| Klemmblock LRS (Code) | X −175,85..−161,25, Y 498,5..585,5; Oberkante Gehäuse 55,9; `wire_z` 30 = Oberkante der abgesenkten Hub-Wand vor den Klemmen (Leitereintritt Z ca. 36) |
| Klemmblock RS (Code) | Y 540,9..580,6, `block_x` −37,5, Oberkante Block 43,7 / Gehäuse 53,0; `wire_z` 29 = Oberkante der abgesenkten Hub-Wand (Leitereintritt Z ca. 33) |

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
- Der Kettenanschlag sperrt nur Biegen nach außen (Hochbiegen), nicht das Durchhängen; Durchhang des freien Obertrums (breit ca. 217 mm) offen.
- Hersteller-Modelle sind Referenzgeometrie; Kollisionen zwischen ihnen und Druckteilen wurden vom Nutzer bewusst ignoriert (STAND 14).
