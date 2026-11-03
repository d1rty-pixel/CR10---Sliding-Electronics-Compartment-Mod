# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/bom_document.py", encoding="utf-8").read())
# Reads the profile groups (named "<2020|2040> L=<mm> #n") from the open document and the printed parts from build/parts.json,
# writes docs/BOM.md. The profile data comes from the model, never typed by hand.
import re, json, datetime, collections

ROOT = "G:/Things/CR10---Sliding-Electronics-Compartment-Mod"
ASSEMBLIES = [("Stock Frame", "Original-CR10-Rahmen, bleibt unverändert, nichts zu kaufen"),
              ("Mod Frame Base", "fester Unterbau"),
              ("Mod Frame Drawer", "Auszug")]
PAT = re.compile(r"^(2020|2040) L=(\d+) #\d+$")

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

by = {n: profiles(next(g for g in groups if g.name == n)) for n, _ in ASSEMBLIES}
mod = by["Mod Frame Base"] + by["Mod Frame Drawer"]
KIND = [("Bezel", "Bezel Ring"), ("Switch Plug", "Switch Plug"), ("Connector Plug", "Connector Plug"),
        ("Front Grille", "Front Grille"), ("Side Panel", "Side Panel Hex")]
printed = collections.Counter()
for d in json.load(open(ROOT + "/build/parts.json")):
    if d["layer"] == "Druckteile (gen)": printed[next(k for p, k in KIND if d["name"].startswith(p))] += 1

out = ["# Stückliste", "",
       f"Stand {datetime.date.today().isoformat()}. Erzeugt aus dem IngeTrazo-Dokument mit `gen/bom_document.py` (Profile) und `build/parts.json` (Druckteile).",
       "Längen sind Modellmaße ohne Sägezugabe. Außer dem Stock Frame sind sie nicht am Teil gegengemessen.", ""]
for name, note in ASSEMBLIES:
    out += [f"## {name}", "", note, ""] + table(by[name]) + [""]
out += ["## Zukauf Profile für den Umbau (Base + Drawer)", ""] + table(mod) + [""]
out += ["| Typ | Stück | Gesamtlänge (mm) |", "|---|---:|---:|"]
for t, (n, L) in sorted(totals(mod).items()): out.append(f"| {t} | {n} | {L} |")
out += ["", "## Weitere Kaufteile (aus dem Modell, ohne Schrauben und Nutensteine)", "",
        "- Auszugschienen, dreiteilig, Vollauszug, 450 mm: 2 Stück (je Seite eine), Befestigung mit M5 und Nutensteinen, je ein Loch mittig in Außen- und Innenschiene",
        "- Original-Füße (`Stock Foot`): 4 Stück, vom Stock Frame abschrauben und am Mod-Rahmen wieder anschrauben", "",
        "## Druckteile (`Druckteile (gen)`)", "", "| Teil | Stück |", "|---|---:|"]
for n, k in printed.items(): out.append(f"| {n} | {k} |")
out += ["", "`Side Panel Fan60` existiert nur als STL und ist noch nicht platziert.", ""]
open(ROOT + "/docs/BOM.md", "w", encoding="utf-8").write("\n".join(out))
print("wrote docs/BOM.md", {k: sum(c.values()) for k, c in by.items()})
