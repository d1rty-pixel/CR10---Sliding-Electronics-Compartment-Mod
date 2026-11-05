# Creality CR10 – Sliding Electronics Compartment Mod

Umbau eines Creality CR10 auf ein ausziehbares Elektronikfach (Tray/Auszug) mit Pi 4, BTT Octopus, Mean-Well-Netzteilen, zwei Kabelschleppketten (breit: CAN/24 V/5 V/Daten, dünn: 230 V) und Zellenhöhe 80 mm (Z 25–105). Der Rahmen besteht aus Alu-Profilen und gekauften Vollauszug-Schubladenschienen (nur im IngeTrazo-Dokument). Gedruckt werden Rück-, Front- und Seitenpaneele, das IEC-Gehäuse, Schleppketten, Kabelkanäle, die 230-V-Boxen (WAGO, LRS, RS) und DIN-Halter.

Ein parametrischer Python-Generator (`manifold3d`) ist die einzige Quelle der Geometrie der Druckteile. Er schreibt `build/parts.json` (Einbaulage, für IngeTrazo) und STLs in Drucklage. Kaufteile (Profile, Schienen, Netzteile, Pi, Octopus, WAGO, IEC-Stecker) liegen nur im Dokument.

## Verzeichnisstruktur

| Pfad | Inhalt |
|---|---|
| `gen/cr10mod.py` | Generator-Hauptmodul: Rahmenkonstanten, Paneele/IEC-Gehäuse, Teileliste `parts()`, Checks (`build --check`), STL-/JSON-Ausgabe |
| `gen/cable.py` | breite Schleppkette (Parametersatz, Bahn, feste/bewegliche Endhalter) |
| `gen/chain_link.py` | gemeinsames parametrisches Kettenglied + Klammer + Halter-Schnittstellen (Gabel, Zunge) für beide Ketten |
| `gen/cable_base.py` | kleine Geometrie-Helfer (box, Zylinder, Prismen) |
| `gen/cable_thin.py` | dünne 230-V-Kette (Parametersatz, Halter) und fester L-Kanal unter der Acrylplatte |
| `gen/tray.py` | Tray-Teile: DC-, Daten- und AC-Kanal, Lüfterkanäle mit Deckeln, Clips der 230-V-Boxen, DIN-Wiegen und -Halter (Netzteile, Octopus, Pi), Lüfterhalter |
| `gen/power_hub.py` | 230-V-Boxen: WAGO-Box an der 2020 (WAGOs liegend, durch den Deckel messbar), LRS- und RS-Box vor den Netzteilklemmen (AC + DC, niedrige Trennwand, Rutschen in den DC-Kanal), Maße des AC-Kanals |
| `gen/cadio.py` | Mesh-Export (Polygonflächen für IngeTrazo, STL) |
| `gen/ingetrazo_import.py` | IngeTrazo-Skript: importiert `build/parts.json`, blendet Handbau-Vorgänger aus |
| `gen/vendor_import.py` | IngeTrazo-Skript: platziert Hersteller-Modelle aus `build/vendor/` (Layer `Electronics (vendor)`) |
| `gen/fan_model.py` | Anzeigemodell des Lüfters San Ace 9LG0624P4H001 (Katalogmaße) -> `build/fan60.json` |
| `gen/fan_import.py` | IngeTrazo-Skript: setzt `build/fan60.json` in die Gruppen `Luefter 60x60x25 #1..4` ein |
| `gen/rail_model.py` | Anzeigemodell der Hutschienen (Phoenix Contact NS 35/7,5 PERF, Datenblattmaße) -> `build/rails.json` |
| `gen/rail_import.py` | IngeTrazo-Skript: setzt `build/rails.json` in die Gruppen `Hutschiene R1a/R1b/R2 ...` ein |
| `gen/step_to_mesh.py` | Konverter STEP -> `build/vendor/*.json` (eigenes venv mit `cadquery-ocp`) |
| `gen/bom_document.py` | IngeTrazo-Skript: erzeugt `docs/BOM.md` aus Dokument (Profile, Kaufteile) und `build/bom_parts.json` (Druckteile) |
| `gen/doc_export.py` | IngeTrazo-Skript: exportiert die sichtbaren Gruppen als Welt-Dreiecke nach `build/doc_scene.json` |
| `gen/travel_sim.py` | Fahrsimulation Auszug/Schienen/Ketten gegen das Dokument (liest `build/doc_scene.json`) |
| `gen/data/` | `side_cover_mount.json` (Originalclip), `chain_link_user.json` (Nutzerglied, Vorlage des Schemas; von keinem Code gelesen) |
| `model/CR10-Sliding-Electronics-Compartment-Mod.igz` | IngeTrazo-Dokument: Rahmen, Kaufteile (Profile, Schienen, Netzteile, Platinen, WAGO), Handbau-Teile und importierte Druckteile |
| `build/parts.json` | Druckteile in Einbaulage (für IngeTrazo), erzeugt, nicht im Repo |
| `build/bom_parts.json` | Druckteil-Liste (STL, Stück, Volumen) für `docs/BOM.md`, erzeugt, nicht im Repo |
| `build/doc_scene.json` | Export des Dokuments für die Fahrsimulation, erzeugt, nicht im Repo |
| `build/stl/` | STLs in Drucklage, erzeugt, nicht im Repo |
| `build/vendor/` | Hersteller-Meshes als JSON (LRS-350, RS-15, Octopus, Pi 4, IEC-GS-1-100); nicht im Repo (Lizenz der Hersteller-Modelle ungeprüft), lokal mit `gen/step_to_mesh.py` aus den STEP-Dateien erzeugen (Quellen: `docs/COMPONENTS.md`) |
| `build/igz_reference.json` | Export des IngeTrazo-Dokuments (Weltboxen in mm) nach dem Umbau auf 80 mm |
| `docs/` | Dokumentation, siehe unten |
| `.claude/HANDOFF.md` | Übergabe: nur die Aufgabe „In Arbeit“ |
| `CR10 Standalone Mod - Documentation.pdf` | nur lokal, nicht im Repo: Referenz aus dem alten Repo dieses Umbaus (Komponentenauswahl, alte Version) |

