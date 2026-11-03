# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen/vendor_import.py", encoding="utf-8").read())
# Replaces the hand-made electronics placeholders (layer "Electronics (neu)") with vendor models from build/vendor/*.json
# (made by gen/step_to_mesh.py). Placeholders are hidden, never deleted. Vendor groups are replaced on every run.
# Placement: rotate the source model, centre it in X/Y on the placeholder's box, put `z_ref` (source mm, after rotation) on its bottom;
# or, with `at` (world mm), put the source origin there. `paint(c)` -> colour from a face's source-coordinate centroid.
import json
from core.layers import Layer

VENDOR_DIR = "G:/Things/CR10---Sliding-Electronics-Compartment-Mod/build/vendor/"
VENDOR_LAYER = "Electronics (vendor)"
PLACEHOLDER_LAYER = "Electronics (Platzhalter)"
# rot maps source axes to world axes: world = (s[i0]*sign0, s[i1]*sign1, s[i2]*sign2)
MODELS = [
    dict(name="PSU Mean Well LRS-350-24", json="lrs350.json", ph="PSU LRS-200-24", rot=((0, -1), (1, -1), (2, 1)), z_ref=None),   # terminals -X in source, +X wanted
    dict(name="PSU Mean Well RS-15-5", json="rs15.json", ph="PSU LRS-15-5", rot=((0, 1), (1, 1), (2, 1)), z_ref=None),
    dict(name="Raspberry Pi 4 Model B", json="pi4.json", ph="Raspberry Pi 4", rot=((0, 1), (2, -1), (1, 1)), z_ref=-0.8),       # source is Y-up, PCB y -0.8..0.8
    dict(name="BTT Octopus (V1.0 STEP)", json="octopus.json", ph="BTT Octopus V1.1", rot=((0, -1), (1, -1), (2, 1)), z_ref=-1.6),   # screw terminals -X in source, +X wanted
    # Adam Tech STEP: origin = flange front centre, +z out of the panel, long side y, rocker at -y, one colour only.
    # Flange back (z -3) on the switch plug's outer face x 534.7, centre on the switch (y 558 - 4.6, z 65); long side along y.
    dict(name="IEC-GS-1-100 Kaltgeraetestecker mit Schalter und Sicherung", json="iec_gs_1_100.json", ph=None,
         rot=((2, 1), (1, -1), (0, 1)), at=(537.7, 553.4, 65.0),
         paint=lambda c: (0.78, 0.78, 0.74) if c[2] < -21.0 else (0.08, 0.08, 0.08)),   # QC terminals tin, insulator black
]

def _layer(nm):
    for l in layers:
        if l.name == nm: return l
    l = Layer(nm); layers.append(l); return l

def _box(g):
    P = [v.position for v in g.mesh.vertices]
    return [f(getattr(p, k)() for p in P) for k in ("x", "y", "z") for f in (min, max)]

ONLY = globals().get("VENDOR_ONLY")   # optional list of json names, for testing one model
_layer(VENDOR_LAYER); _layer(PLACEHOLDER_LAYER)
_names = [m["name"] for m in MODELS if not ONLY or m["json"] in ONLY]
for g in [g for g in groups if g.layer == VENDOR_LAYER and str(g.name) in _names]: groups.remove(g)
made = []
for m in MODELS:
    if ONLY and m["json"] not in ONLY: continue
    ph = None
    if m["ph"]:
        ph = [g for g in groups if str(g.name).startswith(m["ph"])]
        if not ph: print("no placeholder", m["ph"]); continue
        ph = ph[0]; x0, x1, y0, y1, z0, z1 = _box(ph)
    d = json.load(open(VENDOR_DIR + m["json"]))
    R = lambda v: [v[i] * s for i, s in m["rot"]]
    V = [R(v) for v in d["verts"]]
    if "at" in m:
        off = tuple(c / 1000 for c in m["at"])
    else:
        lo = [min(v[k] for v in V) for k in range(3)]; hi = [max(v[k] for v in V) for k in range(3)]
        zr = lo[2] if m["z_ref"] is None else m["z_ref"]
        off = ((x0 + x1) / 2 - (lo[0] + hi[0]) / 2000, (y0 + y1) / 2 - (lo[1] + hi[1]) / 2000, z0 - zr / 1000)
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
    g = Group(msh, name=m["name"]); g.layer = VENDOR_LAYER; g.component = False; groups.append(g); made.append(g)
    if ph: ph.layer = PLACEHOLDER_LAYER
    print(m["name"], len(d["tris"]), "tris +", len(d.get("polys", [])), "polys, failed", bad, "box mm", [round(v * 1000, 1) for v in _box(g)])
try: [l for l in layers if l.name == PLACEHOLDER_LAYER][0].visible = False
except Exception as e: print("hide", repr(e))
viewport.update()
