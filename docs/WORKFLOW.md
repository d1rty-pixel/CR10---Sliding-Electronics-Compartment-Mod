# Arbeitsablauf

## Umgebung

- Claude Code läuft unter WSL (Projekt `/mnt/g/Things/CR10---Sliding-Electronics-Compartment-Mod`), IngeTrazo unter Windows (`C:\Program Files\IngeTrazo`). MCP-Server `ingetrazo` = `/mnt/c/Program Files/IngeTrazo/ingetrazo-mcp.exe` (lokaler Scope), die AI-Bridge (127.0.0.1:4763) muss in IngeTrazo laufen. Skripte, die IngeTrazo per `exec` liest, verwenden Windows-Pfade (`G:/Things/...`).
- Generator: `./venv/bin/python -I gen/cr10mod.py build --check`. Geometrie immer im Generator ändern, nicht in IngeTrazo. Commits nur auf Anweisung, keine Exporte ungefragt.
- Import in IngeTrazo: `ingetrazo_import.py` und `vendor_import.py` per `exec` (genaue Zeilen im `README.md`). Hersteller-Konverter `gen/step_to_mesh.py` nur im separaten venv mit `cadquery-ocp`.
- `vendor_import.py` braucht `build/vendor/*.json` (lokal derzeit nicht vorhanden); fehlt eine Datei, bricht es seit 2026-11-03 ab, bevor es Gruppen entfernt. Den `exec` nicht in try/except packen, sonst wird ein Fehlschritt nicht zurückgerollt. Ohne JSON lässt sich ein Herstellermodell im Dokument direkt drehen/verschieben (so beim Pi in T-030).
- `docs/BOM.md` entsteht per `exec` von `gen/bom_document.py` in `run_python` (liest Profilnamen aus dem Dokument und `build/parts.json`).

## IngeTrazo-Fallstricke

- Dokument in **Metern**, Z oben. Der Generator rechnet in mm.
- `OSError: Eingabe-/Ausgabefehler` aus `run_python` ist eine Python-Exception, die beim Ausgeben scheitert. Code in `try/except` kapseln und `repr(e)` drucken.
- `Face.area` wirft. `Vertex.position` ist ein `QVector3D`.
- Variablennamen im persistenten Scope nicht überschreiben (`a`, `b`, `c`, `d` wurden schon einmal mit Pfosten belegt). Helper im Scope: `wbox`, `leaves`, `parentM`, `apply`, `rr`, `circ`, `prism`-Helfer, `QM`, `I`.
- `wbox(g, I)` liefert `(name, x0, x1, y0, y1, z0, z1)` in mm über alle Nachfahren; nicht ungefiltert ausgeben (sehr lang). Der Auszug-Container (`Mod Frame Drawer`, ex `#36`) liefert ein falsches Gesamt-Bbox-Artefakt.
- Komponenten-Instanzen teilen sich Meshes (z. B. Pfosten): nie Vertexe verschieben, nur `xform` ändern. Eine `xform`-Änderung meldet `changed: False`, ist aber wirksam und nicht zuverlässig im Undo (Löschen von Gruppen ebenso).
- **Indexverschiebung:** Nach jedem Import verschieben sich Top-Level-Indizes (auch Drawer-Kinder nach dem Löschen der Kanäle). Gruppen immer per **Name** suchen, nie per Index ausblenden. `ingetrazo_import.py` sucht alte Teile per Namen.
- `run_python` darf ins Projektverzeichnis schreiben, `/tmp` ist sandboxed.
- Eckpunkte näher als ca. 0,1 mm werden verschmolzen; Überlappungen ≥ 1 mm planen.
- **Berührende Körper bleiben getrennt:** manifold3d verschmilzt Körper, die sich nur flächig berühren, nicht. Überlappung 0,05 (Verschmelzung zu einem Körper) bis 0,5–1 mm bei dünnen Teilen.
- **Near-Duplicate-Vertices:** `offset()`-Rundungen und Kreise an Wänden erzeugen Fast-Duplikate. Gegenmittel: exakte Bögen (`_rounded()` in `power_hub.py`), Grundkörper als ein Block minus Hohlraum, Deckelaussparungen in 2D, Extrusion aus einem (x,z)- oder (y,z)-Schnitt statt Vereinigung koplanarer Flächen (Splitter-Vertices < 0,1 mm), Hex-Gitter per `HEX_SHIFT` verschieben.
- `planar_faces()` in `gen/cadio.py` fasst koplanare Dreiecke zu Polygonflächen mit Löchern zusammen (Import). Kanten mit 4 Flächen im Import: Manifold sagt ok, meist Berührkante; nach dem Import „alle Kanten 2 Flächen“ prüfen.
- Kaufteil-Modell austauschen ohne Löschen: `g.mesh = neues_Mesh` behält Name und Layer der Gruppe (so macht es `gen/fan_import.py`); meldet `changed: False`, wirkt aber.
- Hersteller-Importe: die Wicklung der Polygone wird gegen die STEP-Normale geprüft (wie `addo` in `ingetrazo_import.py`), sonst Fläche gedreht.

## Referenzexport

`build/igz_reference.json` entsteht per `run_python` im offenen Dokument (Weltboxen in mm, Pfad `groups[i].children[k]…`, 287 Teile). Er ist nach dem Umbau auf 80 mm erzeugt worden, Teile über Z 105 wurden dabei um +25 mm verschoben, Pfosten und Seitenpaneele gestreckt. Das Dokument hat sich seitdem stark verändert (Layer, Elektronik, Ketten); die frühere Referenzgruppe `Group#80` wurde auf Nutzeranweisung gelöscht (T-025, 2026-11-03).
