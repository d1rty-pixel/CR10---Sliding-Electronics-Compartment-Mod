# Handoff: T-001 Kabelrouten als Litzen (`gen/wiring.py`)

In Arbeit: nur **T-001** (siehe `docs/PLAN.md`). Alles andere steht in `docs/DESIGN.md`, `COMPONENTS.md`, `WORKFLOW.md`, `PLAN.md`, `done/2026-11.md`. Git-Repo (siehe `CLAUDE.md`). Stand 2026-11-03, `build --check` ok, Import ok.

## Ziel
Nutzer verlangt „sichere Kabelwege mit schönen natürlichen Kurven“ als modellierte Litzen. Noch nicht begonnen (kein `gen/wiring.py`).

## Plan
- Neues Modul `gen/wiring.py`: Rohre entlang geglätteter Pfade (Rahmen per Parallel-Transport, 12 Segmente, Kappen, als Manifold), Layer `Kabel (gen)`, nicht als STL, aus dem Kollisionstest der Druckteile ausnehmen, eigener Check Litzen vs Druckteile (Wände/Deckel nicht durchstoßen). Einbinden in `cr10mod.py`/`ingetrazo_import.py` (`GEN_LAYERS`).
- Farben: L braun, N blau, PE grün-gelb, +V rot, -V schwarz. Biegeradien >= 4 x D (Kette Ø7,3).
- 230 V: Kette (Mantel endet hinter der Zugentlastung, Eingang X -109..-94 ab Z 27) -> L/N/PE von oben in die WAGOs (L -143,15..-124,45; N -123,05..-104,35; PE -93,75..-68,85; Y 558,9..567,2, Z 17,5..36,1); je WAGO nach oben raus, links zum LRS-350 (Eintritt X -149, Z ca. 36) bzw. rechts zum RS-15-5 (X -63, Z ca. 33); PE zusätzlich zur Tray-Öse (X -74..-50, Y 615) durch den PE-Schlitz (X -86..-78, Z 22).
- DC: LRS 3 Paare (Pins 4/7, 5/8, 6/9) -> Octopus DCIN/MOTOR/BED (Octopus-Klemmen am +X-Rand X ca. -145, Y 370..445, ungeprüft, PLAN T-003); RS-Paar -> Pi GPIO 5 V; alle durch das gelbe Fenster (X -140..-72, Z 17,5..25) in den DC-Kanal (Y 453..473).

## Fakten
- LRS-350 Pins Y: L 580,75, N 571,25, FG 561,75, -V 552,25 / 542,75 / 533,25, +V 523,75 / 514,25 / 504,75; Klemmblock X -166,1..-151,5, Schrauben oben Z 48, Eintritt Z ca. 36.
- RS-15-5 Pins Y: L 576,0, N 568,4, FG 560,8, -V 553,1, +V 545,5; Schrauben X ca. -60, oben Z 43,7, Eintritt Z ca. 33.
- AC/DC-Grenze Y 557; seit T-017 zwei Boxen mit Doppelwand (gelb Y 555,3..556,9, rot 557,1..558,7); Hub-Basis X -148,5..-63,5, Boden Z 15,9..17,5, rot auf Hutschiene R1b (Y 577), gelb auf R1a (Y 527), Wände bis Z 58, Deckel 1,6; Wand-Dome X -99,05 (rot Y 560,7, gelb Y 553,3).
- Annahmen: Octopus-PCB-Unterseite source z -1,6 (nicht gemessen); Octopus-PCB im STEP hell statt schwarz.

## Relevante Dateien
`gen/power_hub.py` (`wago_slots`, `ENTRY`, `PE_SLOT`, `DUCT_WIN`), `gen/tray.py`, `gen/cr10mod.py` (`parts()`, `run_checks`), `gen/ingetrazo_import.py`, `gen/vendor_import.py`; Layer `Electronics (vendor)`; Skizzenlayer `Kabelweg (Skizze)` ist veraltet (löschen: T-012, nicht vorher).

## Nächster Schritt
`gen/wiring.py` mit Pfad-/Rohr-Helfer und der 230-V-Route (Kette -> WAGOs -> LRS/RS) schreiben, Check Litzen vs Druckteile, `build --check`, Import, Screenshot; danach DC-Routen.

## Nicht ändern
- `Group#80` (Referenz); Commits/Push nur auf Anweisung, keine Exporte.
- Keine generierten Halter/Brackets schneiden oder abändern (alle Halter aus einem Code, identisch); Kaufteile nur im Dokument.
- Nutzerkomponente `Chain Link (new)` und Layer `Schienen (gen)` unberührt.
- Nicht ungefragt `Kabelweg (Skizze)` löschen, Kanalende hinten (T-014) nicht bauen.

## Tool-Fallen (kurz, Details `docs/WORKFLOW.md`)
Gruppen per Name suchen (Indizes verschieben sich); 0,05 überlappen; Near-Duplicate-Vertices vermeiden (exakte Bögen, Schnitt in 2D); `run_python` in try/except mit `repr(e)`.
