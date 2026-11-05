"""Modelled wires (world mm, tray fully out): 230 V from the thin chain cable through the WAGOs to the LRS-350 and RS-15-5.

Each wire is a tube along a polyline whose corners are rounded with circular arcs (fillets), so every bend radius is known
exactly. Fillet radii are as large as the segments allow, up to R_MAX. Wires are not printed: no STL, not in the collision
test of the printed parts, but checked against them (run_checks in cr10mod.py).
Assumptions: core diameter 3.0, WAGO entry centre y, terminal entry heights (docs/COMPONENTS.md).
"""
import math
import numpy as np
from manifold3d import Manifold, Mesh
import cable_thin as thin
import power_hub as hub

LAYER = "Tray Electrics"
SEG = 12
R_MAX = 15.0
COL = {"L": (0.45, 0.25, 0.1), "N": (0.1, 0.3, 0.85), "PE": (0.55, 0.78, 0.1), "sheath": (0.6, 0.6, 0.62)}
CORE_D = 3.0                    # H07V-K-like core 1.5 mm2 of the OELFLEX FD 855 P 3G1,5 (assumption)
SHEATH_D = 7.3                  # docs/COMPONENTS.md
MIN_R = 4.0                     # bend radius >= 4 x D

# ============================================================ anchor points
def _sheath_exit():
    """centre of the chain cable where it leaves the moving bracket groove through its -y face (y 605)"""
    xa = thin.X_MOVING_EXT + thin.O0
    yc = thin.CHAIN_Y - thin.GROOVE_R
    x = xa + math.sqrt(thin.GROOVE_R ** 2 - (thin.LANE_Y[0] - yc) ** 2)
    return (x, thin.LANE_Y[0], thin.ZL - 5.5 + SHEATH_D / 2)        # lying on the groove floor
SHEATH_END_Y = 594.5            # sheath ends behind the strain relief (tie y 595.4..601.4)

# WAGOs lie flat since 2026-11-04 (levers up, entries +y at the front face): entry centre on the front face (assumption)
W_ENTRY_Y = hub.W_Y0 + hub.W_LEN
W_TOP = hub.W_ZT

def wago_entry(name, k):
    n = 4 if name == "PE" else 3
    _, x0, x1 = [s for s in hub.wago_slots() if s[0] == name][0]
    return (x0 + (x1 - x0) * (k + 0.5) / n, W_ENTRY_Y, (hub.W_Z0 + hub.W_ZT) / 2)

LRS_END_X, LRS_Z = -152.0, 36.0          # inside the terminal block face x -151.5; entry z ca. 36
RS_END_X, RS_Z = hub.RS_BLOCK[0] - 0.5, 33.0   # RS block face (terminals -x since 2026-11-04); entry z ca. 33
LRS_Y = {"L": 580.75, "N": 571.25, "PE": 561.75}
RS_Y = {"L": hub.RS_PINS["L"], "N": hub.RS_PINS["N"], "PE": hub.RS_PINS["FG"]}
PE_LUG = (-65.0, 615.0, 26.6)            # start of the ring-lug barrel on the tray 2020 (top z 25)

# ============================================================ geometry
def fillet_path(pts, r_max=R_MAX, step_deg=10.0, tube_d=0.0):
    """polyline -> sample points with circular-arc corners; returns (points, [(polyline corner index, radius)])"""
    P = [np.array(p, float) for p in pts]
    n = len(P)
    d = [(P[i + 1] - P[i]) / np.linalg.norm(P[i + 1] - P[i]) for i in range(n - 1)]
    L = [np.linalg.norm(P[i + 1] - P[i]) for i in range(n - 1)]
    th = [0.0] + [math.acos(max(-1.0, min(1.0, float(d[i - 1] @ d[i])))) for i in range(1, n - 1)] + [0.0]
    t = [0.0] + [r_max * math.tan(th[i] / 2) for i in range(1, n - 1)] + [0.0]
    for _ in range(50):                                    # shrink tangent lengths until each segment holds both
        for i in range(n - 1):
            s = t[i] + t[i + 1]
            if s > L[i] - 0.5:
                f = max(0.0, L[i] - 0.5) / s
                t[i] *= f; t[i + 1] *= f
    out, radii = [P[0]], []
    for i in range(1, n - 1):
        if th[i] < 1e-6: continue
        R = t[i] / math.tan(th[i] / 2); radii.append((i, R))
        a, b = d[i - 1], d[i]
        s0 = P[i] - a * t[i]
        c = P[i] + (b - a) / np.linalg.norm(b - a) * (R / math.cos(th[i] / 2))
        u = (s0 - c) / R
        if R <= tube_d / 2 + 0.3: raise ValueError(f"corner {i}: radius {R:.2f} too small for a tube of {tube_d}")
        step = max(math.radians(step_deg), 0.15 / (R - tube_d / 2))       # inner edge of the tube: points >= 0.15 apart
        m = max(2, math.ceil(th[i] / step))
        for j in range(m + 1):
            ph = th[i] * j / m
            q = c + R * (math.cos(ph) * u + math.sin(ph) * a)
            if np.linalg.norm(q - out[-1]) > 0.3: out.append(q)
    if np.linalg.norm(P[-1] - out[-1]) > 0.3: out.append(P[-1])
    else: out[-1] = P[-1]
    return np.array(out), radii

