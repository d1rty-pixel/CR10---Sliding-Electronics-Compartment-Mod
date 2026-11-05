# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/vendor_import.py", encoding="utf-8").read())
# Puts the vendor models of build/vendor/*.json (made by gen/step_to_mesh.py) into their groups in the document. The groups
# exist only in the model: the mesh of each is replaced in place (name, layer, position and Newton data stay), the new mesh
# keeps the old one's lower box corner, or with `at` (world mm) puts the source origin there. A missing or ambiguous group raises (step rolls back); nothing is created or deleted.
# `at` is in generator mm (see gen/doc_frame.py). `paint(c)` -> colour from a face's source-coordinate centroid.
import json
import runpy
Z0_MM = runpy.run_path("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/doc_frame.py")["Z0_MM"]   # document = generator + Z0_MM in Z (gen/doc_frame.py)

VENDOR_DIR = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/vendor/"
# rot maps source axes to world axes: world = (s[i0]*sign0, s[i1]*sign1, s[i2]*sign2)
MODELS = [
    dict(name="PSU Mean Well LRS-350-24", json="lrs350.json", rot=((0, -1), (1, -1), (2, 1))),   # terminals -X in source, +X wanted
    dict(name="PSU Mean Well RS-15-5", json="rs15.json", rot=((0, 1), (1, 1), (2, 1))),    # terminals -X as in the source (2026-11-04, T-033 turned back)
    dict(name="Raspberry Pi 4 Model B", json="pi4.json", rot=((0, -1), (2, 1), (1, 1))),       # source is Y-up; turned 180 deg: ports -X
    dict(name="BTT Octopus (V1.0 STEP)", json="octopus.json", rot=((0, -1), (1, -1), (2, 1))),   # screw terminals -X in source, +X wanted
    # Adam Tech STEP: origin = flange front centre, +z out of the panel, long side y, rocker at -y, one colour only.
    # Flange back (z -3) on the switch plug's outer face x 534.7, centre on the switch (y 558 - 4.6, z 65); long side along y.
    dict(name="IEC-GS-1-100 Inlet with Switch and Fuse", json="iec_gs_1_100.json", rot=((2, 1), (1, -1), (0, 1)),
         at=(537.7, 553.4, 65.0),
         paint=lambda c: (0.78, 0.78, 0.74) if c[2] < -21.0 else (0.08, 0.08, 0.08)),   # QC terminals tin, insulator black
]

def _box(g):
    P = [v.position for v in g.mesh.vertices]
    return [f(getattr(p, k)() for p in P) for k in ("x", "y", "z") for f in (min, max)]

ONLY = globals().get("VENDOR_ONLY")   # optional list of json names, for testing one model
import os
_todo = [m for m in MODELS if not ONLY or m["json"] in ONLY]
_missing = [m["json"] for m in _todo if not os.path.exists(VENDOR_DIR + m["json"])]
if _missing: raise FileNotFoundError("missing in build/vendor: " + ", ".join(_missing))
for m in _todo:
    tgt = [g for g in groups if str(g.name) == m["name"]]
    if len(tgt) != 1: raise RuntimeError(f"{m['name']}: {len(tgt)} groups found")
    g = tgt[0]
    x0, _, y0, _, z0, _ = _box(g)
    d = json.load(open(VENDOR_DIR + m["json"]))
    R = lambda v: [v[i] * s for i, s in m["rot"]]
    V = [R(v) for v in d["verts"]]
    lo = [min(v[k] for v in V) for k in range(3)]
    off = (m["at"][0] / 1000, m["at"][1] / 1000, (m["at"][2] + Z0_MM) / 1000) if "at" in m else (x0 - lo[0] / 1000, y0 - lo[1] / 1000, z0 - lo[2] / 1000)
    Q = [QVector3D(v[0] / 1000 + off[0], v[1] / 1000 + off[1], v[2] / 1000 + off[2]) for v in V]
    cols = [tuple(c) + (1.0,) for c in d["colors"]]
    SV = d["verts"]
    def col(ids, ci):
        if "paint" not in m: return cols[ci]
        return tuple(m["paint"]([sum(SV[i][k] for i in ids) / len(ids) for k in range(3)])) + (1.0,)
    msh = Mesh(); bad = 0
    for t in d["tris"]:
        try:
            f = msh.add_face([Q[t[0]], Q[t[1]], Q[t[2]]]); f.attrs["color"] = col(t[:3], t[3])
        except Exception: bad += 1
    for p in d.get("polys", []):
        try:
            f = msh.add_face([Q[i] for i in p["o"]], [[Q[i] for i in h] for h in p["h"]] or None)
            if QVector3D.dotProduct(f.normal(), QVector3D(*R(p["n"]))) < 0:   # same guard as ingetrazo_import.addo
                msh.remove_face(f)
                f = msh.add_face([Q[i] for i in p["o"]][::-1], [[Q[i] for i in h][::-1] for h in p["h"]] or None)
            f.attrs["color"] = col(p["o"], p["c"])
        except Exception: bad += 1
    g.mesh = msh
    print(m["name"], len(d["tris"]), "tris +", len(d.get("polys", [])), "polys, failed", bad, "box mm", [round(v * 1000, 1) for v in _box(g)])
viewport.update()
