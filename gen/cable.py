"""Cable feed parts (world mm): wide drag chain for CAN, 24/5 V, sensors, USB, network (y 290..330) and its end brackets.

Chain: N_LINKS (11) links, pitch CHP, fixed end under the acrylic plate at X_FIXED (upper run), moving end on the 2040 of the tray
(lower run), 180 deg arc at the front. Links stand on their bottom edge when printed (no rotation), brackets and channel
parts are rotated so that their flat mounting face lies on the bed.
"""
import json, math, os
import numpy as np
from manifold3d import Manifold, CrossSection

# ============================================================ geometry that comes from the model (docs/DESIGN.md)
CH_ZT = 102.0                        # underside of the acrylic plate = top of chain upper run and channel
CHAIN_Y = 310.0                      # centre of the chain lane y 290..330 (2040 on the tray)
CHAIN_ZU, CHAIN_ZL = 92.5, 34.5      # pivot height of the upper / lower run (top 102, bottom 25 = tray profile)
X_MOVING_EXT = -83.5                 # moving end with the tray fully out; the groove exit then sits over the tray duct (x -60..-35)
TRAVEL = 396.0
X_FIXED = X_MOVING_EXT + TRAVEL / 2   # fixed end, middle of the travel (x 116.5)

# ============================================================ drag chain
N_LINKS = 11
CHP, CHR, CHT = 29.5, 9.0, 3.0       # pitch (= arc radius, 3 links per 180 deg), plate radius (height 18), plate thickness
CH_YO = (17.0, 20.0)                 # outer plate |y|
CH_YI = (13.7, 16.7)                 # inner plate |y|, 0.3 mm to the outer plate
PIN_D, HOLE_D, SLOT_W = 4.0, 4.4, 3.6
PIN_END = CH_YO[1] - 0.4
BAR_X = (10.4, CHP - 10.4)           # cross bars only between the pivot circles of the neighbours
TONGUE_L = 12.0


def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))

def cyl_z(x, y, z0, z1, d, seg=24):
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, seg).translate((x, y, z0))

def cyl_y(x, z, y0, y1, d, seg=24):
    return Manifold.cylinder(y1 - y0, d / 2, d / 2, seg).rotate((-90, 0, 0)).translate((x, y0, z))

def cyl_x(y, z, x0, x1, d, seg=24):
    return Manifold.cylinder(x1 - x0, d / 2, d / 2, seg).rotate((0, 90, 0)).translate((x0, y, z))

def hex_z(x, y, z0, z1, af=5.7):
    r = af / math.sqrt(3)
    return Manifold.cylinder(z1 - z0, r, r, 6).translate((x, y, z0))

def hex_x(y, z, x0, x1, af=5.7):
    r = af / math.sqrt(3)
    return Manifold.cylinder(x1 - x0, r, r, 6).rotate((0, 90, 0)).translate((x0, y, z))

def _stadium(x0=0.0, x1=CHP, zc=0.0):
    c = CrossSection.circle(CHR, 48)
    return c.translate((x0, zc)) + c.translate((x1, zc)) + CrossSection.square((x1 - x0, 2 * CHR)).translate((x0, zc - CHR))

def _plate_y(cs, y0, y1):
    """cs in (x, z) extruded over y0..y1"""
    return Manifold.extrude(cs, y1 - y0).rotate((90, 0, 0)).translate((0, y1, 0))

def _sides(yr):
    return [tuple(sorted((s * yr[0], s * yr[1]))) for s in (-1, 1)]

def _ccw(poly):
    P = np.array(poly, dtype=float)
    area = 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1])
    return P if area > 0 else P[::-1].copy()

def _prism_x(poly, x0, x1):
    """polygon in (y, z) extruded along x over x0..x1"""
    m = Manifold.extrude(CrossSection([_ccw(poly)]), x1 - x0)
    return m.transform(np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float)).translate((x0, 0, 0))

def _pins(px, pz):
    m = Manifold()
    for s in (-1, 1):
        ya, yb = s * (CH_YI[1] - 0.8), s * PIN_END
        m = m + cyl_y(px, pz, min(ya, yb), max(ya, yb), PIN_D)
    return m

STOP_GAP = 0.15                            # clearance of the stop faces in the straight position

