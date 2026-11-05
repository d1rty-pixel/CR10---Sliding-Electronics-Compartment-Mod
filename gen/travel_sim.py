"""Drawer travel simulation against the document (T-006 / T-007).

    (IngeTrazo) exec of gen/doc_export.py      -> build/doc_scene.json (visible groups, world triangles in mm)
    ./venv/bin/python -I gen/travel_sim.py      -> report

The document shows the drawer fully out (s = 0). Retracting by s (0..TRAVEL) moves the drawer, the tray and all parts on it
by +s in x, the middle members of both slides by +s/2; the frame, the outer slide members, the rear and side panels and the
fixed chain parts stay. The chain links are not taken from the document but from the generator for every pose (both chains).
Checks (intersection volume > VOL_EPS counts as a collision):
  1. every moving part against every fixed part, s sampled every STEP mm where the boxes overlap
  2. middle slide members against the moving and the fixed parts (s / 2)
  3. chain links of both chains against all document parts except their own end brackets, POSE_STEP mm apart
  4. drawer side walls / profiles against the inner slide members (T-007): distance and overlap at s = 0
Generated parts use the exact generator geometry (cr10mod.parts(), same names and places as in the document; their document
copies are often not closed after the polygon round trip). Bought parts come from the document; one that is not a closed solid
is reported and checked only by its box. The retracted end stop is where the drawer frame first touches the base frame; the
sweeps run up to min(TRAVEL, stop). Groups far away from the machine (x > 1000 or y > 1000: other models in the file) and the
user component "Chain Link (new)" are ignored.
"""
import json, math, os, sys
import numpy as np
from manifold3d import Manifold, Mesh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cable
import cable_thin as thin
import cr10mod

SCENE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "doc_scene.json")
TRAVEL = cable.TRAVEL
STEP, POSE_STEP, VOL_EPS = 1.0, 6.0, 1e-3

MOVING_TOPS = ("Mod Frame Drawer", "Front Panel", "Chain Bracket Moving", "Thin Bracket Moving", "PE Ringoese Tray", "WAGO ",
               "Luefter 60x60x25", "Hutschiene", "PSU Mean Well", "Raspberry Pi 4 Model B", "BTT Octopus", "Image")
MOVING_LAYERS = ("Tray Druckteile (gen)",)
MIDDLE = ("Auszugschiene Nah Middle", "Auszugschiene Fern Middle")
INNER = ("Auszugschiene Nah Inner", "Auszugschiene Fern Inner")
OUTER = ("Auszugschiene Nah Outer", "Auszugschiene Fern Outer")
CHAIN_DOC = ("Chain Link ", "Chain Lid ", "Thin Link ", "Thin Lid ")       # replaced by the generator poses
IGNORE = ("Chain Link (new)",)

def kind(g):
    p, t = g["path"], g["top"]
    if t.startswith(IGNORE) or t.startswith(CHAIN_DOC): return None
    if p in MIDDLE: return "middle"
    if p in INNER: return "moving"
    if t.startswith(MOVING_TOPS) or g["layer"] in MOVING_LAYERS: return "moving"
    return "fixed"

def to_manifold(tris):
    P = np.asarray(tris, dtype=float).reshape(-1, 3)
    key = np.round(P, 3)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    tv = inv.reshape(-1, 3).astype(np.uint32)
    tv = tv[(tv[:, 0] != tv[:, 1]) & (tv[:, 1] != tv[:, 2]) & (tv[:, 0] != tv[:, 2])]
    m = Manifold(Mesh(vert_properties=uniq.astype(np.float32), tri_verts=tv))
    if m.status().name != "NoError" or m.volume() <= 0:
        m2 = Manifold(Mesh(vert_properties=uniq.astype(np.float32), tri_verts=tv[:, ::-1].copy()))
        if m2.status().name == "NoError" and m2.volume() > 0: return m2
        return None
    return m

class Part:
    def __init__(self, g, gen=None):
        self.name, self.kind = g["path"], kind(g)
        self.gen = gen is not None
        if gen is not None:
            self.m = gen; bb = gen.bounding_box(); self.lo, self.hi = np.array(bb[:3]), np.array(bb[3:])
            return
        P = np.asarray(g["tris"], dtype=float).reshape(-1, 3)
        self.lo, self.hi = P.min(0), P.max(0)
        self.m = to_manifold(g["tris"])

S_MAX = TRAVEL                                     # set in main() to min(TRAVEL, end stop)

