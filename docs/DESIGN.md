# Konstruktion

Stand 2026-11-03 (HANDOFF STAND 15). Alle Maße in mm, Weltkoordinaten des IngeTrazo-Dokuments (Dokument selbst in m). Codekonstanten gewinnen gegen Prosa. Kaufteile: `docs/COMPONENTS.md`.

## Koordinatensystem

- **x** entlang der Auszugsrichtung. Der Auszug fährt nach −x heraus. Frontplatte außen x −399 (innen −383), Rahmenrückfläche x 515–535, Außenfläche der Rückplatten x 534,7. Tray-Innenraum x −379..31.
- **y** quer. Rahmenbreite 258–658 (Außenkanten der Eckpfosten). Zellen Y 278–438 (`left`, Mitte 358) und Y 478–638 (`right`, Mitte 558), je 160 breit, Mittelpfosten Y 438–478. „Hohes Y“ = rechte Seite (Schalter, dünne Kette, Netzteile).
- **z** oben. Unterkante Füße −25, untere Schiene 5–25, **Zelle 25–105 (80 mm, Mitte ZC 65)**, obere Schiene 105–125. Vor dem Umbau war die Zelle 25–80. Tray-Boden (Oberkante) Z 5.
- Tray-/Kettenmaße gelten für den voll ausgefahrenen Auszug, sofern nicht anders genannt. Verfahrweg 396 (`TRAVEL`, abgeleitet, nicht bestätigt).

## Rahmen, Zellen, Profile

Profile sind Kaufteile (20×20 / 20×40, „Profil Typ B Nut 6“, Nut 6, M3-Nutensteine), nur im Dokument, benannt `<Typ> L=<mm> #n`. Zellenumbau auf 80 mm: oberer Aufbau (+25 Z), Eckpfosten und Seitenpaneele (Hex) per Instanz-Xform gestreckt, Frontgitter/Platten/Anschlüsse +12,5 Z, 4 Zierrahmen Z 25–105 (Fenster Z 42,5–87,5). Alte Ringe `#45/#52/#37` nur ausgeblendet.

| Baugruppe (Top-Level) | Layer | Inhalt |
|---|---|---|
| `Stock Frame` (ex `Group#64`) | `Stock Frame` | Original-CR10-Rahmen, unverändert: 2040 L480 ×4, 2020 L400 ×4, 2040 L563 ×1, 2020 L320 ×1 |
| `Mod Frame Base` (ex `Gruppieren#11`) | `Mod Base` | fester Unterbau: 2040 L80 ×7, 2020 L400 ×1, 2020 L500 ×2 |
| `Mod Frame Drawer` (ex `Gruppieren#36`) | `Mod Drawer` | Auszug/Tray: 2020 L334 ×1, 2020 L80 ×2, 2040 L80 ×1, 2020 L400 ×2, 2040 L410 ×1, 2020 L410 ×1; Wannenplatte `Gruppieren#15` (Material unbekannt) |
| `Stock Foot` (ex `Gruppieren#2`, 1–4) | `Stock Feet` | Original-Füße, später am Mod-Rahmen anschrauben |
| `Gruppieren#48`, `#39` | 0 | Altlasten (Honeycomb von Hand), nicht anfassen |

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
| Zierrahmen / Bezel Ring | 160 × 80 × 3 (`RING_T`), Fenster 150,4 × 45,4 (`FIT` 0,2 je Seite), 4 Instanzen (hinten/vorn × links/rechts) |
| Plug | 150 × 45, Deckblech 2 außen + Rahmen 4 innen mit Tasche |
| Keystone-Ausschnitt | 14,6 × 19,2, Raster 24 (`SEG`), 4 Plätze |
| GX16-4 | Loch Ø16,2 |
| Hex-Raster (Original `Gruppieren#46`) | Flat-Top, Schlüsselweite 17,32, Eckenradius 1,7, Raster 19,4 (Steg 2,1), `HEX_SHIFT` (4,0) gegen Splitter < 0,1 mm |
| Side Panel Hex | 199,5 × 79,5, Rahmen 5 mm (`PANEL_RIM`), Hexfeld 2 mm dick (`GRID_T`); 4 Instanzen: `SIDE_X0` a 55 / b 295, Länge 200 |
| Side Panel Fan60 | nur STL: 60-mm-Lüfter Ø57, 4 × Ø3,4 auf 50 × 50; Hexe im Radius 48 entfallen; nirgends platziert (Lüfterposition offen) |
| Front Grille | 150 × 45 × 2, Hex wie Original, 2 mm Rand; 2 Instanzen |

