#!/usr/bin/env python3
"""Triangulate a vendor STEP file into a coloured mesh JSON for vendor_import.py.

Needs OpenCascade bindings (pip install cadquery-ocp) in a separate venv: vendor models are
reference geometry, not printed parts, so they stay out of the generator venv.
(gmsh was tried first: far too slow on the 10k-face board models.)

usage: step_to_mesh.py IN.step OUT.json [--defl MM] [--ang RAD] [--min-solid MM]
Output: {"name", "bbox": [x0,x1,y0,y1,z0,z1], "verts": [[x,y,z],...], "tris": [[i,j,k,colour_index],...],\n         "polys": [{"n", "o": outer ids, "h": [hole ids], "c": colour_index}] (planar faces), "colors": [[r,g,b],...]}
Coordinates in mm, as in the STEP file (no placement).
"""
import argparse, json, sys
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorSurf, XCAFDoc_ColorGen
from OCP.TDF import TDF_Label
from OCP.OCP.collections import Sequence_TDF_Label as TDF_LabelSequence
from OCP.Quantity import Quantity_Color
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--defl", type=float, default=0.3, help="linear deflection in mm")
ap.add_argument("--ang", type=float, default=0.6, help="angular deflection in rad")
ap.add_argument("--min-solid", type=float, default=0.0, help="skip shapes whose bbox diagonal is below this (tiny SMD parts)")
a = ap.parse_args()

doc = TDocStd_Document(TCollection_ExtendedString("doc"))
rd = STEPCAFControl_Reader(); rd.SetColorMode(True); rd.SetNameMode(True)
if rd.ReadFile(a.inp) != 1: sys.exit("cannot read " + a.inp)
rd.Transfer(doc)
st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
lin = Quantity_Color.Convert_LinearRGB_To_sRGB_s

def label_colour(lab):
    c = Quantity_Color()
    for t in (XCAFDoc_ColorSurf, XCAFDoc_ColorGen):
        if ct.GetColor_s(lab, t, c): return (round(lin(c.Red()), 3), round(lin(c.Green()), 3), round(lin(c.Blue()), 3))
    return None

verts, vidx, tris, colors, cidx = [], {}, [], [], {}
meshed, skipped = set(), 0
polys = []

def polygon(ft):
    """planar face triangles -> {"n", "o": outer ids, "h": [hole ids]}; None if the boundary is not one clean outer loop"""
    cnt = {}
    for t in ft:
        for k in range(3):
            e = (t[k], t[(k + 1) % 3]); cnt[e] = cnt.get(e, 0) + 1
    if any(v > 1 for v in cnt.values()): return None
    nxt = {}
    for e in cnt:
        if (e[1], e[0]) in cnt: continue
        if e[0] in nxt: return None                  # loops touching in one vertex: keep triangles
        nxt[e[0]] = e[1]
    loops = []
    while nxt:
        s0 = next(iter(nxt)); L = [s0]; c = nxt.pop(s0)
        while c != s0:
            if c not in nxt: return None
            L.append(c); c = nxt.pop(c)
        loops.append(L)
    p = [verts[i] for i in ft[0]]
    u = [p[1][k] - p[0][k] for k in range(3)]; w = [p[2][k] - p[0][k] for k in range(3)]
    n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
    ln = sum(x * x for x in n) ** 0.5
    if ln == 0: return None
    n = [x / ln for x in n]
    def area(L):                                     # Newell, signed along n
        sx = sy = sz = 0.0
        for i in range(len(L)):
            a_, b_ = verts[L[i]], verts[L[(i + 1) % len(L)]]
            sx += (a_[1] - b_[1]) * (a_[2] + b_[2]); sy += (a_[2] - b_[2]) * (a_[0] + b_[0]); sz += (a_[0] - b_[0]) * (a_[1] + b_[1])
        return (sx * n[0] + sy * n[1] + sz * n[2]) / 2
    outs = [L for L in loops if area(L) > 0]
    if len(outs) != 1: return None
    return {"n": [round(x, 5) for x in n], "o": outs[0], "h": [L for L in loops if L is not outs[0]]}

def vid(p):
    k = (round(p.X(), 3), round(p.Y(), 3), round(p.Z(), 3))
    if k not in vidx: vidx[k] = len(verts); verts.append(list(k))
    return vidx[k]

def cid(c):
    if c not in cidx: cidx[c] = len(colors); colors.append(list(c))
    return cidx[c]

def emit(lab, loc, inherited):
    global skipped
    shape = st.GetShape_s(lab)
    bb = Bnd_Box(); BRepBndLib.Add_s(shape, bb)
    if bb.IsVoid(): return
    if bb.SquareExtent() ** 0.5 < a.min_solid: skipped += 1; return
    base = label_colour(lab) or inherited or (0.6, 0.6, 0.6)
    face_col = {}                                    # sub-shape colours (per-face styling in the STEP)
    subs = TDF_LabelSequence(); st.GetSubShapes_s(lab, subs)
    for i in range(1, subs.Length() + 1):
        c = label_colour(subs.Value(i))
        if c is None: continue
        ex = TopExp_Explorer(st.GetShape_s(subs.Value(i)), TopAbs_FACE)
        while ex.More(): face_col[hash(ex.Current().Located(TopLoc_Location()))] = c; ex.Next()
    key = hash(shape.Located(TopLoc_Location()))
    if key not in meshed: BRepMesh_IncrementalMesh(shape, a.defl, False, a.ang, True); meshed.add(key)
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()); fl = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(f, fl)
        if tri is not None:
            tr = loc.Multiplied(fl).Transformation()
            ids = [None] + [vid(tri.Node(i).Transformed(tr)) for i in range(1, tri.NbNodes() + 1)]
            ci = cid(face_col.get(hash(f.Located(TopLoc_Location())), base))
            rev = f.Orientation() == TopAbs_REVERSED
            ft = []
            for i in range(1, tri.NbTriangles() + 1):
                n1, n2, n3 = tri.Triangle(i).Get()
                t = [ids[n1], ids[n3], ids[n2]] if rev else [ids[n1], ids[n2], ids[n3]]
                if len(set(t)) == 3: ft.append(t)
            pl = polygon(ft) if ft and BRepAdaptor_Surface(f).GetType() == GeomAbs_Plane else None
            if pl: polys.append(dict(pl, c=ci))
            else: tris.extend(t + [ci] for t in ft)
        ex.Next()

def walk(lab, loc, inherited):
    inherited = label_colour(lab) or inherited
    if st.IsAssembly_s(lab):
        comps = TDF_LabelSequence(); st.GetComponents_s(lab, comps)
        for i in range(1, comps.Length() + 1):
            comp = comps.Value(i); ref = TDF_Label(); st.GetReferredShape_s(comp, ref)
            walk(ref, loc.Multiplied(st.GetLocation_s(comp)), label_colour(comp) or inherited)
    else:
        emit(lab, loc, inherited)

free = TDF_LabelSequence(); st.GetFreeShapes(free)
for i in range(1, free.Length() + 1): walk(free.Value(i), TopLoc_Location(), None)

xs, ys, zs = zip(*verts)
bbox = [min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)]
json.dump({"name": a.inp.rsplit("/", 1)[-1], "bbox": bbox, "verts": verts, "tris": tris, "polys": polys, "colors": colors}, open(a.out, "w"))
print(f"{a.out}: {len(tris)} tris + {len(polys)} polygons, {len(verts)} verts, {len(colors)} colours, skipped {skipped}, bbox {[round(v, 1) for v in bbox]}", file=sys.stderr)
