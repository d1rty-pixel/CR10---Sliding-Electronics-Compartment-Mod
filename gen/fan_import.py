# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/fan_import.py", encoding="utf-8").read())
# Puts the display model of build/fan60.json (made by gen/fan_model.py) into the groups "Fan 60x60x25 #1..4 (...)".
# The mesh of each group is replaced (name, layer and group stay).
import json
import runpy
Z0_MM = runpy.run_path("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/doc_frame.py")["Z0_MM"]   # document = generator + Z0_MM in Z (gen/doc_frame.py)
from collections import Counter

FAN_JSON = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/fan60.json"

def _addo(msh, loop, want, holes=None, col=None):
    f = msh.add_face(loop, holes)
    if QVector3D.dotProduct(f.normal(), want) < 0:
        msh.remove_face(f)
        f = msh.add_face(loop[::-1], [h[::-1] for h in holes] if holes else None)
    if col: f.attrs["color"] = col
    return f

_P = lambda c: QVector3D(c[0] / 1000, c[1] / 1000, (c[2] + Z0_MM) / 1000)
_data = json.load(open(FAN_JSON))
for k in sorted({d["fan"] for d in _data}):
    tgt = [g for g in groups if str(g.name).startswith(f"Fan 60x60x25 #{k} (")]
    if len(tgt) != 1: print("fan", k, "groups found:", len(tgt)); continue
    msh = Mesh()
    for d in [d for d in _data if d["fan"] == k]:
        col = tuple(d["color"]) + (1.0,)
        for f in d["faces"]:
            _addo(msh, [_P(c) for c in f["outer"]], QVector3D(*f["n"]), [[_P(c) for c in h] for h in f["holes"]] or None, col)
    tgt[0].mesh = msh
    print("fan", k, len(list(msh.faces)), "faces, edges", dict(Counter(len(e.faces) for e in msh.edges)))
viewport.update()