**Rückplatten** (`place_rear`): `Switch Plug` auf `CELL_YC["right"]` (Y 483–633, Schalter-Mitte Y 553,4 = 558 − `IEC_U` 4,6, Z 65); `Connector Plug` auf `"left"` (Y 283–433, Check-Zelle 278..438): GX16-4 plus 4 Keystones (RJ45, USB, USB, Blind). Die Plugs wurden getauscht, damit der Netzschalter auf der Seite der dünnen 230-V-Kette liegt.

**Switch Plug / IEC-GS-1-100** (Snap-in, keine Schrauben): Ausschnitt `IEC_CUT` 47 × 27,8 R2 (+2·FIT), `IEC_WALL` 1,0 (Blech in der Tasche auf 1,0 gedünnt), `IEC_RECESS` 53 × 34 (Haken ±15,3 + Federweg). Alter Schraubausschnitt 29,2 × 33,2 + 2 × Ø5,2 entfernt. Rastkraft auf gedrucktem 1,0-mm-Rand ungetestet.

**Cover Mount** (gemeinsame Komponente `cover_mount()`): exakte Kopie des Originalteils `Side Cover - Mount` (131 Eckpunkte, 963 mm³, Lasche 19,7 × 13 × 5, Senkung Ø7 × 1, Loch Ø4), Mesh und vier Lagen in `gen/data/side_cover_mount.json`. Bezel-Ringe übernehmen die Lagen (±40), Seitenpaneele schieben sie 20 mm nach außen (±60, `MT_SIDE_SHIFT`). Wurzel 0,5 mm im Teil (`MT_OVERLAP`, damit es verschmilzt), `MT_ROOT_FIX` −0,3. Laschen liegen immer auf Z 25 bzw. 105 (Check). Die Originalclips sind Panelhalter (Kaufteil).

Nicht gedruckt (Kaufteile): Profile, Schienen, Hutschienen, Alu-Eckverbinder (Druckguss), Original-Panelclips.

## Tray-Layout entlang x (hohe-Y-Seite, Tray innen X −379..31)

