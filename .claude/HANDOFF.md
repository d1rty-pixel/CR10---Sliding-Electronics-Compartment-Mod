# Handoff

Keine Aufgabe in Arbeit (Stand 2026-11-03).

Nächste Aufgabe aus `docs/PLAN.md` („Offen“). Reihenfolge laut Absprache: Probedrucke auswerten (T-010: Ketten, `IEC Housing` und Rückwände aus T-026, neu auch `Fan Holder` aus T-028). Offene Rückfragen stehen in den PLAN-Zeilen. Die DC-Kabelläufe (T-022) sind vertagt. `todo.md` (untracked) ist vollständig abgearbeitet bzw. in PLAN übernommen.

## Nicht ändern
- Keine Exporte; keine Commits/Push ohne Anweisung.
- `Kabelweg (Skizze)` nicht löschen.

## Tool-Fallen
Gruppen per Name; `run_python` in try/except; IngeTrazo läuft unter Windows: `exec`-Pfade `G:/Things/...`; Profile und Rahmenteile sind Kinder von `Mod Frame Drawer`/`Mod Frame Base` (für Bauraum-Scans `children` mit `xform` durchlaufen; `xform` ist `QMatrix4x4`, Zeilen per `X.row(i).x()..w()`); Vertex-Koordinaten über `v.position` (Mesh-Vertices), Face-Vertices sind direkt `QVector3D`; `pgrep -f`/`pkill -f` in Warteschleifen treffen die eigene Befehlszeile – per PID warten. Löschen von Gruppen per `run_python` blockiert der Auto-Modus ohne ausdrückliche Nutzerfreigabe. Hexraster: jede neue Paneelbreite braucht eine eigene splitterfreie Gitterverschiebung (Near-Vertex-Check); ausgesparte Zonen per `hex_exclude` (ganze Hexe weglassen, nie anschneiden). Senkungen als ein `Manifold.revolve`-Profil, sonst Splitter an der Außenfläche.