def _fork_cs(x0, x1, zc=0.0, slot=+1):
    """outer plate of a bracket fork: circle round the socket at x0, straight to x1; hole + slot towards slot*z"""
    cs = CrossSection.circle(CHR, 48).translate((x0, zc)) + CrossSection.square((x1 - x0, 2 * CHR)).translate((x0, zc - CHR))
    sl = CrossSection.square((SLOT_W, CHR + 1)).translate((x0 - SLOT_W / 2, zc if slot > 0 else zc - CHR - 1))
    return cs - CrossSection.circle(HOLE_D / 2, 24).translate((x0, zc)) - sl

# ---- link: exact copy of the hand-made component "Chain Link (new)" of the document (2026-11-03), data/chain_link_user.json
# (internal pin discs and one stray face removed so that it is a closed solid). Rear pivot = pins at x -3.5, front pivot = hole
# at x 26.0 (pitch 29.5); closed top bar on the outer side with vertical stop faces on the top half (anti-sag against hogging),
# open on the inner (bottom) side. Document frame: y centre 310, z centre 92.5, bar on top. Chain frame = rotated 180 deg about x,
# rear pivot at the origin: bar and stops on -z, open side +z (inner side of the bend), front pivot at (CHP, 0, 0).
HERE = os.path.dirname(os.path.abspath(__file__))
DOC_REAR_PIVOT = (-3.5, 310.0, 92.5)

def _load_user_link():
    from manifold3d import Mesh, triangulate
    d = json.load(open(os.path.join(HERE, "data", "chain_link_user.json")))
    V = []; T = []
    for f in d["faces"]:
        loops = [np.array(L, float) for L in [f["outer"]] + f["holes"]]
        P = loops[0]; n = np.zeros(3)
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            n += [(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])]
        n /= np.linalg.norm(n)
        u = np.cross(n, [1, 0, 0] if abs(n[0]) < 0.9 else [0, 1, 0]); u /= np.linalg.norm(u); v = np.cross(n, u)
        allp = np.concatenate(loops)
        for t in triangulate([np.stack([L @ u, L @ v], axis=1) for L in loops]):
            a, b, c = allp[t[0]], allp[t[1]], allp[t[2]]
            base = len(V); V.extend([a, b, c])
            T.append([base, base + 1, base + 2] if np.dot(np.cross(b - a, c - a), n) > 0 else [base, base + 2, base + 1])
    mesh = Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(T, np.uint32)); mesh.merge()
    m = Manifold(mesh)
    if m.status().name != "NoError": raise ValueError("chain_link_user.json is not a closed solid: " + m.status().name)
    return m

_USER_LINK = None
def _doc_to_chain(m):
    """document frame -> chain frame"""
    dx, dy, dz = DOC_REAR_PIVOT
    return m.translate((-dx, -dy, -dz)).rotate((180, 0, 0))

# outer clamp grooves on the outer faces of the plates (added to the copy, the document component stays untouched)
CLAMP_X = (6.3, 10.2)                       # free window beside the plates: neighbour fork ends at x 5.5, own joggle web starts at x 11
CLAMP_GROOVE_Z = (90.0, 92.5)
CLAMP_GROOVE_DEPTH = 0.8
PLATE_OUT_Y = 326.7                         # outer face of the inner plates in the document frame (centre 310 -> |y| 16.7)

def _doc_prism_x(poly, x0, x1):
    return _prism_x(poly, x0, x1)

STOP_H = 2.7          # vertical stop face above the axis: the document component has 9 mm, whose corners (radius 12 around the pivot)
                      # stick 4 mm out of the 25..102 envelope in the arc, so the corners are cut back to the pivot circle

def _cut_corners(m):
    px, pz = DOC_REAR_PIVOT[0], DOC_REAR_PIVOT[2]
    hx = px + CHP                                                    # hole (front pivot)
    big = Manifold.cube((40, 80, 12)).translate((hx, 290.0, pz))
    m = m - (big - Manifold.cylinder(60, CHR, CHR, 96).rotate((90, 0, 0)).translate((hx, 350.0, pz)))
    big2 = Manifold.cube((26.5, 80, 12)).translate((-30.0, 290.0, pz + STOP_H))
    ring = big2 - Manifold.cylinder(60, CHR + 0.45, CHR + 0.45, 96).rotate((90, 0, 0)).translate((px, 350.0, pz))
    return m - ring