| Element | X | Y | Z | Anmerkung |
|---|---|---|---|---|
| LRS-350-24 (Vendor/Platzhalter) | −364..−149 | 475..590 | 25..55,9 | Klemmen +X; DIN-Wiegen bei X −339/−174 (20 breit) |
| Power-Hub (Basis) | −148,5..−63,5 | 475..604 | 5..58 | rot Y 557..604, gelb Y 475..557 |
| RS-15-5 | −63..12 | 530,8..581,8 | 25..53 | Klemmen −X; 2 Wiegen X −50..−38 / −6..6, Y 528,8..583,8; 19 mm bis Querholm |
| BTT Octopus | −300..−140 | 352..452 | PCB-Unterkante 31 | Einspeisung/Heizer +X oben, USB-C +X unten, Motor/Sensor unten (ungefähr, ungeprüft); DIN-Halter X −295/−145 |
| Raspberry Pi 4 | −125..−40 | 374..430 (Lochmitte 402 = R2) | PCB-Unterkante 31 | Ports +X, USB-C −Y, GPIO +Y; Halter X −125..−60, Y 374..430 |
| DC-Kanal (gelb) | −300..−45 | Mitte 463 (453..473) | 5..25 | 20 × 20, Deckel über volle Länge, Fingerschlitze (Raster 10) |
| Datenkanal (grün) | −300..−35 | Mitte 340 (330..350) | 5..25 | vom Austritt der breiten Kette (X −56..−38, Y 330) zum Octopus; offenes Vorderende |
| Hutschiene R1a (Power A, 370 mm) | −361,5..9 | Mitte 527 (509,5..544,5) | 5..12,5 | LRS-350, gelbe Hub-Box, RS-15-5 (`tray.RAIL_A`) |
| Hutschiene R1b (Power B, 370 mm) | −361,5..9 | Mitte 577 (559,5..594,5) | 5..12,5 | LRS-350, rote Hub-Box, RS-15-5 (`tray.RAIL_B`). Abstand A/B 50: Riegelende A 553,7, Haken B ab 557,3. B ist durch die rote Box festgelegt (Haken und Riegel innerhalb Y 557,1..604). Schwerpunkte LRS 532,5 und RS 556,3 liegen zwischen den Schienen |
| Hutschiene R2 (Logik) | −305..−40 | Mitte 402 (384,5..419,5) = Octopus-Mitte | 5..12,5 | unter Octopus und Pi (Pi mittig darüber) |
| PE-Öse Tray | −74..−50 | 615 (auf 2020) | ca. 26 | siehe PE-Erdung |
| PE-Öse Rahmen | 525 | 570 | – | siehe PE-Erdung |

DIN-Teile (`tray.py`, Clips für EN 50022 35 × 7,5, Rail-Oberkante Z 12,5): `DIN PSU24 Cradle 1/2` (20 breit), `DIN PSU5 Cradle 1/2` (12 breit, X −50..−38 und −6..6), `DIN Octopus Holder 1/2` (Balken unter einer Lochspalte, Lochraster 150 × 90), `DIN Pi Holder` (Löcher 58 × 49, M2,5). Clips (`tray._clip_cs`, alle aus einem Code): feste Nase −Y, gefederter Schieber +Y, **alle Riegel zeigen nach +Y**, damit sich benachbarte Halter nicht gegenseitig blockieren. Schieber (Print-in-Place, ein Körper): Nase 1,3 unter dem Flansch, Rampe zum Aufrasten, Mäanderfeder aus 3 Stegen 0,6 (Spalt 0,5) an einem Pfosten des Clips, Schieber 0,4 unter der Clipbasis; Riegelseite bis +26,7 ab Schienenmitte (`LATCH_END`). Lösen: Schlitz von oben (`RELEASE` +18,8..+22,6 ab Schienenmitte, 5 lang in X), Schraubendreher in die Kerbe, Schieber 1,5 nach +Y hebeln; ein Stift ≤ 1,4 in den entstehenden Spalt (Schlitzkante −Y / Kerbwand) hält ihn offen, so lassen sich Halter mit 2 Clips nacheinander entriegeln. LRS-Wiegen und RS-Wiege je 2 Clips (A + B). Lösen der Wiegen erst nach Abnahme des Netzteils (Schlitze A unter dem Gerät; Schlitz B der LRS-Wiegen bei Y 595,8..599,6 frei). Pi-Halter: Clips 14 breit, Schlitze X −115 / −70 (neben den Domen). Hub: rote Box auf R1b, gelbe auf R1a, je 2 Clips, keine Bodenschrauben. Lüfter-Sets von Pi/Octopus sind Nutzer-Handbau: Octopus-Lüfter X −312..−302 / Y 382..422, Pi-Lüfter X −102..−62 / Y 432..442; deren Halterfüße Z 30..33 schweben (offen).

Farbe der Druckteile = Filament: rot 230 V, gelb 24/5 V, grün Daten/Bus, dunkelgrau DIN-Halter; Ketten blau (`CHAIN_COL`), Blenden/Plugs orange.

## Kabelschleppketten

