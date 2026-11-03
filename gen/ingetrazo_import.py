# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/ingetrazo_import.py", encoding="utf-8").read())
# (Re)imports build/parts.json. Groups on the generated layers are replaced. Hand-built predecessors are hidden, never deleted.
import json
from collections import Counter
from core.layers import Layer

PARTS_JSON = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/parts.json"
GEN_LAYERS = ["Druckteile (gen)", "Schlepp (gen)", "Tray Druckteile (gen)"]
OLD_LAYER = "Handbau (alt)"
OLD_TOP = ("Panel Schalter", "Panel Anschluesse", "Front links", "Front rechts")   # hand-built groups from the 80 mm conversion
# paths: top-level name, then child index or child name (drawer children shifted when the white ducts were deleted, 2026-11-03)
OLD_NESTED = [("Mod Frame Base", 10), ("Mod Frame Base", 11), ("Mod Frame Base", 12), ("Mod Frame Base", 13),   # stretched hex panels
              ("Mod Frame Drawer", "Gruppieren#51", 2), ("Mod Frame Drawer", "Gruppieren#42", 2),              # old front grilles
              ("Mod Frame Base", 14, 0, 1), ("Mod Frame Drawer", "Gruppieren#51", 1), ("Mod Frame Drawer", "Gruppieren#42", 1)]   # original clips

def _layer(nm, visible=True):
    for l in layers:
        if l.name == nm: return l
    l = Layer(nm); layers.append(l)
    if not visible:
        try: l.visible = False
        except Exception as e: print("hide", nm, e)
    return l

def addo(msh, loop, want, holes=None, col=None):
    """add a face and make sure its normal points along `want`"""
    f = msh.add_face(loop, holes)
    if QVector3D.dotProduct(f.normal(), want) < 0:
        msh.remove_face(f)
        f = msh.add_face(loop[::-1], [h[::-1] for h in holes] if holes else None)
    if col: f.attrs["color"] = col
    return f

def build_mesh(d):
    m = Mesh(); col = tuple(d["color"]) + (1.0,)
    P = lambda c: QVector3D(c[0] / 1000, c[1] / 1000, c[2] / 1000)      # mm -> m
    for f in d["faces"]:
        addo(m, [P(c) for c in f["outer"]], QVector3D(*f["n"]), [[P(c) for c in h] for h in f["holes"]] or None, col)
    return m

def check(m):   # every edge must have exactly 2 faces
    return dict(Counter(len(e.faces) for e in m.edges))

# 1. generated layers: remove old generated groups
for nm in GEN_LAYERS: _layer(nm)
for g in [g for g in groups if g.layer in GEN_LAYERS and "(new)" not in str(g.name)]: groups.remove(g)   # "(new)" = hand-made components, never touched
# 2. hide hand-built predecessors (idempotent: only groups still outside the generated layers)
_layer(OLD_LAYER, visible=False)
for g in groups:
    if str(g.name).startswith(OLD_TOP) and g.layer not in GEN_LAYERS: g.layer = OLD_LAYER
for pth in OLD_NESTED:
    try:
        g = [t for t in groups if str(t.name) == pth[0]][0]
        for k in pth[1:]: g = list(g.children)[k] if isinstance(k, int) else [c for c in g.children if str(c.name) == k][0]
        g.hidden = True
    except Exception as e: print("skip", pth, repr(e)[:80])
# 3. import
made = []
for d in json.load(open(PARTS_JSON)):
    g = Group(build_mesh(d), name=d["name"]); g.layer = d["layer"]; g.component = False; groups.append(g); made.append(g)
print({g.name: check(g.mesh) for g in made})
viewport.update()