## Ausführen

Generator und Checks (`build` ist das Ausgabeverzeichnis; Kollisions-, Mannigfaltigkeits- und Near-Vertex-Checks müssen bestehen):

```bash
./venv/bin/python -I gen/cr10mod.py build --check
```

Umgebung einrichten: `python3 -m venv venv && ./venv/bin/pip install -r gen/requirements.txt` (`manifold3d`, `numpy`).

### Import nach IngeTrazo

In IngeTrazo (MCP `run_python`, AI-Bridge muss laufen):

```python
exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/ingetrazo_import.py", encoding="utf-8").read())
exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/vendor_import.py", encoding="utf-8").read())
exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/fan_import.py", encoding="utf-8").read())   # vorher: ./venv/bin/python -I gen/fan_model.py
exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/rail_import.py", encoding="utf-8").read())  # vorher: ./venv/bin/python -I gen/rail_model.py
```

Das erste Skript ersetzt die Gruppen der Layer `Druckteile (gen)`, `Schlepp (gen)`, `Tray Druckteile (gen)`; das zweite ersetzt `Electronics (vendor)` (Platzhalter bleiben, nur unsichtbar); das dritte ersetzt die Meshes der vier Lüftergruppen, das vierte die der drei Hutschienen (Name und Layer bleiben). Stückliste neu erzeugen mit `gen/bom_document.py` auf demselben Weg (nach `gen/cr10mod.py build`).

### Fahrsimulation

```python
exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/doc_export.py", encoding="utf-8").read())   # in IngeTrazo
```

```bash
./venv/bin/python -I gen/travel_sim.py
```

### Bewegung (Newton-Erweiterung)

```bash
./venv/bin/python -I gen/newton_model.py      # -> build/newton.json
```

```python
exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/newton_import.py", encoding="utf-8").read())   # in IngeTrazo
newton_view(True)    # Unnötiges ausblenden; newton_view(False) blendet es wieder ein
```

### Hersteller-Modelle konvertieren

`gen/step_to_mesh.py IN.step OUT.json [--defl MM] [--ang RAD] [--min-solid MM]` braucht OpenCascade-Bindings (`pip install cadquery-ocp`) in einem **separaten** venv, nicht in `venv/`. Die STEP-Dateien liegen nicht im Projekt, Quellen und Parameter je Modell: `docs/COMPONENTS.md`.

## Dokumentation

| Datei | Inhalt |
|---|---|
| [docs/DESIGN.md](docs/DESIGN.md) | Koordinaten, Rahmen, Platten, Tray-Layout, Ketten, Kanäle, Power-Hub, PE, Konstruktionsregeln |
| [docs/COMPONENTS.md](docs/COMPONENTS.md) | Kaufteile mit Datenblattfakten und Quellen der 3D-Modelle |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | Umgebung, IngeTrazo-Fallstricke |
| [docs/PLAN.md](docs/PLAN.md) | Aufgabenliste (In Arbeit / Offen / Blockiert) |
| [docs/done/2026-11.md](docs/done/2026-11.md) | Archiv erledigter Aufgaben |
| [docs/BOM.md](docs/BOM.md) | Stückliste (Profile, Kaufteile im Modell, Druckteile mit Volumen) |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Kaufteile-Stückliste (von Hand gepflegt: Elektronik, Lüfter, Mechanik, Schrauben) |
| [CLAUDE.md](CLAUDE.md) | Projektanweisungen und Handoff-Hygiene |
