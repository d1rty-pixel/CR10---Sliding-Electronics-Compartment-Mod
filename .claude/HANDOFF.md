# Handoff: T-001 Kabelrouten als Litzen (`gen/wiring.py`)

In Arbeit: nur **T-001** (siehe `docs/PLAN.md`). Stand 2026-11-03, Branch `feat/t001-wiring-230v` (von `origin/main` 503a9f2), **nichts committet**. `build --check`: all checks passed. Import in IngeTrazo ok (11 Litzen, alle Kanten 2 Flächen).

## Erledigt (230 V)
- `gen/wiring.py`: Polylinie mit Kreisbogen-Ecken (`fillet_path`, Radius je Ecke bekannt), Rohr (`tube`, 12 Segmente, Parallel-Transport, Endkappen rechtwinklig zur End-Strecke), `ROUTES`/`KINK` fest im Code, `bought_boxes()` (WAGO-Körper, LRS/RS-Gehäuse), `sheath_for_cores()`.
- `gen/cr10mod.py`: Litzen in `parts.json` (Layer `Kabel (gen)`), Checks: Manifold/ein Körper, Near-Vertex, R ≥ 4 × D (Knick-Ecken nur Info), gegen alle Druckteile + Kaufteil-Boxen, Litzen untereinander (Kettenadern gegen den um 3 mm gekürzten Mantel).
- `gen/ingetrazo_import.py`: `Kabel (gen)` in `GEN_LAYERS`.
- `gen/power_hub.py`: `PE_SLOT` X −80..−74 (Nutzerentscheidung; alter Schlitz kollidierte mit `Thin Bracket Moving`).
- Docs: `DESIGN.md` (PE-Schlitz, Abschnitt Verdrahtung 230 V), `COMPONENTS.md` (Annahmen Ader Ø 3,0, Mantel grau, WAGO-Eintritt Y 561,4), `PLAN.md` (T-001 Stand, neu T-020, T-021).

## Entscheidungen
- Knick an LRS FG, RS FG, RS N: über die äußere WAGO-Rippe (Z 37,9), kurz vor der Klemme abfallen; R dort < 12 erlaubt (Nutzer).
- WAGO-Belegung: L/N k0 LRS, k1 Kette, k2 RS; PE k0 LRS, k1 Kette, k2 Tray, k3 RS. Kettenadern am Mantelende: L (−1,75/+1,01), N (+1,75/+1,01), PE (+1,75/−2,02) relativ zur Mantelachse (x/z).
- Stützpunkte per Offline-Suche (Skripte in `.claude/router/`, nicht im Generator; `wopt.py` global, `wpolish.py` lokal, `wfix.py` Radius-Reserve RQ 12,25, `w2code.py` + `splice.py` schreiben `ROUTES`; Pfade in den Skripten zeigen auf den Session-Scratchpad und müssen angepasst werden). Danach von Hand: RS-Knickpunkte (PE −66,4/−65,4 mit K1 Z 44,5; N −66,1/−65,2), Stützpunkte N-RS Z 38, PE-RS Z 50.

## Offen / nächster Schritt
1. Nutzer-Sichtprüfung 230 V: mehrere Adern machen große Schleifen (T-021). Abnahme abwarten, ggf. glätten.
2. Danach DC-Routen: LRS 3 Paare (Pins 4/7, 5/8, 6/9) -> Octopus DCIN/MOTOR/BED (Klemmen X ca. −145, Y 370..445, ungeprüft, T-003); RS-Paar -> Pi GPIO 5 V; durch `DUCT_WIN` (X −140..−72, Z 17,5..25) in den DC-Kanal (Y 453..473). LRS −V Y 552,25/542,75/533,25, +V 523,75/514,25/504,75; RS −V 553,1, +V 545,5.
3. Commit nur nach Freigabe (Vorschlag: PE_SLOT / wiring + Integration / Docs getrennt). `model/*.igz` ist durch den Import geändert.

## Nicht ändern
- `Group#80`; keine Exporte; keine Commits/Push ohne Anweisung.
- Generierte Halter nicht anschneiden; Kaufteile nur im Dokument; `Chain Link (new)` (hat schon vorher Kanten ≠ 2 Flächen) und `Schienen (gen)` unberührt.
- `Kabelweg (Skizze)` nicht löschen (T-012), Kanalende hinten (T-014) nicht bauen.

## Tool-Fallen
Gruppen per Name; `run_python` in try/except; `pgrep -f`/`pkill -f` in Warteschleifen treffen die eigene Befehlszeile – per PID warten.