Zwei Ketten, Obertrum fest an der Acrylplatte (Z 102), Untertrum am Tray, 180-Grad-Bogen vorn (−x). Platz Z 25..102 = 77. Kabel: Lapp ÖLFLEX FD 855 P 3G1,5 (siehe COMPONENTS). Bogenradius der Ketten liegt unter R_dyn 36,5 des Kabels (Datenblatt ungeprüft, PLAN T-004).

| Parameter | Breit (`cable.py`) | Dünn (`cable_thin.py`) |
|---|---|---|
| Aufgabe | CAN, 24/5 V, Sensoren, USB, Netzwerk | 230 V |
| Spur | Y 290..330, Mitte 310 (2040) | Mitte Y 615 (2020, Spur 605..627), Kette Y 606,1..623,9 |
| Glieder / Teilung | 11 / 29,5 (= Bogenradius, 3 Glieder je 180°) | 12 / 26 |
| Plattenradius (Höhe) | 9 (18) | 7,5 (15) |
| Plattendicke / Spalt Inner-Outer | 3,0 / 0,3 | 1,8 / 0,3 |
| Innenmaß | 27,4 × ca. 12 | 10 × 10 |
| Außenbreite | 40 (\|y\| 20) | 17,8 |
| Pivothöhe oben / unten | 92,5 / 34,5 | 91,4 / 34,7 (Bogenradius 28,35) |
| `X_MOVING_EXT` (bewegtes Ende, ausgefahren) | −83,5 | −128,5 (`X_SHIFT` 45) |
| `X_FIXED` (festes Ende, Hubmitte) | 114,5 | 69,5 |
| Anschlag (`STOP_H`) | 2,7 (gekürzt, Hülle) | = R (voll, eckig) |
| Gelenk | Zapfen Ø4 hinten, Loch Ø4,4 + Schlitz 3,6 zur Deckelseite | Steg X 12,5..15,5, Balken Z −7,5..−5,5 |
| Glied | Kopie von `Chain Link (new)` (`chain_link_user.json`; Zapfen X −3,5, Loch X 26), Anschlagecken zurückgeschnitten, Außennuten für Klammer | parametrisch nach gleichem Schema (R 9 → 7,5) |
| Klammer (`lid()`) | U-Klammer außen über die Backen, Arme 1,5 × 3,7, Haken 0,8 in Außennut; Basis `LID_BASE_Z` 80,7..83,3 ragt unter das Glied | Bogen 1,8 bündig in Nut der Innenplatten (Kerbe X 8,3..12,2), ganz in der Gliedhülle |
| Scharnier-Check | kein Sweep-Check | `hinge_sweep`: 0..60° frei (Bogen braucht 54,6), Anschlag bei −1,5° |
| Druck | Glieder stehend auf der Unterkante, Klammer Boden unten, ohne Support | wie breit |

**X_SHIFT** der dünnen Kette (45 mm nach vorn): ihr Kabelaustritt landet auf dem Power-Hub (Eingang X −109..−94). Bogenfront eingefahren in Tray-Koordinaten −379,0 (Frontplatte −383, nur ca. 4 mm; Check verlangt >= −380 bzw. `DRAWER_FRONT_IN` + 3).

**Endhalter** (Layer `Schlepp (gen)`):
- breit fest: Gabel um Pivot X 114,5 / Z 92,5, 2 M3 durch die Acrylplatte in Mutterntaschen, Trichter 27 → 16 mm in den (noch nicht gebauten) festen Kanal; für das Kabelbündel zu eng (PLAN T-013). Breit beweglich: Zapfenzunge auf dem 2040 (2 M3 in Hammermuttern, Y 300/320), Kabel in Viertelkurve (Mittellinie R 24 > R_fest 22, Nut 18 breit, 14 tief) durch die +y-Fläche in den Datenkanal (X −60..−35), Austritt Z ca. 27–37.
- dünn fest: Gabel um Pivot X 69,5 / Z 91,4, 2 M3 von oben bei Y 607 (< 618), Tunnel 10 breit. Dünn beweglich: Zunge + Körper auf dem 2020, 2 M3 in Hammermuttern Y 615, Viertelkreis-Nut R 24 / 9,6 breit nach −y; Kabelaustritt X −108..−96, Z 29..39 (zum Hub-Eingang).

