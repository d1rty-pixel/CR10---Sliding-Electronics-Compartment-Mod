# Handoff

Keine Aufgabe in Arbeit (Stand 2026-11-04).

Nächste Aufgabe aus `docs/PLAN.md` („Offen“). Reihenfolge laut Absprache: Probedrucke auswerten (T-010: Ketten, `IEC Housing` und Rückwände aus T-026, `Fan Holder` aus T-028, Rutsche der DC-Box und Lüfterkanäle aus T-032, Hub-Boxen mit L-Trennwand und RS-Wiegen aus T-033), sobald der Druck fertig ist. Offene Rückfragen stehen in den PLAN-Zeilen. Die DC-Kabelläufe (T-022) sind vertagt; die Lüfterlitzen laufen seit T-032 in `Fan Data Duct`/`Fan DC Duct`. Das RS-15-5 ist seit T-033 gedreht; `vendor_import.py` mit der neuen RS-`rot` ist ungetestet (`build/vendor/` fehlt), beim nächsten Vendor-Import Lage prüfen (Soll X −42,05..9,05, Y 475,5..550,06). `todo.md` (untracked) ist vollständig abgearbeitet bzw. in PLAN übernommen.

## Nicht ändern
- Keine Exporte; keine Commits/Push ohne Anweisung.
- `Kabelweg (Skizze)` nicht löschen.

## Tool-Fallen
Gruppen per Name; `run_python` in try/except (Ausnahme: `exec` von `vendor_import.py`, dort muss ein Fehler den Schritt zurückrollen); `build/vendor/*.json` fehlt lokal; IngeTrazo läuft unter Windows: `exec`-Pfade `G:/Things/...`; Profile und Rahmenteile sind Kinder von `Mod Frame Drawer`/`Mod Frame Base` (für Bauraum-Scans `children` mit `xform` durchlaufen; `xform` ist `QMatrix4x4`, Zeilen per `X.row(i).x()..w()`); Vertex-Koordinaten über `v.position` (Mesh-Vertices), Face-Vertices sind direkt `QVector3D`; `pgrep -f`/`pkill -f` in Warteschleifen treffen die eigene Befehlszeile – per PID warten. Löschen von Gruppen per `run_python` blockiert der Auto-Modus ohne ausdrückliche Nutzerfreigabe. Hexraster: jede neue Paneelbreite braucht eine eigene splitterfreie Gitterverschiebung (Near-Vertex-Check); ausgesparte Zonen per `hex_exclude` (ganze Hexe weglassen, nie anschneiden). Senkungen als ein `Manifold.revolve`-Profil, sonst Splitter an der Außenfläche.
