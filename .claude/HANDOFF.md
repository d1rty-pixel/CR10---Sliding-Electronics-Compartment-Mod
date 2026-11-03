# Handoff

Keine Aufgabe in Arbeit (Stand 2026-11-03).

Nächste Aufgabe wählt der Nutzer aus `docs/PLAN.md` („Offen“). Die DC-Kabelläufe sind vertagt.

## Nicht ändern
- `Group#80`; keine Exporte; keine Commits/Push ohne Anweisung.
- `Kabelweg (Skizze)` nicht löschen.

## Tool-Fallen
Gruppen per Name; `run_python` in try/except; IngeTrazo läuft unter Windows: `exec`-Pfade `G:/Things/...`; Profile und Rahmenteile sind Kinder von `Mod Frame Drawer`/`Mod Frame Base` (für Bauraum-Scans `children` mit `xform` durchlaufen); Vertex-Koordinaten über `v.position` (Mesh-Vertices), Face-Vertices sind direkt `QVector3D`; `pgrep -f`/`pkill -f` in Warteschleifen treffen die eigene Befehlszeile – per PID warten.