def box_overlap_s(a, b, fa, fb):
    """s-interval where a (moved by fa*s) and b (moved by fb*s) overlap in their boxes; None if never"""
    for k in (1, 2):
        if a.lo[k] >= b.hi[k] or b.lo[k] >= a.hi[k]: return None
    df = fa - fb                                   # relative motion of a against b in x per unit s
    lo, hi = b.lo[0] - a.hi[0], b.hi[0] - a.lo[0]   # need lo < df*s < hi
    if abs(df) < 1e-9: return (0.0, S_MAX) if lo < 0 < hi else None
    s0, s1 = sorted((lo / df, hi / df))
    s0, s1 = max(s0, 0.0), min(s1, S_MAX)
    return (s0, s1) if s0 < s1 else None

def hit(a, b, fa, fb, s):
    ma = a.m.translate((fa * s, 0, 0)); mb = b.m.translate((fb * s, 0, 0))
    return (ma ^ mb).volume()

FACT = {"moving": 1.0, "middle": 0.5, "fixed": 0.0}

def sweep(a, b):
    """[(s, volume)] for the poses where a and b intersect"""
    r = box_overlap_s(a, b, FACT[a.kind], FACT[b.kind])
    if r is None: return []
    if a.m is None or b.m is None: return [(r[0], float("nan"))]
    out = []
    for s in np.unique(np.concatenate([np.arange(r[0], r[1], STEP), [r[1]]])):
        v = hit(a, b, FACT[a.kind], FACT[b.kind], s)
        if v > VOL_EPS: out.append((float(s), v))
    return out

def summary(res):
    s = [x[0] for x in res]; v = max((x[1] for x in res), default=0.0)
    return f"s {min(s):.0f}..{max(s):.0f} mm, max {v:.1f} mm3" if res else ""

def chain_check(parts):
    """both chains, poses POSE_STEP apart: links and lids vs all parts (moving ones shifted by s); only the link hinged into
    a bracket is not checked against that bracket (fork / tongue)"""
    out = []
    for mod, tag, pre, n in ((cable, "wide", "Chain", cable.N_LINKS), (thin, "thin", "Thin", thin.N_LINKS)):
        skip = {f"{pre} Bracket Fixed": f"{pre} Link 01", f"{pre} Bracket Moving": f"{pre} Link {n:02d}"}
        for s in np.arange(0.0, S_MAX + 1e-9, POSE_STEP).tolist() + ([S_MAX] if S_MAX % POSE_STEP else []):
            xm = mod.X_MOVING_EXT + s
            links, _, _ = mod.chain_links(xm)
            for ln, _, lm in links:
                lb = lm.bounding_box()
                for p in parts:
                    if p.kind is None or skip.get(p.name) == ln.replace("Lid", "Link"): continue
                    f = FACT[p.kind] * s
                    if (lb[0] >= p.hi[0] + f or p.lo[0] + f >= lb[3] or lb[1] >= p.hi[1] or p.lo[1] >= lb[4]
                            or lb[2] >= p.hi[2] or p.lo[2] >= lb[5]): continue
                    v = float("nan") if p.m is None else (lm ^ p.m.translate((f, 0, 0))).volume()
                    if not v <= VOL_EPS: out.append((tag, s, ln, p.name, v))
    return out

def gap_x(a, b):
    """free distance in x between the boxes of a and b (negative = overlap)"""
    return max(b.lo[0] - a.hi[0], a.lo[0] - b.hi[0])

