# Handoff

## T-042 Dokument aufräumen (in Arbeit, Stand 2026-11-05)

Ziel: nur noch die Layer `CR10`, `Mod Frame`, `Mod Frame Print Parts`, `Mod Frame Electrics`, `Drawer Rails`, `Tray Frame`, `Tray Electrics`, `Tray Print Parts`, `Drag Chains`, `Archive` (ausgeblendet) und `Newton Axes`; Objekte zu Gruppen/Komponenten geordnet, alle Namen englisch, Newton-Beziehungen neu, Performance geprüft.

Entscheidungen Nutzer (2026-11-05):
- Generierte Teile per Kennung `g.ext["cr10mod"] = {"generated": True}` erkennen, nicht per Layer (`gen/ingetrazo_import.py`); Layer frei wählbar.
- Altes und Doppeltes zuerst in `Archive`; danach hat der Nutzer alles im Archiv gelöscht außer `Unplaced Part` und `Unplaced Print Parts` (Platzhalter, Kabelskizzen, alte Schienen/Seitenpaneele/DIN-Schienen, Lüfter-Naben). T-012 damit erledigt (`docs/done/2026-11.md`).
- Mod Frame: drei Layer (Rahmen, Druckteile, Elektrik).
- Tray: drei Layer (`Tray Frame`: Rahmen mit Plexiplatte, `Tray Image`; `Tray Electrics`: Kaufteile, DIN-Schienen (Nutzer), WAGO, Lüfter, PE-Öse, Verkabelung; `Tray Print Parts`: generierte Teile).
- Altes CR10-Mainboard und -Netzteil hat der Nutzer gelöscht; Layer `CR10 Electrics` auf Wunsch entfernt. Ebenso gelöscht: `Front Panel Mount R/L (legacy)` und `Rear Panel Mount R (legacy)` mit alten Clips und Frontgittern; `organize_document.py` verweist nicht mehr darauf. Kein Skript erzeugt sie neu (Clip-Geometrie des Generators kommt aus `gen/data/side_cover_mount.json`).
- L = Netzteilseite = hohes Y (ex „Fern/Far“), R = Mainboard-Seite = niedriges Y (ex „Nah/Near“). Front = −X (Auszugsrichtung).
- Alle Gruppen-, Komponenten- und Layernamen englisch, auch im Generator.

Stand (2026-11-05, Dokument vom Nutzer gespeichert, Tray-Aufteilung danach **noch nicht gespeichert** – Nutzer speichert):
- Erledigt: Generator/Pipeline umgestellt (`cr10mod.py` Layer + Namen `Front Panel R/L`, `Side Panel R/L Front/Rear`; `ingetrazo_import.py` Kennung `ext["cr10mod"]`, Linux-Pfad; `vendor_import.py`, `fan_import.py`, `rail_model.py`/`rail_import.py` (Schienen `L1`, `L2`, `R1`), `wiring.py`, `bom_document.py`, `travel_sim.py`, `doc_export.py`, `newton_model.py`, `newton_import.py`). Neu: `gen/organize_document.py` (idempotent).
- Im Dokument ausgeführt: `organize_document.py`, `ingetrazo_import.py` (alle Kanten 2 Flächen), erneut `organize_document.py`, `newton_import.py`, nach Tray-Aufteilung erneut `organize_document.py`, `newton_model.py`, `newton_import.py` (98 dynamisch, 4 statisch, 59 ignore, 27 Gelenke). `cr10mod.py build --check`: alle Checks bestanden. Nur noch die Ziel-Layer + `Layer 0` + `Newton Axes`.
- `gen/vendor_import.py` braucht keine Platzhalter mehr: ersetzt das Mesh der vorhandenen Kaufteil-Gruppe an Ort und Stelle (Name, Layer, Newton-Daten bleiben; Lage = alte untere Boxecke, IEC über `at`). Geprüft: Boxen von LRS-350, RS-15, Pi, Octopus unverändert, IEC 0,01 mm tiefer (Sollpunkt). `fan_import.py` fasst die Naben nicht mehr an. Newton danach: 98 dynamisch, 4 statisch, 36 ignore, 27 Gelenke.
- Achtung Brücke: bricht `run_python` mit `OSError: [Errno 5]` ab, ist der Schritt trotzdem ausgeführt (kein Rollback); Ausgaben per `contextlib.redirect_stdout` in eine Datei im Flatpak-Cache schreiben.
- Annahmen (Nutzer prüfen): Motoren nach Lage (`Motor Z R/L` an den Portalprofilen, `Motor Y` darunter), `CR10 Plexiglass Cover Plate` (ex `Group#45`), `Tray Plexiglass Plate` (ex `Gruppieren#15`), `Bed Carriage` (ex `Gruppo#77`), `CR10 Mechanics Part 1..8` (ex „1“), `Tray Image` (Inhalt unbekannt). Tiefere Unterteile importierter CAD-Modelle (Motorinnenteile, Bett-Komponenten) behalten ihre Namen.

Offen / nächster Schritt:
1. Docs nachziehen: `README.md`, `docs/DESIGN.md`, `docs/COMPONENTS.md`, `docs/WORKFLOW.md`, `docs/BOM.md` (per `gen/bom_document.py`, Pfade dort noch `G:/`), `docs/HARDWARE.md`, `docs/PLAN.md` (Namen in T-036 u. a.); Platzhalter-Hinweise in `docs/COMPONENTS.md`, `docs/DESIGN.md`, `README.md`, `docs/BOM.md` entfernen. `docs/done/` bleibt historisch.
2. Performance: 102 Körper (57 mit `newton_view(True, parts=True)`), Worker 3–4,5 ms/Schritt, aber nur ca. 0,65× Echtzeit, Runde 80 ms → Zeichnen pro Frame bremst (IngeTrazo-Fenster lag im Hintergrund). Vorschlag: Tray-Teile (generiert + Kaufteile) als Kinder von `Tray Frame` statt eigener Körper (Import und BOM müssen Kinder lesen); dann wiederholt messen mit Fenster vorne.
3. `Tray Frame` hat Form `compound`: Newton baut je Kind eine Hülle; ausgeblendete Kinder gibt es nach dem Löschen des Archivs nicht mehr. Ob Newton ausgeblendete Kinder generell überspringen sollte, ist eine Frage an das Newton-Repo.
4. `gen/travel_sim.py` neu laufen lassen (`doc_export.py`, Pfad noch `G:/`, T-041).

Nicht ändern: Geometrie der Druckteile (nur Generator), keine Exporte, keine Commits/Push ohne Anweisung.
