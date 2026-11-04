# Handoff

Keine Aufgabe in Arbeit (Stand 2026-11-04).

Nächste Aufgabe aus `docs/PLAN.md` („Offen“). Probedrucke (T-010) ruhen vorerst (Nutzer 2026-11-04), evtl. später je Bauabschnitt. T-035 (vordere Füße gegen die Schienen) braucht eine Nutzerentscheidung, T-036 (Schienendicke, Hub) eine Messung. Die DC-Kabelläufe (T-022) sind vertagt. Das RS-15-5 ist seit T-033 gedreht; `vendor_import.py` mit der neuen RS-`rot` ist ungetestet (`build/vendor/` fehlt), beim nächsten Vendor-Import Lage prüfen (Soll X −42,05..9,05, Y 475,5..550,06). Nach Änderungen an Tray, Ketten oder Kaufteilen die Fahrsimulation neu laufen lassen (`gen/doc_export.py` in IngeTrazo, dann `gen/travel_sim.py`; Ablauf in `docs/WORKFLOW.md`). `todo.md` (untracked) ist abgearbeitet.

## Nicht ändern
- Keine Exporte; keine Commits/Push ohne Anweisung.
- `Kabelweg (Skizze)` nicht löschen.

## Tool-Fallen
Gruppen per Name; `run_python` in try/except (Ausnahme: `exec` von `vendor_import.py`, dort muss ein Fehler den Schritt zurückrollen); `build/vendor/*.json` fehlt lokal; IngeTrazo läuft unter Windows: `exec`-Pfade `G:/Things/...`; Profile und Rahmenteile sind Kinder von `Mod Frame Drawer`/`Mod Frame Base` (für Bauraum-Scans `children` mit `xform` durchlaufen; `xform` ist `QMatrix4x4`, Zeilen per `X.row(i).x()..w()`); Vertex-Koordinaten über `v.position` (Mesh-Vertices), Face-Vertices sind direkt `QVector3D`; `pgrep -f`/`pkill -f` in Warteschleifen treffen die eigene Befehlszeile – per PID warten. Löschen von Gruppen per `run_python` blockiert der Auto-Modus ohne ausdrückliche Nutzerfreigabe. Hexraster: jede neue Paneelbreite braucht eine eigene splitterfreie Gitterverschiebung (Near-Vertex-Check); ausgesparte Zonen per `hex_exclude` (ganze Hexe weglassen, nie anschneiden). Senkungen als ein `Manifold.revolve`-Profil, sonst Splitter an der Außenfläche. Flächen mit Löchern trianguliert `f.triangulate()` (Liste von QVector3D-Tripeln); Sichtbarkeit: `g.hidden`, `layer.visible`.