def link_doc():
    global _USER_LINK
    if _USER_LINK is None: _USER_LINK = _load_user_link()
    m = _cut_corners(_USER_LINK)
    for s in (0, 1):
        yo = PLATE_OUT_Y if s == 0 else 620.0 - PLATE_OUT_Y
        sg = 1 if s == 0 else -1
        poly = [(yo - sg * CLAMP_GROOVE_DEPTH, CLAMP_GROOVE_Z[0]), (yo + sg * 0.3, CLAMP_GROOVE_Z[0]), (yo + sg * 0.3, CLAMP_GROOVE_Z[1]), (yo - sg * CLAMP_GROOVE_DEPTH, CLAMP_GROOVE_Z[1])]
        m = m - _doc_prism_x(poly, CLAMP_X[0], CLAMP_X[1])
    return m

def link():
    return _doc_to_chain(link_doc())

# ---- lid: U clamp that grips the OUTSIDE of the plates (cable loads pull the arms down and keep the hooks engaged; the arms cannot
# be forced apart from inside). Base under the link + inner plate closing the opening + two outer arms with a hook into the groove.
LID_X = (-0.3, 10.4)
LID_BASE_Z = (80.7, 83.3)
LID_PLATE = dict(y=(296.5, 323.5), z=(83.3, 86.5))
ARM_Y = (326.9, 328.4)                      # outer arm (document frame), mirrored at y = 620 - y
ARM_X = (6.4, 10.1)
ARM_TOP = 92.3
HOOK_Z = (90.3, 92.4)
HOOK_Y = 326.7 - CLAMP_GROOVE_DEPTH + 0.2   # hook tip 0.2 short of the groove bottom

def lid_doc():
    m = box(ARM_X[0], ARM_X[1], 620.0 - ARM_Y[1], ARM_Y[1], LID_BASE_Z[0], LID_BASE_Z[1])
    m = m + box(LID_X[0], LID_X[1], LID_PLATE["y"][0], LID_PLATE["y"][1], LID_PLATE["z"][0] - 0.5, LID_PLATE["z"][1])
    for s in (0, 1):
        ya, yb = ARM_Y if s == 0 else (620.0 - ARM_Y[1], 620.0 - ARM_Y[0])
        m = m + box(ARM_X[0], ARM_X[1], ya, yb, LID_BASE_Z[0], ARM_TOP)
        y0 = ARM_Y[0] if s == 0 else 620.0 - ARM_Y[0]; sg = 1 if s == 0 else -1
        hy = HOOK_Y if s == 0 else 620.0 - HOOK_Y
        hook = [(y0 + sg * 0.3, HOOK_Z[0] - 0.14), (hy, HOOK_Z[0]), (hy, HOOK_Z[1] - 0.6), (y0 + sg * 0.3, ARM_TOP)]
        m = m + _prism_x(hook, ARM_X[0], ARM_X[1])
    return m

def lid():
    return _doc_to_chain(lid_doc())

def lid_print():
    """document frame is already the print orientation (base on the bed, arms up)"""
    return lid_doc()