## Fester Kanal der dünnen Kette (`Thin Channel`)

Offen oben, unter der Acrylplatte (Boden `CH_ZB` Z 86,5, Oberkante 102), Flansch ±13,5. Pfad: gerade bei Y 615 bis X 380, eine L-Kurve R 30 (`L_R`, Mitte 380/585), Schenkel `X_LEG` 410 nach −Y bis zum offenen Ende `Y_END` 573,4 (= Schalter-Y + 20) mit Bodenrampe; hinterste Wand X 417 (`CH_END_X`). Geteilt bei `CH_SPLIT` 262 (0,2 Spalt): Front 147,9 / Rear 161,4 lang (Bett 300). 5 Schrauben M3 (`CH_SCREWS`): (145 | 235 | 290 | 350, 605,5) und (400,5, 579,4), alle Y < 618 und X < 425. Ab dem offenen Ende läuft das 230-V-Kabel frei (Bogen nach +X, R >= 22, Abstieg zum IEC-Stecker Y 553,4 / Z 65). Der Kanal der breiten Kette (Datenkanal unter der Platte bis zum Connector Plug) ist nicht gebaut.

## Power-Hub (`power_hub.py`)

Beide Netzteile haben die AC/DC-Klemmengrenze auf **Y 557** (`Y_DIV`). Zwei getrennte Boxen (rot Netz +Y, gelb DC −Y, je einfarbig), jede mit eigener Wand auf der Grenze: Doppelwand gelb Y 555,3..556,9 (`YW`), rot 557,1..558,7 (`RW`), 0,2 Spalt. Jede Box sitzt auf ihrer eigenen Hutschiene (rot R1b, gelb R1a) mit 2 vollen Clips (`tray.hub_base`, X −142,5..−128,5 und −83,5..−69,5, innerhalb der R-6-Eckbögen) und hat eigene Deckelschrauben; keine Verbindung nötig. Lösen: Deckel ab, Schraubendreher durch die Bodenschlitze (X −134..−129 und −83..−78; rot Y 595,8..599,6, gelb Y 545,8..549,6). Basis X −148,5..−63,5 (0,5 Spiel zum LRS-Gehäuseende −149 und zum RS-Block −63), Boden Z 15,9..17,5 auf den Clips, Wände bis Z 58 (`Z_TOP`), Boden/Wand 1,6 (`T`).

| Teil | Wert |
|---|---|
| Mains Hub Base/Lid (rot) | Y 557,1..604 (`Y_RED`; 2020 des Trays ab 605) |
| DC Hub Base/Lid (gelb) | Y 475..556,9 (`Y_DC`; DC-Kanal bis 473) |
| WAGO-Taschen (`wago_slots()`) | stehend an der roten Wand, Y 558,9..567,2, Z 17,5..36,1, Einführung oben, Hebel +Y; L X −143,15..−124,45; N −123,05..−104,35; PE −93,75..−68,85 (Lücke `SEAM_GAP` 8 für den Wand-Dom); freie Rippen (1,2) mit Fußlippen und Rastnasen |
| WAGO-Breiten (`WAGOS`) | L/N 221-413: 18,7 (Tiefe 18,6, Dicke 8,3); PE 221-414: 24,9 (angenommen) |
| Eingang 230 V Kette (`ENTRY`) | +Y-Wand X −109..−94 ab Z 27, Kabelbinder-Zugentlastung innen |
| PE-Schlitz (`PE_SLOT`) | X −80..−74 (Z 22) zur Tray-Öse; 2026-11-03 von X −86..−78 verschoben, weil dort nur 2,8 mm bis zum beweglichen Kettenbügel (`Thin Bracket Moving` bis X −80,8, ab Y 605) frei waren (Ader Ø 3) |
| DC-Fenster (`DUCT_WIN`) | −Y-Wand X −140..−72, Z 17,5..25 (ab Hub-Bodenoberkante), auf die Fingerschlitze des DC-Kanals (Z 16..25) |
| Deckel | 1,6, Port-Hauben über beide Klemmblöcke (LRS bis X −168, RS bis X −48), Schürzen auf die Gehäuse, je Deckel eigene Grenzschürze auf `RW` bzw. `YW` bis Z 49 (LRS) / 44,2 (RS); Blitz graviert |
| Befestigung | je Deckel 3 M3 mit vollen Bohrungen, alle Dome im eigenen Teil: 2 Eck-Dome (r 4, konzentrisch zum Eck-Radius `R_BASE` 6, voll mit den Außenwänden verbunden) + 1 Wand-Dom (`wall_boss`, r 3,5, X −99,05; rot Y 560,7 in der Lücke N/PE, gelb Y 553,3); keine Bodenschrauben |
| Klemmblock LRS (Code) | X −166,1..−151,5, Y 498,5..585,5; Oberkante Gehäuse 55,9; `wire_z` 30 = Oberkante der abgesenkten Hub-Wand vor den Klemmen (Leitereintritt Z ca. 36) |
| Klemmblock RS (Code) | Y 540,9..580,6, `block_x` −52, Oberkante Block 43,7 / Gehäuse 53,0; `wire_z` 29 = Oberkante der abgesenkten Hub-Wand (Leitereintritt Z ca. 33) |

