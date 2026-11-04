# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/bom_document.py", encoding="utf-8").read())
# Writes docs/BOM.md from
#   - the profile groups ("<2020|2040> L=<mm> #n") of the assemblies in the open document,
#   - the bought parts in the open document (visible top-level groups, counted by name; hidden placeholders are skipped),
#   - the printed parts of build/bom_parts.json (written by `gen/cr10mod.py build`: STL, placed count, volume).
# Every number comes from the model or the generator, never typed by hand. Screws and slot nuts are not in the model.
import re, json, datetime, collections

ROOT = "G:/Things/CR10---Sliding-Electronics-Compartment-Mod"
ASSEMBLIES = [("Stock Frame", "Original-CR10-Rahmen, bleibt unverändert, nichts zu kaufen"),
              ("Mod Frame Base", "fester Unterbau"),
              ("Mod Frame Drawer", "Auszug")]
PAT = re.compile(r"^(2020|2040) L=(\d+) #\d+$")
# (row label, name regex of the top-level group, unit note); a group counts once, the first matching row wins
BOUGHT = [("Netzteil 24 V Mean Well LRS-350-24", r"^PSU Mean Well LRS-350-24$", ""),
          ("Netzteil 5 V Mean Well RS-15-5", r"^PSU Mean Well RS-15-5$", ""),
          ("Mainboard BTT Octopus (Modell V1.0, Kauf V1.1)", r"^BTT Octopus", ""),
          ("Raspberry Pi 4 Model B", r"^Raspberry Pi 4 Model B$", ""),
          ("Netzeinbaustecker IEC-GS-1-100", r"^IEC-GS-1-100", ""),
          ("Lüfter San Ace 60L 9LG0624P4H001", r"^Luefter 60x60x25 #\d+ \(", ""),
          ("WAGO 221-413 (L, N)", r"^WAGO 221-413 [LN] \(", ""),
          ("WAGO 221-414 (PE)", r"^WAGO 221-414 PE \(", ""),
          ("Hutschiene EN 50022 35 × 7,5", r"^Hutschiene ", "lengths"),
          ("Rundsteckverbinder GX16-4 (Einbauteil)", r"^GX16 Koerper$", ""),
          ("Keystone-Modul RJ45", r"^Keystone RJ45 Koerper$", ""),
          ("Keystone-Modul USB", r"^Keystone USB \d Koerper$", ""),
          ("Keystone-Blindmodul", r"^Keystone Blind Koerper$", ""),
          ("Ringöse M5 (PE)", r"^PE Ringoese ", ""),
          ("Auszugschiene dreiteilig, Vollauszug, 450 mm", r"^Auszugschiene( Fern Outer)?$", ""),
          ("Original-Fuß (`Stock Foot`, vom Stock Frame umsetzen)", r"^Stock Foot$", "")]
LAYER_TITLE = [("Druckteile (gen)", "Blenden und Paneele"), ("Schlepp (gen)", "Schleppketten, Halter, fester Kanal"),
               ("Tray Druckteile (gen)", "Tray: Power-Hub, Kanäle, DIN-Halter, Lüfterhalter")]

def profiles(top):
    c = collections.Counter()
    for k in top.children:
        m = PAT.match(str(k.name))
        if m: c[(m.group(1), int(m.group(2)))] += 1
    return c

def table(c):
    rows = ["| Profil | Länge (mm) | Stück | Summe (mm) |", "|---|---:|---:|---:|"]
    for (t, L), n in sorted(c.items()): rows.append(f"| {t} | {L} | {n} | {L * n} |")
    return rows

def totals(c):
    s = collections.defaultdict(lambda: [0, 0])
    for (t, L), n in c.items(): s[t][0] += n; s[t][1] += L * n
    return s

def fmt(v):
    return f"{v:.1f}".replace(".", ",")

