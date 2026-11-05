# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/ingetrazo_import.py", encoding="utf-8").read())
# (Re)imports build/parts.json. Generated groups carry ext["cr10mod"]["generated"] and are replaced; their layer comes
# from gen/cr10mod.py and may hold hand-made or vendor groups too. Hand-built predecessors: gen/organize_document.py.
import json
from collections import Counter
from core.layers import Layer

PARTS_JSON = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/parts.json"
MARK = "cr10mod"
# layers that held only generated groups before the marker existed (T-042); groups on them count as generated
LEGACY_GEN_LAYERS = ["Druckteile (gen)", "Schlepp (gen)", "Tray Druckteile (gen)", "Kabel (gen)"]

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

# 1. remove the previous generated groups ("(new)" = hand-made components on the old generated layers, never touched)
def _generated(g):
    return (g.ext or {}).get(MARK, {}).get("generated") or (g.layer in LEGACY_GEN_LAYERS and "(new)" not in str(g.name))
for g in [g for g in groups if _generated(g)]: groups.remove(g)
# 2. import
made = []
for d in json.load(open(PARTS_JSON)):
    _layer(d["layer"])
    g = Group(build_mesh(d), name=d["name"]); g.layer = d["layer"]; g.component = False; g.ext = {MARK: {"generated": True}}
    groups.append(g); made.append(g)
print({g.name: check(g.mesh) for g in made})
viewport.update()
