# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/rail_import.py", encoding="utf-8").read())
# Puts the display model of build/rails.json (made by gen/rail_model.py) into the groups "DIN Rail L1/L2/R1 ...".
# The mesh of each group is replaced (name, layer and group stay); a missing or ambiguous group raises (step rolls back).
import json
import runpy
Z0_MM = runpy.run_path("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/doc_frame.py")["Z0_MM"]   # document = generator + Z0_MM in Z (gen/doc_frame.py)
from collections import Counter

RAIL_JSON = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/rails.json"

def _addo(msh, loop, want, holes=None, col=None):
    f = msh.add_face(loop, holes)
    if QVector3D.dotProduct(f.normal(), want) < 0:
        msh.remove_face(f)
        f = msh.add_face(loop[::-1], [h[::-1] for h in holes] if holes else None)
    if col: f.attrs["color"] = col
    return f

_P = lambda c: QVector3D(c[0] / 1000, c[1] / 1000, (c[2] + Z0_MM) / 1000)
for d in json.load(open(RAIL_JSON)):
    tgt = [g for g in groups if str(g.name).startswith(f"DIN Rail {d['rail']} ")]
    if len(tgt) != 1: raise RuntimeError(f"rail {d['rail']}: {len(tgt)} groups found")
    col = tuple(d["color"]) + (1.0,)
    msh = Mesh()
    for f in d["faces"]:
        _addo(msh, [_P(c) for c in f["outer"]], QVector3D(*f["n"]), [[_P(c) for c in h] for h in f["holes"]] or None, col)
    tgt[0].mesh = msh
    print("rail", d["rail"], len(list(msh.faces)), "faces, edges", dict(Counter(len(e.faces) for e in msh.edges)))
viewport.update()
