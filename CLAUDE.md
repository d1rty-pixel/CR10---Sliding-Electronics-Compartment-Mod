# Projektanweisungen: CR10 Sliding Electronics Compartment Mod

Persönliches 3D-Druck-/CAD-Projekt, Git-Repo `github.com/d1rty-pixel/CR10---Sliding-Electronics-Compartment-Mod` (Commit-Identität lokal `d1rty-pixel <equinox@lichtspiele.org>`, SSH-Key `id_ed25519_github_d1rty-pixel` per `core.sshCommand`; nie die IONOS-Identität). Sprache aller Dokumente: Deutsch, schlichtes Markdown, sachlich und knapp. Keine Fakten erfinden: jede Zahl stammt aus Code, Datenblatt oder Messung; bei Widerspruch gewinnt der Code vor der Prosa. Annahmen als solche kennzeichnen.

## Sessionstart
`CLAUDE.md`, `docs/PLAN.md` und `.claude/HANDOFF.md` lesen, danach nur die für die Aufgabe nötigen Dateien. Commits und Push nur auf ausdrückliche Anweisung, keine STL-Exporte ungefragt. Das Dokument liegt in `model/CR10-Sliding-Electronics-Compartment-Mod.igz`; `build/vendor/` und das PDF sind nicht im Repo.

## Dokumentenkarte

| Datei | Inhalt |
|---|---|
| `README.md` | Zweck, Verzeichnisse, Befehle, Importzeilen, Links |
| `docs/DESIGN.md` | Koordinaten, Rahmen, Platten, Tray-Layout, Ketten, Kanäle, Power-Hub, PE, Konstruktionsregeln |
| `docs/COMPONENTS.md` | Kaufteile, Datenblattfakten, Pinlagen, Quellen der 3D-Modelle |
| `docs/WORKFLOW.md` | Umgebung, IngeTrazo-Fallstricke |
| `docs/PLAN.md` | Aufgaben: In Arbeit / Offen / Blockiert |
| `docs/done/<YYYY-MM>.md` | Archiv erledigter Aufgaben |
| `docs/BOM.md` | Stückliste (Erzeugung: `gen/bom_document.py` in IngeTrazo) |
| `.claude/HANDOFF.md` | nur die Aufgabe(n) „In Arbeit“ |

## Befehle
- Generator + Checks: `./venv/bin/python -I gen/cr10mod.py build --check`
- Import in IngeTrazo (`run_python`): `exec(open(".../gen/ingetrazo_import.py", encoding="utf-8").read())` und `vendor_import.py` (Pfade im `README.md`).
- Hersteller-STEP konvertieren: `gen/step_to_mesh.py` nur im separaten venv mit `cadquery-ocp`.

## Konstruktionsregeln
- Geometrie der Druckteile nur im Generator ändern, nie in IngeTrazo.
- Alle Halterungen entstehen aus einem Code und sind identisch. Generierte Teile nie anschneiden; Kaufteile wandern, nie ein Halter.
- Kaufteile (Profile, Schienen, Netzteile, Pi, Octopus, WAGO, IEC-Stecker) nur im Dokument, nicht im Generator.
- Kollisionen, Manifold/Ein-Körper und Near-Vertex-Check (< 0,1 mm) müssen bestehen; nach dem Import alle Kanten 2 Flächen.
- Gruppen im Dokument per Namen suchen, nicht per Index; `Group#80` (Referenz) nicht ändern.
- Details und Fallstricke: `docs/DESIGN.md`, `docs/WORKFLOW.md`.

## Handoff-Hygiene (Pflicht nach jeder abgeschlossenen Aufgabe)
a. `docs/PLAN.md`: Status der Aufgabe setzen; erledigte Aufgaben nach `docs/done/<YYYY-MM>.md` verschieben (Datum, Ergebnis, Entscheidung); neu gefundene Aufgaben mit neuer ID (T-nnn, fortlaufend) eintragen.
b. `.claude/HANDOFF.md` neu schreiben: nur die Aufgabe(n) „In Arbeit“ mit ID, Ziel, relevanten Dateien, nötigen Fakten, Stand, nächstem Schritt, „Nicht ändern“; oder „keine Aufgabe in Arbeit“.
c. `README.md`, `docs/DESIGN.md`, `docs/COMPONENTS.md`, `docs/WORKFLOW.md`, `docs/BOM.md` auf Werte prüfen, die die Aufgabe geändert hat, und nachziehen (BOM per `gen/bom_document.py` in IngeTrazo, wenn sich das Modell geändert hat).
d. Sync-Check: jede ID im HANDOFF ist in PLAN „In Arbeit“ und umgekehrt.
e. Ergebnis in einer Zeile melden (z. B. „Hygiene: PLAN ok, HANDOFF T-001, Docs DESIGN aktualisiert, Sync ok“).

Das Skill `handoff-hygiene` führt diesen Ablauf aus.
