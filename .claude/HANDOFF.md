# Handoff

Stand 2026-11-05, Branch `main` (lokal 12 Commits vor `origin/main`, nicht pushen ohne Anweisung).

## T-045 Kettenanschläge in Newton realistisch (In Arbeit, noch nicht begonnen)

**Ziel:** Die Newton-Grenzen der Kettengelenke entsprechen den gedruckten Gliedern, der Durchhang des Obertrums ist realistisch.

**Fakten:**
- Das Newton-Plugin (`~/git/private/ingetrazo-newton`, lokaler `main`, installiert) hat jetzt eine Anschlaghärte pro Achse, Standard 100 %. Damit halten die Grenzen (≤ 0,14° Überschreitung); vorher gaben sie um 13 bis über 100° nach. Am Plugin ist nichts mehr zu tun.
- `gen/newton_model.py`: `STOP_DEG = -1.5` (Zurückbiegen), `FREE_DEG = {"wide": 78.0, "thin": 63.0}` (nur das geprüfte Ende von `hinge_sweep`, kein Anschlag). Der Bogen braucht 73,3° / 57,6°.
- `chain_link.Link.hinge_sweep(max_deg, step)` (`gen/chain_link.py:121`, Aufruf in `gen/cr10mod.py:387` über `cable.hinge_sweep` / `cable_thin.hinge_sweep`) liefert den ersten Winkel, bei dem Nachbarglieder samt Klammer kollidieren, und prüft den Rückbiege-Anschlag nur bei −1,5°.
- Headless-Messung mit harten Grenzen, Hub 0: Durchhang breit 8,9 / dünn 9,9 mm; mit `STOP_DEG` 0: 4,4 / 6,9; zusätzlich Biegegrenze = Bedarf des Bogens: 2,9 / 2,3. Skripte für die Messung (Export der Specs per `prepare()`, dann Worker headless) lagen im Scratchpad der vorigen Sitzung; Muster: `World().load(...)`, Antrieb über `w.step(24, {drive: target})`.

**Entscheidungen Nutzer (2026-11-05):** Werte im Code setzen, nicht pro Glied in der Sidebar. Gedruckte Glieder biegen sich nicht zurück, also Rückbiegen 0°. Den Anschlag in Bogenrichtung aus der CAD-Geometrie berechnen, nicht messen; der Nutzer vergleicht danach kurz am gedruckten Glied.

**Nächster Schritt:**
1. Mit `hinge_sweep` (größeres `max_deg`, feiner Schritt) den echten Kollisionswinkel in Bogenrichtung beider Ketten bestimmen; dazu den genauen Rückbiege-Anschlag zwischen 0 und −1,5°.
2. `STOP_DEG` und `FREE_DEG` in `gen/newton_model.py` daraus setzen (Kommentar und Docstring anpassen), `./venv/bin/python -I gen/newton_model.py`.
3. In IngeTrazo das CR10-Dokument öffnen (`model/CR10-Sliding-Electronics-Compartment-Mod.igz`; im Moment ist dort ein Testdokument offen), `gen/newton_import.py` per `exec` ausführen, Durchhang headless und live prüfen.
4. `docs/DESIGN.md` „Bewegung“ (Grenzen) nachziehen, Hygiene.

**Nicht ändern:** das Newton-Plugin; die Glied-Geometrie im Generator (nur messen).
