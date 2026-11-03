---
name: handoff-hygiene
description: Führt nach einer abgeschlossenen Aufgabe die Handoff-Hygiene aus - PLAN.md aktualisieren, erledigte Aufgaben archivieren, HANDOFF.md neu schreiben, andere Docs prüfen, Sync verifizieren.
---

# Handoff-Hygiene

Regelquelle: `CLAUDE.md`, Abschnitt „Handoff-Hygiene“. Bei Abweichung gilt `CLAUDE.md`.

Checkliste:

1. [ ] `docs/PLAN.md`: Status der Aufgabe setzen; Erledigtes nach `docs/done/<YYYY-MM>.md` verschieben (Datum, Ergebnis, Entscheidung); neu gefundene Aufgaben mit fortlaufender ID `T-nnn` eintragen.
2. [ ] `.claude/HANDOFF.md` neu schreiben: nur Aufgabe(n) „In Arbeit“ (ID, Ziel, Dateien, Fakten, Stand, nächster Schritt, „Nicht ändern“) oder „keine Aufgabe in Arbeit“. Keine Chronik.
3. [ ] `README.md`, `docs/DESIGN.md`, `docs/COMPONENTS.md`, `docs/WORKFLOW.md`, `docs/BOM.md` auf geänderte Werte prüfen und nachziehen; BOM bei Modelländerung per `gen/bom_document.py` in IngeTrazo neu erzeugen.
4. [ ] Sync: jede ID in HANDOFF steht in PLAN unter „In Arbeit“ und umgekehrt.
5. [ ] Ergebnis in einer Zeile melden.