def chain_pivots(x_m, n=N_LINKS, x_f=X_FIXED, chp=CHP, zu=CHAIN_ZU, zl=CHAIN_ZL):
    """(x, z) of the n+1 pivots; chord pitch chp; the last pivot sits at x_m on the lower run"""
    rc = (zu - zl) / 2; zc = (zu + zl) / 2
    def dense(xc):
        pts = [(x_f, zu), (xc, zu)]
        pts += [(xc - rc * math.sin(math.radians(a)), zc + rc * math.cos(math.radians(a))) for a in range(1, 180)]
        pts += [(xc, zl), (xc + 1500.0, zl)]
        P = np.array(pts); seg = np.hypot(*np.diff(P, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
        t = np.arange(0, s[-1], 0.05)
        return np.stack([np.interp(t, s, P[:, 0]), np.interp(t, s, P[:, 1])], axis=1)
    def march(xc):
        D = dense(xc); idx = 0; out = [D[0]]
        for _ in range(n):
            d = np.hypot(D[idx:, 0] - D[idx, 0], D[idx:, 1] - D[idx, 1])
            hit = np.argmax(d >= chp)
            if d[hit] < chp: raise ValueError("chain path too short")
            idx += int(hit); out.append(D[idx])
        return np.array(out)
    lo, hi = x_m - 500.0, x_f + 60.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if march(mid)[-1, 0] < x_m: lo = mid
        else: hi = mid
    return march((lo + hi) / 2), (lo + hi) / 2

def chain_links(x_m):
    """[(name, kind, world manifold)] for the pose with the moving end at x_m"""
    P, xc = chain_pivots(x_m)
    lk, ld = link(), lid()
    out = []
    for k in range(N_LINKS):
        a, b = P[k], P[k + 1]; d = (b - a) / np.linalg.norm(b - a)
        M = np.array([[d[0], 0, -d[1], a[0]], [0, 1, 0, CHAIN_Y], [d[1], 0, d[0], a[1]]])
        out.append((f"Chain Link {k + 1:02d}", "Link", lk.transform(M)))
        out.append((f"Chain Lid {k + 1:02d}", "Lid", ld.transform(M)))
    return out, P, xc

# ============================================================ chain end brackets (world)
def _fork_world(px, pz, slot=+1):
    """outer plates with sockets for the pins of the first link"""
    cs = _fork_cs(px, px + TONGUE_L + 3.0, pz, slot)
    m = Manifold()
    for y0, y1 in _sides(CH_YO): m = m + _plate_y(cs, CHAIN_Y + y0, CHAIN_Y + y1)
    return m

def _tongue(px, pz, direction):
    """two inner plates with pins around the last pivot, reaching `direction` * TONGUE_L into the bracket body"""
    L = TONGUE_L + 3.0
    x0, x1 = (px, px + L) if direction > 0 else (px - L, px)
    cs = CrossSection.circle(CHR, 48).translate((px, pz)) + CrossSection.square((L, 2 * CHR)).translate((x0, pz - CHR))
    m = Manifold()
    for y0, y1 in _sides(CH_YI):
        m = m + _plate_y(cs, CHAIN_Y + y0, CHAIN_Y + y1)
    return m + _pins(px, pz).translate((0, CHAIN_Y, 0))

def bracket_fixed():
    """under the acrylic plate: M3 from above through the plate into nuts in the bracket, cable tunnel into the channel"""
    px, pz = X_FIXED, CHAIN_ZU
    x0, x1 = px + 12.0, px + 44.0                 # body face behind the rear stop corner of the first link (11.85 from the pin)
    body = box(x0, x1, 290.0, 330.0, pz - CHR, CH_ZT)
    fun = [(px + 9.0, 296.8), (px + 9.0, 323.2), (px + 17.0, 313.0), (x1 + 1, 313.0), (x1 + 1, 297.0), (px + 17.0, 297.0), (px + 9.0, 296.8)]
    body = body - Manifold.extrude(CrossSection([_ccw(fun[:-1])]), CH_ZT + 1 - 88.5).translate((0, 0, 88.5))
    for x in (px + 20.0, px + 36.0):
        body = body - cyl_z(x, 323.0, pz - CHR - 1, CH_ZT + 1, 3.4, 16) - hex_z(x, 323.0, pz - CHR - 1, pz - CHR + 2.7)
    return body + _fork_world(px, pz, -1)

GROOVE_R, GROOVE_W = 24.0, 18.0         # centre-line radius (> R_fest 22 of the cable), groove width

def bracket_moving(x_m=X_MOVING_EXT):
    """on top of the 2040 of the tray: M3 into hammer nuts in its two slots (y 300 / 320); the cables leave in a quarter turn
    (centre-line R 24) through the +y face into the tray duct (x -60..-35)"""
    pz = CHAIN_ZL
    xa = x_m + CHR + STOP_GAP + 3.0       # groove start; body face leaves room for the stop extension of the last link
    x1 = xa + GROOVE_R + GROOVE_W / 2 + 3.0
    body = box(xa, x1, 290.0, 330.0, 25.0, pz + CHR)
    ro, ri = GROOVE_R + GROOVE_W / 2, GROOVE_R - GROOVE_W / 2
    ring = cyl_z(xa, 330.0, pz - 5.0, pz + CHR + 1, 2 * ro, 96) - cyl_z(xa, 330.0, pz - 6.0, pz + CHR + 2, 2 * ri, 96)
    cut = ring ^ box(xa, x1 + 1, 289.0, 331.0, pz - 6.0, pz + CHR + 2)
    body = body - cut - box(xa - 1, xa + 0.5, 330.0 - ro - 0.5, 330.0 - ri + 0.5, pz - 5.0, pz + CHR + 1)
    for dx, y in ((20.0, 300.0), (4.0, 320.0)):
        body = body - cyl_z(xa + dx, y, pz - CHR - 1, pz + CHR + 1, 3.4, 16) - cyl_z(xa + dx, y, pz + 4.0, pz + CHR + 1, 6.4, 16)
    return body + _tongue(x_m, pz, +1)

def flat(m):
    """print orientation of parts with the mounting face on top (z = 102 / 102): rotate 180 deg about x"""
    return m.rotate((180, 0, 0))