def bought():
    vis = {str(l.name): bool(l.visible) for l in layers}
    tops = [str(g.name) for g in groups if not g.hidden and vis.get(str(g.layer), True)]
    rows, used = [], set()
    for label, rx, note in BOUGHT:
        hit = [i for i, n in enumerate(tops) if i not in used and re.search(rx, n)]
        used.update(hit)
        extra = ""
        if note == "lengths":
            L = sorted(int(m.group(1)) for i in hit for m in [re.search(r"\((\d+) mm", tops[i])] if m)
            extra = "Längen " + ", ".join(f"{x} mm" for x in L)
        rows.append((label, len(hit), extra))
    return rows

def _write():
    by = {n: profiles(next(g for g in groups if g.name == n)) for n, _ in ASSEMBLIES}
    mod = by["Mod Frame Base"] + by["Mod Frame Drawer"]
    pp = json.load(open(ROOT + "/build/bom_parts.json", encoding="utf-8"))
    out = ["# Stückliste", "",
           f"Stand {datetime.date.today().isoformat()}. Erzeugt mit `gen/bom_document.py` aus dem IngeTrazo-Dokument (Profile, Kaufteile) "
           "und `build/bom_parts.json` (Druckteile, aus `gen/cr10mod.py build`).",
           "Längen sind Modellmaße ohne Sägezugabe. Außer dem Stock Frame sind sie nicht am Teil gegengemessen. "
           "Schrauben, Nutensteine, Kabel und Kleinteile stehen in `docs/HARDWARE.md`.", ""]
    for name, note in ASSEMBLIES:
        out += [f"## {name}", "", note, ""] + table(by[name]) + [""]
    out += ["## Zukauf Profile für den Umbau (Base + Drawer)", ""] + table(mod) + [""]
    out += ["| Typ | Stück | Gesamtlänge (mm) |", "|---|---:|---:|"]
    for t, (n, L) in sorted(totals(mod).items()): out.append(f"| {t} | {n} | {L} |")
    out += ["", "## Kaufteile im Modell", "", "Gezählt nach Gruppennamen im Dokument (sichtbare Gruppen; ausgeblendete Platzhalter zählen nicht).", "",
            "| Teil | Stück | Hinweis |", "|---|---:|---|"]
    for label, n, extra in bought(): out.append(f"| {label} | {n} | {extra} |")
    out += ["", "## Druckteile", "",
            "Volumen = Volumen des Körpers (100 % gefüllt), nicht der Filamentverbrauch des Slicers.", ""]
    total = 0.0
    for layer, title in LAYER_TITLE:
        rows = [d for d in pp if d["layer"] == layer]
        if not rows: continue
        out += [f"### {title} (`{layer}`)", "", "| Teil | STL | Stück | Volumen je Stück (cm³) | Volumen gesamt (cm³) |", "|---|---|---:|---:|---:|"]
        sub = 0.0
        for d in rows:
            v = d["count"] * d["volume_cm3"]; sub += v
            out.append(f"| {d['name']} | `{d['stl']}` | {d['count']} | {fmt(d['volume_cm3'])} | {fmt(v)} |")
        out += [f"| **Summe** | | {sum(d['count'] for d in rows)} | | **{fmt(sub)}** |", ""]
        total += sub
    unplaced = [d["name"] for d in pp if d["count"] == 0]
    out += [f"Alle platzierten Druckteile zusammen: **{fmt(total)} cm³**.", ""]
    if unplaced: out += ["Nicht platziert (nur STL, nicht in der Summe): " + ", ".join(f"`{n}`" for n in unplaced) + ".", ""]
    open(ROOT + "/docs/BOM.md", "w", encoding="utf-8").write("\n".join(out))
    print("wrote docs/BOM.md", {k: sum(c.values()) for k, c in by.items()}, "bought", [(l, n) for l, n, _ in bought()],
          "printed", sum(d["count"] for d in pp), "parts", round(total, 1), "cm3")

try:
    _write()
except Exception as e:
    print("ERR", repr(e))