def tube(path, d, seg=SEG, ends=None):
    """closed tube along the sample points, rings by parallel transport, flat caps;
    ends = (start, end) direction: caps square to the polyline end segments (no tilted cap at a short end)"""
    P = np.asarray(path, float); n = len(P)
    T = np.array([P[min(i + 1, n - 1)] - P[max(i - 1, 0)] for i in range(n)])
    if ends is not None: T[0], T[-1] = ends
    T /= np.linalg.norm(T, axis=1)[:, None]
    ref = np.array([0, 0, 1.0]) if abs(T[0][2]) < 0.9 else np.array([1.0, 0, 0])
    N = np.cross(T[0], ref); N /= np.linalg.norm(N)
    rings = []
    for i in range(n):
        if i:
            N = N - T[i] * (N @ T[i]); N /= np.linalg.norm(N)
        B = np.cross(T[i], N)
        rings.append([P[i] + d / 2 * (math.cos(2 * math.pi * k / seg) * N + math.sin(2 * math.pi * k / seg) * B) for k in range(seg)])
    V = np.array(rings).reshape(-1, 3)
    F = []
    for i in range(n - 1):
        for k in range(seg):
            a, b = i * seg + k, i * seg + (k + 1) % seg
            F += [(a, b, b + seg), (a, b + seg, a + seg)]
    for k in range(1, seg - 1):
        F.append((0, k + 1, k))
        e = (n - 1) * seg; F.append((e, e + k, e + k + 1))
    F = np.array(F, dtype=np.uint32)
    m = Manifold(Mesh(vert_properties=V.astype(np.float32), tri_verts=F))
    if m.volume() < 0 or m.status().name != "NoError":
        m = Manifold(Mesh(vert_properties=V.astype(np.float32), tri_verts=F[:, ::-1].copy()))
    return m

# ============================================================ routes
# Free waypoints were found offline by a penalty search (intersection volume with parts/WAGOs/PSU cases/other wires,
# bend radius deficit, length) and are fixed here so the generator stays deterministic. Fixed points per wire: start
# (sheath end or WAGO entry), the point straight above a WAGO entry (vertical entry), the horizontal run into the
# terminal (or the kink approach over the outer WAGO rib) and the end.
# WAGO entries: L/N k0 -> LRS, k1 -> chain, k2 -> RS; PE k0 -> LRS, k1 -> chain, k2 -> tray lug, k3 -> RS.
# KINK: polyline corner indices allowed below MIN_R x D (user decision 2026-11-03: over the rib, short kink at the terminal).
# 2026-11-03: the 230 V routes were deleted (user): the PSUs moved 5 mm to the tray edges and the hub boxes grew, so the
# waypoints no longer fit. New routes are not generated for now; the tube/fillet code stays for later.
ROUTES = {}
KINK = {}

def routes():
    """[(name, colour key, diameter, polyline, kink corner indices)]"""
    if not ROUTES: return []
    sx, sy, sz = _sheath_exit()
    R = [("230V Kabel Mantel", "sheath", SHEATH_D, [(sx, sy, sz), (sx, SHEATH_END_Y, sz)], ())]
    for name, (cond, pts) in ROUTES.items():
        R.append((name, cond, CORE_D, pts, KINK.get(name, ())))
    return R

def wires():
    out = []
    for name, ck, d, pts, kink in routes():
        path, radii = fillet_path(pts, tube_d=d)
        ends = (np.subtract(pts[1], pts[0]), np.subtract(pts[-1], pts[-2]))
        out.append((name, COL[ck], tube(path, d, ends=ends), dict(d=d, radii=[r for _, r in radii], kinks=[i in kink for i, _ in radii])))
    return out

SHEATH = "230V Kabel Mantel"
def sheath_for_cores():
    """the sheath without its last 3 mm: its own cores leave its end face and may only touch it there"""
    sx, sy, sz = _sheath_exit()
    return tube([(sx, sy, sz), (sx, SHEATH_END_Y + 3.0, sz)], SHEATH_D)

def is_chain_core(name):
    return name.endswith("Kette-WAGO")

def bought_boxes():
    """bought parts the wires must not pierce either (boxes from docs/DESIGN.md / COMPONENTS.md): WAGO bodies, PSU cases"""
    from cable import box
    out = [(f"WAGO {nm}", box(a, b, hub.W_Y0, hub.W_Y0 + hub.W_LEN, hub.W_Z0, hub.W_ZT)) for nm, a, b in hub.wago_slots()]
    out += [("LRS-350 case", box(-364.0 + hub.LRS_DX, -151.5 + hub.LRS_DX, 475.0, 590.0, 25.0, 55.9)),
            ("RS-15-5 case", box(*hub.RS_BODY)), ("RS-15-5 terminal block", box(*hub.RS_BLOCK))]
    return out
