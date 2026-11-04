# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/rail_import.py", encoding="utf-8").read())
# Puts the display model of build/rails.json (made by gen/rail_model.py) into the groups "Hutschiene R1a/R1b/R2 ...".
# The mesh of each group is replaced (name, layer and group stay); a missing or ambiguous group raises (step rolls back).
import json
from collections import Counter

RAIL_JSON = "G:/Things/CR10---Sliding-Electronics-Compartment-Mod/build/rails.json"

def _addo(msh, loop, want, holes=None, col=None):
    f = msh.add_face(loop, holes)
    if QVector3D.dotProduct(f.normal(), want) < 0:
        msh.remove_face(f)
        f = msh.add_face(loop[::-1], [h[::-1] for h in holes] if holes else None)
    if col: f.attrs["color"] = col
    return f

_P = lambda c: QVector3D(c[0] / 1000, c[1] / 1000, c[2] / 1000)
for d in json.load(open(RAIL_JSON)):
    tgt = [g for g in groups if str(g.name).startswith(f"Hutschiene {d['rail']} ")]
    if len(tgt) != 1: raise RuntimeError(f"rail {d['rail']}: {len(tgt)} groups found")
    col = tuple(d["color"]) + (1.0,)
    msh = Mesh()
    for f in d["faces"]:
        _addo(msh, [_P(c) for c in f["outer"]], QVector3D(*f["n"]), [[_P(c) for c in h] for h in f["holes"]] or None, col)
    tgt[0].mesh = msh
    print("rail", d["rail"], len(list(msh.faces)), "faces, edges", dict(Counter(len(e.faces) for e in msh.edges)))
viewport.update()
