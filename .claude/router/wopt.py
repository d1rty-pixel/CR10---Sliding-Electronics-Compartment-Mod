"""offline router: finds free waypoints for the 230 V wires (penalty = intersection volume + bend radius deficit)."""
import sys, json, math
import numpy as np
sys.path.insert(0, "G:/Things/CR10---Sliding-Electronics-Compartment-Mod/gen")
from manifold3d import Manifold
import tray, cable_thin as thin, power_hub as hub
from cable import box
import wiring as W

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
REG = box(-160, -55, 555, 620, 15, 62)
obs = Manifold()
for n, _, m, _ in tray.parts():
    if n.startswith(("Mains Hub", "DC Hub")): obs = obs + (m ^ REG)
obs = obs + (thin.bracket_moving() ^ REG)
for nm, a, b in hub.wago_slots(): obs = obs + box(a, b, hub.W_Y0, hub.W_Y0 + hub.W_THK, hub.W_Z0, W.W_TOP)   # WAGO bodies
obs = obs + box(-364, -151.5, 475, 590, 25, 55.9) + box(-63, 12, 530.8, 581.8, 25, 53)                    # PSU cases
obs = obs + box(-300, 100, 605, 625, 5, 25)                                                                # tray 2020
CL = 0.4                     # clearance added to the diameter while routing
LW = 0.3                     # length weight
RQ = 12.0

V = lambda lo, hi: ("v", lo, hi)
BX, BY, BZ = (-146.0, -66.0), (559.5, 601.5), (19.0, 54.5)
FREE = lambda: (V(*BX), V(*BY), V(*BZ))
E = W.wago_entry
Ye, Zt = W.W_ENTRY_Y, W.W_TOP
sx, sy, sz = W._sheath_exit(); e = W.SHEATH_END_Y
core = {"L": (sx - 1.75, e, sz + 1.01), "N": (sx + 1.75, e, sz + 1.01), "PE": (sx + 1.75, e, sz - 2.02)}
stub = lambda p: (p[0], p[1], V(44.0, 54.0))
LX, RX = -151.5, -63.0
T = {}   # name -> (template, kink corner indices)
for nm, k in (("L", 1), ("N", 1), ("PE", 1)):
    w = E(nm, k); T[f"230V {nm} Kette-WAGO"] = ([core[nm], FREE(), FREE(), stub(w), w], [])
w = E("L", 0); T["230V L WAGO-LRS"] = ([w, stub(w), FREE(), FREE(), (V(-140, -118), 580.75, 36.0), (LX, 580.75, 36.0)], [])
w = E("N", 0); T["230V N WAGO-LRS"] = ([w, stub(w), FREE(), FREE(), (V(-140, -118), 571.25, 36.0), (LX, 571.25, 36.0)], [])
w = E("PE", 0); T["230V PE WAGO-LRS"] = ([w, stub(w), FREE(), FREE(), (-145.6, 561.75, 40.6), (-148.6, 561.75, 36.0), (LX, 561.75, 36.0)], [4, 5])
w = E("L", 2); T["230V L WAGO-RS"] = ([w, stub(w), FREE(), FREE(), (V(-92, -76), 576.0, 33.0), (RX, 576.0, 33.0)], [])
w = E("N", 2); T["230V N WAGO-RS"] = ([w, stub(w), FREE(), FREE(), (-66.0, 568.4, 41.0), (-64.8, 568.4, 33.0), (RX, 568.4, 33.0)], [4, 5])
w = E("PE", 3); T["230V PE WAGO-RS"] = ([w, stub(w), FREE(), FREE(), (-66.0, 560.8, 41.0), (-64.8, 560.8, 33.0), (RX, 560.8, 33.0)], [4, 5])
w = E("PE", 2); T["230V PE WAGO-Tray"] = ([w, stub(w), FREE(), FREE(), (-77.0, V(586, 600), 26.6), (-77.0, 615.0, 26.6), (-63.0, 615.0, 26.6)], [])

def nvars(t): return sum(1 for p in t for c in p if isinstance(c, tuple))
def build(t, x):
    i, pts = 0, []
    for p in t:
        q = []
        for c in p:
            if isinstance(c, tuple): q.append(c[1] + (c[2] - c[1]) * min(1, max(0, x[i]))); i += 1
            else: q.append(c)
        pts.append(q)
    return pts

def cost(name, x, placed):
    t, kink = T[name]
    pts = build(t, x)
    try: path, radii, corner_idx = fp(pts)
    except Exception: return 1e9, None
    m = W.tube(path, W.CORE_D + CL)
    c = 200 * (m ^ obs).volume()
    for o in placed.values(): c += 200 * (m ^ o).volume()
    for R, ci in zip(radii, corner_idx):
        if ci in kink: continue
        c += 300 * max(0, RQ - R) ** 2
    c += LW * sum(np.linalg.norm(path[i + 1] - path[i]) for i in range(len(path) - 1))
    return c, m

def fp(pts):
    path, radii = W.fillet_path(pts)
    return path, [r for _, r in radii], [i for i, _ in radii]

def opt(name, placed, iters=1500, starts=4):
    n = nvars(T[name][0]); best = (1e18, None, None)
    for s in range(starts):
        x = rng.random(n); c, m = cost(name, x, placed); sig = 0.25
        for it in range(iters):
            y = np.clip(x + rng.normal(0, sig, n), 0, 1); cy, my = cost(name, y, placed)
            if cy < c: x, c, m = y, cy, my; sig = min(0.3, sig * 1.3)
            else: sig = max(0.005, sig * 0.985)
        if c < best[0]: best = (c, x, m)
    return best

order = list(T)
placed = {"sheath": W.tube(np.array([(sx, sy, sz), (sx, e, sz)]), W.SHEATH_D + CL)}
res = {}
for rnd in range(3):
    for name in order:
        others = {k: v for k, v in placed.items() if k != name}
        c, x, m = opt(name, others, iters=900 if rnd else 1500, starts=1 if rnd else 6)
        if name not in res or c < res[name][0]: res[name] = (c, x); placed[name] = m
        print(rnd, f"{name:22s} cost {res[name][0]:.2f}", flush=True)
out = {n: [list(map(lambda v: round(float(v), 2), p)) for p in build(T[n][0], res[n][1])] for n in order}
json.dump({"pts": out, "kink": {n: T[n][1] for n in order}, "cost": {n: res[n][0] for n in order}},
          open(sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-1000/-home-equinox-git-private-Vodafone-Station-Rackmount/9a510f42-3b60-4339-95fb-862bcb43e163/scratchpad/routes.json", "w"), indent=1)