Pin-Positionen für die Verdrahtung: `docs/COMPONENTS.md`.

## Verdrahtung 230 V (`wiring.py`)

Modellierte Litzen auf Layer `Kabel (gen)`, nicht als STL, nicht im Kollisionstest der Druckteile, aber eigener Check: Litze gegen alle Druckteile, WAGO-Körper und Netzteilgehäuse (Boxen), Litzen untereinander, Biegeradius ≥ 4 × D.

- Geometrie: Polylinie mit Kreisbogen-Ecken (Radius exakt bekannt, bis 15), Rohr mit 12 Segmenten, Ringe per Parallel-Transport, flache Kappen.
- Stützpunkte: offline per Strafkosten-Suche gefunden (Schnittvolumen, Radiusdefizit, Länge) und fest im Code; der Generator rechnet nicht selbst.
- Mantel Ø 7,3 (grau, **Annahme**) vom Kettenbügel (Y 605) bis hinter die Zugentlastung (Y 594,5); Adern Ø 3,0 (**Annahme**), L braun, N blau, PE grün-gelb.
- WAGO-Eintritt senkrecht von oben bei Y 561,4 (**Annahme**: Löcher auf der −Y-Hälfte, Hebel +Y), gleichmäßig über die WAGO-Breite. Belegung: L/N k0 LRS, k1 Kette, k2 RS; PE k0 LRS, k1 Kette, k2 Tray-Öse, k3 RS.
- Klemmen waagrecht: LRS bis X −151,5 auf Z 36, RS bis X −63 auf Z 33 (Eintrittshöhen „ca.“, **ungeprüft**).
- Knick (Nutzerentscheidung 2026-11-03): LRS FG, RS FG und RS N laufen über die äußere WAGO-Rippe (bis Z 37,9; zur Wand nur 2,45 frei) und fallen kurz vor der Klemme ab; dort ist R < 4 × D zugelassen, der Check meldet den Radius als Info.
- PE zur Tray-Öse: durch `PE_SLOT` (X −77, Z 26,6), auf der 2020 nach +X, Litzenende X −63, Y 615 (Kabelschuh-Hülse dort; Öse im Dokument ggf. nachziehen).

## PE-Erdung

- **Rahmen-Öse:** M5 im oberen Schlitz der hinteren Base-2020 bei X 525, **Y 570** (Ringöse Y 564..576), zwischen den Bezel-Mounts (Y 527..588). Die frühere Lage Y 594..606 saß im unteren Mount von `Bezel Rear Right` (Y 588..604, Z 25..30) und wurde verworfen (Regel unten).
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