def main():
    global S_MAX
    data = json.load(open(SCENE))
    data = [g for g in data if not (np.asarray(g["tris"]).reshape(-1, 3).min(0)[:2] > 1000).any()]
    _, inst = cr10mod.parts(); gen = dict(inst)
    parts = [Part(g, gen.get(g["path"])) for g in data if kind(g) is not None]
    names = {p.name for p in parts}
    for nm in ("Thin Bracket Fixed", "Thin Bracket Moving", "Chain Bracket Fixed", "Chain Bracket Moving"):   # always the current ones
        if nm not in names: parts.append(Part(dict(path=nm, top=nm, layer="Schlepp (gen)"), gen[nm]))
    bad = [p.name for p in parts if p.m is None]
    n = {k: sum(p.kind == k for p in parts) for k in FACT}
    print(f"{len(parts)} document parts: {n['moving']} moving, {n['middle']} middle, {n['fixed']} fixed; not closed (box only): {', '.join(bad) or 'none'}")
    mov = [p for p in parts if p.kind == "moving"]; mid = [p for p in parts if p.kind == "middle"]
    fix = [p for p in parts if p.kind == "fixed"]
    print(f"generated parts from the generator: {sum(p.gen for p in parts)}")
    # end stop: first contact of the drawer frame with the base frame (boxes, then exact)
    stop = TRAVEL
    for a in (p for p in mov if p.name.startswith("Mod Frame Drawer/")):
        for b in (p for p in fix if p.name.startswith("Mod Frame Base/")):
            if a.lo[1] >= b.hi[1] or b.lo[1] >= a.hi[1] or a.lo[2] >= b.hi[2] or b.lo[2] >= a.hi[2]: continue
            g = b.lo[0] - a.hi[0]
            if 0 <= g < stop: stop, who = g, (a.name, b.name)
    S_MAX = min(TRAVEL, stop)
    print(f"end stop: drawer frame touches the base frame at s {stop:.2f} ({who[0]} on {who[1]}); TRAVEL {TRAVEL:.1f} -> checks up to s {S_MAX:.2f}"
          if stop < TRAVEL else f"no frame contact up to TRAVEL {TRAVEL:.1f}")
    print("\n1. moving parts against fixed parts (s = 0 .. %.2f retracting)" % S_MAX)
    c1 = [(a.name, b.name, r) for a in mov for b in fix for r in [sweep(a, b)] if r]
    for a, b, r in c1: print(f"  HIT   {a}  x  {b}: {summary(r)}")
    if not c1: print("  ok    no collision")
    print("\n2. middle slide members against moving and fixed parts (except the members of the same slide, see 4.)")
    own = set(INNER) | set(OUTER)
    c2 = [(a.name, b.name, r) for a in mid for b in mov + fix if b.name not in own for r in [sweep(a, b)] if r]
    for a, b, r in c2: print(f"  HIT   {a}  x  {b}: {summary(r)}")
    if not c2: print("  ok    no collision")
    print(f"\n3. chain links (generator poses every {POSE_STEP:.0f} mm) against document parts")
    c3 = chain_check(parts)
    agg = {}
    for tag, s, ln, pn, v in c3:
        k = (tag, pn); a = agg.setdefault(k, [s, s, 0.0, set()]); a[0] = min(a[0], s); a[1] = max(a[1], s); a[2] = max(a[2], v); a[3].add(ln)
    for (tag, pn), (s0, s1, v, ls) in sorted(agg.items()):
        print(f"  HIT   {tag} chain x {pn}: s {s0:.0f}..{s1:.0f}, max {v:.1f} mm3, links {', '.join(sorted(ls))}")
    if not c3: print("  ok    no collision")
    print("\n4. slides: inner members against the drawer, middle against inner/outer (s = 0)")
    byname = {p.name: p for p in parts}
    for side, inner, outer, mid_n in (("near", INNER[0], OUTER[0], MIDDLE[0]),
                                      ("far", INNER[1], OUTER[1], MIDDLE[1])):
        pi = byname[inner]
        prof = [p for p in mov if p.name.startswith("Mod Frame Drawer/") and p.lo[0] < pi.hi[0] and pi.lo[0] < p.hi[0]
                and p.lo[2] < pi.hi[2] and pi.lo[2] < p.hi[2]]
        for p in prof:
            dy = max(p.lo[1] - pi.hi[1], pi.lo[1] - p.hi[1])
            v = (pi.m ^ p.m).volume() if pi.m and p.m else float("nan")
            if dy < 5.0:
                print(f"  info  {side} inner y {pi.lo[1]:.1f}..{pi.hi[1]:.1f} z {pi.lo[2]:.1f}..{pi.hi[2]:.1f}  vs  {p.name} y {p.lo[1]:.1f}..{p.hi[1]:.1f} z {p.lo[2]:.1f}..{p.hi[2]:.1f}: gap y {dy:.2f}, overlap {v:.1f} mm3")
        for a, b in ((mid_n, inner), (mid_n, outer), (inner, outer)):
            pa, pb = byname[a], byname[b]
            v = (pa.m ^ pb.m).volume() if pa.m and pb.m else float("nan")
            print(f"  info  {side}: {a.split('/')[-1]} x {b.split('/')[-1]} at s = 0: overlap {v:.2f} mm3")
    print("\n5. fixed parts touching the slides (both fixed, info): outer slide members against the feet and the base")
    for o in OUTER:
        po = byname[o]
        for p in fix:
            if p is po or p.m is None or any(po.lo[k] >= p.hi[k] or p.lo[k] >= po.hi[k] for k in range(3)): continue
            ii = po.m ^ p.m
            if ii.volume() > VOL_EPS:
                bb = ii.bounding_box()
                print(f"  info  {o.split('/')[-1]} x {p.name}: {ii.volume():.1f} mm3 in x {bb[0]:.1f}..{bb[3]:.1f} y {bb[1]:.1f}..{bb[4]:.1f} z {bb[2]:.1f}..{bb[5]:.1f}")
    print("\n" + ("all travel checks passed" if not (c1 or c2 or c3) else "TRAVEL COLLISIONS FOUND"))

if __name__ == "__main__":
    main()
